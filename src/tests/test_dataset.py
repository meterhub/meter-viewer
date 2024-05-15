from meterviewer import dataset
import pathlib


def test_scan_pics():
    path = pathlib.Path(r"D:\Store\MeterData\lens_6\XL\XL\M1L1XL\Digit\0")
    count = 0
    pics = []

    def update_count(name):
        nonlocal count, pics
        pics.append(name)
        count += 1

    [update_count(name) for name in dataset.scan_pics(path)]
    assert count == 20
    # assert False, pics
