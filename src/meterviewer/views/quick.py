from meterviewer import types as T, files
from pathlib import Path as P

from meterviewer.datasets import dataset
from . import current


def more_quick_view(
    current_dataset: P,
    write_config=True,
):
    name_func = files.use_smart_name(current_dataset)
    return quick_view(str(current_dataset), name_func, write_config)


def quick_view(
    current_dataset: str,
    get_x_y_name: T.NameFunc,
    write_config=True,
):
    x_name, y_name = get_x_y_name()
    x = files.load_from_disk(P(current_dataset) / x_name)
    y = files.load_from_disk(P(current_dataset) / y_name)

    current.view_merge_np(current_dataset, get_x_y=get_x_y_name)
    if write_config:
        current.write_details(current_dataset, get_xy_name=get_x_y_name)
    return x, y


# from meterviewer.views.quick import fast_preview
def fast_preview(current_dataset: P):
    return more_quick_view(current_dataset)
