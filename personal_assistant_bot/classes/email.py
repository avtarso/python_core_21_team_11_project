import re

try:
   from classes.field import Field
except ModuleNotFoundError:
   from personal_assistant_bot.classes.field import Field

from colorama import init, Fore
init(autoreset=True)


class Email(Field):
    def __init__(self, value):
        super().__init__(value)
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(pattern, value):
            raise ValueError(Fore.RED + 'Incorrect email format. Please enter email like user@example.com.')
        self.__value = value
