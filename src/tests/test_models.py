from meterviewer.models.func import get_first_item
from pathlib import Path as P


def test_get_item():
    item = get_first_item(P("./alldata.db"))
    assert item.id == 1
