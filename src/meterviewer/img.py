# process image, to fit the training proposals.

from tabnanny import check
import typing as t
import numpy as np

Img = np.ndarray

global_func: t.Dict[str, t.Any] = {}


def use_func(name: str):
    f = global_func.get(name, None)
    if not f:
        raise ValueError(f"func {name} not found")


def join_img(imglist: t.List[Img], check_func: t.Callable) -> Img:
    # merge images vertically
    check_func()
    return np.vstack(imglist)


def get_random_img(num: int, img_from: t.Callable) -> Img:
    """get random img
    num: digit num of img
    """
    get_img = img_from()
    return get_img(num)


def check_img_size(img: Img, size: t.Tuple[int, int], then: t.Callable[[Img], t.Any]) -> bool | t.Any:
    if img.shape == size:
        return then(img)
    return False


def img_from(folder: str = ""):
    # open folder to get all images.
    def get_img(num):
        return np.random.randint(1, 255, size=(10, 20))

    return get_img


def get_img_list(nums: t.List[int]) -> t.List[Img]:
    imgs = []
    for i in nums:
        imgs.append(get_random_img(int(i), lambda: None))
    return imgs


def number_to_string(number: int) -> t.List[str]:
    num_s: str = str(number)
    num_l = num_s.split("")
    return num_l


def empty_check():
    """do nothing function"""
    pass


def gen_block_img(number: int):
    num_l = [int(i) for i in number_to_string(number)]
    return join_img(get_img_list(num_l), empty_check)


def create_dataset(train_nums: int, test_nums: int, save_method: t.Callable):
    pass


def dataset():
    data = {}
    str_template = "{name}_{peroid}.npy"

    def get_root_path():
        pass
