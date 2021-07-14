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
        try:
            PUF.__init__(self, length, err_prob, response)
            self.code = BCH(int(self.err_prob[0] * self.length), self.length)
            self.helperdata = []
        except Exception as e:
            raise e
        self.generate()

    def generate(self):
        '''
        Generating a Key
        '''

        print("Generating Key for: ")
        print(f"{''.join([str(i) for i in self.response])}")
        print("Generating RNG:\n")
        RNG = [int(bit) for bit in f'{getrandbits(self.code.k):0{self.code.k}b}']
        self.encoded = encoded = self.code.encode(RNG)
        while True:
            if RNG[-1] == 1:
                break
            RNG = RNG[:-1]
        print(f"\t{CYAN}Enocding ⇒  {''.join([str(bit) for bit in RNG[::-1]])}\n\t{BLUE}Encoded  ⇒  {YELLOW}{''.join([str(bit) for bit in encoded[::-1]])}{RESET}")
        print(f"\t{RED}[!] {RESET}Generating Helper Data {RED}[!]")
        _helperdata = [int(bit_rng)^int(bit_res) for bit_rng, bit_res in zip(encoded, self.response)]
        helperdata = _helperdata
        _helperdata = "".join(str(i) for i in _helperdata[0:self.code.k])
        print(f"\t\t{RESET}→ Generated Helper Data {BLUE}{_helperdata}{GREEN} [✓]{RESET}")
        self.helperdata.append(helperdata)

    def verify(self, res: list):
        print(f"{BLUE}Received Response => {''.join([BLUE + str(bit) if bit == self.response[i] else RED + str(bit) for i, bit in enumerate(res)])}{RESET}")
        self.code.decode([int(i) ^ int(j) for i, j in zip(res, self.response)])


    def __repr__(self):
        return f'''\
PowerPuf Properties:
    {PUF.__repr__(self)}
    {BCH.__repr__(self.code)}
'''
