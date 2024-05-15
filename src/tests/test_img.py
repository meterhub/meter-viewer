from meterviewer import img
from matplotlib import pyplot as plt

# import functools


def show_img(img):
    # TODO: img valid test. use a gui to validate.
    is_show = 0
    if is_show:
        plt.imshow(img)
        plt.show()


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
