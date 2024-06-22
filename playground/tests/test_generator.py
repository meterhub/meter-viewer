from meterviewer.imgs import img
from PIL import Image


def test_gen_pics():
    im = img.gen_empty_im((30, 120, 3))
    im = Image.fromarray(im)
    filename = "/tmp/test.png"
    im.save(filename)
    img.show_img(im, is_stop=False)
