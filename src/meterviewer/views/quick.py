import typing as t

from meterviewer import dataset, types as T
from pathlib import Path as P
from . import current


def quick_view(
    current_dataset: str,
    get_x_y_name: T.NameFunc,
    write_config=True,
):
    x_name, y_name = get_x_y_name()
    x = dataset.get_data(P(current_dataset), x_name)
    y = dataset.get_data(P(current_dataset), y_name)
    current.view_merge_np(current_dataset, get_x_y=get_x_y_name)
    if write_config:
        current.write_details(current_dataset, get_xy_name=get_x_y_name)
    return x, y
