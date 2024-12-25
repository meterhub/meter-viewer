import pathlib

from playground.generate_jsondb import gen_db


def test_the_db():
  gen_db(output=pathlib.Path(__file__).parent / "meterdb.json")

  assert (pathlib.Path(__file__).parent / "meterdb.json").exists()
