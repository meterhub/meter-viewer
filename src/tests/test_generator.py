from meterviewer.generator import single


def test_img_selector(root_path):
    get_random_img = single.img_selector(root_path)
    get_random_img("")


def test_single_digit(root_path):
    pass
    # gen = single.generate_single(root_path)
    # gen()
