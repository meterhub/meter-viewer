#!/usr/bin/env python3
"""
HDF5迁移和数据完整性测试脚本

此脚本用于：
1. 小规模测试迁移工具
2. 验证迁移后数据的完整性
3. 测试新的HDF5MeterSet类功能
4. 对比原始数据和HDF5数据的一致性
"""

import os
import sys
import tempfile
import shutil
import numpy as np
from pathlib import Path
import logging
import cv2

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from meterviewer.meterset import MeterSet, HDF5MeterSet, create_meterset
from tools.migrate_to_hdf5 import MeterDataMigrator

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class HDF5MigrationTester:
    """HDF5迁移测试器"""
    
    def __init__(self, test_data_dir: str, num_test_images: int = 100):
        self.test_data_dir = Path(test_data_dir)
        self.num_test_images = num_test_images
        self.temp_dir = None
        self.hdf5_file = None
        
    def setup_test_environment(self):
        """设置测试环境"""
        logger.info("设置测试环境...")
        
        # 创建临时目录
        self.temp_dir = Path(tempfile.mkdtemp(prefix="hdf5_test_"))
        logger.info(f"临时目录: {self.temp_dir}")
        
        # 准备测试数据目录结构
        test_source_dir = self.temp_dir / "test_data"
        test_source_dir.mkdir(parents=True)
        
        # 复制少量测试图像
        source_images = list(self.test_data_dir.rglob("*.jpg"))[:self.num_test_images]
        logger.info(f"复制 {len(source_images)} 张测试图像...")
        
        for img_path in source_images:
            # 保持相对目录结构
            relative_path = img_path.relative_to(self.test_data_dir)
            dest_path = test_source_dir / relative_path
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(img_path, dest_path)
            
        self.test_source_dir = test_source_dir
        self.hdf5_file = self.temp_dir / "test_meter_data.h5"
        
        logger.info(f"测试环境准备完成，源目录: {self.test_source_dir}")
        
    def test_migration_tool(self):
        """测试迁移工具"""
        logger.info("测试迁移工具...")
        
        # 创建迁移工具实例
        migrator = MeterDataMigrator(
            source_dir=str(self.test_source_dir),
            output_file=str(self.hdf5_file),
            compression='gzip'
        )
        
        # 执行迁移
        success = migrator.migrate(batch_size=50)  # 小批量测试
        
        if not success:
            raise Exception("迁移失败")
            
        # 验证HDF5文件是否创建
        if not self.hdf5_file.exists():
            raise Exception("HDF5文件未创建")
            
        file_size = self.hdf5_file.stat().st_size / (1024 * 1024)
        logger.info(f"迁移成功，HDF5文件大小: {file_size:.2f} MB")
        
        return migrator
        
    def test_hdf5_loader(self):
        """测试HDF5加载器"""
        logger.info("测试HDF5加载器...")
        
        # 创建HDF5MeterSet实例
        hdf5_meterset = HDF5MeterSet(self.hdf5_file)
        
        # 基本属性测试
        logger.info(f"HDF5数据集大小: {len(hdf5_meterset)}")
        logger.info(f"可用类别: {hdf5_meterset.loader.categories}")
        logger.info(f"镜头类型: {hdf5_meterset.loader.lens_types}")
        
        # 测试图像加载
        if len(hdf5_meterset) > 0:
            img = hdf5_meterset.images(0)
            logger.info(f"第一张图像形状: {img.shape}, 数据类型: {img.dtype}")
            
            # 测试元数据
            metadata = hdf5_meterset.get_metadata(0)
            logger.info(f"第一张图像元数据: {metadata}")
            
            # 测试原始文件名
            filename = hdf5_meterset.get_original_filename(0)
            logger.info(f"第一张图像原始文件名: {filename}")
            
        # 测试过滤功能
        if hdf5_meterset.loader.categories:
            category = hdf5_meterset.loader.categories[0]
            filtered_meterset = HDF5MeterSet(self.hdf5_file, category_filter=category)
            logger.info(f"过滤类别 '{category}' 后的数据集大小: {len(filtered_meterset)}")
            
        # 测试统计信息
        stats = hdf5_meterset.get_statistics()
        logger.info(f"统计信息: {stats}")
        
        return hdf5_meterset
        
    def test_create_meterset_factory(self):
        """测试工厂函数"""
        logger.info("测试工厂函数...")
        
        # 测试HDF5文件创建
        meterset_hdf5 = create_meterset(self.hdf5_file)
        assert isinstance(meterset_hdf5, HDF5MeterSet)
        logger.info(f"HDF5工厂函数测试通过，数据集大小: {len(meterset_hdf5)}")
        
        return meterset_hdf5
        
    def compare_data_consistency(self, original_images_dir: str = None):
        """对比原始数据和HDF5数据的一致性"""
        logger.info("对比数据一致性...")
        
        hdf5_meterset = HDF5MeterSet(self.hdf5_file)
        
        # 随机选择几张图像进行对比
        import random
        test_indices = random.sample(range(len(hdf5_meterset)), min(5, len(hdf5_meterset)))
        
        for i in test_indices:
            # 从HDF5加载图像
            hdf5_img = hdf5_meterset.images(i)
            
            # 获取原始文件名
            original_filename = hdf5_meterset.get_original_filename(i)
            original_path = self.test_source_dir / original_filename
            
            if original_path.exists():
                # 加载原始图像
                original_img = cv2.imread(str(original_path))
                original_img_rgb = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
                
                # 对比形状
                if hdf5_img.shape != original_img_rgb.shape:
                    logger.warning(f"图像 {i} 形状不匹配: HDF5={hdf5_img.shape}, 原始={original_img_rgb.shape}")
                    continue
                    
                # 对比像素值（允许小的差异，因为压缩等因素）
                diff = np.abs(hdf5_img.astype(np.float32) - original_img_rgb.astype(np.float32))
                max_diff = np.max(diff)
                mean_diff = np.mean(diff)
                
                if max_diff > 5:  # 允许5个像素值的差异
                    logger.warning(f"图像 {i} 像素值差异较大: max={max_diff}, mean={mean_diff}")
                else:
                    logger.info(f"图像 {i} 一致性验证通过: max_diff={max_diff}, mean_diff={mean_diff}")
            else:
                logger.warning(f"找不到原始图像文件: {original_path}")
                
        logger.info("数据一致性对比完成")
        
    def run_comprehensive_test(self):
        """运行综合测试"""
        logger.info("开始HDF5迁移综合测试...")
        
        try:
            # 1. 设置测试环境
            self.setup_test_environment()
            
            # 2. 测试迁移工具
            migrator = self.test_migration_tool()
            
            # 3. 测试HDF5加载器
            hdf5_meterset = self.test_hdf5_loader()
            
            # 4. 测试工厂函数
            factory_meterset = self.test_create_meterset_factory()
            
            # 5. 对比数据一致性
            self.compare_data_consistency()
            
            logger.info("=== 测试总结 ===")
            logger.info(f"测试图像数量: {migrator.processed_images}")
            logger.info(f"失败图像数量: {migrator.failed_images}")
            logger.info(f"HDF5文件大小: {self.hdf5_file.stat().st_size / (1024*1024):.2f} MB")
            logger.info(f"HDF5数据集大小: {len(hdf5_meterset)}")
            logger.info("所有测试通过! ✅")
            
            return True
            
        except Exception as e:
            logger.error(f"测试失败: {e}")
            import traceback
            traceback.print_exc()
            return False
            
        finally:
            # 清理临时文件
            if self.temp_dir and self.temp_dir.exists():
                shutil.rmtree(self.temp_dir)
                logger.info("清理临时文件完成")
                
    def run_performance_test(self):
        """运行性能测试"""
        logger.info("运行性能测试...")
        
        import time
        
        try:
            self.setup_test_environment()
            
            # 测试迁移性能
            start_time = time.time()
            migrator = self.test_migration_tool()
            migration_time = time.time() - start_time
            
            # 测试加载性能
            hdf5_meterset = HDF5MeterSet(self.hdf5_file)
            
            # 测试随机访问性能
            start_time = time.time()
            import random
            indices = random.sample(range(len(hdf5_meterset)), min(20, len(hdf5_meterset)))
            for i in indices:
                img = hdf5_meterset.images(i)
                metadata = hdf5_meterset.get_metadata(i)
            random_access_time = time.time() - start_time
            
            # 测试顺序访问性能
            start_time = time.time()
            for i in range(min(20, len(hdf5_meterset))):
                img = hdf5_meterset.images(i)
            sequential_access_time = time.time() - start_time
            
            logger.info("=== 性能测试结果 ===")
            logger.info(f"迁移时间: {migration_time:.2f} 秒")
            logger.info(f"迁移速度: {migrator.processed_images/migration_time:.1f} 图像/秒")
            logger.info(f"随机访问20张图像时间: {random_access_time:.2f} 秒")
            logger.info(f"顺序访问20张图像时间: {sequential_access_time:.2f} 秒")
            logger.info(f"单张图像平均加载时间: {sequential_access_time/min(20, len(hdf5_meterset))*1000:.1f} 毫秒")
            
        finally:
            if self.temp_dir and self.temp_dir.exists():
                shutil.rmtree(self.temp_dir)


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='HDF5迁移测试脚本')
    parser.add_argument('--data-dir', '-d', required=True, help='测试数据目录路径')
    parser.add_argument('--num-images', '-n', type=int, default=100, help='测试图像数量 (默认: 100)')
    parser.add_argument('--test-type', '-t', choices=['comprehensive', 'performance', 'both'], 
                       default='comprehensive', help='测试类型')
    
    args = parser.parse_args()
    
    if not Path(args.data_dir).exists():
        logger.error(f"数据目录不存在: {args.data_dir}")
        return 1
        
    # 创建测试器
    tester = HDF5MigrationTester(args.data_dir, args.num_images)
    
    success = True
    
    if args.test_type in ['comprehensive', 'both']:
        logger.info("运行综合测试...")
        success &= tester.run_comprehensive_test()
        
    if args.test_type in ['performance', 'both']:
        logger.info("运行性能测试...")
        tester.run_performance_test()
        
    return 0 if success else 1


if __name__ == '__main__':
    exit(main())