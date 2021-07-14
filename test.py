from puf import PUF
from bch import BCH
from powerpuf import PowerPuf
import os
DIV = '-' * os.get_terminal_size().columns

def test_puf():
    p = PUF(10)
    print(p)
    print(p())

def test_bch():
    code = BCH(3, 15)
    encoded = code.encode([1, 1, 0, 1, 1])
    print(encoded, [1, 1, 0, 1, 1])
    print(code.decode(encoded), [1, 1, 0, 1, 1])

def test_powerpuf():
    n = int(input("Enter the length of the response: "))
    err = float(input("Enter the error prob of each bit: "))
    pufs = []
    p = PowerPuf(n, err)
    print(p)
    p.generate()
    p.verify(p())


if __name__ == "__main__":
    # test_puf()
    print(DIV)
    # test_bch()
    # print(DIV)
    test_powerpuf()
