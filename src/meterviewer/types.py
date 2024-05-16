import typing as t
import numpy as np

Img = np.ndarray
Label = np.ndarray

ImgList = t.List[Img]
DigitStr = t.List[str]
DigitInt = t.List[int]

CheckFunc = t.Callable[[t.Any], t.Any]
JoinFunc = t.Callable[[ImgList, CheckFunc], Img]
