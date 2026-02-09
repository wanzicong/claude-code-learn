# -*- coding: utf-8 -*-
"""
使用 bilibili-api 获取UP主全部视频并批量处理
支持：获取视频列表 -> 下载视频 -> 提取字幕 -> 生成笔记
"""
import sys
import json
import asyncio
from pathlib import Path
from datetime import datetime

# 设置UTF-8编码
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

try:
    from bilibili_api import user, video, sync
except ImportError:
    print("错误：未安装 bilibili-api-python")
    print("请运行：python -m pip install bilibili-api-python")
    sys.exit(1)

# 配置
UP_UID = 28554995  # 小天fotos的UID
OUTPUT_DIR = Path("docs")
VIDEO_LIST_FILE = OUTPUT_DIR / "bilibili_api_videos.json"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


async def get_user_info(uid):
    """获取UP主信息"""
    print(f"\n正在获取UP主信息 (UID: {uid})...")
    u = user.User(uid)
    info = await u.get_user_info()

    user_data = {
        'uid': uid,
        'name': info.get('name', ''),
        'sign': info.get('sign', ''),
        'level': info.get('level', 0),
        'face': info.get('face', ''),
    }

    print(f"✓ UP主：{user_data['name']}")
    print(f"  签名：{user_data['sign']}")
    print(f"  等级：{user_data['level']}")

    return user_data


async def get_all_videos(uid):
    """获取UP主的所有视频"""
    print(f"\n正在获取UP主的所有视频...")
    u = user.User(uid)

    all_videos = []
    page = 1
    page_size = 30

    while True:
        print(f"  获取第 {page} 页...")
        try:
            result = await u.get_videos(pn=page, ps=page_size)
            videos = result.get('list', {}).get('vlist', [])

            if not videos:
                break

            for v in videos:
                video_data = {
                    'bvid': v.get('bvid', ''),
                    'aid': v.get('aid', 0),
                    'title': v.get('title', ''),
                    'description': v.get('description', ''),
                    'duration': v.get('length', ''),
                    'pubdate': v.get('created', 0),
                    'play': v.get('play', 0),
                    'comment': v.get('comment', 0),
                    'pic': v.get('pic', ''),
                }
                all_videos.append(video_data)

            print(f"    ✓ 获取到 {len(videos)} 个视频")

            # 检查是否还有更多视频
            total = result.get('page', {}).get('count', 0)
            if len(all_videos) >= total:
                break

            page += 1
            await asyncio.sleep(1)  # 避免请求过快

        except Exception as e:
            print(f"    ✗ 获取第 {page} 页失败: {e}")
            break

    print(f"\n✓ 共获取到 {len(all_videos)} 个视频")
    return all_videos


async def get_video_detail(bvid):
    """获取视频详细信息"""
    try:
        v = video.Video(bvid=bvid)
        info = await v.get_info()
        return info
    except Exception as e:
        print(f"  ✗ 获取视频详情失败 ({bvid}): {e}")
        return None


def format_duration(seconds):
    """格式化时长"""
    if isinstance(seconds, str):
        return seconds
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"


def format_date(timestamp):
    """格式化日期"""
    if not timestamp:
        return "未知"
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


async def main():
    """主函数"""
    print("=" * 80)
    print("使用 bilibili-api 获取UP主全部视频")
    print("=" * 80)

    # 1. 获取UP主信息
    user_info = await get_user_info(UP_UID)

    # 2. 获取所有视频
    videos = await get_all_videos(UP_UID)

    if not videos:
        print("\n✗ 未获取到任何视频")
        return

    # 3. 保存视频列表
    data = {
        'uploader': user_info,
        'videos': videos,
        'total': len(videos),
        'fetch_time': datetime.now().isoformat()
    }

    with open(VIDEO_LIST_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n✓ 视频列表已保存到: {VIDEO_LIST_FILE}")

    # 4. 显示视频列表
    print("\n" + "=" * 80)
    print("视频列表")
    print("=" * 80)

    for i, v in enumerate(videos, 1):
        print(f"\n{i}. {v['title']}")
        print(f"   BV号: {v['bvid']}")
        print(f"   时长: {v['duration']}")
        print(f"   播放: {v['play']:,}")
        print(f"   评论: {v['comment']}")
        print(f"   发布: {format_date(v['pubdate'])}")
        print(f"   链接: https://www.bilibili.com/video/{v['bvid']}")

    # 5. 统计信息
    print("\n" + "=" * 80)
    print("统计信息")
    print("=" * 80)
    print(f"UP主: {user_info['name']}")
    print(f"视频总数: {len(videos)}")
    print(f"总播放量: {sum(v['play'] for v in videos):,}")
    print(f"总评论数: {sum(v['comment'] for v in videos):,}")

    # 按播放量排序
    top_videos = sorted(videos, key=lambda x: x['play'], reverse=True)[:5]
    print(f"\n播放量TOP5:")
    for i, v in enumerate(top_videos, 1):
        print(f"  {i}. {v['title']} - {v['play']:,}次")

    print("\n" + "=" * 80)
    print("✓ 完成！")
    print("=" * 80)

    print("\n下一步操作:")
    print("1. 查看视频列表: cat docs/bilibili_api_videos.json")
    print("2. 批量下载视频: python batch_download_from_api.py")
    print("3. 生成笔记: 使用现有的批量处理脚本")


if __name__ == '__main__':
    # 运行异步主函数
    sync(main())
