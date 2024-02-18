from collections import UserDict
from datetime import date, datetime
# from simple_term_menu import TerminalMenu
import re
import pickle
import sys
import os

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

from sort import sort

from classes.settings import filename, PAG, notes_filename


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

# Функції для роботи з нотатками - початок
def split_text(text: str) -> list:

    NOTE_LEN = 40

    result = []

    while len(text) > NOTE_LEN:
        result.append(text[0:NOTE_LEN])
        text = text[NOTE_LEN:]
    result.append(text)

    return result


def add_note(notesbook: Notes) -> None:

    note_text = input("Input note text: ")
    note_text = note_text.strip()

    print("Input note tags one per line (type q for finish):")
    note_tag = ""
    note_tags = []

    while True:
        note_tag = input("> ")
        if note_tag == "q":
            break
        note_tag = note_tag.strip().replace(" ", "_").replace(",", "_")
        if note_tag:
            note_tags.append(note_tag)

    if not note_text and not note_tags:
        print("Nothing to add!")
    else:
        notesbook.add_note(Note(note_text, tags=note_tags))
        print("Success!")
        show_notes(notesbook, uid=(notesbook.uid - 1))

    input("Press Enter to continue...")


def edit_note(notesbook: Notes) -> None:

    uid = input("Input note UID you want to edit: ")

    try:
        uid = int(uid)
        if not notesbook.is_note_exists(uid):
            raise ValueError
    except:
        print("A note with this UID does not exist!")
        input("Press Enter to continue...")
        return

    show_notes(notesbook, uid=uid)

    note_text = ""
    note_tags = []

    choice = input(
        "Do you want to edit the note text? (y = yes / any key = no): ")

    if choice == "y":
        note_text = input("Input new note text: ")
        note_text = note_text.strip()

    choice = input(
        "Do you want to edit the note tags? (y = yes / any key = no): ")

    if choice == "y":
        print("Input new note tags one per line (type q for finish):")
        note_tag = ""

        while True:
            note_tag = input("> ")
            if note_tag == "q":
                break
            note_tag = note_tag.strip().replace(" ", "_").replace(",", "_")
            if note_tag:
                note_tags.append(note_tag)

    if not note_text and not note_tags:
        print("Nothing to change!")
        input("Press Enter to continue...")
        return

    if note_text:
        notesbook.edit_note(uid, new_text=note_text)

    if note_tags:
        notesbook.edit_note(uid, new_tags=note_tags)

    print("Success!")
    show_notes(notesbook, uid=uid)
    input("Press Enter to continue...")


def remove_note(notesbook: Notes) -> None:

    uid = input("Input note UID you want to remove: ")

    try:
        uid = int(uid)
        if not notesbook.is_note_exists(uid):
            raise ValueError
    except:
        print("A note with this UID does not exist!")
        input("Press Enter to continue...")
        return

    show_notes(notesbook, uid=uid)

    choice = input(
        "Do you want to remove this note? (y = yes / any key = no): ")

    if choice == "y":
        notesbook.remove_note(uid)
        print("Success!")

    input("Press Enter to continue...")


def show_note(notesbook: Notes) -> None:

    uid = input("Input note UID you want to show: ")

    try:
        uid = int(uid)
        show_notes(notesbook, uid=uid)
    except:
        show_notes(notesbook, uid=-1)

    input("Press Enter to continue...")


