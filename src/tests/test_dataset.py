import functools
from meterviewer import dataset, img, files
import pathlib
import pytest

from tests.utils import show_img


@pytest.fixture
def root_path() -> pathlib.Path:
    return pathlib.Path(r"D:\Store\MeterData")


def test_view_on_disk():
    dataset.view_dataset_on_disk(
        prefix_name=pathlib.Path(r"D:\Store\MeterData\generated"),
        load_from_disk=files.load_from_disk,
        show=True,
    )


def test_create_dataset(root_path):
    P = functools.partial
    gen_block = P(
        dataset.generate_block_img,
        root_path=root_path,
        join_func=dataset.join_with_resize,
        get_dataset=lambda: "M1L1XL",
    )

    path = pathlib.Path(r"D:\Store\MeterData\generated")
    path.mkdir(exist_ok=True)

    filesave = P(
        files.save_img_labels,
        prefix_name=path,
        save_to_disk=files.save_to_disk,
    )

    dataset.create_dataset(
        length=5,
        nums=10,
        gen_block_img=gen_block,
        save_dataset=filesave,
    )


def test_generate_block_img(root_path):
    im = dataset.generate_block_img(
        ["1", "2", "3", "4"],
        root_path,
        img.join_img,
        lambda: "M1L1XL",
    )
    show_img(im)

    im = dataset.generate_block_img(
        ["1", "2", "3", "5", "6"],
        root_path,
        dataset.join_with_resize,
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
