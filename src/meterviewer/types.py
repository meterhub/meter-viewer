import typing as t
import numpy as np

Img = np.ndarray
Label = np.ndarray

ImgDataset = np.ndarray
LabelData = np.ndarray

ImgList = t.List[Img]
DigitStr = t.List[str]
DigitInt = t.List[int]

CheckFunc = t.Callable[[t.Any], t.Any]
JoinFunc = t.Callable[[ImgList, CheckFunc], Img]
NameFunc = t.Callable[[], t.Tuple[str, str]]

x_name: str = "x_train.npy"
y_name: str = "y_train.npy"
x_test: str = "x_test.npy"
y_test: str = "y_test.npy"


def isImgDataset(x: t.Any) -> bool:
    return isinstance(x, np.ndarray) and len(x.shape) == 4


def isLabelData(y: t.Any) -> bool:
    return isinstance(y, np.ndarray) and len(y.shape) == 2
