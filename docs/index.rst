
Meter Viewer
============

meter-viewer is a tool to view and generate meter images.

Features
--------

..

   What can ``meter-viewer`` do?



#. 读取\ ``MeterData``\ 数据集
#. Reuse old dataset format ``MeterData``. Make it easy to reuse the library.
#. 使用 ``playground/main.py`` 可以生成新的数据集。
#. Validate ``data format`` for meter dataset. Check the dataset with ``meterviewer.validator``.
#. 生成 jsondb，通过 ``./examples/playground/generate_jsondb/main.ipynb``

Problems
^^^^^^^^


#. 进位状态不一致。这导致不同数位进位状态不太准确，失去了原本的判断依据。
#. 需要筛选出处于进位状态的数据，来重新生成。

Dependencies
------------


* Future, 使用 returns 框架来完成返回值判定
* `streamui <https://docs.streamlit.io/get-started/tutorials/create-an-app>`_


.. toctree::
   :maxdepth: 2
   :caption: 基础文档

   general/index

.. toctree::
   :maxdepth: 2
   :caption: 示例
   
   examples/index

.. toctree::
   :maxdepth: 2
   :caption: 功能文档

   views/index
   views/quickstart

.. toctree::
   :maxdepth: 2
   :caption: API参考

   api/index
   api/generator
   api/datasets_v1
   api/datasets
   api/img
   api/meterset

.. toctree::
   :maxdepth: 3
   :caption: 其他资源

   journals/index
   uncommon/index

