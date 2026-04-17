#!/usr/bin/env python3
"""
图片转 PDF Skill
将指定目录下的图片合并为 PDF 文件
"""

import os
import sys
import subprocess
import re


def install_dependency():
    """检查并安装 img2pdf 库"""
    try:
        import img2pdf
        return True
    except ImportError:
        print("检测到缺少 img2pdf 库，正在自动安装...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "img2pdf"])
            print("img2pdf 安装成功！")
            return True
        except subprocess.CalledProcessError as e:
            print(f"安装 img2pdf 失败: {e}")
            print("请手动运行: pip install img2pdf")
            return False


def natural_sort_key(filename):
    """
    自然排序（Alphanumeric sort）
    将文件名中的数字部分按数值排序
    """
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(r'(\d+)', filename)]


def get_image_files(input_dir):
    """
    获取指定目录下的所有 jpg 和 png 文件
    返回按自然排序后的文件路径列表
    """
    if not os.path.exists(input_dir):
        raise FileNotFoundError(f"输入文件夹不存在: {input_dir}")

    if not os.path.isdir(input_dir):
        raise NotADirectoryError(f"路径不是文件夹: {input_dir}")

    valid_extensions = ('.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG')

    image_files = [
        f for f in os.listdir(input_dir)
        if f.endswith(valid_extensions) and os.path.isfile(os.path.join(input_dir, f))
    ]

    if not image_files:
        raise ValueError(f"文件夹 '{input_dir}' 中没有找到 jpg 或 png 图片")

    image_files.sort(key=natural_sort_key)

    return [os.path.join(input_dir, f) for f in image_files]


def convert_images_to_pdf(image_paths, output_path):
    """
    将图片列表转换为 PDF
    """
    import img2pdf

    print(f"\n开始转换，共 {len(image_paths)} 张图片:")
    for i, img_path in enumerate(image_paths, 1):
        print(f"  [{i}] {os.path.basename(img_path)}")

    with open(output_path, "wb") as f:
        f.write(img2pdf.convert(image_paths))

    print(f"\nPDF 生成成功: {output_path}")
    print(f"  文件大小: {os.path.getsize(output_path) / 1024:.1f} KB")


def run(input_dir: str = None, output_filename: str = None) -> str:
    """
    Skill 入口函数

    Args:
        input_dir: 输入图片文件夹路径，默认为脚本同级目录下的 input 文件夹
        output_filename: 输出 PDF 文件名，默认为 output/combined_result.pdf

    Returns:
        操作结果信息
    """
    # 获取脚本所在目录的绝对路径
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # 设置默认输入目录为脚本同级目录下的 input 文件夹
    if input_dir is None:
        input_dir = os.path.join(script_dir, "input")

    # 设置默认输出文件为脚本同级目录下的 output/combined_result.pdf
    if output_filename is None:
        output_dir = os.path.join(script_dir, "output")
        os.makedirs(output_dir, exist_ok=True)
        output_filename = os.path.join(output_dir, "combined_result.pdf")

    print("=" * 50)
    print("图片转 PDF Skill")
    print("=" * 50)
    print(f"输入目录: {input_dir}")
    print(f"输出文件: {output_filename}")

    # 检查并安装依赖
    if not install_dependency():
        return "错误: 无法安装必要的依赖库 img2pdf"

    # 重新导入（安装后可能需要重新导入）
    import img2pdf

    try:
        # 获取图片文件
        image_paths = get_image_files(input_dir)

        # 转换为 PDF
        convert_images_to_pdf(image_paths, output_filename)

        return f"成功生成 PDF: {output_filename} (包含 {len(image_paths)} 张图片)"

    except FileNotFoundError as e:
        return f"错误: {e}。请创建 '{input_dir}' 文件夹并放入图片文件"

    except ValueError as e:
        return f"错误: {e}"

    except Exception as e:
        return f"转换失败: {e}"


if __name__ == "__main__":
    # 命令行调用支持
    import argparse

    # 获取脚本所在目录，用于显示帮助信息
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_input = os.path.join(script_dir, "input")
    default_output = os.path.join(script_dir, "output", "combined_result.pdf")

    parser = argparse.ArgumentParser(description="将图片合并为 PDF")
    parser.add_argument("--input-dir", "-i", default=None, help=f"输入图片文件夹 (默认: {default_input})")
    parser.add_argument("--output", "-o", default=None, help=f"输出 PDF 文件名 (默认: {default_output})")
    args = parser.parse_args()

    result = run(args.input_dir, args.output)
    print(result)
