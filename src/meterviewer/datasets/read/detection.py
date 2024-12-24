import pathlib
import typing as t

from . import config


def read_image_area(file_path: pathlib.Path) -> t.List[config.RectO]:
  """这个函数仅为了读取矩形部分"""
  return config.read_xml_to_get(file_path, config.read_single_digit_rect)
