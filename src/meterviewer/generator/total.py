"""create new generated dataset"""

import functools
import typing as t
from meterviewer.datasets import dataset, single, config, imgv
from meterviewer import files, img, T
from meterviewer.imgs import cut
from pathlib import Path as P


def cut_one_img(filepath: P) -> t.Tuple[T.ImgList, T.DigitStr]:
    im, val, pos = imgv.view_one_img_v(filepath)
    xml_path = config.get_xml_config_path(filepath, "single")
    pos_list = config.read_rect_from_file(xml_path, "single")

    assert isinstance(pos_list, t.List)
    im_list = []
    for pos in pos_list:
        im1 = cut.cut_img(im, rect=pos.to_dict())
        im_list.append(im1)
    return im_list, list(val)


def cut_all_img(dbfiles: P):
    pass


def generate_dataset(root_path: P):
    P = functools.partial

    def gen_block(
        the_digit: T.DigitStr,
    ):
        return dataset.generate_block_img(
            the_digit=the_digit,
            root_path=root_path,
            join_func=dataset.join_with_resize,
            get_dataset=lambda: "M1L1XL",
            read_rand_img=single.read_rand_img,
        )

    path = root_path / "generated"
    path.mkdir(exist_ok=True)

    filesave = P(
        files.save_img_labels,
        prefix_name=path,
        save_to_disk=files.save_to_disk,
    )

    def check_imgs(imglist):
        size = imglist[0].shape
        img.show_img(imglist[0], is_stop=0)
        imgs = img.resize_imglist(imglist)
        for im in imgs:
            img.show_img(im, is_stop=0)
            assert size == im.shape

    dataset.create_dataset(check_imgs=lambda x: None)(
        length=5,
        nums=10,
        gen_block_img=gen_block,
        save_dataset=filesave,
    )
