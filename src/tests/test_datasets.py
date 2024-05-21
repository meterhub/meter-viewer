from meterviewer.datasets import config


def test_read_xml(root_path):
    v, r = config.read_xml(root_path / r"lens_6/XL/XL/M1L3XL" / "baocun" / "2018-11-23-12-16-01.xml")
    assert v == "000994"
    assert r.get("xmin") == "79"


def test_img_to_xml(root_path):
    p = config.get_xml_config_path(root_path / r"lens_6/XL/XL/M1L3XL" / "2018-11-23-12-16-01.jpg")
    assert p.exists(), p
