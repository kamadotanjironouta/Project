import os
import pprint
import colorama
from puf import PUF
from powerpuf import PowerPuf
import bch
DIV = colorama.Fore.LIGHTBLACK_EX + '-'*os.get_terminal_size()[0] + colorama.Fore.RESET
MENU='''\
1. Generate a PUF instance
2. Generate a PowerPuf instance
3. Generate a Random Response
0. Exit
'''

def print_success(string):
    '''
    '''
    print(f"{colorama.Fore.GREEN}[✓] {string} {colorama.Fore.RESET}")

def print_error(string):
    """
    """
    print(f"{colorama.Fore.RED}[✗] {string} {colorama.Fore.RESET}")

def handle_puf_generation() -> PUF:
    """
    Handles option: 1

    :returns: PUF instance

    """
    length: int = None
    err_prob: float = None
    try:
        length = int(input("Enter The PUF's response length: "))
        err_prob = float(input("Enter the PUF's error probability per bit: "))
        return PUF(length, err_prob)
    except ValueError as _e:
        print_error(f"Exception: {_e}")
        return None

def handle_powerpuf_generation(p) -> PowerPuf:
    """
    Handles option: 2

    :returns: PowerPuf instance

    """
    try:
        return PowerPuf(p.length, p.err_prob[0], p.response)
    except ValueError as _e:
        print_error(f"Exception: {_e}")
        return None


def handle_random_powerpuf_response_generation(pp) -> list:
    '''
    '''
    try:
        return pp()
    except Exception as _e:
        print_error(f"Exception: {_e}")
        return None


if __name__ == "__main__":
    os.system('clear')
    p:PUF = None
    pp:PowerPuf = None
    user_input:int = None
    while user_input != 0:
        print(DIV, MENU, sep = '\n')
        try:
            user_input = int(input("input: "))
        except ValueError as _e:
            print_error(f"Exception: {_e}")
            continue
        if user_input == 1:
            p = handle_puf_generation()
            if p:
                print_success(f'Successfully created a PUF instance\n {p}')
            continue
        if user_input == 2:
            if p:
                pp = handle_powerpuf_generation(p)
                print_success(f'Successfully created a PowerPuf instance\n {pp}')
            continue
        if user_input == 3:
            if pp:
                res = handle_random_powerpuf_response_generation(p)
                if res:
                    print_success('Successfully Generated a PowerPuf Response') 
                    print(f'{"".join([colorama.Fore.YELLOW + str(r_bit) if o_bit == r_bit else colorama.Fore.RED + str(r_bit) for o_bit, r_bit in zip(res, pp.response)])}')
                    print("Do You Want to Correct it? (1/0)")
            continue
