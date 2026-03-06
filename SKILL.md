---
name: gemini-watermark-remover
description: 专门用于去除 Google Gemini（Nano Banana）生成图片上的右下角水印。当用户需要去除 Google Gemini 或 Nano Banana 生成的图片水印时，使用此 Skill。注意：这不是通用的去水印工具，仅适用于 Google Gemini/Nano Banana 的特定水印。
---

# Google Gemini Watermark Remover Skill

⚠️ **重要说明**：此 Skill **仅适用于 Google Gemini（Nano Banana）生成的图片**，不是通用的去水印工具。

此 Skill 提供使用 **Reverse Alpha Blending** 算法去除 Google Gemini 生成图片右下角水印的知识和工具。

## 适用范围

### ✅ 适用场景

此 Skill **仅适用于**以下情况：

- 去除 **Google Gemini**（原 Nano Banana）生成的图片水印
- 图片右下角的 **"Google Gemini"** 或 **"Nano Banana"** 白色半透明水印
- 批量处理 Google Gemini 生成的带水印图片

### ❌ 不适用场景

此 Skill **不适用于**：

- 其他 AI 生成工具的图片（如 DALL-E、Midjourney 等）
- 网站截图或普通照片的水印
- 彩色水印、随机位置水印、完全不透明水印
- 没有 Google Gemini 特定水印的图片

**如果用户需要去除其他类型的水印，请告知用户此 Skill 仅适用于 Google Gemini 生成的图片。**

## 工作流程

### 第一步：获取水印信息

向用户确认以下信息：
1. 水印在图片上的位置（默认为右下角）
2. 水印距离边缘的边距（margin）
3. 是否有水印的 Mask 图（黑底白字）
4. 水印的颜色（默认为白色）

### 第二步：准备 Mask

Mask 是一个黑底白字的图片：
- **黑色区域**：表示无水印（alpha = 0）
- **白色区域**：表示有水印（alpha > 0）

Mask 可以通过以下方式创建：
1. 从无水印的图片中截取水印区域
2. 使用图像编辑工具创建
3. 使用本 Skill 提供的示例 Mask（位于 `assets/` 目录）

### 第三步：执行水印去除

算法公式：`Original = (Composite - Watermark × α) / (1 - α)`

## 参考资源

使用 `references/algorithm.md` 查看详细的算法说明、参数调整和局限性。

## 示例 Mask

Skill 提供了两个 Google Gemini/Nano Banana 水印的 Mask 示例：
- `assets/mask_48.png` - 48px 水印 Mask（用于较小尺寸的图片）
- `assets/mask_96.png` - 96px 水印 Mask（用于较大尺寸的图片）

这些 Mask 专门针对 Google Gemini/Nano Banana 的水印形状设计。如果需要去除其他水印，需要创建对应的 Mask。

## 使用脚本快速去除水印

Skill 提供了 Python 脚本 `scripts/remove_watermark.py`，可以直接运行去除水印：

```bash
# 基本用法
python3 scripts/remove_watermark.py input.png output.png

# 完整用法（指定边距）
python3 scripts/remove_watermark.py input.png output.png 32
```

脚本会自动：
1. 检测图片是否有水印
2. 根据图片尺寸选择合适的 Mask（48px 或 96px）
3. 执行 Reverse Alpha Blending 算法
4. 保存处理后的图片

**依赖**：需要安装 Pillow 和 NumPy
```bash
pip install Pillow numpy
```

## 实现注意事项

1. **Alpha 强度调整**：如果水印去除不干净，可以增大 alpha 强度系数；如果去除后有痕迹，可以减小
2. **边距调整**：水印距离边缘的边距需要根据实际情况调整
3. **Mask 选择**：根据图片尺寸选择合适的 Mask（大图片用大 Mask，小图片用小 Mask）
4. **边界处理**：确保水印位置不会超出图片边界
