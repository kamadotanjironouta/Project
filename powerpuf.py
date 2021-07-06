from puf import PUF
from bch import BCH
from random import getrandbits
import colorama
from sage.all import *
RED=colorama.Fore.LIGHTRED_EX
BLUE=colorama.Fore.LIGHTBLUE_EX
GREEN=colorama.Fore.LIGHTGREEN_EX
RESET=colorama.Fore.RESET
CYAN=colorama.Fore.LIGHTCYAN_EX
YELLOW=colorama.Fore.LIGHTYELLOW_EX
BCYAN = colorama.Fore.CYAN

class PowerPuf(PUF):

    """Docstring for PowerPuf. """

    def __init__(self, length: int = None, err_prob: float = None, response:list = None ):
        """TODO: to be defined. """
        PUF.__init__(self, length, err_prob, response)
        self.code = BCH(int(self.err_prob[0] * self.length), self.length)
        self.helperdata = []

    def generate(self, p: PUF):
        '''
        Generating a Key
        '''

        print("Generating Key for: ")
        print(f"{''.join([str(i) for i in p.response])}")
        print("Generating RNG:\n")
        RNG = [int(bit) for bit in f'{getrandbits(self.code.k):0{self.code.k}b}']
        self.encoded = encoded = self.code.encode(RNG)
        syndrome = [self.code.pr(encoded)(self.code.gf.gen()**i) for i in range(1, self.code.d)]
        while True:
            if RNG[-1] == 1:
                break
            RNG = RNG[:-1]
        print(f"\t{CYAN}Enocding ⇒  {''.join([str(bit) for bit in RNG[::-1]])}\n\t{BLUE}Encoded  ⇒  {YELLOW}{''.join([str(bit) for bit in encoded[::-1]])}{RESET}")
        print(f"\t{RED}[!] {RESET}Generating Helper Data {RED}[!]")
        self.code.calculate_syndrome(_helperdata := [int(bit_rng)^int(bit_res) for bit_rng, bit_res in zip(encoded, self.response)])
        helperdata = _helperdata
        _helperdata = "".join(str(i) for i in _helperdata[0:self.code.k])
        print(f"\t\t{RESET}→ Generated Helper Data {BLUE}{_helperdata}{GREEN} [✓]{RESET}")
        self.helperdata.append(helperdata)

    def verify(self, res: list):
        print(f"{RED}[!] {RESET}Calculating the Syndromes for the Generated Response: {CYAN}{''.join([str(bit) for bit in res])}{RESET}")
        for helper in self.helperdata:
            print("".join([str(int(bit_res) ^ int(bit_key)) for bit_res, bit_key in zip(res, helper)]))
            syndromes = self.code.calculate_syndrome([int(bit_res) ^ int(bit_key) for bit_res, bit_key in zip(res, helper)])
            print(f"Syndromes: {YELLOW}{syndromes}")
            for j in range(self.code.t):
                try:
                    syn_mat =  Matrix(self.code.gf, [list(map(lambda x: x.polynomial(), syndromes[i:self.code.t + i])) for i in range(self.code.t - j)])
                    print(syn_mat,-Matrix(self.code.gf, syndromes[self.code.t-j:len(syndromes) - j:]).transpose(), sep = '\n')
                    error_poly = syn_mat.inverse()*(-Matrix(self.code.gf, syndromes[self.code.t-j:len(syndromes) - j:]).transpose())
                    print(error_poly)
                    print(f"{GREEN}Error Locator Matrix: {BCYAN}")
                    err_mat = Matrix(self.code.gf, [(vector(i[0])) for i in error_poly])
                    print(err_mat)
                    print(vector([self.code.gf.gen()**(err_mat.dimensions()[1]- 1 - i) for i in range(err_mat.dimensions()[1])]))
                    print(errors := err_mat * vector([self.code.gf.gen()**(err_mat.dimensions()[1]- 1 - i) for i in range(err_mat.dimensions()[1])]))
                    print([self.code.n - i.log(self.code.gf.gen()) for i in errors])
                    break
                except Exception as e:
                    print("trying with less roots", e)
            for (key, _) in self.code.syndromes.items():
                if key == None:
                    print(f"{GREEN}[✓] {RESET}The response was verified {GREEN}[✓]{RESET}")
                    return
        else:
            print(f"{RED}[✗] {RESET}The response wasn't verified {RED}[✗]{RESET}")


    def __repr__(self):
        return f'''\
PowerPuf Properties:
    {PUF.__repr__(self)}
    {BCH.__repr__(self.code)}
'''
