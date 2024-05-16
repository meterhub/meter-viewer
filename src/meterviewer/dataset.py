# 统一数据集表示
import typing as t
from string import Template
import pathlib
import functools


def create_dataset(train_nums: int, test_nums: int, save_method: t.Callable):
    pass


def path_fusion(root: pathlib.Path, dataset_name: str, num: int):
    p = root / "lens_6" / "XL" / "XL" / dataset_name / "Digit" / str(num)
    return p


def scan_pics(path: pathlib.Path) -> t.Iterator[pathlib.Path]:
    for p in path.iterdir():
        yield p


def get_dataset_list(root: pathlib.Path) -> t.Iterator[pathlib.Path]:
    for p in root.iterdir():
        if p.is_dir():
            yield p


def read_single_digt(get_root_path: t.Callable, path_fusion: t.Callable, dataset_name: str, num: int) -> t.Callable:
    p: pathlib.Path = get_root_path() / path_fusion(dataset_name, num)
    return functools.partial(scan_pics, p)


def dataset():
    data = {}
    str_template = Template("$name_$peroid.npy")

    names = ["x", "y"]
    peroids = ["train", "test"]

    s = str_template.safe_substitute(name="train", peroid="2021")

    def get_root_path():
        pass
