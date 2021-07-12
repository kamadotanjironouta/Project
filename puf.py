from sage.all import *
import colorama
RED=colorama.Fore.LIGHTRED_EX
BLUE=colorama.Fore.LIGHTBLUE_EX
GREEN=colorama.Fore.LIGHTGREEN_EX
RESET=colorama.Fore.RESET
CYAN=colorama.Fore.LIGHTCYAN_EX
YELLOW=colorama.Fore.LIGHTYELLOW_EX

class PUF:
    '''
    Params:
    ---
    → length: The PUF response length (bits).
    → err_prob: error probability for each bit (optional)
    → response: pre caclulated response (optional)
    ---
    '''

    def __init__(self, length:int = None, err_prob:float = None, response:list = None):
        if (length <= 0) or (not (0 <= err_prob <= 1)):
            raise ValueError("Bad Arguements")
        if response:
            self.response = response
            self.length = len(response)
        else:
            self.length = length
            self.response = [randint(0,1) for _ in range(self.length)]
        self.err_prob = [err_prob]*self.length if err_prob else [random() % 0.1]*self.length

    def __call__(self):
        '''
        Generating a Response
        '''
        return [bit if err < random() else bit ^ 1 for bit, err in zip(self.response, self.err_prob)]

    def __repr__(self):
        return f'''\
{RED}PUF properties:
{BLUE}    → Response Length:   {RESET}{self.length}
{BLUE}    ⇒ Response:          {YELLOW}{''.join([str(bit) for bit in self.response])}
{BLUE}    ⇒ Error Probability: {RESET}{self.err_prob[0]}{RESET}\
'''
