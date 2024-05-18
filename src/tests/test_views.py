from meterviewer.views import current


def test_view_merge_np():
    """test view_merge_np"""
    d = r"D:\Store\MeterData\generated"
    current.view_merge_np(d)
    assert True
