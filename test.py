import json


def main():
    a = b"('asd', (asd,asd), 1234567)s,hjvshfsdjf;"
    c = a.rsplit(b")")
    c[0] += b")"
    c[1] += b")"
    d = c[0] + c[1]


if __name__ == '__main__':
    main()
