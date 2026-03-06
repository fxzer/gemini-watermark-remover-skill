# Reverse Alpha Blending 算法原理

## 基本概念

Reverse Alpha Blending 是一种用于去除半透明水印的算法。当水印通过 Alpha Blending 叠加到原图上时，可以通过逆向计算还原原图。

## Alpha Blending 公式

正常 Alpha Blending（混合）公式：

```
Composite = Original × (1 - α) + Watermark × α
```

其中：
- `Composite` - 混合后的图片（带水印）
- `Original` - 原图
- `Watermark` - 水印层
- `α` - 透明度 (0-1)

## Reverse Alpha Blending 公式

从上述公式推导出逆向公式：

```
Original = (Composite - Watermark × α) / (1 - α)
```

## 实现步骤

### 1. 准备 Mask

Mask 是一个与水印形状相同的图片：
- **黑底白字**：黑色区域 alpha=0（无水印），白色区域 alpha>0（有水印）
- 从 RGB 亮度提取 alpha 值：`alpha = luminance = 0.299×R + 0.587×G + 0.114×B`

### 2. 水印检测

检测图片是否有水印的方法：
- 计算水印区域的平均亮度
- 计算周围参考区域的平均亮度
- 如果水印区域明显更亮（差值 > 阈值），则认为有水印

### 3. 执行逆向处理

对每个像素应用逆向公式：

```javascript
for (each pixel in watermark region) {
    let alpha = maskAlpha * alphaIntensity;
    alpha = Math.min(alpha, 0.99); // 防止除零

    if (alpha < 0.01) continue; // 跳过低 alpha 区域
    if (1 - alpha < 0.01) continue; // 跳过完全覆盖区域

    // Reverse Alpha Blending
    original = (composite - watermark * alpha) / (1 - alpha);
}
```

## 参数调整

### Alpha 强度调整系数

```javascript
export const ALPHA_INTENSITY = 1.0;
```

- 如果水印去除不干净，增大值（如 1.2）
- 如果去除后有明显痕迹，减小值（如 0.8）

### 边距调整

水印距离右下角的边距需要根据实际情况调整：

```javascript
export const MASK_CONFIGS = [
    { size: 96, path: '/assets/mask_96.png', margin: 64 },
    { size: 48, path: '/assets/mask_48.png', margin: 32 }
];
```

## 局限性

1. **固定位置水印** - 算法要求水印位置固定
2. **半透明水印** - 不适用于完全不透明的水印
3. **Mask 准确性** - 效果取决于 Mask 的准确度
4. **颜色限制** - 适用于单色水印（如白色）

## 适用场景

- ✅ 白色半透明水印
- ✅ 固定位置（如右下角）
- ✅ 有准确的 Mask 图
- ❌ 彩色水印
- ❌ 随机位置水印
- ❌ 完全不透明水印
