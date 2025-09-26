import glob
import pathlib
from typing import Union, Optional
from abc import ABC, abstractmethod

import cv2
import matplotlib.pyplot as plt
import numpy as np

from meterviewer.datasets.read.config import get_xml_config
from meterviewer.datasets.read.detection import read_area_pos
from meterviewer.img.draw import draw_rectangle

# 延迟导入HDF5相关模块，避免强依赖
try:
    from meterviewer.hdf5_loader import HDF5MeterLoader
    HDF5_AVAILABLE = True
except ImportError:
    HDF5_AVAILABLE = False


class BaseMeterSet(ABC):
  """MeterSet的抽象基类"""
  
  @abstractmethod
  def images(self, i: int) -> np.ndarray:
    """获取第i张图像"""
    pass
    
  @abstractmethod  
  def values(self, i: int):
    """获取第i张图像的值"""
    pass
    
  @abstractmethod
  def pos(self, i: int):
    """获取第i张图像的位置信息"""
    pass
    
  @abstractmethod
  def __len__(self) -> int:
    """返回图像总数"""
    pass
    
  def print_img(self, i: int, with_area: bool = False):
    """显示第i张图像"""
    img = self.images(i)
    if with_area:
      try:
        rect = self.pos(i)
        img = draw_rectangle(img, rect)
      except:
        pass  # 如果无法获取位置信息，忽略错误
    plt.imshow(img)
    plt.show()


class MeterSet(BaseMeterSet):
  def __init__(self, root_path: pathlib.Path, name: str):
    self.name = name
    self.root_path = root_path
    self.image_list: list[str] = []
    self.load_list()

  def images(self, i: int):
    if i > len(self.image_list):
      raise ValueError(f"index {i} out of range")
    return cv2.imread(self.image_list[i])


  def __len__(self):
    return len(self.image_list)

  def values(self, i: int):
    if i > len(self.image_list):
      raise ValueError(f"index {i} out of range")
    v, _ = get_xml_config(pathlib.Path(self.image_list[i]))
    return v

  def pos(self, i: int):
    if i > len(self.image_list):
      raise ValueError(f"index {i} out of range")
    filepath = self.image_list[i]
    rect = read_area_pos(pathlib.Path(filepath))
    return rect

  def load_list(self):
    self.image_list = glob.glob(str(self.root_path / self.name / "*.jpg"))


