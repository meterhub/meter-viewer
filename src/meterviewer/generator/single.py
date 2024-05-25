# generate single digit
from meterviewer.datasets import dataset
from meterviewer import T, img, files
import pathlib
from pathlib import Path as P
from datetime import datetime
import typing as t
import numpy as np


def write_im(im: T.Img, filename: str) -> t.Callable[[P, int, t.Literal["normal", "digit"]], None]:
    def write_to(
        root_path: P,
        digit: int,
        type_: t.Literal["normal", "digit"],
    ):
        # get date
        date = datetime.now().strftime("%Y-%m-%d")
        dataset_path = root_path / f"generated-{date}"
        digit_path = dataset_path / type_ / str(digit)

        # create dir
        digit_path.mkdir(parents=True, exist_ok=True)
        np.save(digit_path / filename, im)

    return write_to


def generate_total_dataset(
    length: int,
    size: int,
    create_np: t.Callable[[T.ImgList, t.List[t.List[int]]], None],
):
    """size: dataset samples size"""

    def get_random_number():
        pass

    def get_one_img(digit: int):
        pass

    def join_with(imglist: T.ImgList):
        # this join-with will check the size
        return img.join_img(imglist, img.size_check)

    def multiple_gen(get_random_number: t.Callable, get_one_img: t.Callable):
        img_list = []
        v_list = []
        for _ in range(size):
            gen_func = generate_block(length, get_random_number)
            im, v = gen_func(get_one_img=get_one_img, join_img=join_with)
            img_list.append(im)
            v_list.append(v)

        return create_np(img_list, v_list)

    return multiple_gen


def generate_block(length: int, get_random_number: t.Callable[[int], t.List[int]]):
    def gen(
        get_one_img: t.Callable[[int], T.Img],
        join_img: t.Callable[[T.ImgList], T.Img],
    ):
        """generate single digit image"""

        number: t.List[int] = get_random_number(length)
        assert len(number) == length

        img_list = []
        for digit in number:
            img = get_one_img(digit)
            img_list.append(img)

        im = join_img(img_list)
        return im, number

    return gen


def img_selector(root_path: P):
    def get_random_img(dataset_name: str) -> t.Tuple[T.ImgList, t.List[str], t.Literal["normal", "digit"]]:
        dp = dataset.get_dataset_path(root_path, dataset_name)

    return get_random_img


def generate_single(
    root_path: pathlib.Path,
    get_random_img: t.Callable[[str], t.Tuple[T.ImgList, t.List[str], t.Literal["normal", "digit"]]],
):
    """generate single digit image, split to normal and digit folder"""

    def handle_img(
        im: T.Img,
        filename: str,
        digit: int,
        type_: t.Literal["normal", "digit"],
    ):
        """write to specific folder"""
        write = write_im(im, filename)
        write(root_path, digit, type_)

    def inner(filename):
        def handle_dataset(dataset_name: str | pathlib.Path):
            imgs, values, types_ = get_random_img(str(dataset_name))
            for im, v in zip(imgs, values):
                handle_img(im, v, filename, types_)

        dataset.handle_datasets(root_path, handle_dataset)

    return inner
