from classes.record import Record
from classes.addressbook import AddressBook
from classes.notes import Notes
from functions.functions import make_menu
from functions.make_header import make_header
from functions.sort import sort
from settings.settings import addressbook_filename, notes_filename


from colorama import init, Fore
init(autoreset=True)


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
                book = AddressBook.read_contacts_from_file(addressbook_filename)
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

                    book.appruve_record(new_record)

                    input("\nPress Enter to continue...")

                elif choice2 == "5":
                    make_header("EDIT RECORD")
                    
                    book.edit_record()

                    input("\nPress Enter to continue...")

                elif choice2 == "6":
                    make_header("DELETE RECORD")
                    
                    contact_name = input("\nPlease enter contact name you need to delete: ")
                    print("")
                    
                    book.delete(contact_name)

                    input("\nPress Enter to continue...")

                elif choice2 == "7":
                    make_header("SAVE ADDRESSBOOK")
                    book.write_contacts_to_file(addressbook_filename)

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

                print(Fore.GREEN + f"\nFiles and folders in {folder} sorted successful!")

                input("\nPress Enter to continue...")

        elif choice1 == "0":
            break


if __name__ == '__main__':
    main()
