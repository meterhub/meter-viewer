from __future__ import annotations
import typing as t
import pathlib
from meterviewer import files, types as T
from meterviewer.datasets import dataset


def view_merge_np(
    current_dataset: str | pathlib.Path,
    view_dataset: t.Callable[[int, T.ImgList], None] = dataset.view_dataset,
    get_x_y: T.NameFunc = lambda: (T.x_name, T.y_name),
):
    """view already handled data."""
    pp = pathlib.Path(current_dataset)

    x_name, _ = get_x_y()
    view_func = dataset.view_dataset_on_disk(x_name)

    view_func(
        prefix_name=pp,
        view_dataset=view_dataset,
        load_from_disk=files.load_from_disk,
    )


def read_details(current_dataset: str) -> t.Optional[t.Dict]:
    return files.read_toml(pathlib.Path(current_dataset) / "details.gen.toml")


def get_x_y_name() -> t.Tuple[str, str]:
    return T.x_name, T.y_name


def write_details(current_dataset: str, get_xy_name: T.NameFunc = get_x_y_name):
    pp = pathlib.Path(current_dataset)

    def write_to_file(details, overwrite=True):
        p = pp / "details.gen.toml"
        if not overwrite and p.exists():
            print("Failed to write, file exists")
            return
        return files.write_toml(p, details)

    x_name, y_name = get_xy_name()

    dataset.show_details(
        get_x_train=lambda: files.load_from_disk(pp / x_name),
        get_y_train=lambda: files.load_from_disk(pp / y_name),
        get_details=lambda x, y: dataset.get_details(pp, x, y),
        write_to_file=write_to_file,
    )
