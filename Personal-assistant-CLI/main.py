from collections import UserDict
from datetime import datetime
import pickle
# from clean import main as clean


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


class Email(Field):
    def __init__(self, value):
        super().__init__(value)
        self.value = value


class Address(Field):
    def __init__(self, value):
        super().__init__(value)
        self.value = value


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


class Note(Field):
    def __init__(self, value, tags=None):
        super().__init__(value)
        self.tags = tags if tags else []

    def add_tag(self, tag):
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag):
        if tag in self.tags:
            self.tags.remove(tag)

    def search_tag(self, tag):
        return tag in self.tags

    def __str__(self):
        tags_info = f"Tags: {', '.join(self.tags)}" if self.tags else ""
        return f"Note: {self.value} ({tags_info})"


class Record:
    def __init__(self, name, birthday=None, note=None):
        self.name = Name(name)
        self.phones = []
        self.email = None
        self.address = None
        self.birthday = Birthday(birthday) if birthday else None
        self.note = Note(note) if note else None

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

    def add_email(self, email):
        if self.validate_email(email):
            self.email = Email(email)
        else:
            raise ValueError("Invalid email format")

    def edit_email(self, new_email):
        if self.validate_email(new_email):
            self.email.value = new_email
        else:
            raise ValueError("Invalid email format")

    @staticmethod
    def validate_email(email):
        return '@' in email

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

    def add_note_with_tags(self, note_value, tags=None):
        self.note = Note(note_value, tags)

    def add_tag_to_note(self, tag):
        if self.note:
            self.note.add_tag(tag)

    def remove_tag_from_note(self, tag):
        if self.note:
            self.note.remove_tag(tag)

    def search_by_tag(self, tag):
        return self.note and self.note.search_tag(tag)

    def add_address(self, address):
        self.address = Address(address)

    def edit_address(self, new_address):
        self.address.value = new_address

    def __str__(self):
        phones_info = '; '.join(p.value for p in self.phones)
        email_info = f", Email: {self.email}" if self.email else ""
        address_info = f", Address: {self.address}" if self.address else ""
        birthday_info = f", Birthday: {self.birthday.value}" if self.birthday else ""
        note_info = f", {self.note}" if self.note else ""

        return (f"Contact name: {self.name.value}, "
                f"phones: {phones_info}{email_info}{address_info}{birthday_info}{note_info}")


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

        keys_chunk = self._keys[self._index:self._index + self._chunk_size]
        records_chunk = [self.data[key] for key in keys_chunk]
        self._index += self._chunk_size
        return records_chunk

    def edit_contact(self, name, new_name=None, new_phones=None, new_email=None, new_address=None):
        record = self.find(name)
        if record:
            if new_name:
                record.name.value = new_name
            if new_phones:
                record.phones = [Phone(phone) for phone in new_phones if Phone.validate_phone(phone)]
            if new_email:
                record.add_email(new_email)
            if new_address:
                record.add_address(new_address)
            return f"Contact {name} edited successfully"
        else:
            return f"Contact {name} not found"

    def delete_contact(self, name):
        if name in self.data:
            del self.data[name]
            return f"Contact {name} deleted"
        else:
            return f"Contact {name} not found"

    def add_note_to_contact_with_tags(self, name, note_value, tags=None):
        record = self.find(name)
        if record:
            record.add_note_with_tags(note_value, tags)
            return f"Note added to contact {name} with tags {tags}"
        else:
            return f"Contact {name} not found"

    def add_tag_to_note_of_contact(self, name, tag):
        record = self.find(name)
        if record:
            record.add_tag_to_note(tag)
            return f"Tag {tag} added to note of contact {name}"
        else:
            return f"Contact {name} not found"

    def remove_tag_from_note_of_contact(self, name, tag):
        record = self.find(name)
        if record:
            record.remove_tag_from_note(tag)
            return f"Tag {tag} removed from note of contact {name}"
        else:
            return f"Contact {name} not found"

    def search_notes_by_tag(self, tag):
        results = []
        for record in self.data.values():
            if record.note and tag in record.note.tags:
                results.append(record)
        return results

    def sort_notes_by_tag(self, tag):
        sorted_records = sorted(
            filter(lambda r: r.note and tag in r.note.tags, self.data.values()),
            key=lambda r: r.note.tags.index(tag) if tag in r.note.tags else float('inf')
        )
        return sorted_records

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

    def upcoming_birthdays(self, days):
        today = datetime.now().date()
        upcoming_birthdays_list = []

        for record in self.data.values():
            if record.birthday:
                days_to_birthday = record.days_to_birthday()
                if 0 < days_to_birthday <= days:
                    upcoming_birthdays_list.append(record)

        return upcoming_birthdays_list

    def search(self, query):
        results = []
        for record in self.data.values():
            # Пошук за номером телефону
            for phone in record.phones:
                if query in phone.value:
                    results.append(record)
                    break

            # Пошук за ім'ям
            if query.lower() in record.name.value.lower() and record not in results:
                results.append(record)

            # Пошук за email
            if record.email and query in record.email.value and record not in results:
                results.append(record)

            # Пошук за адресою
            if record.address and query in record.address.value and record not in results:
                results.append(record)

            # Пошук за тегами в нотатці
            if record.note and any(tag in record.note.tags for tag in query.split()):
                results.append(record)

        return results

    @staticmethod
    def add_contact(name):
        record = Record(name)
        address_book.add_record(record)
        address_book.save_to_file("address_book.pkl")
        return f"Contact {name} added"

    @staticmethod
    def add_phone(name, phone):
        record = address_book.find(name)
        record.add_phone(phone)
        address_book.add_record(record)
        address_book.save_to_file("address_book.pkl")
        return f"Contact {name} Add phone:{phone}"

    @staticmethod
    def change_handler(name, new_number):
        record = address_book.find(name)
        if record:
            record.phones = []
            record.add_phone(new_number)
            address_book.save_to_file("address_book.pkl")
            return f"Change name:{name}, phone number:{new_number}"

    @staticmethod
    def phone_handler(name):
        record = address_book.find(name)
        if record:
            return f"Phone number: {record.phones[0].value}" if record.phones else f"No phone number for {name}"

    @staticmethod
    def add_email_handler(name, email):
        record = address_book.find(name)
        if record:
            try:
                record.add_email(email)
                address_book.save_to_file("address_book.pkl")
                return f"Email added to contact {name}"
            except ValueError as e:
                return f"Error: {e}"
        else:
            return f"Contact {name} not found"

    @staticmethod
    def add_address_handler(name, address):
        record = address_book.find(name)
        if record:
            record.add_address(address)
            address_book.save_to_file("address_book.pkl")
            return f"Address added to contact {name}"
        else:
            return f"Contact {name} not found"

    @staticmethod
    def print_contact_info(name):
        record = address_book.find(name)
        if record:
            print(record)
        else:
            print(f"Contact {name} not found")

    @staticmethod
    def load():
        address_book.load_from_file('address_book.pkl')
        return address_book


