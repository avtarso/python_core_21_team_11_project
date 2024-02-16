from collections import UserDict
from datetime import date, datetime
import re
import pickle

from settings import filename, PAG


wellcome_message = f"Please enter your command:  "
hello_message = "How can I help you?"
good_bye_message = "Good bye!"
bad_command = "Incorrect command!"
help_string = """For working with me, please, input one of next command:
"hello" - I print "How can I help you?"
"show all" - I print all recorded phone numbers
"find" - I find record by name or phone
"good bye", "close" or "exit" - I stop working
"help" - I print this text"""


class Field:
    def __init__(self, value):
        self.value = value


    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


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


class Phone(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError('Incorrect number format. Please enter a 10-digit number.')
        self.__value = value


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
            raise ValueError('Incorrect email format. Please enter email like user@example.com.')
        self.__value = value


class Address(Field):
    pass


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = ""
        self.email = ""
        self.address = ""

    def __str__(self):
        phones_str = '; '.join(p.value for p in self.phones)
        birthday_str = f", birthday: {self.birthday.value.strftime('%d/%m/%Y')}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones_str}{birthday_str}"

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for i in self.phones:
            if phone == i.value:
                self.phones.remove(i)
                return True
        raise ValueError('Incorrect number. Reinput, please')

    def edit_phone(self, old_phone, edited_phone):
        cash_phones = []
        for i in self.phones:
            cash_phones.append(i.value)
        if old_phone in cash_phones:
            new_phones = []
            for i in self.phones:
                if i.value == old_phone:
                    new_phones.append(Phone(edited_phone))
                else:
                    new_phones.append(Phone(i.value))
            self.phones = new_phones
            return True
        else: 
            raise ValueError('Incorrect number. Reinput, please')

    def find_phone(self, phone):
        cash_phones = []
        for i in self.phones:
            cash_phones.append(i.value)
        if phone in cash_phones:
            for i in self.phones:
                if phone == i.value:
                    return i
        else:
            return None

    def add_birthday(self, birthday):
        if not self.birthday:
            self.birthday = Birthday(birthday)
        else:
            print(f'Record {self.name} yet have field birthday - {self.birthday.value.strftime("%d/%m/%Y")}')

    def edit_birthday(self, new_birthday): #в завданні відсутній, але потрібний для консистентності
        pass 

    def delete_birthday(self): #в завданні відсутній, але потрібний для консистентності
        pass 

    def days_to_birthday(self):
        if not self.birthday:
            return f"Record {self.name} saved without birthday"
        today_date = date.today()
        birthday_date = date(today_date.year, self.birthday.value.month, self.birthday.value.day)
        if birthday_date < today_date:
            birthday_date = birthday_date.replace(year=today_date.year + 1)
        delta = birthday_date - today_date
        return delta.days

    def add_email(self, email):
        if not self.email:
            self.email = Email(email)
        else:
            print(f'Record {self.name} yet have field birthday - {self.email.value}')

    def add_address(self, address):
        if not self.address:
            self.address = Address(address)
        else:
            print(f'Record {self.name} yet have field birthday - {self.address.value}')


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        if name in self:
            for i in self:
                if i == name:
                    return self.data[i]
        else:
            return None

    def delete(self, name):
        if name in self:
            for i in self:
                if i == name:
                    self.data.pop(name)
                    return True
        else:
            return None

    def iterator_simple(self):
        st_list, obj_len = [], len(self.data)

        for i, (name, record) in enumerate(self.data.items(), 1):
            st_list.append(str(record))
            if i % PAG == 0:
                print('\n'.join(st_list))
                st_list.clear()
                if i != obj_len and input(f"-->You can ^^see^^ {i} records from {obj_len}\n-->press any key to continue or 'q' to exit --> ").lower() == "q":
                    break
        if st_list:
            print('\n'.join(st_list))
        print(f"-->You can ^^see^^ {i} records from {obj_len}\n")

    def iterator(self):
        obj_len = len(self.data)
        i = 0

        def generate_records():
            for name, record in self.data.items():
                yield str(record)

        record_generator = generate_records()
        while True:
            portion = [next(record_generator, None) for _ in range(PAG)]
            portion = [item for item in portion if item is not None]  # Исключить None (когда записи закончились)
            i += len(portion)
            print('\n'.join(portion))
            if not portion or i == obj_len:
                print(f"-->You can ^^see^^ {i} records from {obj_len}\n")
                break
            if input(f"-->You can ^^see^^ {i} records from {obj_len}\n-->press any key to continue or 'q' to exit --> ").lower() == "q":
                break
    
    def write_contacts_to_file(self, filename):
        with open(filename, "wb") as fh:
            pickle.dump(self, fh)
    
    @classmethod
    def read_contacts_from_file(cls, filename):
        book = cls()
        with open(filename, "rb") as fh:
            book = pickle.load(fh)
        return book
    
    def find_record(self, find_string):
        find_string = find_string.lower()

        book = AddressBook()
        for i, (name, record) in enumerate(self.data.items(), 1):
            if find_string.isdigit():
                for phone in record.phones:
                    if str(phone).find(find_string) > -1:
                        book.add_record(record)
            else:
                if name.lower().find(find_string) > -1:
                    book.add_record(record)
        return book

def main():
    
    book = AddressBook()
    book = AddressBook.read_contacts_from_file(filename)
    book.write_contacts_to_file("adressbook.pkl")

    while True:
        user_input = input(wellcome_message)
        user_command = user_input.lower()
 
        if user_command == "help": 
            print(help_string)
        elif user_command == "hello":
            print(hello_message)
        elif user_command == "show all":
            book.iterator()

        elif user_command.startswith("find"):
            find_string = input("Please input what you want find: ")
            find_result = AddressBook()
            find_result = book.find_record(find_string)
            if find_result:
                book.find_record(find_string).iterator_simple()
            else:
                print(f"I can`t find any matches with '{find_string}'")

        # elif user_command.startswith("add"):
        #     print(new_phone(user_input))

        # elif user_command.startswith("change"):
        #     print(edit_phone(user_input))
        
        elif user_command in ["good bye", "close", "exit"]:
            print(good_bye_message)
            break

        else: print(bad_command + "\n" + help_string)

if __name__ == '__main__':
    main()