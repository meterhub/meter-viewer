def my_gen(start: int):
    for i in range(start, start + 5):
        yield i


def gen2():
    for g in [my_gen(2), my_gen(3)]:
        yield g
