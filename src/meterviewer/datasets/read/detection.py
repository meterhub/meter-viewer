import glob
import pathlib
import random
import typing as t

from . import config


def read_image_area(file_path: pathlib.Path) -> t.List[config.RectO]:
  """这个函数仅为了读取矩形部分"""
  assert file_path.suffix == ".xml", "仅支持xml文件"
  return config.read_xml_to_get(file_path, config.read_single_digit_rect)


def get_random_image_file(root_dir: pathlib.Path) -> pathlib.Path:
  """获取随机图像文件"""
  return random.choice(list(root_dir.glob("*.jpg")))


def read_area_img(
  root: pathlib.Path,
  get_dataset: t.Callable[[], t.Union[str, pathlib.Path]],
  range_: tuple[float, float],
  promise=False,
):
  def might_fail_func() -> pathlib.Path:
    return root / str(get_dataset())

  pass


def list_images(root: pathlib.Path, dataset_name: str) -> list[pathlib.Path]:
  dataset_full_path = f"lens_6/XL/XL/{dataset_name}"
  return glob.glob(str(root / dataset_full_path / "*.jpg"))
