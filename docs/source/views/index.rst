视图文档
========

本节介绍 Meter Viewer 的各种视图功能和使用方法。

DatasetView
--------------

可以查看 Dataset 中的示例；以下的代码是 functional 的风格。

.. code-block:: python
   # 在使用这个方法之前，需要首先定义其他的变量，例如 jsondb.set_local_config

   from meterviewer.views.dataset import gen_plt_images, get_random_image_by_dataset

   # 需要获取数据集列表，可以用 get-dataset
   datasets = get_dataset(digit_num=5, is_train=True)

   # 获取随机图片
   im = get_random_image_by_dataset(datasets.dataset_list[0], digit_num, stage)
   plt.imshow(im)


