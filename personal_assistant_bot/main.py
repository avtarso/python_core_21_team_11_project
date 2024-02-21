# from collections import UserDict
# from datetime import date, datetime

# import os
# import re
# import pickle
#import sys

import importlib.resources
try:
    importlib.resources.files("personal_assistant_bot")
except:
    # from classes.field import Field
    # from classes.name import Name
    # from classes.birthday import Birthday
    # from classes.phone import Phone
    # from classes.email import Email
    # from classes.address import Address
    from classes.record import Record
    from classes.addressbook import AddressBook

    #from classes.note import Note
    from classes.notes import Notes
    from classes.functions import make_menu, make_header
    from classes.sort import sort
    from classes.settings import filename, notes_filename
else:
    # from personal_assistant_bot.classes.field import Field
    # from personal_assistant_bot.classes.name import Name
    # from personal_assistant_bot.classes.birthday import Birthday
    # from personal_assistant_bot.classes.phone import Phone
    # from personal_assistant_bot.classes.email import Email
    # from personal_assistant_bot.classes.address import Address
    from personal_assistant_bot.classes.record import Record
    from personal_assistant_bot.classes.addressbook import AddressBook

    #from personal_assistant_bot.classes.note import Note
    from personal_assistant_bot.classes.notes import Notes
    from personal_assistant_bot.classes.functions import make_menu, make_header
    from personal_assistant_bot.classes.sort import sort
    from personal_assistant_bot.classes.settings import filename, notes_filename


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

    contact_name = input("\nPlease enter the name of the contact what you want to change: ")
    find_record = book.find(contact_name)
    if find_record is None:
        print(Fore.RED + "\nContact name not found!")
    else:
        edit_record_menu = '''\nEdit Record menu:
1. Edit Name
2. Edit Phone
3. Edit Birthday
4. Edit Email
5. Edit Address
6. Save and Exit
7. Exit'''
        edit_swither = True
        while  edit_swither:
            print("")
            print(find_record)
            print(edit_record_menu)
            choice = input("\nPlease input your choice: ")
            if choice == '7':
                break
            elif choice == "1":
                new_name = input("Please enter new Name: ")
                print("")
                find_record.edit_name(new_name)
                if new_name != contact_name:
                    book.add_record(find_record)
                    book.delete(contact_name)
            elif choice == "2":
                while True:
                    new_phone = input("Please enter new Phone: ")
                    print("")
                    try:
                        find_record.add_phone(new_phone)
                    except:
                        pass
                    else:
                        break
            elif choice == "3":
                while True:
                    new_birthday = input("Please enter new Birthday in format DD/MM/YYYY: ")
                    print("")
                    try:
                        find_record.edit_birthday(new_birthday)
                    except:
                        pass
                    else:
                        break
            elif choice == "4":
                while True:
                    new_email = input("Please enter new Email: ")
                    print("")
                    try:
                        find_record.edit_email(new_email)
                    except:
                        pass
                    else:
                        break
            elif choice == "5":
                new_address = input("Please enter new Address: ")
                print("")
                find_record.edit_address(new_address) 
            elif choice == "6":
                book.write_contacts_to_file(filename)
                print(Fore.GREEN + "\nChanges saved successful")
                break

def appruve_record(book, new_record):
    print(new_record)
    print('''\nWhat You will do with this record?
1 - Save changes
2 - Discard changes''')
    choise = input()
    if choise == "1":
        book.write_contacts_to_file(filename)
        #print(new_record)
        print(Fore.GREEN + "Changes saved successful")
    elif choise == "2":
        book.delete(new_record)
        print(Fore.GREEN + "Changes discard successful")


