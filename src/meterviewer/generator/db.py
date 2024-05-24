"""generate database"""

import typing as t
from meterviewer.datasets import dataset, imgv, single
from meterviewer import T, files
from pathlib import Path as P

from meterviewer.models import littledb
from meterviewer.values import is_carry


dbInsertFunc = t.Callable[[str, int, bool], None]


def generate_for_one_dataset(dataset: P, insert: dbInsertFunc):
    assert dataset.is_absolute()
    for img_file in files.scan_pics(dataset):
        _, v, _ = imgv.view_one_img_v(img_file)
        # transform str to int
        val = int(v)

        insert(str(img_file), val, is_carry(v))


def generate_db_for_all(root: P, db_path: P):
    # insert to one database.
    assert not db_path.is_absolute()

    insert, _ = littledb.create_db(str(db_path))

    def generate_one(dataset: P):
        return generate_for_one_dataset(single.get_dataset_path(root, str(dataset)), insert)

    dataset.handle_datasets(
        root,
        generate_one,
    )


def create_db(root_path: P):
    db_name = "items.db"

    def handle_dataset(dataset_name: P):
        dataset_path = dataset.get_dataset_path(root_path, str(dataset_name))
        littledb.create_db(str(dataset_path / db_name))

    dataset.handle_datasets(
        root_path,
        handle_func=handle_dataset,
    )
