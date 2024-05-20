from meterviewer.datasets import config
from pathlib import Path as P

base_path = P(r"D:\Store\MeterData")


def test_read_xml():
    v, r = config.read_xml(base_path / r"lens_6\XL\XL\M1L3XL" / "baocun" / "2018-11-23-12-16-01.xml")
    assert v == "000994"
    assert r.get("xmin") == "79"
