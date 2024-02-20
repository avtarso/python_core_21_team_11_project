from collections import UserDict
from datetime import date, datetime

import os
import re
import pickle
import sys

import importlib.resources
try:
    importlib.resources.files("personal_assistant")
except:
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
    from classes.functions import make_menu

    from classes.sort import sort

    from classes.settings import filename, PAG, notes_filename
else:
    from personal_assistant.classes.field import Field
    from personal_assistant.classes.name import Name
    from personal_assistant.classes.birthday import Birthday
    from personal_assistant.classes.phone import Phone
    from personal_assistant.classes.email import Email
    from personal_assistant.classes.address import Address
    from personal_assistant.classes.record import Record
    from personal_assistant.classes.addressbook import AddressBook

    from personal_assistant.classes.note import Note
    from personal_assistant.classes.notes import Notes
    from personal_assistant.classes.functions import make_menu

    from personal_assistant.classes.sort import sort

    from personal_assistant.classes.settings import filename, PAG, notes_filename


from colorama import init, Fore
init(autoreset=True)

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
  

def edit_record(book):

    contact_name = input("Please enter the name of the contact what you want to change ")
    find_record = book.find(contact_name)
    if find_record is None:
        print("Contact name not found ")
    else:
        edit_record_menu = '''Edit Record menu: Please, input your choice:
1. Edit Name
2. Edit Phone
3. Edit Birthday
4. Edit Email
5. Edit Address
6. Save and Exit
7. Exit''' 
        edit_swither = True
        while  edit_swither:
            print(find_record)
            print(edit_record_menu)
            choice = input()
            if choice == '7':
                break
            elif choice == "1":
                new_name = input("Please enter new name ")
                find_record.edit_name(new_name)
                if new_name != contact_name:
                    book.add_record(find_record)
                    book.delete(contact_name)
            elif choice == "2":
                print("Please enter new phone ")
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
            elif choice == "6":
                book.write_contacts_to_file(filename)
                break


def appruve_record(book, new_record):
    print(new_record)
    print('''What You will do with this record?
1 - Save
2 - Edit
3 - Delete''')
    choise = input()
    if choise == "1":
        book.write_contacts_to_file(filename)
        print(new_record)
        print(Fore.GREEN + "Record saved successful")
    elif choise == "2":
        pass

    elif choise == "3":
        book.delete(new_record)


def main():
    
    if len(sys.argv) > 1:
        sort(sys.argv[1])
        quit()

    else:

        main_menu = '''Main Menu: Please, input your choice:
1 - About Bot Helper
2 - Hello, User!
3 - Use Records
4 - Use Notes
5 - Sort Files in Folder
6 - Exit
'''

        while True:

            choice1 = input(main_menu)

            if choice1 == "1":
                print(Fore.CYAN + "I'm a great bot and I will facilitate your work, now I will describe what I can do\n"
                      "I can work with contact: add, edit, remove contact's phone, email, birthday, address.\nAlso "
                      "I can work with your notes: add, edit, remove, show note or all notes, find and sort notes.\n"
                      "And finally, I have very useful function - sort, it helps you to sort all your files in "
                      "some directory. \nWhere do you want to start?")
            elif choice1 == "2":
                print(Fore.CYAN + 'Hello! How are you today? Are you ready to work?')
                pass

            elif choice1 == "3":
                switcher = True

                while switcher:

                    book = AddressBook()
                    book = AddressBook.read_contacts_from_file(filename)
                    record_menu = '''Record menu: Please, input your choice:
1. Show all Records
2. Find Records
3. Show Record with birthday in N days
4. Add Record
5. Edit Record
6. Delete record
7. Save AddressBook and Exit
8. Exit to previous menu
'''
                    choice2 = input(record_menu)
                    if choice2 == "1":
                        book.iterator()
                    elif choice2 == "2":
                        find_string = input("Please input Name of record, which you want find: ")
                        find_result = AddressBook()
                        find_result = book.find_record(find_string)
                        if find_result:
                            book.find_record(find_string).iterator_simple()
                        else:
                            print(Fore.RED + f"I can`t find any matches with '{find_string}'")
                    
                    elif choice2 == "3":
                        days_to_serch = input("Please, input number of days to search")
                        book.find_birthdays(days_to_serch).iterator()
                    
                    elif choice2 == "4":
                        name = input("Please enter the name ")
                        new_record = Record(name)
                        try:
                            phone = input("Please enter the phone ")
                            new_record.add_phone(phone)
                        except ValueError:
                            print(Fore.RED + 'Incorrect number format. Please enter a 10-digit number.')
                            phone = input("Please enter the phone ")
                            new_record.add_phone(phone)
                        try:
                            email = input("Please enter the email ")
                            new_record.add_email(email)
                        except ValueError:
                            print(Fore.RED + 'Incorrect email format. Please enter email like user@example.com.')
                            email = input("Please enter the email ")
                            new_record.add_email(email)
                        address = input("Please enter the address ")
                        new_record.add_address(address)
                        try:
                            birthday = input("Please enter the date of birth ")
                            new_record.add_birthday(birthday)
                        except ValueError:
                            print(Fore.RED + 'Waiting format of date - DD/MM/YYYY. Reinput, please')
                            birthday = input("Please enter the date of birth ")
                            new_record.add_birthday(birthday)
                        book.add_record(new_record)
                        print('Contact added')
                        appruve_record(book, new_record)
                    elif choice2 == "5":
                        edit_record(book)
                    elif choice2 == "6":
                        contact_name = input("Please enter contact name you need to delete ")
                        book.delete(contact_name)            
                    elif choice2 == "7":
                        book.write_contacts_to_file(filename)
                        quit()      
                    elif choice2 == "8":
                        switcher = False

            elif choice1 == "4":
                notes = Notes().load_from_file(notes_filename)
                make_menu(notes)
            
            elif choice1 == "5":
                
                print("Please, input folder name")
                print(Fore.RED + "Carefully! Files will be sorted! You won't be able to find them in your usual place!")
                sort(input())

            elif choice1 == "6":
                break


if __name__ == '__main__':
    main()
