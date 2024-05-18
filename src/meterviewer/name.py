# dataset name.
import typing as t
from meterviewer import types as T


def normal_x_y() -> t.Tuple[str, str]:
    return "x.npy", "y.npy"


def train_x_y() -> t.Tuple[str, str]:
    return T.x_name, T.y_name


name_funcs = {
    "normal": normal_x_y,
    "train": train_x_y,
}
