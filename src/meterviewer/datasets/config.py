# read dataset from file system.
from pathlib import Path as P
import xml.etree.ElementTree as ET
import typing as t
from meterviewer import types as T, func as F


class RectO(object):
    xmin: str
    ymin: str
    xmax: str
    ymax: str

    def to_dict(self) -> T.Rect:
        return {"xmin": self.xmin, "ymin": self.ymin, "xmax": self.xmax, "ymax": self.ymax}


def read_xml(filename: P) -> t.Tuple[str, T.Rect]:
    # 解析 XML 文件
    tree = ET.parse(filename)
    root = tree.getroot()

    # 遍历 XML 树
    val, rect_dict = "", RectO()
    for child in root:
        # find object
        if not child.tag == "object":
            continue
        for subchild in child:
            if subchild.tag == "name":
                val = F.must_str(subchild.text)

            # print(subchild.tag, subchild.text)
            if subchild.tag == "bndbox":
                for sub in subchild:
                    setattr(rect_dict, sub.tag, sub.text)

    return val, rect_dict.to_dict()


def get_rectangle(filename: P) -> T.Rect:
    _, rect = read_xml(filename)
    return rect


def get_xml_config_path(img_path: P) -> P:
    """filename -> test.png or test.jpg"""
    dataset_path = img_path.parent
    config_p = P(dataset_path) / "baocun"
    assert img_path.suffix in (".jpg", ".jpeg")
    filename = img_path.name[: -len(img_path.suffix)] + ".xml"
    return config_p / filename


def get_xml_config(img_path: P) -> t.Tuple[str, T.Rect]:
    return read_xml(get_xml_config_path(img_path))
