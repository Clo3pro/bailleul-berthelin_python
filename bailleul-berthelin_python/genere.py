from copiage import genlist


def gener():
    for i in range(11, 96):
        print(f"\"{i}\": {genlist[i-11]},")


def test():
    for i in range(1, 9+1):
        print(str(i).zfill(2))
    for i in range(10, 95+1):
        print(str(i))


if __name__ == "__main__":
    test()
