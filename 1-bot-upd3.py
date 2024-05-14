from datetime import datetime
import re
from collections import UserDict

# Field: Базовий клас для полів запису
class Field: 
    # Ініціалізація класу
    def __init__(self, value):
        self.value = value
    # Код форматування об"єкта як рядка
    def __str__(self):
        return str(self.value)

# Name: Клас для зберігання імені контакту. Обов'язкове поле.
class Name(Field):
    def __init__(self, value):
        # Виклик конструктора базового класу Field
        super().__init__(value)

# Phone: Клас для зберігання номера телефону. Має валідацію формату (10 цифр).
class Phone(Field):
    def __init__(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Номер телефону має складатись з 10 цифр", {value})
        # Виклик конструктора базового класу Field
        super().__init__(value)

# Створенню класу Birthday з можливістю додавання поля для дня народження до контакту
class Birthday(Field):
    def __init__(self, value):
        try:
            # Додайте перевірку коректності даних та перетворіть рядок на об'єкт datetime - просто дату
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

# Record: Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів.
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        # Додаємо новий номер в кінець списку через виклик класу Phone
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        # Ітеруємо список телефонів та перезаписуємо у список ті, що не співпадають із вказаним
        new_phones = []
        for p in self.phones:
            if str(p) != phone:
                new_phones.append(p)
        self.phones = new_phones

    def edit_phone(self, old_phone, new_phone):
        # Пошук записів з відповідним телефоном та заміна на новий
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone

    def find_phone(self, phone):
        # Перебираємо всі номери контакту і повертаємо чи знаходимо вказаний
        for p in self.phones:
            if str(p) == phone:
                return p
        return f"Немає номера {phone}"

    def add_birthday(self, birthday):
        # Перевірка, що день народження ще не встановлено
        if self.birthday is None:
            self.birthday = Birthday(birthday)
        else:
            raise ValueError("Контакт вже містить день народження")

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"

# AddressBook: Клас для зберігання та управління записами.
class AddressBook(UserDict):
    def add_record(self, record):
        # У словник data для зберігання вмісту класу UserDict записуємо значення по імені контакту
        contact_name = record.name.value
        self.data[contact_name] = record
#       return print(f"[contact_name] == {contact_name}, record == {record}")
        
    def find(self, name):
        # Повертаємо значення із словника data UserDict за ключем - ім"я
        return self.data.get(name)

    def delete(self, name):
        # Видалення запису із словника по ключу/імені
        if name in self.data:
            del self.data[name]
            return print(f"Видалено запис по ключу/імені {name}")
        else:
            return print(f"Не знайдено ключ/імя на видалення")

    def get_upcoming_birthdays(self):
        # Визначте поточну дату системи за допомогою datetime.today().date().
        today = datetime.today().date()
        # Список для зберігання інформації про привітання
        upcoming_birthdays = []
        # Пройдіться по record та аналізуйте дати народження кожного користувача (for record in values).
        for record in self.data.values():
            # Конвертуйте дату народження із рядка у datetime об'єкт - datetime.strptime(value, "%Y.%m.%d").date(). 
            # Оскільки потрібна лише дата (без часу), використовуйте .date() для отримання тільки дати.
            if record.birthday is not None:
                birthday = record.birthday.value
                # Визначення дати наступного дня народження
                next_birthday = birthday.replace(year=today.year)
                if next_birthday < today:
                    next_birthday = next_birthday.replace(year=today.year + 1)
                # Перевірка, чи день народження припадає на вихідний
                while next_birthday.weekday() >= 5: # 5 і 6 - субота і неділя
                    next_birthday += timedelta(days=1) # Переносимо наступний день на понеділок
                # Якщо наступне день народження у поточному тижні, додаємо до списку привітань
                if 1 <= (next_birthday - today).days <= 7:
                    upcoming_birthdays.append({
                        "name": record.name.value,
                        "congratulation_date": next_birthday.strftime("%d.%m.%Y")
                    })
        return upcoming_birthdays  


# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання дня народження
john_record.add_birthday("20.05.1990")

# Перевірка видалення номера у контакта
#john_record.remove_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
jane_record.add_birthday("22.05.1990")
book.add_record(jane_record)

# Створення та додавання нового запису для Lary
lary_record = Record("Lary")
lary_record.add_phone("7777777777")
lary_record.add_birthday("21.05.2000")
book.add_record(lary_record)

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# Видалення запису Jane
book.delete("Jane")

# Отримання списку днів народження на наступний тиждень
upcoming_birthdays = book.get_upcoming_birthdays()
if upcoming_birthdays:
    print("Протягом тижня ДН у:")
    for birthday in upcoming_birthdays:
        print(f"- {birthday['name']}: {birthday['congratulation_date']}")
else:
    print("Протягом тижня ДН відсутні")