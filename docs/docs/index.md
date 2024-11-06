# Meter Viewer

meter-viewer is a tool to view and generate meter images.

## Features

> What can `meter-viewer` do?

1. 读取`MeterData`数据集
2. Reuse old dataset format `MeterData`. Make it easy to reuse the library.
3. 使用 `playground/main.py` 可以生成新的数据集。

## TODO
- [ ] create a `data format` for meter dataset.

### Problems

1. 进位状态不一致。这导致不同数位进位状态不太准确，失去了原本的判断依据。
2. 需要筛选出处于进位状态的数据，来重新生成。

### CMD

> !NOTICE
> Not finished.

- CMD 中是所有的命令

## Dependencies

- Future, 使用 returns 框架来完成返回值判定
- [streamui](https://docs.streamlit.io/get-started/tutorials/create-an-app)