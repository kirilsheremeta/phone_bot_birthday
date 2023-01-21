from collections import UserDict
from datetime import datetime


class BirthdayTypeError(Exception):

    """ Exception when birthday date has an invalid input format"""


class PhoneLengthError(Exception):

    """ Exception when the phone number has wrong length """


class PhoneTypeError(Exception):

    """ Exception when the phone number has letters """


class AddressBook(UserDict):

    """ Create user's addressbook """

    def add_record(self, record):
        self.data[record.name.value] = record

    def delete_record(self, record):
        self.data.pop(record.name.value, None)

    def show_record(self, name):
        return f"Name: {name} (Birthday: {self.data[name].birthday}); Phone: {', '.join([str(phone.value) for phone in self.data[name].phones])}"

    def show_all_records(self):
        return "\n".join(f"Name: {rec.name} (Birthday: {rec.birthday}); Phone: {', '.join([p.value for p in rec.phones])}" for rec in self.data.values())

    def change_record(self, name_user, old_number, new_number):
        record = self.data.get(name_user)
        if record:
            record.change(old_number, new_number)

    def iterator(self, n):
        records = list(self.data.keys())
        records_num = len(records)
        count = 0
        result = ""
        if n > records_num:
            n = records_num
        for rec in self.data.values():
            if count < n:
                result += f"Name: {rec.name} (Birthday: {rec.birthday}); {', '.join([p.value for p in rec.phones])}\n"
                count += 1
        yield result


class Birthday:

    """ Class to create a birthday tab """

    @staticmethod
    def date_standard(day, month, year):
        try:
            birthday = datetime.strptime(
                str(day, month, year), "%d.%m.%Y").date()
        except ValueError:
            raise BirthdayTypeError(
                "Enter birthday date in format dd.mm.yyyy")
        else:
            return str(birthday.date())

    def __init__(self, day, month, year):
        self.__birthday = self.date_standard(day, month, year)

    def __str__(self):
        return str(self.__birthday)

    def __repr__(self):
        return str(self.__birthday)

    @property
    def birthday(self):
        return self.__birthday

    @birthday.setter
    def birthday(self, year, month, day):
        self.__birthday = self.date_standard(day, month, year)


class Field:
    def __init__(self, value):
        self.__value = value

    def __eq__(self, __o: object):
        if self.value == __o.value:
            return True
        return False

    def __str__(self):
        return self.__value

    def __repr__(self):
        return self.__value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Name(Field):
    def __str__(self):
        return str(self.__value)

    def __repr__(self):
        return str(self.__value)

    @Field.value.setter
    def value(self, value):
        self.__value = value


class Phone(Field):

    """ Phone numbers standardization """

    @staticmethod
    def number_standard(phone):
        new_number = (
            str(phone).strip()
            .removeprefix("+")
            .replace(" ", "")
            .replace("-", "")
            .replace("(", "")
            .replace(")", "")
        )

        try:
            new_number = [str(int(i)) for i in new_number]
        except ValueError:
            raise PhoneTypeError(
                "Incorrect number entered. Check it and try again")

        else:
            new_number = "".join(new_number)
            if len(new_number) == 12:
                return f"+{new_number}"
            elif len(new_number) > 12:
                raise PhoneLengthError("Phone number is too long. Try again")
            elif len(new_number) == 10:
                return f"+38{new_number}"
            else:
                raise PhoneLengthError("Phone number is too short. Try again")

    def __init__(self, value):
        super().__init__(value)
        self.__value = Phone.number_standard(value)

    def __str__(self):
        return str(self.__value)

    def __repr__(self):
        return str(self.__value)

    @Field.value.setter
    def value(self, value):
        self.__value = Phone.number_standard(value)

    @property
    def value(self):
        return self.__value


class Record:

    """ Class to create and edit contacts """

    def __init__(self, name, phone=None, birthday=None):
        self.name = name
        self.phone = Phone(phone)
        self.phones = []
        if isinstance(phone, Phone):
            self.phones.append(phone)
        if isinstance(birthday, Birthday):
            self.birthday = birthday
        else:
            self.birthday = None

    def __str__(self) -> str:
        return f'Name: {self.name} Phone: {", ".join([str(p) for p in self.phones])} {"Birthday: " + str(self.birthday) if self.birthday else ""}'

    def __repr__(self) -> str:
        return str(self)

    def add_phone(self, new_number):
        if new_number not in self.phones:
            self.phones.append(new_number)
            return f"Phone number {new_number} created"
        elif new_number in self.phones:
            self.phones.append(new_number)
            return f"Phone number {new_number} added"
        else:
            return f"Something went wrong. Please try again"

    def edit_phone(self, old_number, new_number):
        if old_number in self.phones:
            self.phones.remove(old_number)
            self.phones.append(new_number)
            return f"Old number {old_number} successfully changed to new number {new_number}"
        else:
            return f"Phone number {old_number} is not found. Please try again"

    def remove_phone(self, old_number):
        if old_number in self.phones:
            self.phones.remove(old_number)
            return f"Phone number {old_number} has been deleted"
        else:
            return f"Phone number {old_number} is not found. Please try again"

    def add_birthday(self, day, month, year):
        self.birthday = Birthday.date_standard(int(year), int(month), int(day))

    def days_to_birthday(self):
        birthday = self.birthday.value
        today = datetime.now().date()
        current_year = datetime.year
        if self.birthday:
            current_year_birthday = datetime(
                current_year, birthday.month, birthday.day).date
            delta = current_year_birthday - today
            if delta >= 0:
                return f"{self.name}'s birthday will be in {delta} days"
            else:
                next_year_birthday = datetime(
                    current_year + 1, birthday.month, birthday.day).date()
                delta = next_year_birthday - today
                return f"{self.name}'s birthday will be in {delta} days"
        else:
            return f"{self.name} don't have a birthday date"

    def get_contact(self):
        phones = ", ".join([str(p) for p in self.phones])
        return {
            "Name": str(self.name.value),
            "Phone": phones,
            "Birthday": self.birthday
        }
