from datetime import date, datetime
from classes.field import Field

class Birthday(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value        
    
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        try:
            self.__value = datetime.strptime(value, "%d/%m/%Y")
        except ValueError:
            print('Waiting format of date - DD/MM/YYYY. Reinput, please')

    def __str__(self):
        return self.value.strftime('%d/%m/%Y')