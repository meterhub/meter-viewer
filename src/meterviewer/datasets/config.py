# read dataset from file system.
from pathlib import Path as P
from dataclasses import dataclass
import xml.etree.ElementTree as ET
import typing as t

from meterviewer import types as T, func as F


@dataclass
class RectO(object):
    xmin: str = ""
    ymin: str = ""
    xmax: str = ""
    ymax: str = ""

    def check(self):
        # assert rect.xmin != "" and rect.ymin != "" and rect.xmax != "" and rect.ymax != "", rect
        assert self.xmin != "" and self.ymin != "" and self.xmax != "" and self.ymax != "", self

    def to_dict(self) -> T.Rect:
        return {"xmin": self.xmin, "ymin": self.ymin, "xmax": self.xmax, "ymax": self.ymax}

    def __str__(self):
        return f"RectO({self.xmin}, {self.ymin}, {self.xmax}, {self.ymax})"

    def __repr__(self):
        return self.__str__()


def read_xml(filename: P, read_func: t.Callable[[t.Any], t.Any]):
    # 解析 XML 文件
    tree = ET.parse(filename)
    root = tree.getroot()
    return read_func(root)


def read_rect(root) -> t.Tuple[str, T.Rect]:
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


def read_single_digit(root: t.Iterable):
    def find_no(node) -> t.Tuple[int, RectO]:
        no = -1
        rect = RectO()
        for subchild in node:
            if subchild.tag == "no":
                no = int(subchild.text.strip())
            else:
                rect = set_rect(rect, subchild)
        rect.check()
        assert no != -1, "cannot find no number"
        return no, rect

    def set_rect(rect: RectO, sub) -> RectO:
        assert hasattr(rect, sub.tag), (sub.tag, sub.text)
        setattr(rect, sub.tag, sub.text)
        assert getattr(rect, sub.tag) != ""
        return rect

    def num_check():
        seta = {0, 1, 2, 3, 4, 5}
        setb = set()

        def is_valid():
            return seta == setb, (seta, setb)

        def set_num(no):
            setb.add(no)

        return set_num, is_valid

    digit_rect = [RectO() for _ in range(6)]
    set_num, is_valid = num_check()
    is_loop, set_loop = F.looped()

    for child in root:
        if child.tag == "digit":
            no, rect = find_no(child)
            _ = set_loop(), set_num(no)
            digit_rect[no] = rect

    assert is_loop(), "node has no child"
    cond, _ = is_valid()
    assert cond

    # return digit_rect, root, find_no, find_rect
    return digit_rect


def get_single_digit(filename: P) -> t.Tuple[str, T.Rect]:
    val, _ = read_xml(filename, read_single_digit)
    pos = read_xml(filename, read_single_digit)
    return val, pos


def get_rectangle(filename: P) -> T.Rect:
    _, rect = read_xml(filename, read_rect)
    return rect


def get_xml_config_path(img_path: P, types: t.Literal["value", "block", "single"] = "value") -> P:
    """filename (test.png or test.jpg) to config (res.xml or suffix.xml)"""
    dataset_path = img_path.parent

    def value_path():
        config_p = P(dataset_path) / "baocun"
        assert img_path.suffix in (".jpg", ".jpeg")
        filename = img_path.name[: -len(img_path.suffix)] + ".xml"
        return config_p / filename

    def block_path():
        return P(dataset_path) / "config" / "block.xml"

    def single_path():
        return P(dataset_path) / "config" / "res.xml"

    funcs: t.Mapping[str, t.Callable] = {
        "value": value_path,
        "block": block_path,
        "single": single_path,
    }

    return funcs[types]()


def get_xml_config(img_path: P) -> t.Tuple[str, T.Rect]:
    return read_xml(get_xml_config_path(img_path), read_rect)