class HDF5MeterSet(BaseMeterSet):
  """基于HDF5存储的MeterSet实现"""
  
  def __init__(self, hdf5_path: Union[str, pathlib.Path], 
               category_filter: Optional[str] = None,
               lens_filter: Optional[str] = None,
               meter_filter: Optional[str] = None,
               dataset_filter: Optional[str] = None):
    if not HDF5_AVAILABLE:
      raise ImportError("HDF5支持不可用，请安装h5py: pip install h5py")
      
    self.hdf5_path = pathlib.Path(hdf5_path)
    self.loader = HDF5MeterLoader(self.hdf5_path)
    
    # 应用过滤器
    if any([category_filter, lens_filter, meter_filter, dataset_filter]):
      self.filtered_ids = self.loader.get_images_by_filter(
        category=category_filter,
        lens_type=lens_filter, 
        meter_model=meter_filter,
        dataset_type=dataset_filter
      )
    else:
      # 使用所有图像
      self.filtered_ids = list(range(len(self.loader)))
      
    # 缓存经常访问的数据
    self._metadata_cache = {}
    
  def images(self, i: int) -> np.ndarray:
    """获取第i张图像（基于过滤后的索引）"""
    if i >= len(self.filtered_ids):
      raise ValueError(f"index {i} out of range (filtered size: {len(self.filtered_ids)})")
      
    real_id = self.filtered_ids[i]
    img_data = self.loader.get_image(real_id)
    
    if img_data is None:
      raise ValueError(f"无法加载图像 (filtered index: {i}, real id: {real_id})")
      
    # 确保图像是RGB格式的uint8
    if img_data.dtype != np.uint8:
      img_data = (img_data * 255).astype(np.uint8)
      
    return img_data
    
  def values(self, i: int):
    """获取第i张图像的值（基于元数据中的category）"""
    if i >= len(self.filtered_ids):
      raise ValueError(f"index {i} out of range (filtered size: {len(self.filtered_ids)})")
      
    real_id = self.filtered_ids[i]
    
    # 从缓存或HDF5获取元数据
    if real_id not in self._metadata_cache:
      self._metadata_cache[real_id] = self.loader.get_metadata(real_id)
      
    metadata = self._metadata_cache[real_id]
    category = metadata['category']
    
    # 如果category是数字字符串，返回数字值
    if category.isdigit():
      return float(category)
    else:
      return category
      
  def pos(self, i: int):
    """获取第i张图像的位置信息（HDF5版本暂不支持位置信息）"""
    if i >= len(self.filtered_ids):
      raise ValueError(f"index {i} out of range (filtered size: {len(self.filtered_ids)})")
      
    # HDF5版本中没有存储位置信息，返回None或默认值
    # 可以考虑在未来版本中添加位置信息到HDF5
    import warnings
    warnings.warn("HDF5MeterSet暂不支持位置信息，返回None", UserWarning)
    return None
    
  def __len__(self) -> int:
    """返回过滤后的图像总数"""
    return len(self.filtered_ids)
    
  def get_original_filename(self, i: int) -> str:
    """获取第i张图像的原始文件名"""
    if i >= len(self.filtered_ids):
      raise ValueError(f"index {i} out of range (filtered size: {len(self.filtered_ids)})")
      
    real_id = self.filtered_ids[i]
    
    if real_id not in self._metadata_cache:
      self._metadata_cache[real_id] = self.loader.get_metadata(real_id)
      
    return self._metadata_cache[real_id]['filename']
    
  def get_metadata(self, i: int) -> dict:
    """获取第i张图像的完整元数据"""
    if i >= len(self.filtered_ids):
      raise ValueError(f"index {i} out of range (filtered size: {len(self.filtered_ids)})")
      
    real_id = self.filtered_ids[i]
    
    if real_id not in self._metadata_cache:
      self._metadata_cache[real_id] = self.loader.get_metadata(real_id)
      
    return self._metadata_cache[real_id]
    
  def get_statistics(self) -> dict:
    """获取当前过滤器下的统计信息"""
    stats = self.loader.get_statistics()
    
    if len(self.filtered_ids) == len(self.loader):
      # 没有过滤，返回全部统计信息
      return stats
    else:
      # 计算过滤后的统计信息
      filtered_metadata = [
        self.loader.get_metadata(img_id) for img_id in self.filtered_ids
      ]
      
      # 重新计算分布
      categories = [meta['category'] for meta in filtered_metadata]
      lens_types = [meta['lens_type'] for meta in filtered_metadata]
      dataset_types = [meta['dataset_type'] for meta in filtered_metadata]
      
      category_counts = {}
      for cat in categories:
        category_counts[cat] = category_counts.get(cat, 0) + 1
        
      lens_counts = {}
      for lt in lens_types:
        lens_counts[lt] = lens_counts.get(lt, 0) + 1
        
      dataset_counts = {}
      for dt in dataset_types:
        dataset_counts[dt] = dataset_counts.get(dt, 0) + 1
        
      return {
        'total_images': len(self.filtered_ids),
        'failed_images': 0,  # 过滤后的数据假设都是有效的
        'category_distribution': category_counts,
        'lens_type_distribution': lens_counts,
        'dataset_type_distribution': dataset_counts,
        'unique_categories': len(set(categories)),
        'unique_lens_types': len(set(lens_types)),
        'unique_meter_models': len(set(meta['meter_model'] for meta in filtered_metadata)),
      }


def create_meterset(source: Union[str, pathlib.Path], 
                   name: Optional[str] = None,
                   **kwargs) -> BaseMeterSet:
  """工厂函数：根据源类型自动创建合适的MeterSet实例"""
  source_path = pathlib.Path(source)
  
  if source_path.suffix.lower() == '.h5' or source_path.suffix.lower() == '.hdf5':
    # HDF5文件
    return HDF5MeterSet(source_path, **kwargs)
  elif source_path.is_dir():
    # 目录（传统方式）
    if name is None:
      raise ValueError("使用目录作为数据源时，必须指定name参数")
    return MeterSet(source_path, name)
  else:
    raise ValueError(f"不支持的数据源类型: {source_path}")


# 向后兼容的别名
MeterSetHDF5 = HDF5MeterSet
