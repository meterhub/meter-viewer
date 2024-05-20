from meterviewer.img import show_img
from meterviewer.imgs import draw
from meterviewer.datasets import imgv
from meterviewer import types as T
from pathlib import Path as P


def test_draw(root_path):
    img_path = root_path / "lens_6/XL/XL/M1L3XL/2018-11-23-12-16-01.jpg"
    im, v, rect = imgv.view_one_img_v(img_path)
    im = draw.draw_rectangle(im, rect)
    show_img(im, is_stop=0)


def test_draw_text(root_path):
    img_path = root_path / "lens_6/XL/XL/M1L3XL/2018-11-23-12-16-01.jpg"
    im, v, _ = imgv.view_one_img_v(img_path)
    im = draw.draw_text(im, v)
    show_img(im, is_stop=0)
