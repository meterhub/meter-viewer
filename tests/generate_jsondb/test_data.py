import pathlib

from playground.generate_jsondb import get_random_data


def test_get_local_config():
  data = get_random_data()
  assert pathlib.Path(data).exists()
