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
        self.keys = {}

    def generate(self, p: PUF):
        '''
        Generating a Key
        '''

        print("Generating RNG:\n")
        RNG = [int(bit) for bit in f'{getrandbits(self.code.k):0{self.code.k}b}']
        encoded = self.code.encode(RNG)
        syndrome = [self.code.pr(encoded)(self.code.gf.gen()**i) for i in range(1, self.code.d)]
        while True:
            if RNG[-1] == 1:
                break
            RNG = RNG[:-1]
        print(f"\t{CYAN}Enocding ⇒  {''.join([str(bit) for bit in RNG[::-1]])}\n\t{BLUE}Encoded  ⇒  {YELLOW}{''.join([str(bit) for bit in encoded[::-1]])}{RESET}")
        print(f"\t{RED}[!] {RESET}Generating Key {RED}[!]")
        key = self.code.calculate_syndrome([int(bit_rng)^int(bit_res) for bit_rng, bit_res in zip(encoded, self.response)])
        print(f"\t\t{RESET}→ Generated Key {BLUE}{key}{GREEN} [✓]{RESET}")
        self.keys[tuple(key)] = syndrome

    def verify(self, res: list):
        print(f"{RED}[!] {RESET}Calculating the Syndrome for the Generated Response: {CYAN}{''.join([str(bit) for bit in res])}{RESET}")
        for key in self.keys.values():
            print(res, key)
            print([int(bit_res) ^ int(bit_key) for bit_res, bit_key in zip(res, key)])
            syndrome = self.code.calculate_syndrome([int(bit_res) ^ int(bit_key) for bit_res, bit_key in zip(res, key)])
            for (key, _) in self.code.syndromes.items():
                if key == syndrome:
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
