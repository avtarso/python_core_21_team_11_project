from datetime import datetime

from .field import Field

from colorama import init, Fore
init(autoreset=True)


class Birthday(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value        
    
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if not datetime.strptime(value, "%d/%m/%Y"):
            raise ValueError(Fore.RED + 'Waiting format of date - DD/MM/YYYY. Reinput, please')
        else:
            self.__value = datetime.strptime(value, "%d/%m/%Y")

    def __str__(self):
        return self.value.strftime('%d/%m/%Y')