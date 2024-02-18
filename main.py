from collections import UserDict
from datetime import date, datetime
from simple_term_menu import TerminalMenu
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
from classes.note import Note
from classes.notes import Notes


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
    #book.write_contacts_to_file("adressbook.pkl")

    main_options = ["About Bot Helper",
               "Hello, User",
               "Show all records",
               "Find records",
               "Add record",
               "Change record",
               "Delete record",
               "Exit"]
    terminal_menu = TerminalMenu(main_options)

    while True:

        main_menu_entry_index = terminal_menu.show()

        user_command = main_options[main_menu_entry_index]
 
        if user_command == "About Bot Helper": 
            print(help_string)
        elif user_command == "Hello, User!":
            print(hello_message)
        elif user_command == "Show all records":
            book.iterator()

        elif user_command.startswith("Find records"):
            find_string = input("Please input what you want find: ")
            find_result = AddressBook()
            find_result = book.find_record(find_string)
            if find_result:
                book.find_record(find_string).iterator_simple()
            else:
                print(f"I can`t find any matches with '{find_string}'")

        elif user_command.startswith("Add record"):
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
        elif user_command.startswith("Change record"):
            contact_name = input("Please enter the name of the contact you want to change ")
            find_record = book.find(contact_name)
            if find_record is None:
                print("Contact name not found ")
            else:
                edit_options = ["Edit Name",
                            "Edit Phone",
                            "Edit Birthday",
                            "Edit Email",
                            "Edit Address",
                            "Exit"]
                edit_terminal_menu = TerminalMenu(edit_options)
                while True:
                    print()
                    print("Choose the field to change (or 'Exit'' to finish changing):")
                    edit_menu_entry_index = edit_terminal_menu.show()
                    choice = edit_options[edit_menu_entry_index]
                    if choice == 'Exit':
                        break
                    elif choice == "Edit Name":
                        new_name = input("Please enter new name ")
                        find_record.edit_name(new_name)
                        if new_name != contact_name:
                            book.add_record(find_record)
                            book.delete(contact_name)
                    elif choice == "Phone":
                        print("Please enter new phone ")
                        new_phone = input("Please enter new phone ")
                        find_record.add_phone(new_phone)
                    elif choice == "Birthday":
                        new_birthday = input("Please enter new birthday ")
                        find_record.edit_birthday(new_birthday)
                    elif choice == "Email":
                        new_email = input("Please enter new email ")
                        find_record.edit_email(new_email)
                    elif choice == "Address":
                        new_address = input("Please enter new address ")
                        find_record.edit_address(new_address)


        elif user_command.startswith("Delete record"):
            contact_name = input("Please enter contact name you need to delete ")
            book.delete(contact_name)




        elif user_command in ["Exit"]:
            print(good_bye_message)
            break

if __name__ == '__main__':
    main()