def main():
    
    main_menu = '''
1. About Bot Helper
2. Hello, User!
3. Use Records
4. Use Notes
5. Sort Files in Folder

0. Exit

Please, input your choice: '''

    while True:

        make_header("MAIN MENU")
        choice1 = input(main_menu)

        if choice1 == "1":

            make_header("ABOUT BOT HELPER")
            print("\nI'm a great bot and I will facilitate your work, now I will describe what I can do\n"
                    "I can work with contact: add, edit, remove contact's phone, email, birthday, address.\nAlso "
                    "I can work with your notes: add, edit, remove, show note or all notes, find and sort notes.\n"
                    "And finally, I have very useful function - sort, it helps you to sort all your files in "
                    "some directory. \nWhere do you want to start?")
            
            input("\nPress Enter to continue...")

        elif choice1 == "2":

            make_header("HELLO, USER!")
            print('\nHello! How are you today? Are you ready to work?')

            input("\nPress Enter to continue...")

        elif choice1 == "3":

            switcher = True                
            while switcher:

                book = AddressBook()
                book = AddressBook.read_contacts_from_file(filename)
                record_menu = '''
1. Show all Records
2. Find Records
3. Show Records with birthday in N days
4. Add Record
5. Edit Record
6. Delete Record
7. Save AddressBook

0. Exit to previous menu

Please, input your choice: '''

                make_header("ADDESSBOOK MENU")
                choice2 = input(record_menu)

                if choice2 == "1":
                    make_header("SHOW ALL RECORDS")

                    book.iterator()

                    input("\nPress Enter to continue...")

                elif choice2 == "2":
                    make_header("FIND RECORDS")

                    find_string = input("\nPlease input Name of record, which you want find: ")

                    find_result = AddressBook()
                    find_result = book.find_record(find_string)
                    
                    if find_result:
                        print("")
                        book.find_record(find_string).iterator_simple()
                    else:
                        print(Fore.RED + f"\nI can`t find any matches with '{find_string}'")

                    input("\nPress Enter to continue...")

                elif choice2 == "3":
                    make_header("N DAYS FROM BIRTHDAY")

                    days_to_serch = input("\nPlease input number of days to search: ")
                    print("")

                    book.find_birthdays(days_to_serch).iterator()

                    input("\nPress Enter to continue...")
                
                elif choice2 == "4":
                    make_header("ADD RECORD")

                    name = input("\nPlease enter the name: ")
                    new_record = Record(name)

                    while True:
                        phone = input("Please enter the phone: ")
                        try:                                
                            new_record.add_phone(phone)
                        except ValueError:
                            print(Fore.RED + 'Incorrect number format. Please enter a 10-digit number.')
                        else:
                            break

                    while True:
                        email = input("Please enter the email: ")
                        try:                            
                            new_record.add_email(email)
                        except ValueError:
                            print(Fore.RED + 'Incorrect email format. Please enter email like user@example.com.')
                        else:
                            break

                    address = input("Please enter the address: ")
                    new_record.add_address(address)

                    while True:
                        birthday = input("Please enter the date of birth in format DD/MM/YYYY: ")
                        try:                                
                            new_record.add_birthday(birthday)
                        except ValueError:
                            print(Fore.RED + 'Waiting format of date - DD/MM/YYYY. Reinput, please.')
                        else:
                            break

                    book.add_record(new_record)
                    print(Fore.GREEN + "\nRecord added successful!\n")

                    appruve_record(book, new_record)

                    input("\nPress Enter to continue...")

                elif choice2 == "5":
                    make_header("EDIT RECORD")
                    
                    edit_record(book)

                    input("\nPress Enter to continue...")

                elif choice2 == "6":
                    make_header("DELETE RECORD")
                    
                    contact_name = input("\nPlease enter contact name you need to delete: ")
                    print("")
                    
                    book.delete(contact_name)

                    input("\nPress Enter to continue...")

                elif choice2 == "7":
                    make_header("SAVE ADDRESSBOOK")
                    book.write_contacts_to_file(filename)

                    print(Fore.GREEN + "\nAddressBook saved successful!")

                    input("\nPress Enter to continue...")

                elif choice2 == "0":
                    switcher = False

        elif choice1 == "4":
            notes = Notes().load_from_file(notes_filename)
            make_menu(notes)
        
        elif choice1 == "5":
            make_header("SORT FILES IN FOLDER")
            print(Fore.RED + "\nCarefully! Files will be sorted! You won't be able to find them in your usual place!")

            folder = input("\nPlease input folder name or press Enter to exit: ")

            if not folder:
                pass
            else:
                sort(folder)

        elif choice1 == "0":
            break


if __name__ == '__main__':
    main()
