"""create new generated dataset, generate all suitable images."""

import functools
import typing as t
from meterviewer.datasets import dataset, single, config, imgv
from meterviewer import files, img, T
from meterviewer.imgs import cut
from pathlib import Path as P
from PIL import Image


def cut_one_img(filepath: P) -> t.Tuple[T.ImgList, T.DigitStr]:
    im, val, pos = imgv.view_one_img_v(filepath)
    xml_path = config.get_xml_config_path(filepath, "single")
    pos_list = config.read_rect_from_file(xml_path, "single")

    assert isinstance(pos_list, t.List)
    im_list = []
    for pos in pos_list:
        im1 = cut.cut_img(im, rect=pos.to_dict())
        im_list.append(im1)
    return im_list, list(val)


SaveFunc = t.Callable[[T.Img, str, int], t.Any]


def create_save_func(dataset_path: P, original_filepath: P) -> SaveFunc:
    assert dataset_path.exists(), f"the dataset: {dataset_path} should exist"

    def save_to_disk(im: T.Img, val: str, i: int):
        folder = dataset_path / val
        folder.mkdir(exist_ok=True)
        Image.fromarray(im).save(folder / f"{original_filepath.stem}_{i}.png")

    return save_to_disk


def cut_save_one(root_path: P, filepath: P):

    def cut_save(filepath: P, save_to_disk: SaveFunc):
        """切割图片并保存到磁盘上."""
        im_list, val = cut_one_img(filepath)
        for i, im in enumerate(im_list):
            save_to_disk(im, val[i], i)

    cut_save(filepath, create_save_func(root_path / "./generated", filepath))


def generate_dataset(root_path: P, total: int):
    """total: the total number of digits."""

    def read_rand_img(digit: int | str):
        return single.read_rand_img(
            digit=digit,
            root=root_path,
            get_dataset=lambda: "M1L1XL",
        )

    def gen_block(
        the_digit: T.DigitStr,
    ):
        return dataset.generate_block_img(
            the_digit=the_digit,
            join_func=dataset.join_with_resize,
            read_rand_img=read_rand_img,
        )

    path = root_path / "generated"
    path.mkdir(exist_ok=True)

    filesave = functools.partial(
        files.save_img_labels_with_default,
        prefix_name=path,
        save_to_disk=files.save_to_disk,
    )

    def check_imgs(imglist):
        size = imglist[0].shape
        img.show_img(imglist[0], is_stop=0)
        imgs = img.resize_imglist(imglist)
        for im in imgs:
            img.show_img(im, is_stop=0)
            assert size == im.shape

    create_dataset = dataset.create_dataset_func(check_imgs=lambda x: None)
    create_dataset(
        length=5,
        nums=10,
        gen_block_img=gen_block,
        save_dataset=filesave,
    )
