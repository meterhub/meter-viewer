from meterviewer.generator import single, db
from meterviewer import littledb
from pathlib import Path as P
import pytest


def test_is_carry():
    assert db.is_carry("123") is False
    assert db.is_carry("1239")
    assert db.is_carry("1230")


@pytest.mark.skip("long time to generate")
def test_generate_db_for_all(root_path):
    p = P("./alldata.db")
    db.generate_db_for_all(root_path, p)


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
