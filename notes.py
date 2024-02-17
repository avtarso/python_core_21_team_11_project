from collections import UserDict
from datetime import datetime
import pickle

class Note:

    def __init__(self, text="", tags=[]):

        if type(text) != str or type(tags) != list:
            raise TypeError

        self.text = text

        for item in tags:
            if type(item) != str:
                raise TypeError

        self.tags = list(set(tags))
        self.tags.sort()

    def edit_text(self, data):

        if type(data) != str:
            raise TypeError

        self.text = data

        return self

    def show_text(self):

        return self.text

    def add_tags(self, data):

        proc_tags = []

        if type(data) == str:
            if data not in self.tags:
                proc_tags.append(data)
        elif type(data) == list:
            for item in data:
                if type(item) == str:
                    if item not in self.tags:
                        proc_tags.append(item)
                else:
                    raise TypeError
        else:
            raise TypeError

        self.tags.extend(list(set(proc_tags)))
        self.tags.sort()

        return self

    def edit_tag(self, current_tag, new_tag):

        if type(new_tag) != str:
            raise TypeError

        if current_tag in self.tags:
            idx = self.tags.index(current_tag)

            self.tags[idx] = new_tag

        return self

    def remove_tags(self, data):

        if type(data) == str:
            if data in self.tags:
                self.tags.remove(data)
        elif type(data) == list:
            for item in data:
                if item in self.tags:
                    self.tags.remove(item)
        else:
            pass

        return self

    def show_tags(self):

        return self.tags

    def is_in_tags(self, data):

        return (data in self.tags)

    def __str__(self):

        return f'Note(text="{self.text}", tags={self.tags})'

    def __repr__(self):

        return f'Note(text="{self.text}", tags={self.tags})'


class Notes(UserDict):

    uid = 0

    def __init__(self, *args):

        super().__init__()

        for item in args:
            if not isinstance(item, Note):
                raise TypeError
            else:
                self.data.setdefault(self.uid, []).append(item)
                self.data[self.uid].append(datetime.now().strftime("%d-%m-%Y, %H:%M:%S"))
                self.data[self.uid].append(datetime.now().strftime("%d-%m-%Y, %H:%M:%S"))
                self.uid += 1

    def add_note(self, note):

        if not isinstance(note, Note):
            raise TypeError

        self.data.setdefault(self.uid, []).append(note)
        self.data[self.uid].append(datetime.now().strftime("%d-%m-%Y, %H:%M:%S"))
        self.data[self.uid].append(datetime.now().strftime("%d-%m-%Y, %H:%M:%S"))
        self.uid += 1

        return self

    def edit_note(self, uid, new_text="", new_tags=[]):

        if self.data.get(uid, None):

            if new_text:
                self.data[uid][0] = self.data[uid][0].edit_text(new_text)
                self.data[uid][2] = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")

            if new_tags:
                old_tags = self.data[uid][0].show_tags()
                tags_to_remove = []

                for tag in old_tags:
                    if tag in new_tags:
                        continue
                    else:
                       tags_to_remove.append(tag)

                self.data[uid][0] = self.data[uid][0].remove_tags(tags_to_remove)
                self.data[uid][0] = self.data[uid][0].add_tags(new_tags)

                self.data[uid][2] = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")

        return self

    def remove_note(self, uid):

        if self.data.get(uid, None):
            self.data.pop(uid)

        return self

    def show_note(self, uid):
        
        if self.data.get(uid, None):
            return [uid, *self.data[uid]]
        else:
            return None

    def show_all_notes(self):

        result = []

        for key in self.data.keys():
            result.append(self.show_note(key))

        return result

    def find_notes(self, find_str):

        if type(find_str) != str:
            raise TypeError

        result = []
        find_tag = False

        for key, value in self.data.items():
            note_text = value[0].show_text()
            note_tags = value[0].show_tags()

            for tag in note_tags:
                if tag.find(find_str) != -1:
                    result.append(self.show_note(key))
                    find_tag = True
                    break
            
            if find_tag:
                continue

            if note_text.find(find_str) != -1:
                result.append(self.show_note(key))

        return result

    def sort_notes(self, sort_by="text", revers=False):

        is_sorted = False

        proc_list = self.show_all_notes()

        if sort_by == "text":

            while not is_sorted:
                is_sorted = True
                for i in range(0, len(proc_list) - 1):
                    for j in range(i + 1, len(proc_list)):
                        if proc_list[i][1].show_text() > proc_list[j][1].show_text():
                            proc_list[i], proc_list[j] = proc_list[j], proc_list[i]
                            is_sorted = False

        elif sort_by == "tag":

            while not is_sorted:
                is_sorted = True
                for i in range(0, len(proc_list) - 1):
                    for j in range(i + 1, len(proc_list)):
                        if proc_list[i][1].show_tags()[0] > proc_list[j][1].show_tags()[0]:
                            proc_list[i], proc_list[j] = proc_list[j], proc_list[i]
                            is_sorted = False

        if revers:
            proc_list = proc_list[::-1]

        return proc_list                

    def save_to_file(self, filename):
        with open(filename, "wb") as file:
            pickle.dump(self, file)

    def load_from_file(self, filename):
        with open(filename, "rb") as file:
            content = pickle.load(file)

        return content

    def __repr__(self):

        out = ""

        for key, value in self.data.items():
            out += f'id={key}, {value[0]}, created={value[1]}, last_modified={value[2]}\n'

        return out


if __name__ == "__main__":
    pass