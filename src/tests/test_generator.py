from meterviewer.generator import single, db, total
from meterviewer import littledb, files
from pathlib import Path as P
import pytest

from tests.utils import show_img


@pytest.mark.skip("cannot easy to test.")
def test_create_db(root_path):
    db.create_db(root_path)


def test_cut_one_img(root_path):
    # 裁剪所有图片
    img_filepath = root_path / r"lens_6/XL/XL/M1L1XL"
    img = next(files.scan_pics(img_filepath))
    im_list, v_list = total.cut_one_img(root_path / img)

    # might be changed when img changed.
    assert v_list[0] == "0"
    show_img(im_list[-1])


def test_is_carry():
    assert db.is_carry("123") is False
    assert db.is_carry("1239")
    assert db.is_carry("1230")


def test_generate_dbfiles(root_path):
    dataset_path = root_path / r"lens_6/XL/XL/M1L1XL"
    db_path = dataset_path / "items-temp.db"
    insert_one = littledb.create_db(db_path)
    db.generate_for_one_dataset(dataset_path, insert_one)


def test_img_selector(root_path):
    get_random_img = single.img_selector(root_path)
    get_random_img("")


def test_single_digit(root_path):
    pass
    # gen = single.generate_single(root_path)
    # gen()
