# Google Gemini Watermark Remover Skill

专门用于去除 Google Gemini（Nano Banana）生成图片上的右下角水印的 Claude Code Skill。

## ✨ 特性

- 🎯 **专门针对 Google Gemini 水印** - 仅适用于 Google Gemini/Nano Banana 生成的图片
- 🔍 **自动检测水印** - 通过亮度差分析智能识别水印区域
- 🔬 **Reverse Alpha Blending 算法** - 使用数学公式精确还原原图
- 📦 **开箱即用** - 包含预制的 Mask 图片和详细文档

## 📦 安装

### 方法一：手动安装

```bash
# 下载 Skill
gh repo clone fxzer/gemini-watermark-remover-skill
cd gemini-watermark-remover-skill

# 复制到 Claude Code skills 目录
cp -r watermark-remover ~/.claude/skills/
```

### 方法二：使用 ZIP

1. 下载 [Releases](https://github.com/fxzer/gemini-watermark-remover-skill/releases) 中的 ZIP 文件
2. 解压到 `~/.claude/skills/` 目录

## 🚀 使用方法

当与 Claude Code 对话时，只需说：

- "去除这张 Google Gemini 图片的水印"
- "帮我批量处理这些 Gemini 生成的图片"
- "去掉右下角的 Google Gemini 水印"

Claude 会自动识别并使用此 Skill。

## 📂 Skill 结构

```
watermark-remover/
├── SKILL.md                      # Skill 主文档
├── README.md                     # 本文件
├── references/
│   └── algorithm.md              # Reverse Alpha Blending 算法详解
└── assets/
    ├── mask_48.png               # 48px 水印 Mask
    └── mask_96.png               # 96px 水印 Mask
```

## ⚠️ 重要说明

此 Skill **仅适用于 Google Gemini（原 Nano Banana）生成的图片**，不是通用的去水印工具。

### 适用范围
✅ Google Gemini/Nano Banana 生成的图片  
✅ 右下角的白色半透明水印

❌ 其他 AI 生成工具（DALL-E、Midjourney 等）  
❌ 网站截图或普通照片的水印  
❌ 彩色水印、随机位置水印

## 🔬 算法原理

使用 **Reverse Alpha Blending** 算法：

```
Original = (Composite - Watermark × α) / (1 - α)
```

其中：
- `Composite` - 带水印的图片
- `Watermark` - 水印图层（白色）
- `α` - 水印透明度
- `Original` - 还原后的原图

详细说明请查看 [references/algorithm.md](references/algorithm.md)

## 📄 License

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 🔗 相关链接

- [在线体验](https://banana-watermark.vercel.app/) - Web 版本
- [原项目](https://github.com/fxzer/banana-watermark-remove) - 完整的 React 实现
