datasets
=========

数据集相关接口

read
-----

数据集读取相关的接口

config
^^^^^^

读取配置文件中的标签，标记数值。

::: meterviewer.datasets.read.config


single
^^^^^^

::: meterviewer.datasets.read.single


detection
^^^^^^^

Read block area.

.. code-block:: python

   sample_dataset = "M1L3XL"

   def select_one(root_path, dataset_name: str) -> pathlib.Path:
     """第一个图片"""
     return pathlib.Path(detection.list_images(root_path, dataset_name)[0])


   def test_read_to_get(root_path):
     res = detection.read_image_area(
       select_one(root_path, sample_dataset),
     )
     assert len(res) > 0

这样可以读取任意一个图片的 block 值.

::: meterviewer.datasets.read.detection