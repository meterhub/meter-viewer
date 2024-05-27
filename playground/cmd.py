import sys
import importlib


def main():
    mode = sys.argv[1]
    module = importlib.import_module(mode)
    module.main()


if __name__ in ("__main__"):
    main()
