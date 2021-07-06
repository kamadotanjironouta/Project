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
    n = int(input("Enter the length of the response: "))
    err = float(input("Enter the error prob of each bit: "))
    pufs = []
    p = PowerPuf(n, err)
    print(p)
    p.generate( tmp := PUF(n,err) )
    pufs.append(tmp)
    p.verify(res := tmp())
    print("".join([f"{i[0]}" if i[0] == i[1] else f"{i[0]}({i[1]})" for i in zip(res, tmp.response)]))



if __name__ == "__main__":
    #test_puf()
    #print(DIV)
    #test_bch()
    print(DIV)
    test_powerpuf()
