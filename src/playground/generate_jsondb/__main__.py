import pathlib

from playground.generate_jsondb import gen_db

if __name__ == "__main__":
  gen_db(output=pathlib.Path(__file__).parent / "meterdb.json")
