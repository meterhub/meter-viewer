import typing as t
import toml
import pathlib
import random
import functools
from meterviewer.datasets import dataset, single
from meterviewer import files, T, img
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

    def read_rand_img(digit: int | str) -> T.Img:
        return single.read_rand_img(
            digit=digit,
            root=root_path,
            get_dataset=get_dataset,
            promise=True,
        )

    gen_block = P(
        dataset.generate_block_img,
        join_func=dataset.join_with_resize,
        read_rand_img=read_rand_img,
    )

    generated_path = root_path / pathlib.Path(r"generated")
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
        length=8,
        nums=10,
        gen_block_img=gen_block,
    )
    filesave(imgs, labels)
