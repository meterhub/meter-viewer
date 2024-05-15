# 统一数据集表示
import typing as t
from string import Template


def create_dataset(train_nums: int, test_nums: int, save_method: t.Callable):
    pass


def dataset():
    data = {}
    str_template = Template("$name_$peroid.npy")

    names = ["x", "y"]
    peroids = ["train", "test"]

    s = str_template.safe_substitute(name="train", peroid="2021")

    def get_root_path():
        pass
