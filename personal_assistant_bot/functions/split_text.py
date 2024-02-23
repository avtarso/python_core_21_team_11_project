import sys
sys.path.append('..')

from settings.settings import NOTE_LEN


def split_text(text: str) -> list:

    result = []

    while len(text) > NOTE_LEN:
        result.append(text[0:NOTE_LEN])
        text = text[NOTE_LEN:]
    result.append(text)

    return result