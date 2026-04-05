<div align="center">

# 鸣朝角色动作获取工具

<img src="https://img.shields.io/badge/Python-3.12+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/ffmpeg-required-purple?style=for-the-badge&logo=ffmpeg&logoColor=white" alt="ffmpeg">
<img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">

**获取鸣朝（Wuthering Waves）游戏中所有角色的动作视频**

将 webm 视频与独立音频文件合并为完整的 mp4 文件

</div>

---

## ✨ 功能特性

- 🎮 自动获取所有角色的 actionList 数据
- 📥 下载 webm 视频和音频文件（wav/mp3）
- 🎬 使用 ffmpeg 合并为 mp4，替换 webm 内置音频
- 📁 每个角色单独文件夹存放，便于管理

---

## 📋 环境要求

| 依赖 | 版本要求 | 说明 |
|------|----------|------|
| Python | 3.12+ | 运行环境 |
| uv | 最新版 | Python 包管理器 |
| ffmpeg | 任意版本 | 视频处理工具 |

> **注意**: ffmpeg 需提前安装并添加到系统 PATH

---

## 🚀 快速开始

### 安装依赖

```bash
uv sync
```

### 运行程序

```bash
uv run python main.py
```

程序将自动：
1. 从 API 获取角色列表
2. 遍历每个角色的 actionList
3. 下载视频和音频文件
4. 使用 ffmpeg 合并输出 mp4

---

## 📂 输出结构

```
output/
├── 西格莉卡/
│   ├── 动作1_西格莉卡.mp4
│   ├── 动作2_西格莉卡.mp4
│   └── 动作3_西格莉卡.mp4
├── 陆·赫斯/
│   ├── 动作1_陆·赫斯.mp4
│   ├── 动作2_陆·赫斯.mp4
│   └── 动作3_陆·赫斯.mp4
├── 琳奈/
│   └── ...
└── ...（更多角色）
```

---

## 🔧 技术细节

### 数据来源

角色数据来自官方 API 接口：

```
https://jsonschema.qpic.cn/.../rolelist
```

`actionList` 字段结构：

```json
{
  "audio": "//wegame.gtimg.com/.../音频.wav",
  "url": "//wegame.gtimg.com/.../视频.webm"
}
```

### 合成原理

webm 文件内置音频流，通过 ffmpeg `-map` 参数精确控制：

```bash
ffmpeg -i video.webm -i audio.wav \
  -map 0:v -map 1:a \    # 只用视频的视频流，音频文件的音频流
  -c:v copy -c:a aac \   # 视频直接复制，音频转 aac
  -shortest output.mp4   # 以最短流为准
```

---

## 📄 开源协议

本项目采用 [MIT](LICENSE) 协议开源。

---

<div align="center">

**仅供学习交流使用，数据版权归鸣朝官方所有**

</div>