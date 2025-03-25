import numpy as np
from PIL import Image
import os
from tqdm import tqdm

# 配置参数
num_samples = 10436
height, width, channels = 32, 192, 3
images_dir = r'D:\Files\Code\2024Master\Xiu\MeterData\generated_new_test\images'
label_file = r'D:\Files\Code\2024Master\Xiu\MeterData\generated_new_test\labels.txt'

def validate_and_process():
    # 处理标签
    y = np.zeros((num_samples, 1), dtype=np.int64)
    
    # 读取并验证标签文件
    with open(label_file, 'r') as f:
        for i in tqdm(range(num_samples), desc='验证标签文件'):
            line = f.readline().strip()
            if not line:
                raise ValueError(f"标签文件行数不足，第 {i} 行缺失")
                
            parts = line.split()
            if len(parts) != 2:
                raise ValueError(f"第 {i} 行格式错误：'{line}'")
                
            filename, label = parts
            expected_name = f"img_{i:05d}.jpg"
            
            if filename != expected_name:
                raise ValueError(f"第 {i} 行文件名不匹配，期望 {expected_name}，实际 {filename}")
                
            y[i] = int(label)

    # 处理图像
    x = np.zeros((num_samples, height, width, channels), dtype=np.uint8)
    
    for i in tqdm(range(num_samples), desc='处理图像'):
        filename = f"img_{i:05d}.jpg"
        img_path = os.path.join(images_dir, filename)
        
        try:
            img = Image.open(img_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"图像文件缺失：{filename}")
            
        img_array = np.array(img)
        
        if img_array.shape != (height, width, channels):
            raise ValueError(f"图像 {filename} 尺寸不匹配，期望 {(height, width, channels)}，实际 {img_array.shape}")
            
        x[i] = img_array

    return x, y

# 执行处理并保存结果
x, y = validate_and_process()

y_flat = y.flatten()
formatted_strings = [f"{x:06d}" for x in y_flat]
y_str = np.array(formatted_strings, dtype='<U6').reshape(-1, 1)

np.save('x_test1.npy', x)
np.save('y_test1.npy', y_str)

print("\n转换完成！")
print(f"x_test.npy 形状：{x.shape}")
print(f"y_test.npy 形状：{y.shape}")