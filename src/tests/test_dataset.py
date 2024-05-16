from meterviewer import dataset
import pathlib
import pytest

from tests.utils import show_img


@pytest.fixture
def root_path() -> pathlib.Path:
    return pathlib.Path(r"D:\Store\MeterData")


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


def test_scan_pics():
    path = pathlib.Path(r"D:\Store\MeterData\lens_6\XL\XL\M1L1XL\Digit\0")
    count = 0
    pics = []

    def update_count(name):
        nonlocal count, pics
        pics.append(name)
        count += 1

    [update_count(name) for name in dataset.scan_pics(path)]
    assert count == 20
    # assert False, pics
