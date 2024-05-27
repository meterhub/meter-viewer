import typing as t
import toml
import pathlib
import random
import functools
from meterviewer.datasets import dataset, single
from meterviewer import files
from meterviewer import img
from . import config_path

from meterviewer.labeling.config import get_root_path


dataset_list: t.List[str] = []


def get_dataset() -> str:
    global dataset_list
    if len(dataset_list) == 0:
        with open(config_path, "r") as f:
            data = toml.load(f)
        dataset_list = data["generate_config"]["dataset"]
    return random.choice(dataset_list)


def main():
    P = functools.partial
    root_path = get_root_path()

    gen_block = P(
        dataset.generate_block_img,
        root_path=root_path,
        join_func=dataset.join_with_resize,
        get_dataset=get_dataset,
        read_rand_img=P(single.read_rand_img, promise=True),
    )

    generated_path = root_path / pathlib.Path(r"generated")
    generated_path.mkdir(exist_ok=True)

    filesave = P(
        files.save_img_labels,
        prefix_name=generated_path,
        save_to_disk=files.save_to_disk,
    )

    def check_imgs(imglist):
        size = imglist[0].shape
        imgs = img.resize_imglist(imglist)
        for im in imgs:
            assert size == im.shape

    dataset.create_dataset_func(check_imgs=lambda x: None)(
        length=8,
        nums=10,
        gen_block_img=gen_block,
        save_dataset=filesave,
    )
