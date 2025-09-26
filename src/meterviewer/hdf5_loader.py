"""
HDF5数据加载器 - 用于访问迁移到HDF5格式的MeterViewer数据
"""

import h5py
import numpy as np
from pathlib import Path
from typing import Optional, List, Dict, Tuple, Union
import logging
from contextlib import contextmanager

logger = logging.getLogger(__name__)


class HDF5MeterLoader:
    """HDF5格式的MeterViewer数据加载器"""
    
    def __init__(self, hdf5_path: Union[str, Path]):
        self.hdf5_path = Path(hdf5_path)
        if not self.hdf5_path.exists():
            raise FileNotFoundError(f"HDF5文件不存在: {self.hdf5_path}")
            
        # 缓存基本信息
        self._total_images = None
        self._categories = None
        self._lens_types = None
        self._meter_models = None
        self._filename_to_id_cache = None
        
    @contextmanager
    def _open_file(self, mode='r'):
        """安全的文件打开上下文管理器"""
        hf = h5py.File(self.hdf5_path, mode)
        try:
            yield hf
        finally:
            hf.close()
            
    @property 
    def total_images(self) -> int:
        """获取图像总数"""
        if self._total_images is None:
            with self._open_file() as hf:
                self._total_images = hf['index']['stats'].attrs['total_images']
        return self._total_images
        
    @property
    def categories(self) -> List[str]:
        """获取所有类别列表"""
        if self._categories is None:
            with self._open_file() as hf:
                categories = hf['metadata']['categories'][:]
                self._categories = sorted(list(set(cat.decode('utf-8') for cat in categories)))
        return self._categories
        
    @property
    def lens_types(self) -> List[str]:
        """获取所有镜头类型列表"""
        if self._lens_types is None:
            with self._open_file() as hf:
                lens_types = hf['metadata']['lens_types'][:]
                self._lens_types = sorted(list(set(lt.decode('utf-8') for lt in lens_types)))
        return self._lens_types
        
    @property
    def meter_models(self) -> List[str]:
        """获取所有仪表型号列表"""
        if self._meter_models is None:
            with self._open_file() as hf:
                meter_models = hf['metadata']['meter_models'][:]
                self._meter_models = sorted(list(set(mm.decode('utf-8') for mm in meter_models)))
        return self._meter_models
        
    def get_image(self, image_id: int) -> Optional[np.ndarray]:
        """根据ID获取图像数据"""
        if image_id < 0 or image_id >= self.total_images:
            raise IndexError(f"图像ID {image_id} 超出范围 [0, {self.total_images})")
            
        with self._open_file() as hf:
            dataset_name = f'image_{image_id}'
            if dataset_name not in hf['images']:
                logger.warning(f"图像 {dataset_name} 不存在")
                return None
            return hf['images'][dataset_name][:]
            
    def get_image_by_filename(self, filename: str) -> Optional[np.ndarray]:
        """根据原始文件名获取图像数据"""
        image_id = self.get_image_id_by_filename(filename)
        if image_id is None:
            return None
        return self.get_image(image_id)
        
    def get_image_id_by_filename(self, filename: str) -> Optional[int]:
        """根据原始文件名获取图像ID"""
        if self._filename_to_id_cache is None:
            self._build_filename_cache()
            
        return self._filename_to_id_cache.get(filename)
        
    def _build_filename_cache(self):
        """构建文件名到ID的缓存"""
        logger.info("构建文件名索引缓存...")
        with self._open_file() as hf:
            filename_keys = hf['index']['filename_keys'][:]
            filename_values = hf['index']['filename_values'][:]
            
            self._filename_to_id_cache = {
                key.decode('utf-8'): int(value) 
                for key, value in zip(filename_keys, filename_values)
            }
        logger.info(f"文件名索引缓存构建完成，包含 {len(self._filename_to_id_cache)} 条记录")
        
    def get_metadata(self, image_id: int) -> Optional[Dict[str, str]]:
        """获取图像元数据"""
        if image_id < 0 or image_id >= self.total_images:
            raise IndexError(f"图像ID {image_id} 超出范围 [0, {self.total_images})")
            
        with self._open_file() as hf:
            metadata_group = hf['metadata']
            
            return {
                'filename': metadata_group['filenames'][image_id].decode('utf-8'),
                'image_shape': tuple(metadata_group['image_shapes'][image_id]),
                'category': metadata_group['categories'][image_id].decode('utf-8'),
                'dataset_type': metadata_group['dataset_types'][image_id].decode('utf-8'),
                'lens_type': metadata_group['lens_types'][image_id].decode('utf-8'),
                'meter_model': metadata_group['meter_models'][image_id].decode('utf-8'),
            }
            
    def get_images_by_category(self, category: str) -> List[Tuple[int, np.ndarray]]:
        """获取特定类别的所有图像"""
        with self._open_file() as hf:
            categories = hf['metadata']['categories'][:]
            
            # 找到匹配的图像ID
            matching_ids = [
                i for i, cat in enumerate(categories) 
                if cat.decode('utf-8') == category
            ]
            
            # 加载对应的图像
            images = []
            for img_id in matching_ids:
                img_data = self.get_image(img_id)
                if img_data is not None:
                    images.append((img_id, img_data))
                    
        return images
        
    def get_images_by_filter(self, 
                           category: Optional[str] = None,
                           lens_type: Optional[str] = None, 
                           meter_model: Optional[str] = None,
                           dataset_type: Optional[str] = None) -> List[int]:
        """根据条件过滤图像，返回图像ID列表"""
        with self._open_file() as hf:
            metadata_group = hf['metadata']
            
            # 获取所有元数据
            categories = metadata_group['categories'][:] if category else None
            lens_types = metadata_group['lens_types'][:] if lens_type else None
            meter_models = metadata_group['meter_models'][:] if meter_model else None
            dataset_types = metadata_group['dataset_types'][:] if dataset_type else None
            
            matching_ids = []
            for i in range(self.total_images):
                match = True
                
                if category and categories[i].decode('utf-8') != category:
                    match = False
                if lens_type and lens_types[i].decode('utf-8') != lens_type:
                    match = False
                if meter_model and meter_models[i].decode('utf-8') != meter_model:
                    match = False
                if dataset_type and dataset_types[i].decode('utf-8') != dataset_type:
                    match = False
                    
                if match:
                    matching_ids.append(i)
                    
        return matching_ids
        
    def get_batch_images(self, image_ids: List[int]) -> List[Tuple[int, np.ndarray]]:
        """批量获取图像数据"""
        images = []
        with self._open_file() as hf:
            for img_id in image_ids:
                if img_id < 0 or img_id >= self.total_images:
                    logger.warning(f"跳过无效的图像ID: {img_id}")
                    continue
                    
                dataset_name = f'image_{img_id}'
                if dataset_name in hf['images']:
                    img_data = hf['images'][dataset_name][:]
                    images.append((img_id, img_data))
                else:
                    logger.warning(f"图像 {dataset_name} 不存在")
                    
        return images
        
    def get_statistics(self) -> Dict:
        """获取数据集统计信息"""
        with self._open_file() as hf:
            stats_group = hf['index']['stats']
            
            # 获取基本统计信息
            basic_stats = {
                'total_images': stats_group.attrs['total_images'],
                'failed_images': stats_group.attrs['failed_images']
            }
            
            # 计算详细统计信息
            metadata_group = hf['metadata']
            
            # 类别分布
            categories = [cat.decode('utf-8') for cat in metadata_group['categories'][:]]
            category_counts = {}
            for cat in categories:
                category_counts[cat] = category_counts.get(cat, 0) + 1
                
            # 镜头类型分布  
            lens_types = [lt.decode('utf-8') for lt in metadata_group['lens_types'][:]]
            lens_counts = {}
            for lt in lens_types:
                lens_counts[lt] = lens_counts.get(lt, 0) + 1
                
            # 数据集类型分布
            dataset_types = [dt.decode('utf-8') for dt in metadata_group['dataset_types'][:]]
            dataset_counts = {}
            for dt in dataset_types:
                dataset_counts[dt] = dataset_counts.get(dt, 0) + 1
                
            return {
                **basic_stats,
                'category_distribution': category_counts,
                'lens_type_distribution': lens_counts,
                'dataset_type_distribution': dataset_counts,
                'unique_categories': len(set(categories)),
                'unique_lens_types': len(set(lens_types)),
                'unique_meter_models': len(set(mm.decode('utf-8') for mm in metadata_group['meter_models'][:])),
            }
            
    def __len__(self) -> int:
        """返回数据集大小"""
        return self.total_images
        
    def __getitem__(self, index: int) -> Tuple[np.ndarray, Dict[str, str]]:
        """支持索引访问"""
        img_data = self.get_image(index)
        metadata = self.get_metadata(index)
        return img_data, metadata