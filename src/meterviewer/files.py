import typing as t
import numpy as np


def save_to_disk(filename: str, data: np.ndarray):
    with open(filename, "wb") as f:
        np.save(f, data)


def load_from_disk(filename, constraint: t.Callable):
    with open(filename, "rb") as f:
        return np.load(f)
