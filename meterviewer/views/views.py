import pathlib
from meterviewer import dataset, files


def view_merge_np():
    """view already handled data."""
    p = r"D:\Store\MeterData\lens_6\XL\merge_np\Block\Train"
    pp = pathlib.Path(p)

    dataset.view_dataset_on_disk(
        prefix_name=pp,
        load_from_disk=files.load_from_disk,
    )
