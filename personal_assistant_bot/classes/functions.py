from .note import Note
from .notes import Notes

from os import system
from .settings import PAG, notes_filename

from colorama import Fore

# Функції для роботи з нотатками - початок
def split_text(text: str) -> list:

    NOTE_LEN = 40

    result = []

    while len(text) > NOTE_LEN:
        result.append(text[0:NOTE_LEN])
        text = text[NOTE_LEN:]
    result.append(text)

    return result


def make_header(title: str) -> None:
    system('cls')
    print(Fore.CYAN + "*" * 30)
    print(Fore.CYAN + "*{:^28}*".format(title))
    print(Fore.CYAN + "*" * 30)
    Fore.RESET


def save_changes(notesbook: Notes, p=False) -> None:

    if p:
        make_header("SAVE NOTES TO FILE")

    choice = input(
        "\nDo you want to save your changes? (1 = yes / any key = no): ")

    if choice == "1":
        try:
            notesbook.save_to_file(notes_filename)

            print(Fore.GREEN + "\nChanges saved successfully!")
            Fore.RESET

        except:
            print(Fore.RED + "\nError saving changes!")
            Fore.RESET
    
    if p:
        input("\nPress Enter to continue...")


def add_note(notesbook: Notes) -> None:

    make_header("ADD NOTE")

    note_text = input("\nInput note text: ")
    note_text = note_text.strip()

    print("\nInput note tags one per line (type 0 for finish):")
    note_tag = ""
    note_tags = []

    while True:
        note_tag = input("> ")
        if note_tag == "0":
            break
        note_tag = note_tag.strip().replace(" ", "_").replace(",", "_")
        if note_tag:
            note_tags.append(note_tag)

    if not note_text and not note_tags:
        print(Fore.GREEN + "\nNothing to add!")
        Fore.RESET
    else:
        notesbook.add_note(Note(note_text, tags=note_tags))

        print(Fore.GREEN + "\nSuccess!")
        Fore.RESET

        show_notes(notesbook, uid=(notesbook.uid - 1))

        save_changes(notesbook)

    input("\nPress Enter to continue...")


def edit_note(notesbook: Notes) -> None:

    make_header("EDIT NOTE")

    uid = input("\nInput note UID you want to edit: ")

    try:
        uid = int(uid)
        if not notesbook.is_note_exists(uid):
            raise ValueError
    except:
        print(Fore.RED + "\nA note with this UID does not exist!")
        Fore.RESET

        input("\nPress Enter to continue...")
        return

    show_notes(notesbook, uid=uid)

    note_text = ""
    note_tags = []

    choice = input(
        "\nDo you want to edit the note text? (1 = yes / any key = no): ")

    if choice == "1":
        note_text = input("\nInput new note text: ")
        note_text = note_text.strip()

    choice = input(
        "\nDo you want to edit the note tags? (1 = yes / any key = no): ")

    if choice == "1":
        print("\nInput new note tags one per line (type 0 for finish):")
        note_tag = ""

        while True:
            note_tag = input("> ")
            if note_tag == "0":
                break
            note_tag = note_tag.strip().replace(" ", "_").replace(",", "_")
            if note_tag:
                note_tags.append(note_tag)

    if not note_text and not note_tags:
        print(Fore.GREEN + "\nNothing to change!")
        Fore.RESET

        input("\nPress Enter to continue...")
        return

    if note_text:
        notesbook.edit_note(uid, new_text=note_text)

    if note_tags:
        notesbook.edit_note(uid, new_tags=note_tags)

    print(Fore.GREEN + "\nSuccess!")
    Fore.RESET

    show_notes(notesbook, uid=uid)

    save_changes(notesbook)

    input("\nPress Enter to continue...")


def remove_note(notesbook: Notes) -> None:

    make_header("REMOVE NOTE")

    uid = input("\nInput note UID you want to remove: ")

    try:
        uid = int(uid)
        if not notesbook.is_note_exists(uid):
            raise ValueError
    except:
        print(Fore.RED + "\nA note with this UID does not exist!")
        Fore.RESET

        input("\nPress Enter to continue...")
        return

    show_notes(notesbook, uid=uid)

    choice = input(
        "\nDo you want to remove this note? (1 = yes / any key = no): ")

    if choice == "1":
        notesbook.remove_note(uid)

        print(Fore.GREEN + "\nSuccess!")
        Fore.RESET

        save_changes(notesbook)

    input("\nPress Enter to continue...")


def show_note(notesbook: Notes) -> None:

    make_header("SHOW NOTE")

    uid = input("\nInput note UID you want to show: ")

    try:
        uid = int(uid)
        if not notesbook.is_note_exists(uid):
            raise ValueError
    except:
        print(Fore.RED + "\nA note with this UID does not exist!")
        Fore.RESET

        input("\nPress Enter to continue...")
        return
    
    show_notes(notesbook, uid=uid)

    input("\nPress Enter to continue...")


def show_notes(notesbook: Notes, uid=0, notes_list=[]) -> None:
    """
    Функція перегляду нотаток.
    Параметри відпрацьовують з наступним пріорітетом:
    1. Якщо заданий uid, то виводить нотатку з цим uid
    2. Якщо заданий notes_list, то виводить список нотаток
    3. Якщо не заданий жоден з цих параметрів - виводить всі нотатки
    """

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

        make_header("SHOW ALL NOTES")

        proc_list = notesbook.show_all_notes()
        print_end = True

    print("-" * 141)
    print("|{:^5}|{:^40}|{:^40}|{:^25}|{:^25}|".format(
        'UID', 'Text', 'Tags', 'Created', 'Modified'))
    print("-" * 141)

    count = 0
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

        if count + 1 == PAG:
            count = 0
            choice = input("Press Enter to continue or 0 + Enter to break... ")            
            if choice == "0":
                break
            else:
                print("\n")
                print("-" * 141)
                continue
        else:
            count += 1

    if print_end:
        input("\nPress Enter to continue...")


def find_notes(notesbook: Notes) -> None:

    make_header("FIND NOTES")

    find_text = input("\nInput a search phrase: ")

    search_result = notesbook.find_notes(find_text)

    show_notes(notesbook, notes_list=search_result)

    input("\nPress Enter to continue...")


def sort_notes(notesbook: Notes) -> None:

    make_header("SORT NOTES")

    sort_by = ""
    sort_revers = False

    choice = input(
        "\nDo you want to sort by note text? (1 = yes / any key = no): ")

    if choice == "1":
        sort_by = "text"
    else:
        choice = input(
            "\nDo you want to sort by note tags? (1 = yes / any key = no): ")

        if choice == "1":
            sort_by = "tag"
        else:
            input("\nPress Enter to continue...")
            return

    choice = input("\nDo you want to sort by asc? (1 = yes / any key = no): ")

    if choice != "1":
        sort_revers = True

    sort_result = notesbook.sort_notes(sort_by=sort_by, revers=sort_revers)

    show_notes(notesbook, notes_list=sort_result)

    input("\nPress Enter to continue...")


def make_menu(notesbook: Notes) -> None:
    while True:

        make_header("NOTES MENU")

        print(
            """ 
1. Add note
2. Edit note (by UID)
3. Remove note (by UID)
4. Show note (by UID)
5. Show all notes
6. Find notes
7. Sort notes
8. Save notes to file

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
        elif cmd == "8":
            save_changes(notesbook, p=True)
        else:
            print("Wrong input!")
# Функції для роботи з нотатками - кінець


if __name__ == '__main__':
    pass
