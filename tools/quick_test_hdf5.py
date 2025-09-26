#!/usr/bin/env python3
"""
快速小规模HDF5迁移测试

仅使用少量数据（10-50张图像）进行快速验证
"""

import os
import sys
from pathlib import Path
import logging

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def quick_test():
    """快速小规模测试"""
    logger.info("开始快速小规模HDF5迁移测试...")
    
    # 设置路径
    data_dir = Path("/home/svtter/Datasets/MeterData")
    output_file = Path("./test_small_meter_data.h5")
    
    # 检查数据目录
    if not data_dir.exists():
        logger.error(f"数据目录不存在: {data_dir}")
        return False
        
    # 找到前50张图像进行测试
    logger.info("扫描测试图像...")
    test_images = []
    for img_path in data_dir.rglob("*.jpg"):
        test_images.append(img_path)
        if len(test_images) >= 50:
            break
            
    if not test_images:
        logger.error("未找到测试图像")
        return False
        
    logger.info(f"找到 {len(test_images)} 张测试图像")
    
    # 创建临时测试目录结构
    temp_test_dir = Path("./temp_test_data")
    temp_test_dir.mkdir(exist_ok=True)
    
    try:
        # 复制测试图像，保持目录结构
        logger.info("准备测试数据...")
        import shutil
        for img_path in test_images:
            relative_path = img_path.relative_to(data_dir)
            dest_path = temp_test_dir / relative_path
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(img_path, dest_path)
            
        # 导入迁移工具
        sys.path.insert(0, str(Path(__file__).parent))
        from migrate_to_hdf5 import MeterDataMigrator
        
        # 执行迁移
        logger.info(f"开始迁移到 {output_file}...")
        migrator = MeterDataMigrator(
            source_dir=str(temp_test_dir),
            output_file=str(output_file),
            compression='gzip'
        )
        
        success = migrator.migrate(batch_size=25)
        
        if not success:
            logger.error("迁移失败")
            return False
            
        logger.info("迁移完成，开始验证...")
        
        # 验证HDF5文件
        import h5py
        try:
            with h5py.File(output_file, 'r') as hf:
                logger.info(f"HDF5文件结构:")
                
                def print_structure(name, obj):
                    if isinstance(obj, h5py.Group):
                        logger.info(f"  群组: {name}")
                    else:
                        logger.info(f"  数据集: {name}, 形状: {obj.shape}, 类型: {obj.dtype}")
                        
                hf.visititems(print_structure)
                
                # 基本验证
                images_count = len([k for k in hf['images'].keys() if k.startswith('image_')])
                metadata_count = len(hf['metadata']['filenames'])
                
                logger.info(f"图像数量: {images_count}")
                logger.info(f"元数据记录数: {metadata_count}")
                
                if images_count != metadata_count:
                    logger.error("图像数量与元数据不匹配")
                    return False
                    
        except Exception as e:
            logger.error(f"HDF5文件验证失败: {e}")
            return False
            
        # 测试加载器
        logger.info("测试HDF5加载器...")
        try:
            from meterviewer.hdf5_loader import HDF5MeterLoader
            loader = HDF5MeterLoader(output_file)
            
            logger.info(f"加载器图像总数: {loader.total_images}")
            logger.info(f"可用类别: {loader.categories}")
            logger.info(f"镜头类型: {loader.lens_types}")
            
            # 测试加载第一张图像
            if loader.total_images > 0:
                img = loader.get_image(0)
                metadata = loader.get_metadata(0)
                logger.info(f"第一张图像形状: {img.shape if img is not None else None}")
                logger.info(f"第一张图像元数据: {metadata}")
                
        except Exception as e:
            logger.error(f"加载器测试失败: {e}")
            return False
            
        # 测试HDF5MeterSet
        logger.info("测试HDF5MeterSet...")
        try:
            from meterviewer.meterset import HDF5MeterSet
            meterset = HDF5MeterSet(output_file)
            
            logger.info(f"MeterSet大小: {len(meterset)}")
            
            if len(meterset) > 0:
                img = meterset.images(0)
                filename = meterset.get_original_filename(0)
                logger.info(f"通过MeterSet加载的第一张图像形状: {img.shape}")
                logger.info(f"原始文件名: {filename}")
                
        except Exception as e:
            logger.error(f"HDF5MeterSet测试失败: {e}")
            return False
            
        # 显示文件大小
        file_size = output_file.stat().st_size / (1024 * 1024)
        logger.info(f"HDF5文件大小: {file_size:.2f} MB")
        
        logger.info("✅ 快速测试全部通过!")
        return True
        
    except Exception as e:
        logger.error(f"测试过程中出错: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # 清理临时文件
        import shutil
        if temp_test_dir.exists():
            shutil.rmtree(temp_test_dir)
            logger.info("清理临时文件完成")
            
        # 可选：清理输出文件
        # if output_file.exists():
        #     output_file.unlink()
        #     logger.info("清理输出文件完成")


if __name__ == '__main__':
    success = quick_test()
    exit(0 if success else 1)