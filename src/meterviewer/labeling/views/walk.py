""" walk around the dataset """

import typing as t
from meterviewer.datasets import dataset
from meterviewer import files
from pathlib import Path
from .types import viewReturn


def view_dataset(root_path: Path) -> viewReturn:
    def get_images(dataset_path: Path):
        # lookup 3 images.
        pics = list(files.scan_pics(dataset_path))[:3]
        return pics

    datasets = dataset.get_dataset_list(root_path)
    for dataset_name in datasets:
        res = dataset.get_dataset_path(root_path, str(dataset_name))
        pics = get_images(res)
        for pic in pics:
            yield pic, dataset_name, "_"