def main():

    while True:

        user_input = input(">>> ")
        user_input = user_input.lower()

        if user_input in ["good bye", "close", "exit"]:
            print("Good bye!")
            break
        elif user_input == "show all":
            print(address_book)
            continue
        elif user_input == "hello":
            print("How can I help you?")
            continue

        elif user_input.startswith("add"):
            _, command, *args = user_input.split(" ")
            if command == "contact":
                print(AddressBook.add_contact(*args))
            elif command == "phone":
                print(AddressBook.add_phone(*args))
            elif command == "email":
                print(AddressBook.add_email_handler(*args))
            elif command == "address":
                print(AddressBook.add_address_handler(*args))
            else:
                print("Invalid command")

        elif user_input.startswith("info"):
            _, name = user_input.split(" ", 1)
            AddressBook.print_contact_info(name)

        elif user_input.startswith("upcoming_birthdays"):
            _, days_str = user_input.split(" ", 1)
            try:
                days = int(days_str)
                upcoming_birthdays_list = address_book.upcoming_birthdays(days)
                print("Upcoming birthdays:")
                for record in upcoming_birthdays_list:
                    print(record)
            except ValueError:
                print("Invalid number of days")

        elif user_input.startswith("search"):
            _, query = user_input.split(" ", 1)
            search_results = address_book.search(query)
            if search_results:
                print("Search results:")
                for record in search_results:
                    print(record)
            else:
                print("No matching contacts found.")

        elif user_input.startswith("edit"):
            _, name, *edit_params = user_input.split(" ")
            print(AddressBook.edit_contact(name, *edit_params))

        elif user_input.startswith("delete"):
            _, name = user_input.split(" ")
            print(AddressBook.delete_contact(name))


address_book = AddressBook()


if __name__ == "__main__":
    main()

