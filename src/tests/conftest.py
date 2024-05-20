import pytest
import pathlib


@pytest.fixture
def root_path() -> pathlib.Path:
    return pathlib.Path(r"D:\Store\MeterData")
