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


其中，``config.toml`` 文件内容如下:

.. code-block:: toml

  [base]
  root_path = "/data/xiu-hao/work/Dataset/MeterData/"
  description = "These dataset has high quality, could be used to generate block image. The length is 5."
  output_path = "meterdb.json"

  [base.6_digit]

  train_dataset = [
      "M2L10XL",
      "M3L1X",
      "neweyem6l1XL",
      "M1L4XL",
      "M3L10XL",
      "M10L1XL",
      "M2L9XL",
      "neweyem3l1XL",
      "M1L10XL",
      "M2L1XL",
      "M8L10XL",
      "M2L8XL",
      "M2L7XL",
      "neweyem1l4XL",
      "M2L2XL",
      "M8L1XL",
      "M3L6XL",
      "neweyem8l1XL",
      "M8L2XL",
      "M3L8XL",
      "neweyem7l1XL",
      "M1L6XL",
      "M8L7XL",
      "M3L9XL",
      "neweyem1l1XL",
      "M2L3XL",
      "M3L2XL",
      "M1L9XL",
      "M1L1XL",
      "M1L5XL",
      "M1L8XL",
  ]

  test_dataset = [
      "M8L10CS",
      "M1L7CS",
      "neweyem8l3CS",
      "M10L4CS",
      "neweyem3l4CS",
      "neweyem7l2CS",
      "M3L7CS",
      "M8L9CS",
      "M3L4CS",
      "neweyem7l1CS",
      "M10L3CS",
      "neweyem8l1CS",
      "neweyem1l2CS",
      "M10L10CS",
      "M2L6CS",
      "M3L3CS",
      "M8L8CS",
      "M8L1CS",
      "neweyem1l3CS",
      "neweyem7l4CS",
      "neweyem8l2CS",
      "M10L1CS",
      "neweyem6l5CS",
      "M3L5CS",
      "M10L6CS",
      "M1L4CS",
      "M1L8CS",
      "M2L10CS",
      "M8L3CS",
      "neweyem3l2CS",
      "M7666-1112L0C2640CS",
      "M1L9CS",
      "neweyem8l5CS",
      "neweyem3l3CS",
      "neweyem6l1CS",
      "M10L5CS",
      "M8L4CS",
      "neweyem7l5CS",
      "M10L9CS",
      "M3L10CS",
      "M1L6CS",
      "M10L8CS",
      "M10L2CS",
      "M1L3CS",
      "M2L3CS",
      "M2L9CS",
      "M8L7CS",
      "M7666-3576L1C2640CS",
      "M10L7CS",
      "M2L7CS",
      "M2L5CS",
      "M8L2CS",
      "M2L8CS",
      "M1L5CS",
      "M3L6CS",
      "neweyem7l3CS",
      "M8L5CS",
      "M3L8CS",
      "neweyem1l5CS",
      "neweyem1l4CS",
      "M3L2CS",
      "neweyem6l2CS",
      "M3L1CS",
      "M8L6CS",
      "M2L4CS",
      "neweyem6l4CS",
      "M7666-3576L0C2640CS",
      "M3L9CS",
      "neweyem3l1CS",
      "neweyem8l4CS",
      "M7666-8936L1C2640CS",
      "M1L10CS",
      "M2L1CS",
      "M7666-8936L0C2640CS",
      "neweyem3l5CS",
      "neweyem1l1CS",
      "M1L1CS",
      "neweyem6l3CS",
      "M2L2CS",
  ]

  [base.5_digit]

  train_dataset = [
      "M11L5CS",
      "M4L3CS",
      "M5L13CS",
      "M11L2CS",
      "neweyem11l2CS",
      "M5L14CS",
      "M5L15CS",
      "M4L1CS",
      "M5L2CS",
      "M5L4CS",
      "M5L11CS",
      "M11L4CS",
      "M5L16CS",
      "M5L1CS",
      "M11L3CS",
      "M5L12CS",
      "M4L2CS",
      "M11L1CS",
      "M5L3CS",
      "M4L5CS",
      "neweyem11l1CS",
      "M5L18CS",
      "M4L4CS",
      "M5L17CS",
  ]
  test_dataset = [
      "M5L3XL",
      "M5L4XL",
      "M4L5XL",
      "M5L16XL",
      "M5L18XL",
      "M5L14XL",
      "M11L3XL",
      "M11L4XL",
      "M5L17XL",
      "M5L12XL",
      "M4L3XL",
      "M5L15XL",
      "20181112xnd",
      "M5L1XL",
      "M4L2XL",
      "M11L2XL",
      "M5L11XL",
      "M4L1XL",
      "M5L13XL",
      "M4L4XL",
      "M5L2XL",
      "neweyem11l1XL",
      "M11L1XL",
      "neweyem11l2XL",
      "M11L5XL",
  ]

