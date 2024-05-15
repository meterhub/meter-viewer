import numpy as np


def save_to_disk(filename: str, data: np.ndarray):
    with open(filename, "wb") as f:
        np.save(f, data)
