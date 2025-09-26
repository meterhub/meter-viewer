#!/usr/bin/env python3
"""
MeterViewer数据迁移工具：将分散的图像文件整合到HDF5格式

HDF5存储结构设计：
├── /images/                          # 图像数据组
│   ├── image_0 (dataset)            # 第一张图像的像素数据  
│   ├── image_1 (dataset)            # 第二张图像的像素数据
│   └── ...
├── /metadata/ (group)               # 元数据组
│   ├── filenames (dataset)          # 原始完整文件路径
│   ├── image_shapes (dataset)       # 每张图像的尺寸 (height, width, channels)
│   ├── categories (dataset)         # 图像类别/标签 
│   ├── dataset_types (dataset)      # train/test等数据集类型
│   ├── lens_types (dataset)         # 镜头类型 (lens_5, lens_6 等)
│   └── meter_models (dataset)       # 仪表型号
└── /index/ (group)                  # 索引信息
    ├── filename_to_id (dataset)     # 文件名到image_id的映射
    └── stats (dataset)              # 统计信息
"""

import os
import h5py
import cv2
import numpy as np
from pathlib import Path
from tqdm import tqdm
import argparse
from typing import List, Tuple, Dict, Optional
import logging
import re

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class MeterDataMigrator:
    """MeterViewer数据迁移到HDF5的工具类"""
    
    def __init__(self, source_dir: str, output_file: str, compression: str = 'gzip'):
        self.source_dir = Path(source_dir)
        self.output_file = Path(output_file)
        self.compression = compression
        
        # 数据统计
        self.total_images = 0
        self.processed_images = 0
        self.failed_images = 0
        
        # 数据存储
        self.image_data: List[np.ndarray] = []
        self.filenames: List[str] = []
        self.image_shapes: List[Tuple[int, int, int]] = []
        self.categories: List[str] = []
        self.dataset_types: List[str] = []
        self.lens_types: List[str] = []
        self.meter_models: List[str] = []
        
    def scan_images(self) -> List[Path]:
        """扫描所有JPG图像文件"""
        logger.info(f"扫描目录: {self.source_dir}")
        image_files = list(self.source_dir.rglob("*.jpg"))
        self.total_images = len(image_files)
        logger.info(f"找到 {self.total_images} 张图像")
        return image_files
        
    def parse_image_metadata(self, image_path: Path) -> Dict[str, str]:
        """从文件路径解析图像元数据"""
        path_str = str(image_path.relative_to(self.source_dir))
        parts = path_str.split('/')
        
        metadata = {
            'category': 'unknown',
            'dataset_type': 'unknown', 
            'lens_type': 'unknown',
            'meter_model': 'unknown'
        }
        
        # 解析镜头类型
        if 'lens_5' in path_str:
            metadata['lens_type'] = 'lens_5'
        elif 'lens_6' in path_str:
            metadata['lens_type'] = 'lens_6'
        elif 'new_noise_QtData' in path_str:
            metadata['lens_type'] = 'new_noise_QtData'
            
        # 解析数据集类型
        if 'train' in path_str:
            metadata['dataset_type'] = 'train'
        elif 'test' in path_str:
            metadata['dataset_type'] = 'test'
        elif 'val' in path_str or 'validation' in path_str:
            metadata['dataset_type'] = 'validation'
            
        # 解析类别（数字0-9）
        digit_match = re.search(r'/(\d)/', path_str)
        if digit_match:
            metadata['category'] = digit_match.group(1)
            
        # 解析仪表型号
        model_match = re.search(r'(M\d+|QLC-DDS\d+-\d+)', path_str)
        if model_match:
            metadata['meter_model'] = model_match.group(1)
            
        return metadata
        
    def load_and_process_image(self, image_path: Path) -> Optional[np.ndarray]:
        """加载和预处理图像"""
        try:
            # 使用OpenCV加载图像
            img = cv2.imread(str(image_path))
            if img is None:
                logger.warning(f"无法加载图像: {image_path}")
                return None
                
            # 转换为RGB格式 (OpenCV默认是BGR)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            return img_rgb
            
        except Exception as e:
            logger.error(f"处理图像时出错 {image_path}: {e}")
            return None
            
    def process_images(self, image_files: List[Path], batch_size: int = 1000):
        """批量处理图像数据"""
        logger.info("开始处理图像数据...")
        
        with tqdm(total=len(image_files), desc="处理图像") as pbar:
            for image_path in image_files:
                try:
                    # 加载图像
                    img_data = self.load_and_process_image(image_path)
                    if img_data is None:
                        self.failed_images += 1
                        continue
                        
                    # 解析元数据
                    metadata = self.parse_image_metadata(image_path)
                    
                    # 存储数据
                    self.image_data.append(img_data)
                    self.filenames.append(str(image_path.relative_to(self.source_dir)))
                    self.image_shapes.append(img_data.shape)
                    self.categories.append(metadata['category'])
                    self.dataset_types.append(metadata['dataset_type'])
                    self.lens_types.append(metadata['lens_type'])
                    self.meter_models.append(metadata['meter_model'])
                    
                    self.processed_images += 1
                    
                    # 批量写入HDF5（节省内存）
                    if len(self.image_data) >= batch_size:
                        self._write_batch_to_hdf5()
                        
                except Exception as e:
                    logger.error(f"处理图像失败 {image_path}: {e}")
                    self.failed_images += 1
                    
                pbar.update(1)
                
        # 写入剩余数据
        if self.image_data:
            self._write_batch_to_hdf5()
            
        logger.info(f"处理完成: {self.processed_images} 成功, {self.failed_images} 失败")
        
    def _write_batch_to_hdf5(self):
        """将批量数据写入HDF5文件"""
        if not self.image_data:
            return
            
        mode = 'a' if self.output_file.exists() else 'w'
        
        with h5py.File(self.output_file, mode) as hf:
            # 创建或获取组
            if 'images' not in hf:
                images_group = hf.create_group('images')
                metadata_group = hf.create_group('metadata')
                index_group = hf.create_group('index')
            else:
                images_group = hf['images']
                metadata_group = hf['metadata']
                index_group = hf['index']
                
            # 计算当前索引偏移
            current_offset = len([key for key in images_group.keys() if key.startswith('image_')])
            
            # 写入图像数据
            for i, img_data in enumerate(self.image_data):
                img_id = current_offset + i
                dataset_name = f'image_{img_id}'
                images_group.create_dataset(
                    dataset_name, 
                    data=img_data, 
                    compression=self.compression,
                    compression_opts=9 if self.compression == 'gzip' else None
                )
                
            # 写入元数据 (采用可扩展的数据集)
            self._append_to_dataset(metadata_group, 'filenames', self.filenames)
            self._append_to_dataset(metadata_group, 'image_shapes', self.image_shapes)
            self._append_to_dataset(metadata_group, 'categories', self.categories)
            self._append_to_dataset(metadata_group, 'dataset_types', self.dataset_types)
            self._append_to_dataset(metadata_group, 'lens_types', self.lens_types)
            self._append_to_dataset(metadata_group, 'meter_models', self.meter_models)
            
        # 清空缓存
        self.image_data.clear()
        self.filenames.clear()
        self.image_shapes.clear()
        self.categories.clear()
        self.dataset_types.clear()
        self.lens_types.clear()
        self.meter_models.clear()
        
    def _append_to_dataset(self, group, dataset_name: str, data: List):
        """向可扩展数据集追加数据"""
        if not data:
            return
            
        if dataset_name not in group:
            # 创建可扩展数据集
            if dataset_name == 'image_shapes':
                dtype = np.int32
                maxshape = (None, 3)
                data_array = np.array(data, dtype=dtype)
            else:
                dtype = h5py.string_dtype(encoding='utf-8')
                maxshape = (None,)
                data_array = np.array(data, dtype=dtype)
                
            group.create_dataset(
                dataset_name,
                data=data_array,
                maxshape=maxshape,
                compression=self.compression
            )
        else:
            # 扩展现有数据集
            dataset = group[dataset_name]
            old_size = dataset.shape[0]
            new_size = old_size + len(data)
            dataset.resize((new_size,) + dataset.shape[1:])
            
            if dataset_name == 'image_shapes':
                dataset[old_size:new_size] = np.array(data, dtype=np.int32)
            else:
                dataset[old_size:new_size] = np.array(data, dtype=h5py.string_dtype(encoding='utf-8'))
                
    def create_indices(self):
        """创建索引以便快速查询"""
        logger.info("创建索引...")
        
        with h5py.File(self.output_file, 'a') as hf:
            metadata_group = hf['metadata']
            index_group = hf['index']
            
            filenames = metadata_group['filenames'][:]
            
            # 创建文件名到ID的映射
            filename_to_id = {filename.decode('utf-8'): i for i, filename in enumerate(filenames)}
            
            # 存储映射为两个平行数组
            filenames_array = np.array(list(filename_to_id.keys()), dtype=h5py.string_dtype())
            ids_array = np.array(list(filename_to_id.values()), dtype=np.int32)
            
            if 'filename_keys' in index_group:
                del index_group['filename_keys']
            if 'filename_values' in index_group:
                del index_group['filename_values']
                
            index_group.create_dataset('filename_keys', data=filenames_array, compression=self.compression)
            index_group.create_dataset('filename_values', data=ids_array, compression=self.compression)
            
            # 创建统计信息
            stats = {
                'total_images': self.processed_images,
                'failed_images': self.failed_images,
                'categories': list(set(cat.decode('utf-8') for cat in metadata_group['categories'][:])),
                'lens_types': list(set(lt.decode('utf-8') for lt in metadata_group['lens_types'][:])),
                'meter_models': list(set(mm.decode('utf-8') for mm in metadata_group['meter_models'][:]))
            }
            
            if 'stats' in index_group:
                del index_group['stats']
                
            # 存储统计信息为属性
            stats_group = index_group.create_group('stats')
            stats_group.attrs['total_images'] = self.processed_images
            stats_group.attrs['failed_images'] = self.failed_images
            
        logger.info("索引创建完成")
        
    def migrate(self, batch_size: int = 1000):
        """执行完整的数据迁移过程"""
        logger.info("开始MeterViewer数据迁移...")
        
        # 确保输出目录存在
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # 扫描和处理图像
        image_files = self.scan_images()
        if not image_files:
            logger.error("未找到图像文件")
            return False
            
        # 处理图像数据
        self.process_images(image_files, batch_size)
        
        # 创建索引
        self.create_indices()
        
        # 显示结果
        file_size = self.output_file.stat().st_size / (1024*1024*1024)
        logger.info(f"迁移完成!")
        logger.info(f"输出文件: {self.output_file}")
        logger.info(f"文件大小: {file_size:.2f} GB")
        logger.info(f"成功处理: {self.processed_images} 张图像")
        logger.info(f"失败: {self.failed_images} 张图像")
        
        return True


def main():
    parser = argparse.ArgumentParser(description='MeterViewer数据迁移工具')
    parser.add_argument('--source', '-s', required=True, help='源数据目录路径')
    parser.add_argument('--output', '-o', required=True, help='输出HDF5文件路径')
    parser.add_argument('--batch-size', '-b', type=int, default=1000, help='批处理大小 (默认: 1000)')
    parser.add_argument('--compression', '-c', default='gzip', 
                       choices=['gzip', 'lzf', 'szip'], help='压缩方式 (默认: gzip)')
    
    args = parser.parse_args()
    
    # 验证输入
    if not Path(args.source).exists():
        logger.error(f"源目录不存在: {args.source}")
        return 1
        
    # 创建迁移工具并执行
    migrator = MeterDataMigrator(args.source, args.output, args.compression)
    success = migrator.migrate(args.batch_size)
    
    return 0 if success else 1


if __name__ == '__main__':
    exit(main())