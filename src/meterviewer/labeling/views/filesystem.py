import typing as t
from meterviewer import files
from meterviewer.datasets import dataset
import pathlib


def from_filesystem(root_path: pathlib.Path) -> t.Generator[t.Tuple[pathlib.Path, pathlib.Path, str], None, None]:
    for dataset_name in dataset.get_dataset_list(root_path):
        img_p = files.scan_pics(dataset.get_dataset_path(root_path, str(dataset_name)))
        img_p = list(img_p)
        for p in img_p:
            yield p, dataset_name, "invalid"
