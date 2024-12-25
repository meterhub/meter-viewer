from playground.generate_jsondb import get_all_dataset


def test_get_all_dataset():
  assert len(get_all_dataset()) > 0
