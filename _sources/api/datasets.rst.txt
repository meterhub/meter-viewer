datasets
=========

数据集相关接口，用于操作整个数据集，而不是单张图片。

read
-----

数据集读取相关的接口

config
^^^^^^

读取配置文件中的标签，标记数值。

.. currentmodule:: meterviewer.datasets.read.config
.. automodule:: meterviewer.datasets.read.config
  :members:

single
^^^^^^

.. currentmodule:: meterviewer.datasets.read.single
.. automodule:: meterviewer.datasets.read.single
  :members:


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

.. currentmodule:: meterviewer.datasets.read.detection
.. automodule:: meterviewer.datasets.read.detection
  :members:
