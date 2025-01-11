"""view the dataset"""

import pathlib
import random

import cv2

from meterviewer.generator import jsondb
from meterviewer.img import draw
from meterviewer.types import Rect


# 从数据集中随机获取一张图
def get_random_images(dataset: str, digit_num: int, stage: str):
  images = jsondb.get_images_with_full_path(
    jsondb.get_base_dir(),
    dataset,
    digit_num,
    is_test=stage == "test",
  )
  return images


# 生成样例数据图片列表
def gen_plt_images(datasets: jsondb.DatasetList, digit_num: int, stage: str):
  plt_images = []
  for dataset in datasets.dataset_list:
    images = get_random_images(dataset, digit_num, stage)
    if len(images) == 0:
      print(f"empty dataset: {dataset}")
      continue

    item = {
      "dataset": (dataset, len(images)),
      "image": get_random_image(images),
    }
    plt_images.append(item)
  return plt_images


# 根据数据集随机返回一张图片
def get_random_image_by_dataset(dataset: str, digit_num: int, stage: str):
  images = get_random_images(dataset, digit_num, stage)
  return get_random_image(images)


# 随机抽取一张图片，画框
def get_random_image(images: list[str]):
  """
  draw random image from image list
  images: image list, full path
  """
  image = pathlib.Path(random.choice(images))
  area = jsondb.read_image_area(image)
  area = Rect.model_validate(area)
  im = cv2.imread(image)
  drawed_im = draw.draw_rectangle(im, area)
  print(area)
  return drawed_im
