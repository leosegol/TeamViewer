import json


def main():
    a = ('RGB', 6220000, (1920, 1080), 'x1x2x2')
    print(a)
    print(type(a))
    b = str(a)
    print(b)
    print(type(b))
    c = b.encode()
    d = c.decode()
    e = eval(d)
    print(e)
    print(type(e))



if __name__ == '__main__':
    main()
