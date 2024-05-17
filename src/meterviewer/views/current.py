import pathlib
from meterviewer import dataset, files, types as T


def view_merge_np(current_dataset: str):
    """view already handled data."""
    pp = pathlib.Path(current_dataset)

    dataset.view_dataset_on_disk(
        prefix_name=pp,
        load_from_disk=files.load_from_disk,
    )


def write_details(current_dataset: str):
    pp = pathlib.Path(current_dataset)
    dataset.show_details(
        get_x_train=lambda: files.load_from_disk(pp / T.x_name),
        get_y_train=lambda: files.load_from_disk(pp / T.y_name),
        get_details=dataset.get_details,
        write_to_file=lambda details: files.write_toml(pp / "details.toml", details),
    )
