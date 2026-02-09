#!/usr/bin/env python3
import sys
import json
import argparse
import urllib.request
from pathlib import Path
from datetime import datetime
import re

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def parse_args():
    parser = argparse.ArgumentParser(description='哔哩哔哩UP主信息与视频列表获取器')
    parser.add_argument('uploader_url', help='UP主链接、UID')
    parser.add_argument('limit', nargs='?', type=int, default=30)
    parser.add_argument('--sort', '-s', choices=['plays', 'pubtime'], default='pubtime')
    parser.add_argument('--order', '-o', choices=['desc', 'asc'], default='desc')
    parser.add_argument('--output', '-out', default='docs')
    parser.add_argument('--notes', action='store_true')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--cookie', '-c', help='B站Cookie（用于绕过反爬虫验证）')
    return parser.parse_args()

def extract_uid(url):
    url = url.strip()
    if url.isdigit():
        return url
    match = re.search(r'space\.bilibili\.com/(\d+)', url)
    if match:
        return match.group(1)
    return None

def get_uploader_info(uid, cookie=None):
    url = f'https://api.bilibili.com/x/space/acc/info?mid={uid}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    if cookie:
        headers['Cookie'] = cookie
    try:
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read().decode('utf-8'))
        if data.get('code') == 0:
            info = data.get('data', {})
            return {'mid': info.get('mid'), 'name': info.get('name'), 'face': info.get('face'),
                    'sign': info.get('sign'), 'level': info.get('level'), 'follower': info.get('follower'),
                    'following': info.get('following')}
        else:
            print(f'API错误: {data.get("message", "未知错误")}', file=sys.stderr)
    except Exception as e:
        print(f'获取UP主信息失败: {e}', file=sys.stderr)
    return None

def get_video_list(uid, limit=30, cookie=None):
    url = f'https://api.bilibili.com/x/space/arc/search?mid={uid}&ps={limit}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    if cookie:
        headers['Cookie'] = cookie
    try:
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read().decode('utf-8'))
        if data.get('code') == 0:
            vlist = data.get('data', {}).get('list', {}).get('vlist', [])
            videos = []
            for v in vlist:
                videos.append({'bvid': v.get('bvid'), 'aid': v.get('aid'), 'title': v.get('title'),
                    'description': v.get('description'), 'duration': v.get('length'), 'pubtime': v.get('created'),
                    'plays': v.get('play'), 'likes': v.get('like'), 'coins': v.get('coin'),
                    'favorites': v.get('favorite'), 'comments': v.get('comment'), 'pic': v.get('pic')})
            return videos
        else:
            print(f'API错误: {data.get("message", "未知错误")}', file=sys.stderr)
    except Exception as e:
        print(f'获取视频列表失败: {e}', file=sys.stderr)
    return []

def format_time(timestamp):
    if not timestamp: return '未知'
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')

def format_number(num):
    if num is None: return '0'
    return f'{num/10000:.1f}万' if num >= 10000 else str(num)

def sort_videos(videos, sort_by='pubtime', order='desc'):
    reverse = (order == 'desc')
    key = 'plays' if sort_by == 'plays' else 'pubtime'
    videos.sort(key=lambda x: x.get(key, 0), reverse=reverse)
    return videos

def print_table(uploader, videos):
    print('')
    print('=' * 100)
    print(f"UP主: {uploader.get('name')} (UID: {uploader.get('mid')})")
    print(f"签名: {uploader.get('sign', '无')}")
    print(f"粉丝: {format_number(uploader.get('follower', 0))} | 关注: {format_number(uploader.get('following', 0))}")
    print(f'投稿数: {len(videos)}')
    print('=' * 100)
    print('')
    print(f"{'序号':<4} {'标题':<45} {'播放':<10} {'点赞':<8} {'发布时间':<15}")
    print('-' * 100)
    for i, video in enumerate(videos, 1):
        title = video.get('title', '')[:43]
        print(f"{i:<4} {title:<45} {format_number(video.get('plays', 0)):<10} {format_number(video.get('likes', 0)):<8} {format_time(video.get('pubtime')):<15}")

def main():
    args = parse_args()
    uid = extract_uid(args.uploader_url)
    if not uid:
        print('错误: 无法提取UID', file=sys.stderr)
        sys.exit(1)

    cookie = args.cookie
    if not cookie:
        print('提示: B站API需要Cookie才能正常访问', file=sys.stderr)
        print('获取Cookie方法: 登录 bilibili.com → F12 → Application → Cookies → 复制 SESSDATA 和 bili_jct', file=sys.stderr)
        print('使用格式: --cookie "SESSDATA=xxx; bili_jct=xxx;"', file=sys.stderr)
        print('将尝试无Cookie访问...', file=sys.stderr)

    print(f'获取 UP 主信息 (UID: {uid})...')
    uploader = get_uploader_info(uid, cookie)
    if not uploader:
        print('获取UP主信息失败', file=sys.stderr)
        print('请提供B站Cookie后重试: --cookie "SESSDATA=xxx; bili_jct=xxx;"', file=sys.stderr)
        sys.exit(1)
    print(f'获取最新 {args.limit} 个视频...')
    videos = get_video_list(uid, args.limit, cookie)
    if not videos:
        print('未找到视频')
        sys.exit(1)
    videos = sort_videos(videos, args.sort, args.order)
    output = {'uploader': uploader, 'videos': videos, 'total': len(videos)}
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    safe_name = re.sub(r'[\\/*?:"<>|]', '_', uploader.get('name', 'unknown'))
    json_file = output_dir / f'{safe_name}_videos.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    if not args.json:
        print_table(uploader, videos)
        print('')
        print(f'JSON已保存到: {json_file}')
    else:
        print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
