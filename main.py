from collections import UserDict
from datetime import datetime
import pickle
from clean import main as clean

class Field:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    def __str__(self):
        return str(self._value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.value = value

    @Field.value.setter
    def value(self, new_value):
        if not self.validate_phone(new_value):
            raise ValueError("Invalid phone number format")
        self._value = new_value

    @staticmethod
    def validate_phone(phone):
        return len(phone) == 10 and phone.isdigit()


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        if Phone.validate_phone(phone):
            new_phone = Phone(phone)
            self.phones.append(new_phone)
        else:
            raise ValueError("Invalid phone number format")

    def edit_phone(self, old_phone, new_phone):
        if not Phone.validate_phone(new_phone):
            raise ValueError("Invalid phone number format")

        phone_found = False
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                phone_found = True
                break

        if phone_found:
            return f"Phone number {old_phone} edited to {new_phone}"
        else:
            raise ValueError(f"Phone number {old_phone} not found")

    def find_phone(self, phone):
        for phone_number in self.phones:
            if phone_number.value == phone:
                return phone_number
        return None

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]
        return "Phone number {phone} removed"

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now().date()
            birthday_date = datetime.strptime(self.birthday.value, '%Y-%m-%d').date().replace(year=today.year)

            if birthday_date < today:
                birthday_date = birthday_date.replace(year=today.year + 1)

            days_left = (birthday_date - today).days
            return days_left
        else:
            return None

    def __str__(self):
        birthday_info = f", Birthday: {self.birthday.value}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}{birthday_info}"


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        self.value = value

    @Field.value.setter
    def value(self, new_value):
        try:
            datetime.strptime(new_value, "%Y-%m-%d")
            self._value = new_value
        except ValueError:
            raise ValueError("Invalid birthday format. Use 'YYYY-MM-DD'.")

    def __str__(self):
        return f"Birthday: {self.value}"


class AddressBook(UserDict):

    def __iter__(self, chunk_size=1):
        self._chunk_size = chunk_size
        self._keys = list(self.data.keys())
        self._index = 0
        return self

    def __next__(self):
        if self._index >= len(self._keys):
            raise StopIteration

        keys_chunk = self._keys[self._index:self._index+self._chunk_size]
        records_chunk = [self.data[key] for key in keys_chunk]
        self._index += self._chunk_size
        return records_chunk

    def add_record(self, record):
        self.data[record.name.value] = record

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return f"Contact {name} deleted"
        else:
            return f"Contact {name} not found"

    def find(self, name):
        return self.data.get(name, None)

    def save_to_file(self, file_name):
        with open(file_name, "wb") as file:
            pickle.dump(self.data, file)

    def load_from_file(self, file_name):
        try:
            with open(file_name, "rb") as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            print("File not found")
        except Exception as e:
            print(f"Error when downloading data from a file: {e}")

    def search(self, query):
        results = []
        for record in self.data.values():
            for phone in record.phones:
                if query in phone.value:
                    results.append(record)
                    break

        for record in self.data.values():
            if query.lower() in record.name.value.lower():
                if record not in results:
                    results.append(record)

        return results

class Clean():
    def sort_folder(self, file_path):
        clean(file_path)