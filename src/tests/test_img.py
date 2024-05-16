from meterviewer import img

# import functools
# from matplotlib import pyplot as plt
from tests.utils import show_img


def test_number_to_string():
    assert img.number_to_string(1, 5) == list("00001")
    assert img.number_to_string(10, 5) == ["0", "0", "0", "1", "0"]
    assert img.number_to_string(100, 5) == list("00100")
    assert img.number_to_string(1000, 5) == list("01000")


def test_join():
    imglist = [
        img.get_random_img(1, img.img_from),
        img.get_random_img(2, img.img_from),
        img.get_random_img(3, img.img_from),
    ]
    res = img.join_img(imglist, img.empty_check)
    assert res.shape[1] > res.shape[0]
    # seems correct
    show_img(res)
