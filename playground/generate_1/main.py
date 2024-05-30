import typing as t
import toml
import pathlib
import random
import functools
from meterviewer.datasets import dataset, single
from meterviewer import files, T, img
from . import config_path

from meterviewer.labeling.config import get_root_path

from loguru import logger
import sys

# 设置控制台输出的日志级别为 WARNING
logger.remove()  # 移除默认的控制台输出
logger.add(sys.stdout, level="ERROR")


dataset_list: t.List[str] = []
getList = t.Literal["dataset", "path"]


def load_config() -> t.Callable[[getList], t.Any]:
    data: t.Optional[dict] = None

    def load_conf() -> dict:
        nonlocal data
        if data is None:
            if len(dataset_list) == 0:
                with open(config_path, "r") as f:
                    data = toml.load(f)
        assert data is not None, config_path
        return data

    def get_dataset() -> str:
        global dataset_list
        data = load_conf()
        dataset_list = data.get("generate_config").get("dataset")
        return random.choice(dataset_list)

    def get_path():
        return load_conf().get("generate_config").get("path")

    def get_func(name: getList) -> t.Callable:
        func_map: t.Mapping[str, t.Callable] = {
            "dataset": get_dataset,
            "path": get_path,
        }
        return func_map[name]

    return get_func


def main():
    P = functools.partial
    root_path = get_root_path()
    get_f = load_config()

    def read_rand_img(digit: int | str) -> T.Img:
        return single.read_rand_img(
            digit=digit,
            root=root_path,
            get_dataset=get_f("dataset"),
            promise=True,
        )

    gen_block = P(
        dataset.generate_block_img,
        join_func=dataset.join_with_resize,
        read_rand_img=read_rand_img,
    )

    generated_path = root_path / pathlib.Path(get_f("path")())
    generated_path.mkdir(exist_ok=True)

    filesave = P(
        files.save_img_labels_with_default,
        prefix_name=generated_path,
        save_to_disk=files.save_to_disk,
    )

    def check_imgs(imglist):
        size = imglist[0].shape
        imgs = img.resize_imglist(imglist)
        for im in imgs:
            assert size == im.shape

    create_dataset = dataset.create_dataset_func(check_imgs=lambda x: None, total=9)
    imgs, labels = create_dataset(
        length=6,
        nums=100000,
        gen_block_img=gen_block,
    )
    filesave(imgs, labels)
