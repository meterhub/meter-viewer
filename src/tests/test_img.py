from meterviewer import img

# import functools
# from matplotlib import pyplot as plt
from tests.utils import show_img, gen_img


def test_resize_imglist():
    imglist = [gen_img(size=(35, 25, 3)), gen_img(size=(34, 25, 3))]
    img.resize_imglist(imglist, size=[35, 25])

    imglist = [gen_img(size=(31, 170, 3)), gen_img(size=(31, 175, 3))]
    img.resize_imglist(imglist)


def test_resize_img():

    im = gen_img(size=(35, 25, 3))
    img.resize_img(im, size=[35, 25])


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
