from sage.all import *
from math import log2
import colorama
RED=colorama.Fore.LIGHTRED_EX
BLUE=colorama.Fore.LIGHTBLUE_EX
GREEN=colorama.Fore.LIGHTGREEN_EX
RESET=colorama.Fore.RESET
CYAN=colorama.Fore.LIGHTCYAN_EX

class BCH:
    '''
    BCH code class
    → n: code length
    → t: error correction capabilities
    → d: minimum hamming weight of a codeword
    → k: amount of information bits
    → r: amount of redundancy bits
    → m: power of the field
    → p: irreducible polynomial
    → gf: GF field of power m
    → gp: generator poly
    '''

    def __init__(self, t = None, n = None):
        if t > n//2 or t < 0 or n < 0:
            raise ValueError("Bad Args")
        self.t = t
        self.n = n
        self.m = int(ceil(log2(n + 1)))
        self.d = 2*t + 1
        self.gf = GF(2**self.m, 'x'); self.gf.inject_variables(verbose = False)
        self.pr = self.gf.polynomial_ring()
        self.p = self.pr.irreducible_element(self.m)
        self.minpolys = {}
        for i in range(1, self.d - 1):
            self.minpolys[i] = self.gf(x**i).minpoly()
        self.gp = LCM([self.minpolys[i] for i in range(1, self.d - 1)])
        self.k = self.n - self.gp.degree()
        self.r = self.gp.degree()
        self.cosets = {poly[0].polynomial():poly[0].polynomial().list() for poly in self.gf.cyclotomic_cosets(1) if 0 < poly[0].polynomial().list().count(1) < self.d}
        self.syndromes = {coset: [coset(x**i) for i in range(1, self.d)] for coset in self.cosets}
        self.syndromes[0] = self.pr(self.gf.gen() * 0)

    def encode(self, res: list):
        encode_gf = GF(2**(self.n), 'x'); encode_gf.inject_variables(verbose = False)
        px = encode_gf(res)*(x**(self.n - self.k))
        temp = list(px.polynomial() - px.polynomial().mod(self.gp))
        return ((2**self.m - 1)-(len(temp))) * [0] + temp

    def calculate_syndromes(self, codeword: list):
        return [self.pr(self.pr(codeword))(self.gf.gen()**i) for i in range(1, self.d)]

    def decode(self, codeword: list):
        syndromes = self.calculate_syndromes(codeword)
        syndrome_matrix = Matrix([line for line in [syndromes[i:self.t + i] for i in range(self.t)]])
        m = None
        for i in range(self.t):
            try:
                if (self.t - i == 1):
                    m = syndrome_matrix[range(0, self.t - i), range(0,self.t - i)].inverse() * vector([syndromes[self.d - 2 - i]])
                    break
                else:
                    print(syndromes[self.t - 1 - i: self.d - 2 - i])
                    m = syndrome_matrix[range(0, self.t - i), range(0,self.t - i)].inverse() * vector(syndromes[self.t - 1 - i: self.d - 2 - i])
                    break
            except Exception as _e:
                print("Trying with a matrix of lower degree {}x{}".format(self.t-i-1, self.t-i-1))
        if not m:
            print("Couldn't correct")
            return None
        m = (list(m) + [1])[::-1]
        m = Matrix(m)
        u = PolynomialRing(GF(2), 'y'); u.inject_variables(verbose = False)
        v = vector([y**i for i in range(m.dimensions()[1])])
        factors = factor((m * v)[0])
        roots = tuple((i for i, _ in factors.value().roots()))
        error_location = [2**self.m - root.log(self.gf.gen()) for root in roots]
        if len(error_location):
            print("True")
        else:
            print("False")
        return 0
        

    def __repr__(self):
        return f'''\
{RED}BCH properties ({self.n}, {self.k}, {self.d}):
{BLUE}    → k:   {RESET}{self.k}
{BLUE}    ⇒ r:   {RESET}{self.r}
{BLUE}    ⇒ d:   {RESET}{self.d}
{BLUE}    ⇒ n:   {RESET}{self.n}
{BLUE}    ⇒ Irreducible Polynomial of GF^{self.m}:   {RESET}{self.p}
{BLUE}    ⇒ Generator Polynomial: {RESET}{self.gp}{RESET}\
'''
