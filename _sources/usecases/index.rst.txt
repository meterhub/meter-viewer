Use Cases
==========

.. _use-cases-label:


自定义加载的数据集
------------------------------


.. code-block:: python

    from meterviewer.dataset import MeterDataset

    train_list = ['M1L1XL', 'M1L3XL', 'M1L4XL']
    train_folder = 'lens_6/XL/XL'
    test_folder = 'lens_6/CS/all_CS'
    test_list = ['M1L1CS', 'M1L3CS', 'M1L4CS']

    class CustomDataset(MeterDataset):
      def load_metersets(self):
        self.build_metersets(train_list, train_folder, test_list, test_folder)


    ds = CustomDataset(root_dir="data", stage="train")

    print(ds.start_end_list)
    data = ds[10]
    print(data['pos'])


通过这样的方式，可以选择加载的数据集。用户可以指定训练数据集的列表，以及测试数据集的列表。