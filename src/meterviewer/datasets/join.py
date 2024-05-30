import typing as t
import functools
from meterviewer import T
from meterviewer import img
from loguru import logger


def join_with_fix(imglist: T.ImgList, check_func: t.Callable, fix_func: t.Callable) -> T.Img:
    """修饰 join_func"""
    # merge images horizontally
    try:
        return img.join_img(imglist, check_func)
    except ValueError as e:
        logger.warning(e)
        imglist = fix_func(imglist)
    return img.join_img(imglist, check_func)


join_with_resize: T.JoinFunc = functools.partial(join_with_fix, fix_func=img.resize_imglist)
