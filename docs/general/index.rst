通用文档
========

本节包含 Meter Viewer 的基本概念和通用功能说明。


一个简单的 API
---------------

您可以用 MeterSet 来读取图片，例如，`meterset(name='XL1213)`，

.. code-block:: python

   from meterviewer.meterset import MeterSet

   meterset = MeterSet('XL1123')
   meterset.images(i)

可以读取对应的图片，

.. code-block:: python

   meterset.pos(i)


可以读取对应的位置，

.. code-block:: python

   meterset.values(i)

可以读取对应的数值。



.. toctree::
   :maxdepth: 2

   introduction
   installation
   quickstart
   configuration
   files
   func