def show_notes(notesbook: Notes, uid=0, notes_list=[]) -> None:
    """
    Функція перегляду нотаток.
    Параметри відпрацьовують з наступним пріорітетом:
    1. Якщо заданий uid, то виводить нотатку з цим uid
    2. Якщо заданий notes_list, то виводить список нотаток
    3. Якщо не заданий жоден з цих параметрів - виводить всі нотатки
    """

    print("-" * 141)
    print("|{:^5}|{:^40}|{:^40}|{:^25}|{:^25}|".format(
        'UID', 'Text', 'Tags', 'Created', 'Modified'))
    print("-" * 141)

    proc_list = []
    print_end = False

    if uid != 0:
        if notesbook.show_note(uid):
            proc_list.append(notesbook.show_note(uid))
        else:
            return
    elif notes_list:
        proc_list = notes_list
    else:
        proc_list = notesbook.show_all_notes()
        print_end = True

    for item in proc_list:
        note_text = item[1].show_text()
        note_tags = item[1].show_tags()

        note_tags = ", ".join(note_tags)

        text_list = split_text(note_text)
        tags_list = split_text(note_tags)

        if len(split_text(note_text)) > 1:
            if len(split_text(note_tags)) > 1:
                print("|{:^5}|{:<40}|{:<40}|{:^25}|{:^25}|".format(
                    item[0], text_list[0], tags_list[0], item[2], item[3]))
                for i in range(1, max(len(text_list), len(tags_list))):
                    text = text_list[i] if i < len(text_list) else ""
                    tag = tags_list[i] if i < len(tags_list) else ""
                    print("|{:^5}|{:<40}|{:<40}|{:^25}|{:^25}|".format(
                        "", text, tag, "", ""))
            else:
                print("|{:^5}|{:<40}|{:<40}|{:^25}|{:^25}|".format(
                    item[0], text_list[0], note_tags, item[2], item[3]))
                for i in range(1, len(text_list)):
                    print("|{:^5}|{:<40}|{:<40}|{:^25}|{:^25}|".format(
                        "", text_list[i], "", "", ""))
        else:
            if len(split_text(note_tags)) > 1:
                print("|{:^5}|{:<40}|{:<40}|{:^25}|{:^25}|".format(
                    item[0], note_text, tags_list[0], item[2], item[3]))
                for i in range(1, len(tags_list)):
                    print("|{:^5}|{:<40}|{:<40}|{:^25}|{:^25}|".format(
                        "", "", tags_list[i], "", ""))
            else:
                print("|{:^5}|{:<40}|{:<40}|{:^25}|{:^25}|".format(
                    item[0], note_text, note_tags, item[2], item[3]))

        print("-" * 141)

    if print_end:
        input("Press Enter to continue...")


def find_notes(notesbook: Notes) -> None:

    find_text = input("Input a search phrase: ")

    search_result = notesbook.find_notes(find_text)

    show_notes(notesbook, notes_list=search_result)

    input("Press Enter to continue...")


def sort_notes(notesbook: Notes) -> None:

    sort_by = ""
    sort_revers = False

    choice = input(
        "Do you want to sort by note text? (y = yes / any key = no): ")

    if choice == "y":
        sort_by = "text"
    else:
        choice = input(
            "Do you want to sort by note tags? (y = yes / any key = no): ")

        if choice == "y":
            sort_by = "tag"
        else:
            input("Press Enter to continue...")
            return

    choice = input("Do you want to sort by asc? (y = yes / any key = no): ")

    if choice != "y":
        sort_revers = True

    sort_result = notesbook.sort_notes(sort_by=sort_by, revers=sort_revers)

    show_notes(notesbook, notes_list=sort_result)

    input("Press Enter to continue...")


def make_menu(notesbook: Notes) -> None:
    while True:
        os.system('cls')  # Очищає термінал
        print(
""" 
1. Add note
2. Edit note (by UID)
3. Remove note (by UID)
4. Show note (by UID)
5. Show all notes
6. Find notes
7. Sort notes

0. Exit to previous menu
"""
        )

        cmd = input("Choose an action: ")

        if cmd == "0":
            return
        elif cmd == "1":
            add_note(notesbook)
        elif cmd == "2":
            edit_note(notesbook)
        elif cmd == "3":
            remove_note(notesbook)
        elif cmd == "4":
            show_note(notesbook)
        elif cmd == "5":
            show_notes(notesbook)
        elif cmd == "6":
            find_notes(notesbook)
        elif cmd == "7":
            sort_notes(notesbook)
        else:
            print("Wrong input!")
# Функції для роботи з нотатками - кінець

