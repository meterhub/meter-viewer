import typing as t
from meterviewer import dataset
from pathlib import Path as P
from . import current


def quick_view(
    current_dataset: str,
    get_x_y_name: t.Callable,
    write_config=True,
):
    x_name, y_name = get_x_y_name()
    x = dataset.get_data(P(current_dataset), x_name)
    y = dataset.get_data(P(current_dataset), y_name)
    current.view_merge_np(current_dataset)
    if write_config:
        current.write_details(current_dataset)
    return x, y
