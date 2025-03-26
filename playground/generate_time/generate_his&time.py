# 通过XL原始图像来生成x_train_history.npy & x_time.npy

import os
import numpy as np
from PIL import Image
from PIL import ImageFile

# 启用截断文件处理
ImageFile.LOAD_TRUNCATED_IMAGES = True

def process_dataset(main_folder):
    for folder_name in sorted(os.listdir(main_folder)):
        folder_path = os.path.join(main_folder, folder_name)
        
        if not os.path.isdir(folder_path):
            continue

        # 获取并排序图片文件
        image_files = sorted([f for f in os.listdir(folder_path) if f.lower().endswith('.jpg')])
        if not image_files:
            print(f"跳过空文件夹: {folder_name}")
            continue

        x_train = []
        x_time = []
        valid_count = 0

        for img_file in image_files:
            img_path = os.path.join(folder_path, img_file)
            time_str = os.path.splitext(img_file)[0]
            
            try:
                # 双重验证确保文件完整性
                with Image.open(img_path) as img:
                    img.verify()
                with Image.open(img_path) as img:
                    img_array = np.array(img.convert('RGB'))
                    
                    # 验证图像尺寸
                    if img_array.shape != (240, 320, 3):
                        print(f"尺寸不符跳过: {img_file}")
                        continue
                        
                    x_train.append(img_array)
                    x_time.append(time_str)  # 保持字符串格式
                    valid_count += 1
                    
            except Exception as e:
                print(f"损坏文件跳过: {img_file} | 错误: {str(e)}")
                continue

        if valid_count == 0:
            print(f"警告: {folder_name} 无有效图片")
            continue
            
        try:
            # 转换图像数据
            x_train_np = np.array(x_train, dtype=np.uint8)
            
            # 转换时间数据为二维数组
            if x_time:
                str_length = len(x_time[0])
                # 创建二维字符串数组
                x_time_np = np.array(x_time, dtype=f'U{str_length}')[:, np.newaxis]
                
                # 保存文件
                np.save(os.path.join(folder_path, 'x_train_history.npy'), x_train_np)
                np.save(os.path.join(folder_path, 'x_time.npy'), x_time_np)
                print(f"成功保存: {folder_name} | 图片: {valid_count} | 时间数组形状: {x_time_np.shape}")
        except Exception as e:
            print(f"保存错误: {folder_name} | {str(e)}")

if __name__ == "__main__":
    main_folder = r"D:\Files\Code\2024Master\Xiu\MeterData\lens_6\XL\XL"
    
    if not os.path.exists(main_folder):
        raise ValueError("文件夹路径不存在")
    
    process_dataset(main_folder)