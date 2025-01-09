# Overview


这个文档中包含了 datasets 的相关方法。

`datasets`可以读取一些单字数据集，比如 `MeterData` 这种由 xml, json, *.png 组成的数据集。


## format

一般一个 MeterData 的组成形式如下：

```txt
- ImageSets_block_zoom  # blocked images
- config  # 标签文件，用于 detection
- Numpy_block_zoom # 已经切割的 np
- ImageSets_seg # 通过单子分割的np文件
- id # 编号。每个数据集都有对应的 id，用于 track。
- baocun # 标签文件，数值
- .DS_Store
- coor_all_img_np  # 没有根据 config 切割的文件
- ImageSets # 单子的分割
- Numpy_seg # 单字分割的数据文件
- Digit # 似乎与 digit 相同
```

### config folder

total files:

- `['block.xml', 'type.xml', 'res.xml', 'valid.xml']`
- block: 读数范围
- res: 单个读数的数据和位置

