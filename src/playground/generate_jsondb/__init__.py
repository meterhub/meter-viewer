import glob
import json
import pathlib
import random
import typing as t

import toml

from meterviewer.datasets.read.detection import read_image_area

from .schema import Item, MeterDB


# cache config function (only read disk once), returns get_random_dataset and load_conf
def load_config(config_path: pathlib.Path) -> t.Callable[[], dict]:
  data: t.Optional[dict] = None

  def load_conf() -> dict:
    nonlocal data
    if data is None:
      with open(config_path, "r") as f:
        data = toml.load(f)
    assert data is not None, (config_path, data)
    return data

  return load_conf


get_local_config = load_config(
  config_path=pathlib.Path(__file__).parent / "config.toml"
)


def get_random_dataset() -> str:
  """随机选择一个数据集"""
  dataset_list = get_all_dataset()
  return random.choice(dataset_list)


def get_all_dataset() -> list[str]:
  config = get_local_config()
  return config["generate_config"]["dataset"]


def get_base_dir():
  config = get_local_config()
  return config["base"]["root_path"]


def get_random_data() -> pathlib.Path:
  dataset = get_random_dataset()
  base_dir = get_base_dir()
  data_path = glob.glob(
    str(pathlib.Path(base_dir) / "lens_6/XL/XL" / dataset / "*.jpg")
  )
  return random.choice(data_path)


def gen_db(output: pathlib.Path):
  """读取数据集下所有的图片，以及点的位置，生成一个json文件"""
  data = []
  for dataset in get_all_dataset():
    base_dir = get_base_dir()
    data_path = glob.glob(
      str(pathlib.Path(base_dir) / "lens_6/XL/XL" / dataset / "*.jpg")
    )
    for jpg_data in data_path:
      rect = read_image_area(pathlib.Path(jpg_data))
      item = Item(
        filepath=jpg_data,
        dataset=dataset,
        xmin=rect["xmin"],
        xmax=rect["xmax"],
        ymin=rect["ymin"],
        ymax=rect["ymax"],
      )
      data.append(item)

  meter_db = MeterDB(data=data)

  with open(output, "w") as f:
    json.dump(meter_db.model_dump(), f)

  return output
