from classes.note import Note
from classes.notes import Notes

import os

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


if __name__ == '__main__':
    pass
