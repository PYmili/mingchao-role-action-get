import requests
import subprocess
from pathlib import Path
import re

API_URL = "https://jsonschema.qpic.cn/4977140ca7efbac3a690ee6a9803967e/9eadb85a9dca203df1da1c1997fd339e/rolelist"
OUTPUT_DIR = Path("output")


def sanitize_filename(name: str) -> str:
    """清理文件名中的非法字符"""
    return re.sub(r'[<>:"/\\|?*]', '', name).strip()


def ensure_url(url: str) -> str:
    """确保URL有https前缀"""
    if url.startswith("//"):
        return "https:" + url
    return url


def download_file(url: str, save_path: Path) -> bool:
    """下载文件"""
    try:
        url = ensure_url(url)
        with requests.get(url, stream=True, timeout=30) as r:
            r.raise_for_status()
            with open(save_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return True
    except Exception as e:
        print(f"下载失败: {url}, 错误: {e}")
        return False


def merge_audio_video(audio_path: Path, video_path: Path, output_path: Path) -> bool:
    """使用ffmpeg合并音频和视频，用下载的音频替换webm内置音频"""
    try:
        cmd = [
            "ffmpeg",
            "-y",  # 覆盖输出文件
            "-i", str(video_path),  # 输入0: 视频(webm已含内置音频)
            "-i", str(audio_path),  # 输入1: 外部音频(wav/mp3)
            "-map", "0:v",          # 只使用输入0的视频流
            "-map", "1:a",          # 只使用输入1的音频流
            "-c:v", "copy",         # 视频流直接复制
            "-c:a", "aac",          # 音频转码为aac
            "-shortest",            # 使用最短的流长度
            str(output_path)
        ]
        subprocess.run(cmd, capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"ffmpeg合并失败: {e.stderr.decode() if e.stderr else str(e)}")
        return False
    except FileNotFoundError:
        print("ffmpeg未安装或不在PATH中")
        return False


def process_role(role: dict):
    """处理单个角色的actionList"""
    cn_name = role.get("cnName", "未知")
    action_list = role.get("actionList", [])

    if not action_list:
        print(f"角色 {cn_name} 没有actionList")
        return

    # 创建角色文件夹
    role_dir = OUTPUT_DIR / sanitize_filename(cn_name)
    role_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n处理角色: {cn_name} ({len(action_list)} 个动作)")

    for idx, action in enumerate(action_list, 1):
        audio_url = action.get("audio")
        video_url = action.get("url")

        if not audio_url or not video_url:
            print(f"  动作 {idx}: 缺少audio或url")
            continue

        # 从URL提取文件名
        audio_filename = sanitize_filename(Path(audio_url).name)
        video_filename = sanitize_filename(Path(video_url).name)

        audio_path = role_dir / audio_filename
        video_path = role_dir / video_filename
        merged_path = role_dir / f"动作{idx}_{cn_name}.mp4"

        print(f"  下载动作 {idx}...")

        # 下载音频
        if not download_file(audio_url, audio_path):
            continue

        # 下载视频
        if not download_file(video_url, video_path):
            continue

        # 合并
        print(f"  合并动作 {idx}...")
        if merge_audio_video(audio_path, video_path, merged_path):
            print(f"  完成: {merged_path}")
            # 删除临时文件
            audio_path.unlink(missing_ok=True)
            video_path.unlink(missing_ok=True)
        else:
            print(f"  合并失败,保留原始文件")


def main():
    print("获取角色列表...")
    try:
        response = requests.get(API_URL, timeout=30)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"获取API数据失败: {e}")
        return

    role_list = data.get("RoleList", [])
    print(f"共 {len(role_list)} 个角色")

    OUTPUT_DIR.mkdir(exist_ok=True)

    for role in role_list:
        process_role(role)

    print("\n全部完成!")


if __name__ == "__main__":
    main()