import json
import os
import pathlib

import pytest

from playground import generate_jsondb
from playground.generate_jsondb.schema import MeterDB


@pytest.fixture
def gen():
  yield generate_jsondb.gen_db(output=pathlib.Path(__file__).parent / "meterdb.json")
  os.unlink(pathlib.Path(__file__).parent / "meterdb.json")


def test_the_db(gen):
  assert gen.exists()


def test_db_content(gen):
  with open(gen, "r") as f:
    content = json.load(f)
  db = MeterDB.model_validate(content)
  assert len(db.data) > 0

  data = generate_jsondb.get_random_data()

  find = False
  for item in db.data:
    if item.filepath == data:
      find = True
      break
  assert find
