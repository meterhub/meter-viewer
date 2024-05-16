import functools
from meterviewer import dataset, img, types as T
import pathlib
import pytest

from tests.utils import show_img


@pytest.fixture
def root_path() -> pathlib.Path:
    return pathlib.Path(r"D:\Store\MeterData")


def test_generate_block_img(root_path):
    im = dataset.generate_block_img(
        root_path,
        ["1", "2", "3", "4"],
        img.join_img,
        lambda: "M1L1XL",
    )
    show_img(im)

    new_join: T.JoinFunc = functools.partial(dataset.join_with_fix, fix_func=img.resize_imglist)

    im = dataset.generate_block_img(
        root_path,
        ["1", "2", "3", "5"],
        new_join,
        lambda: "M1L1XL",
    )
    show_img(im)


def test_get_random_dataset(root_path):
    _, index = dataset.get_random_dataset(root_path, dataset.get_dataset_list)
    assert index in range(0, 74)


def test_read_random_img(root_path):
    im = dataset.read_rand_img(root_path, "M1L1XL", 5)
    show_img(im)


def test_read_random_digit(root_path):
    path_gen = dataset.read_single_digt(lambda: root_path, dataset.path_fusion, "M1L1XL", 0)()
    p = next(path_gen)
    assert pathlib.Path(p).exists()


def test_dataset_list():
    path = pathlib.Path(r"D:\Store\MeterData\lens_6\XL\XL")
    count = 0
    pics = []

    def update_count(name):
        nonlocal count, pics
        pics.append(name)
        count += 1

    [update_count(name) for name in dataset.get_dataset_list(path)]
    assert count == 74
    # assert False, pics