def main():
    
    if len(sys.argv) > 1:
        sort(sys.argv[1])
        quit()

    else:

        #book.write_contacts_to_file("adressbook.pkl")

        notes = Notes()
        notes = notes.load_from_file(notes_filename)

        main_menu = '''Main Menu: Please, input your choice:
1 - About Bot Helper
2 - Hello, User"
3 - Use Records
4 - Use Notes
5 - Exit
6 - Save All and Exit'''

        while True:

            choice1 = input(main_menu)

            if choice1 == "1":
                pass
                #about bot
            elif choice1 == "2":
                #hello user
                pass

            elif choice1 == "3":
                book = AddressBook()
                book = AddressBook.read_contacts_from_file(filename)
                record_menu = '''Record menu: Please, input your choice:
1. Show all Records ----
2. Find Records
3. Show Record whit birthday in N days
4. Add Record
5. Edit Record
6. Delete record
7. Save AdressBook and Exit
8. Exit
'''
                choice2 = input(record_menu)
                if choice2 == "1":
                    book.iterator()
                elif choice2 == "2":
                    find_string = input("Please input what you want find: ")
                    find_result = AddressBook()
                    find_result = book.find_record(find_string)
                    if find_result:
                        book.find_record(find_string).iterator_simple()
                    else:
                        print(f"I can`t find any matches with '{find_string}'")
                elif choice2 == "3":
                    pass      
                elif choice2 == "4":
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
                elif choice2 == "5":
                    contact_name = input("Please enter the name of the contact you want to change ")
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

                        while True:
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



                elif choice2 == "6":
                    contact_name = input("Please enter contact name you need to delete ")
                    book.delete(contact_name)            
                elif choice2 == "7":
                    book.write_contacts_to_file(filename)
                    break       
                elif choice2 == "8":
                    break   





            elif choice1 == "4":
                make_menu(notes)

            elif choice1 == "5":
                break

            elif choice1 == "6":
                book.write_contacts_to_file(filename)
                notes.save_to_file(notes_filename)
                break




    
            # if user_command == "About Bot Helper": 
            #     print(help_string)
            # elif user_command == "Hello, User!":
            #     print(hello_message)
            # elif user_command == "Show all records":
            #     book.iterator()

            # elif user_command.startswith("Find records"):
            #     find_string = input("Please input what you want find: ")
            #     find_result = AddressBook()
            #     find_result = book.find_record(find_string)
            #     if find_result:
            #         book.find_record(find_string).iterator_simple()
            #     else:
            #         print(f"I can`t find any matches with '{find_string}'")

            # elif user_command.startswith("Add record"):
            #     name = input("Please enter the name ")
            #     phone = input("Please enter the phone ")
            #     email = input("Please enter the email ")
            #     address = input("Please enter the address ")
            #     birthday = input("Please enter the date of birth ")
            #     new_record = Record(name)
            #     new_record.add_phone(phone)
            #     new_record.add_email(email)
            #     new_record.add_address(address)
            #     new_record.add_birthday(birthday)
            #     book.add_record(new_record)
            #     print('Contact added')
            # elif user_command.startswith("Change record"):
            #     contact_name = input("Please enter the name of the contact you want to change ")
            #     find_record = book.find(contact_name)
            #     if find_record is None:
            #         print("Contact name not found ")
            #     else:
            #         edit_options = ["Edit Name",
            #                     "Edit Phone",
            #                     "Edit Birthday",
            #                     "Edit Email",
            #                     "Edit Address",
            #                     "Exit"]
            #         edit_terminal_menu = TerminalMenu(edit_options)
            #         while True:
            #             print()
            #             print("Choose the field to change (or 'Exit'' to finish changing):")
            #             edit_menu_entry_index = edit_terminal_menu.show()
            #             choice = edit_options[edit_menu_entry_index]
            #             if choice == 'Exit':
            #                 break
            #             elif choice == "Edit Name":
            #                 new_name = input("Please enter new name ")
            #                 find_record.edit_name(new_name)
            #                 if new_name != contact_name:
            #                     book.add_record(find_record)
            #                     book.delete(contact_name)
            #             elif choice == "Phone":
            #                 print("Please enter new phone ")
            #                 new_phone = input("Please enter new phone ")
            #                 find_record.add_phone(new_phone)
            #             elif choice == "Birthday":
            #                 new_birthday = input("Please enter new birthday ")
            #                 find_record.edit_birthday(new_birthday)
            #             elif choice == "Email":
            #                 new_email = input("Please enter new email ")
            #                 find_record.edit_email(new_email)
            #             elif choice == "Address":
            #                 new_address = input("Please enter new address ")
            #                 find_record.edit_address(new_address)


            # elif user_command.startswith("Delete record"):
            #     contact_name = input("Please enter contact name you need to delete ")
            #     book.delete(contact_name)




            # elif user_command in ["Exit"]:
            #     print(good_bye_message)
            #     break

if __name__ == '__main__':
    main()
