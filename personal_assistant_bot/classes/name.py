try:
   from classes.field import Field
except ModuleNotFoundError:
   from personal_assistant_bot.classes.field import Field


class Name(Field):
    pass
