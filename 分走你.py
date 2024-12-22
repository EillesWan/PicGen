"""
版权所有 © 2024 EillesWan(EillesWan@outlook.com)
Copyright (R) 2024 EillesWan 

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""




import os
import shutil
from datetime import datetime


def organize_images(source_folder):
    # 确保源文件夹存在
    if not os.path.exists(source_folder):
        print(f"源文件夹 {source_folder} 不存在。")
        return

    # 确保目标文件夹存在
    target_root = os.path.join(os.getcwd(), "#已分类")
    os.makedirs(target_root, exist_ok=True)

    # 确保 ERR 文件夹存在
    err_root = os.path.join(os.getcwd(), "#错误的")
    os.makedirs(err_root, exist_ok=True)

    # 遍历源文件夹及其子文件夹中的所有文件
    for root, dirs, files in os.walk(source_folder):
        for filename in files:
            # 检查文件扩展名是否为 .png, .jpg, 或 .jpeg
            if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                try:
                    # 提取日期部分（假设格式为 yyyymmddhhmmss）
                    date_str = filename[:14]
                    dt = datetime.strptime(date_str, "%Y%m%d%H%M%S")

                    # 创建目标文件夹路径 yyyy mm
                    target_folder = os.path.join(
                        target_root, f"{dt.year:04d} {dt.month:02d}"
                    )
                    os.makedirs(target_folder, exist_ok=True)

                    # 构建完整的目标文件路径
                    target_path = os.path.join(target_folder, filename)

                    # 移动文件
                    source_path = os.path.join(root, filename)
                    shutil.move(source_path, target_path)
                    print(f"已将 {source_path} 移动到 {target_path}")

                except ValueError as e:
                    # 处理无效文件名
                    print(f"跳过文件 {filename}: 无效的日期格式 - {e}")
                    handle_error_file(os.path.join(root, filename), err_root)


def handle_error_file(file_path, err_root):
    # 获取文件的修改时间
    modification_time = os.path.getmtime(file_path)
    dt = datetime.fromtimestamp(modification_time)

    # 创建 ERR 目录下的子目录 yyyy mm
    error_folder = os.path.join(err_root, f"{dt.year:04d} {dt.month:02d}")
    os.makedirs(error_folder, exist_ok=True)

    # 构建完整的错误文件路径
    error_path = os.path.join(error_folder, os.path.basename(file_path))

    # 移动文件到 ERR 目录
    shutil.move(file_path, error_path)
    print(f"已将 {file_path} 移动到 {error_path}")


# 示例调用：读取当前目录下的 #待分类 文件夹
current_directory = os.path.join(os.getcwd(), "#待分类")
organize_images(current_directory)
