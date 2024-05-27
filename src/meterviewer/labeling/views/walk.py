""" walk around the dataset """

import typing as t
from meterviewer.datasets import dataset
from meterviewer import files
from pathlib import Path

FullPath = Path


def isFullPath(p: FullPath):
    return p.is_absolute()


def view_dataset(root_path: Path) -> t.Iterable[FullPath]:
    def get_images(dataset_path: Path):
        # lookup 3 images.
        pics = list(files.scan_pics(dataset_path))[:3]
        for pic in pics:
            yield pic

    datasets = dataset.get_dataset_list(root_path)
    for dataset_name in datasets:
        res = dataset.get_dataset_path(root_path, str(dataset_name))
        yield from get_images(res)
