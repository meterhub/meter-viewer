import pathlib

config_path = pathlib.Path(__file__).parent / "dataset-gen.toml"

from .main import main

__all__ = ["main", "config_path"]
