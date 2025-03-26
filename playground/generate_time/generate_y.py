import os
import xml.etree.ElementTree as ET
import numpy as np

def extract_names_and_save(base_dir):
    # 遍历主目录下的所有子文件夹
    for folder in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder)
        
        # 检查是否为目录
        if not os.path.isdir(folder_path):
            continue
            
        baocun_path = os.path.join(folder_path, 'baocun')
        
        # 检查baocun文件夹是否存在
        if not os.path.exists(baocun_path):
            print(f"警告：{folder} 中未找到baocun文件夹")
            continue
            
        names = []
        
        # 获取所有XML文件并排序
        xml_files = sorted([f for f in os.listdir(baocun_path) if f.endswith('.xml')])
        
        # 处理每个XML文件
        for xml_file in xml_files:
            xml_path = os.path.join(baocun_path, xml_file)
            
            try:
                tree = ET.parse(xml_path)
                root = tree.getroot()
                
                # 提取name标签内容
                name_element = root.find('.//object/name')
                if name_element is not None:
                    name = name_element.text.strip()
                    names.append([name])  # 保持二维数组结构
            except Exception as e:
                print(f"处理文件 {xml_path} 时出错: {str(e)}")
                continue
        
        # 转换为numpy数组并保存
        if names:
            y_train = np.array(names)
            save_path = os.path.join(folder_path, 'y_train.npy')
            np.save(save_path, y_train)
            print(f"已生成: {save_path} (包含 {len(names)} 个标签)")
        else:
            print(f"警告：{baocun_path} 中没有有效XML文件")

if __name__ == "__main__":
    # 设置主目录路径（需要用户修改为实际路径）
    main_directory = r"D:\Files\Code\2024Master\Xiu\MeterData\lens_6\XL\XL"
    extract_names_and_save(main_directory)