#!/usr/bin/env python3
"""
Google Gemini 水印去除工具
使用 Reverse Alpha Blending 算法去除右下角的 Google Gemini 水印
"""

import sys
from PIL import Image
import numpy as np

# Alpha 强度调整系数
ALPHA_INTENSITY = 1.0

def load_mask(mask_path):
    """加载并预处理 Mask"""
    mask = Image.open(mask_path).convert('RGBA')
    mask_array = np.array(mask)

    # 从 RGB 亮度提取 alpha 值
    # 原始 mask 是黑底白字，白色区域的亮度作为 alpha
    luminance = (0.299 * mask_array[:,:,0] +
                 0.587 * mask_array[:,:,1] +
                 0.114 * mask_array[:,:,2])

    # 创建新的 mask：RGB 为白色（水印颜色），alpha 为亮度
    new_mask = np.zeros_like(mask_array)
    new_mask[:,:,0] = 255  # R
    new_mask[:,:,1] = 255  # G
    new_mask[:,:,2] = 255  # B
    new_mask[:,:,3] = luminance.astype(np.uint8)  # Alpha

    return new_mask

def detect_watermark(img_array, mask_array, margin):
    """检测图片是否含有水印"""
    height, width = img_array.shape[:2]
    mask_height, mask_width = mask_array.shape[:2]

    # 计算 mask 在图片右下角的位置
    offset_x = width - mask_width - margin
    offset_y = height - mask_height - margin

    if offset_x < 0 or offset_y < 0:
        return False, "水印位置超出图片范围"

    # 提取水印区域
    watermark_region = img_array[offset_y:offset_y+mask_height,
                                 offset_x:offset_x+mask_width]

    # 计算水印区域的平均亮度（只计算 mask alpha > 0.1 的区域）
    mask_alpha = mask_array[:,:,3] / 255.0
    alpha_mask = mask_alpha > 0.1

    if not np.any(alpha_mask):
        return False, "Mask 无有效区域"

    watermark_brightness = np.mean(watermark_region[:,:,0][alpha_mask]) * 0.299 + \
                          np.mean(watermark_region[:,:,1][alpha_mask]) * 0.587 + \
                          np.mean(watermark_region[:,:,2][alpha_mask]) * 0.114

    # 计算周围参考区域亮度
    sample_size = min(mask_width, mask_height)
    surrounding_brightness = []

    # 左侧参考区域
    left_start = max(0, offset_x - sample_size)
    if left_start < offset_x:
        left_region = img_array[offset_y:offset_y+mask_height, left_start:offset_x]
        surrounding_brightness.append(np.mean(left_region[:,:,0]) * 0.299 +
                                      np.mean(left_region[:,:,1]) * 0.587 +
                                      np.mean(left_region[:,:,2]) * 0.114)

    # 上方参考区域
    top_start = max(0, offset_y - sample_size)
    if top_start < offset_y:
        top_region = img_array[top_start:offset_y, offset_x:offset_x+mask_width]
        surrounding_brightness.append(np.mean(top_region[:,:,0]) * 0.299 +
                                     np.mean(top_region[:,:,1]) * 0.587 +
                                     np.mean(top_region[:,:,2]) * 0.114)

    avg_surrounding = np.mean(surrounding_brightness) if surrounding_brightness else 128
    brightness_diff = watermark_brightness - avg_surrounding

    has_watermark = brightness_diff > 10

    return has_watermark, {
        "watermark_brightness": watermark_brightness,
        "surrounding_brightness": avg_surrounding,
        "brightness_diff": brightness_diff,
        "threshold": 10,
        "has_watermark": has_watermark
    }

