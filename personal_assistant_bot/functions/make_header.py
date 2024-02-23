from os import system, name
from colorama import Fore


def make_header(title: str) -> None:
    # for windows
    if name == 'nt':
        system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        system('clear')

    print(Fore.CYAN + "*" * 30)
    print(Fore.CYAN + "*{:^28}*".format(title))
    print(Fore.CYAN + "*" * 30)
    Fore.RESET