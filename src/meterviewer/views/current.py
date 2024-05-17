import typing as t
import pathlib
from meterviewer import dataset, files, types as T


def view_merge_np(current_dataset: str):
    """view already handled data."""
    pp = pathlib.Path(current_dataset)

    dataset.view_dataset_on_disk(
        prefix_name=pp,
        load_from_disk=files.load_from_disk,
    )


def read_details(current_dataset: str) -> t.Optional[t.Dict]:
    return files.read_toml(pathlib.Path(current_dataset) / "details.toml")


def write_details(current_dataset: str):
    pp = pathlib.Path(current_dataset)

    def write_to_file(details, overwrite=True):
        p = pp / "details.toml"
        if not overwrite and p.exists():
            print("Failed to write, file exists")
            return
        return files.write_toml(p, details)

    dataset.show_details(
        get_x_train=lambda: files.load_from_disk(pp / T.x_name),
        get_y_train=lambda: files.load_from_disk(pp / T.y_name),
        get_details=lambda x, y: dataset.get_details(pp, x, y),
        write_to_file=write_to_file,
    )
