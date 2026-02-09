#!/usr/bin/env python3
"""
哔哩哔哩视频字幕和元数据提取器

支持两种方式获取字幕：
1. B站API接口（推荐，无需额外依赖）
2. yt-dlp（备选，功能更强）

使用方法：
    python bilibili_subtitle.py "<bilibili-url>"
    python bilibili_subtitle.py "BV1xxxxxxxxxx"

输出：
    JSON 格式的视频信息，包含标题、字幕、时间戳等
"""

import sys
import json
import re
import urllib.request
import urllib.parse
import gzip
import io

# 修复Windows控制台编码问题
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')


def extract_bvid(url_or_bvid: str) -> str:
    """从B站URL或直接的BV号中提取BV ID"""
    # 直接是BV号
    if re.match(r'^BV[a-zA-Z0-9]+$', url_or_bvid):
        return url_or_bvid

    # 从URL中提取
    patterns = [
        r'bilibili\.com/video/(BV[a-zA-Z0-9]+)',
        r'b23\.tv/(BV[a-zA-Z0-9]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, url_or_bvid)
        if match:
            return match.group(1)

    # 尝试处理短链接 b23.tv
    if 'b23.tv' in url_or_bvid:
        try:
            req = urllib.request.Request(url_or_bvid, method='HEAD')
            req.add_header('User-Agent', 'Mozilla/5.0')
            resp = urllib.request.urlopen(req, timeout=10)
            real_url = resp.url
            match = re.search(r'bilibili\.com/video/(BV[a-zA-Z0-9]+)', real_url)
            if match:
                return match.group(1)
        except Exception:
            pass

    return None


def api_request(url: str) -> dict:
    """发送B站API请求"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.bilibili.com',
        'Accept-Encoding': 'gzip, deflate',
    }
    req = urllib.request.Request(url, headers=headers)
    resp = urllib.request.urlopen(req, timeout=15)

    if resp.headers.get('Content-Encoding') == 'gzip':
        data = gzip.GzipFile(fileobj=io.BytesIO(resp.read())).read()
    else:
        data = resp.read()

    return json.loads(data.decode('utf-8'))


def get_video_info_api(bvid: str) -> dict:
    """通过B站API获取视频信息和字幕"""
    result = {
        "bvid": bvid,
        "url": f"https://www.bilibili.com/video/{bvid}",
        "title": "",
        "description": "",
        "uploader": "",
        "duration": 0,
        "transcript": [],
        "method": "bilibili_api"
    }

    try:
        # 1. 获取视频基本信息
        info_url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
        info_data = api_request(info_url)

        if info_data.get('code') != 0:
            result["error"] = f"API错误: {info_data.get('message', '未知错误')}"
            return result

        video_data = info_data.get('data', {})
        result["title"] = video_data.get('title', '')
        result["description"] = video_data.get('desc', '')
        result["uploader"] = video_data.get('owner', {}).get('name', '')
        result["duration"] = video_data.get('duration', 0)
        result["aid"] = video_data.get('aid', 0)
        result["cid"] = video_data.get('cid', 0)
        result["view_count"] = video_data.get('stat', {}).get('view', 0)
        result["like_count"] = video_data.get('stat', {}).get('like', 0)
        result["tags"] = video_data.get('tname', '')

        # 处理分P视频
        pages = video_data.get('pages', [])
        if pages:
            result["pages"] = [
                {"cid": p.get('cid'), "part": p.get('part', ''), "duration": p.get('duration', 0)}
                for p in pages
            ]

        cid = result["cid"]
        aid = result["aid"]

        if not cid or not aid:
            result["error"] = "无法获取视频cid/aid"
            return result

        # 2. 获取字幕信息
        subtitle_url = f"https://api.bilibili.com/x/player/wbi/v2?bvid={bvid}&cid={cid}"
        subtitle_data = api_request(subtitle_url)

        if subtitle_data.get('code') == 0:
            player_data = subtitle_data.get('data', {})
            subtitle_info = player_data.get('subtitle', {})
            subtitle_list = subtitle_info.get('subtitles', [])

            if subtitle_list:
                # 优先选择中文字幕
                chosen = None
                for sub in subtitle_list:
                    lang = sub.get('lan', '')
                    if 'zh' in lang or 'cn' in lang.lower():
                        chosen = sub
                        break
                if not chosen:
                    chosen = subtitle_list[0]

                sub_url = chosen.get('subtitle_url', '')
                if sub_url:
                    if sub_url.startswith('//'):
                        sub_url = 'https:' + sub_url

                    sub_data = api_request(sub_url)
                    body = sub_data.get('body', [])

                    for item in body:
                        result["transcript"].append({
                            "text": item.get('content', ''),
                            "start": item.get('from', 0),
                            "duration": item.get('to', 0) - item.get('from', 0)
                        })

                    result["subtitle_lang"] = chosen.get('lan_doc', chosen.get('lan', ''))
            else:
                # 3. 尝试获取AI生成的字幕
                ai_subtitle_url = f"https://api.bilibili.com/x/player/wbi/v2?bvid={bvid}&cid={cid}"
                result["subtitle_note"] = "该视频无CC字幕，可尝试yt-dlp方式获取"

    except urllib.error.HTTPError as e:
        result["error"] = f"HTTP错误: {e.code}"
    except urllib.error.URLError as e:
        result["error"] = f"网络错误: {str(e.reason)}"
    except Exception as e:
        result["error"] = str(e)

    return result


def get_video_info_ytdlp(url: str) -> dict:
    """使用yt-dlp获取B站视频信息（备选方案）"""
    import subprocess

    result = {
        "url": url,
        "title": "",
        "description": "",
        "uploader": "",
        "duration": 0,
        "transcript": [],
        "method": "yt-dlp"
    }

    try:
        cmd = [
            'yt-dlp',
            '--dump-json',
            '--no-playlist',
            '--write-subs',
            '--sub-langs', 'zh.*,zh-Hans,zh-CN,ai-zh',
            url
        ]

        process = subprocess.run(cmd,
                                capture_output=True,
                                text=True,
                                timeout=60,
                                encoding='utf-8',
                                errors='replace')

        if process.returncode != 0:
            result["error"] = process.stderr
            return result

        video_info = json.loads(process.stdout)

        result["title"] = video_info.get('title', '')
        result["description"] = video_info.get('description', '')
        result["uploader"] = video_info.get('uploader', '')
        result["duration"] = video_info.get('duration', 0)
        result["bvid"] = video_info.get('id', '')

        # 获取字幕
        subtitles = video_info.get('subtitles', {})
        automatic_captions = video_info.get('automatic_captions', {})

        lang_priority = ['zh-Hans', 'zh-CN', 'zh-Hant', 'zh-TW', 'zh', 'ai-zh', 'en']

        sub_data = None
        for lang in lang_priority:
            if lang in subtitles and subtitles[lang]:
                sub_data = subtitles[lang]
                break
            if lang in automatic_captions and automatic_captions[lang]:
                sub_data = automatic_captions[lang]
                break

        if sub_data:
            # 找JSON格式的字幕
            json_sub = None
            for fmt in sub_data:
                if fmt.get('ext') == 'json3' or 'json' in fmt.get('ext', ''):
                    json_sub = fmt
                    break
            if not json_sub:
                json_sub = sub_data[0]

            sub_url = json_sub.get('url', '')
            if sub_url:
                req = urllib.request.Request(sub_url)
                req.add_header('User-Agent', 'Mozilla/5.0')
                resp = urllib.request.urlopen(req, timeout=10)
                sub_content = json.loads(resp.read().decode('utf-8'))

                events = sub_content.get('events', sub_content.get('body', []))
                for event in events:
                    if 'segs' in event:
                        text = ''.join(seg.get('utf8', '') for seg in event['segs']).strip()
                    elif 'content' in event:
                        text = event['content'].strip()
                    else:
                        continue

                    if text:
                        start = event.get('tStartMs', event.get('from', 0))
                        if start > 1000:
                            start = start / 1000
                        dur = event.get('dDurationMs', event.get('to', 0) - event.get('from', 0))
                        if dur > 1000:
                            dur = dur / 1000

                        result["transcript"].append({
                            "text": text,
                            "start": start,
                            "duration": dur
                        })

    except FileNotFoundError:
        result["error"] = "yt-dlp 未安装，请运行: pip install yt-dlp"
    except subprocess.TimeoutExpired:
        result["error"] = "获取视频信息超时"
    except Exception as e:
        result["error"] = str(e)

    return result


def format_time(seconds: float) -> str:
    """将秒数格式化为时间戳"""
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "请提供B站视频URL或BV号",
            "usage": 'python bilibili_subtitle.py "<bilibili-url-or-bvid>"'
        }, ensure_ascii=False))
        sys.exit(1)

    url_or_bvid = sys.argv[1]
    method = sys.argv[2] if len(sys.argv) > 2 else "auto"

    bvid = extract_bvid(url_or_bvid)

    if method == "ytdlp":
        result = get_video_info_ytdlp(url_or_bvid)
    elif method == "api" and bvid:
        result = get_video_info_api(bvid)
    else:
        # auto: 先尝试API，失败则用yt-dlp
        if bvid:
            result = get_video_info_api(bvid)
            if result.get("error") or (not result.get("transcript") and result.get("subtitle_note")):
                ytdlp_result = get_video_info_ytdlp(url_or_bvid)
                if not ytdlp_result.get("error") and ytdlp_result.get("transcript"):
                    result = ytdlp_result
                elif not result.get("error"):
                    result["fallback_error"] = ytdlp_result.get("error", "yt-dlp也未获取到字幕")
        else:
            result = get_video_info_ytdlp(url_or_bvid)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