def reverse_alpha_blend(img_array, mask_array, margin, alpha_intensity=ALPHA_INTENSITY):
    """执行 Reverse Alpha Blending 算法"""
    height, width = img_array.shape[:2]
    mask_height, mask_width = mask_array.shape[:2]

    # 计算 mask 在图片右下角的位置
    offset_x = width - mask_width - margin
    offset_y = height - mask_height - margin

    # 复制图片数据
    result = img_array.copy()

    # 对每个像素应用逆向公式
    for my in range(mask_height):
        for mx in range(mask_width):
            img_x = offset_x + mx
            img_y = offset_y + my

            if img_x >= width or img_y >= height:
                continue

            # 获取 alpha 值并应用强度调整
            alpha = (mask_array[my, mx, 3] / 255.0) * alpha_intensity
            alpha = min(alpha, 0.99)  # 防止除零

            if alpha < 0.01:
                continue  # 跳过低 alpha 区域

            inv_alpha = 1 - alpha
            if inv_alpha < 0.01:
                continue  # 完全覆盖，无法还原

            # 水印颜色（白色）
            wm_r, wm_g, wm_b = 255, 255, 255

            # 当前像素值（带水印）
            comp_r = float(img_array[img_y, img_x, 0])
            comp_g = float(img_array[img_y, img_x, 1])
            comp_b = float(img_array[img_y, img_x, 2])

            # Reverse Alpha Blending
            orig_r = (comp_r - wm_r * alpha) / inv_alpha
            orig_g = (comp_g - wm_g * alpha) / inv_alpha
            orig_b = (comp_b - wm_b * alpha) / inv_alpha

            # 限制在 0-255 范围内
            result[img_y, img_x, 0] = np.clip(orig_r, 0, 255)
            result[img_y, img_x, 1] = np.clip(orig_g, 0, 255)
            result[img_y, img_x, 2] = np.clip(orig_b, 0, 255)

    return result

def remove_watermark(input_path, output_path, mask_path, margin):
    """去除水印的主函数"""
    print(f"📸 加载图片: {input_path}")
    img = Image.open(input_path).convert('RGB')
    img_array = np.array(img)

    print(f"📏 图片尺寸: {img.size[0]}x{img.size[1]}")

    print(f"🎭 加载 Mask: {mask_path}")
    mask_array = load_mask(mask_path)
    print(f"📏 Mask 尺寸: {mask_array.shape[1]}x{mask_array.shape[0]}")

    # 检测水印
    print("\n🔍 检测水印...")
    has_watermark, detection_info = detect_watermark(img_array, mask_array, margin)

    if isinstance(detection_info, dict):
        print(f"   水印区域亮度: {detection_info['watermark_brightness']:.1f}")
        print(f"   周围区域亮度: {detection_info['surrounding_brightness']:.1f}")
        print(f"   亮度差: {detection_info['brightness_diff']:.1f}")
        print(f"   阈值: {detection_info['threshold']}")
        print(f"   检测结果: {'✅ 检测到水印' if detection_info['has_watermark'] else '❌ 未检测到水印'}")
    else:
        print(f"   ⚠️ {detection_info}")
        has_watermark = False

    if not has_watermark:
        print("\n⚠️ 未检测到水印，将保存原图")
        img.save(output_path)
        return False

    # 去除水印
    print(f"\n🔧 开始去除水印 (Alpha 强度: {ALPHA_INTENSITY})...")
    result_array = reverse_alpha_blend(img_array, mask_array, margin, ALPHA_INTENSITY)

    # 保存结果
    result_img = Image.fromarray(result_array.astype(np.uint8))
    result_img.save(output_path)
    print(f"✅ 已保存到: {output_path}")

    return True

def main():
    if len(sys.argv) < 3:
        print("用法: python remove_watermark.py <输入图片> <输出图片> [margin]")
        print("示例: python remove_watermark.py input.png output.png 32")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    margin = int(sys.argv[3]) if len(sys.argv) > 3 else 32

    # 根据图片尺寸选择 mask
    img = Image.open(input_path)
    if img.size[0] > 1024 and img.size[1] > 1024:
        mask_path = "/Users/fxj/dotfiles/.agents/skills/watermark-remover/assets/mask_96.png"
        margin = 64
    else:
        mask_path = "/Users/fxj/dotfiles/.agents/skills/watermark-remover/assets/mask_48.png"
        margin = 32

    remove_watermark(input_path, output_path, mask_path, margin)

if __name__ == "__main__":
    main()
