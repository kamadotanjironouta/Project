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
        self.m = int(ceil(log2(n)))
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
        px = encode_gf(res)*(x**self.r)
        return list(px.polynomial() - px.polynomial().mod(self.gp))

    def calculate_syndrome(self, codeword: list):
        syndrome = [self.pr(codeword)(self.gf.gen()**i) for i in range(1, self.d)]
        return syndrome

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
