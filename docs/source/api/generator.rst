Generator
========

Generator 用于生成不同的数据集格式，方便后续进行处理。

JSONDB
------

JSONDB 是 Generator 的子类，用于生成 JSON 格式的数据集。

使用方法:

.. code-block:: python

   from meterviewer.generator.jsondb import get_dataset, set_local_config

   # 设置好本地配置目录，里面包含选出来的数据集
   set_local_config(
     "/data/xiu-hao/work/project/meter-project/meter-viewer/examples/playground/generate_jsondb/config.toml"
   )

   datasets = get_dataset(digit_num=5, is_train=True)

