from meterviewer import littledb
from meterviewer.datasets import dataset
from pathlib import Path as P


def test_insert_one(root_path):
    dataset_name = "M1L1XL"
    p = dataset.get_dataset_path(root_path, dataset_name)
    db = p / "items-temp.db"
    insert_one = littledb.create_db(str(db))
    assert db.exists()

    insert_one("test", 0, False)
    db.unlink()


def test_create_db(root_path):
    p = P("test.db")
    littledb.create_db(str(p))
    p.unlink()

    p = P(root_path / "test.db")
    littledb.create_db(str(p))
    p.unlink()
