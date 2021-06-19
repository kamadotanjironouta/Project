from puf import PUF
from bch import BCH
from powerpuf import PowerPuf
DIV = '-' * 212

def test_puf():
    p = PUF(10)
    print(p)
    print(p())

def test_bch():
    code = BCH(2, 16)
    encoded = code.encode([1, 1, 0, 1, 0, 0, 1])
    print(encoded)

def test_powerpuf():
    pufs = []
    p = PowerPuf(127, 0.1)
    print(p)
    p.generate( tmp := PUF(127, 0.01) )
    pufs.append(tmp)
    p.verify(res := tmp())



if __name__ == "__main__":
    #test_puf()
    #print(DIV)
    #test_bch()
    print(DIV)
    test_powerpuf()
