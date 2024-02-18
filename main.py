from collections import UserDict
from datetime import date, datetime
import re
import pickle

from classes.field import Field
from classes.name import Name
from classes.birthday import Birthday
from classes.phone import Phone
from classes.email import Email
from classes.address import Address
from classes.record import Record
from classes.addressbook import AddressBook

from classes.settings import filename, PAG


wellcome_message = f"Please enter your command:  "
hello_message = "How can I help you?"
good_bye_message = "Good bye!"
bad_command = "Incorrect command!"
add = "Please write name, address, phone, email, date of birth"
change = "Write the name of the contact you want to change"
delete = "Write the name of contact you want to delete"
find = "Write the name or phone number of the contact you want to find"
help_string = """For working with me, please, input one of next command:
"hello" - I print "How can I help you?"
"show all" - I print all recorded phone numbers
"find" - I find record by name or phone
"good bye", "close" or "exit" - I stop working
"help" - I print this text
"add" - I add name, phone, email, date of birth, address
"change" - I can change the data
"delete" - I can delete contact"""


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

        elif user_command.startswith("add"):
            name = input("Please enter the name ")
            phone = input("Please enter the phone ")
            email = input("Please enter the email ")
            address = input("Please enter the address ")
            birthday = input("Please enter the date of birth ")
            new_record = Record(name)
            new_record.add_phone(phone)
            new_record.add_email(email)
            new_record.add_address(address)
            new_record.add_birthday(birthday)
            book.add_record(new_record)
            print('Contact added')
        elif user_command.startswith("change"):
            contact_name = input("Please enter the name of the contact you want to change ")
            find_record = book.find(contact_name)
            if find_record is None:
                print("Contact name not found ")
            else:
                while True:
                    print("Choose the field to change (or type 'done' to finish changing):")
                    print("1. Name")
                    print("2. Phone")
                    print("3. Birthday")
                    print("4. Email")
                    print("5. Address")
                    choice = input("Enter your choice (1-5): ")
                    if choice == 'done':
                        break
                    elif choice == "1":
                        new_name = input("Please enter new name ")
                        find_record.edit_name(new_name)
                        if new_name != contact_name:
                            book.add_record(find_record)
                            book.delete(contact_name)
                    elif choice == "2":
                        new_phone = input("Please enter new phone ")
                        find_record.add_phone(new_phone)
                    elif choice == "3":
                        new_birthday = input("Please enter new birthday ")
                        find_record.edit_birthday(new_birthday)
                    elif choice == "4":
                        new_email = input("Please enter new email ")
                        find_record.edit_email(new_email)
                    elif choice == "5":
                        new_address = input("Please enter new address ")
                        find_record.edit_address(new_address)
                    else:
                        print("Please type numbers 1-5 or done ")

        elif user_command.startswith("delete"):
            contact_name = input("Please enter contact name you need to delete ")
            book.delete(contact_name)




        elif user_command in ["good bye", "close", "exit"]:
            print(good_bye_message)
            break

        else: print(bad_command + "\n" + help_string)

if __name__ == '__main__':
    main()
