import re

PHONE_PATTERN = re.compile(r"^\+?\d[\d\-\s\(\)]{5,14}\d$")
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate_contact(name, phone, email):
    """Проверяет корректность данных контакта.
    Возвращает список сообщений об ошибках.
    Пустой список означает, что данные верны.
    """
    errors = []
    name = name.strip()
    phone = phone.strip()
    email = email.strip()

    if not name:
        errors.append("Укажите имя контакта")
    elif len(name) < 2:
        errors.append("Имя слишком короткое (менее 2 символов)")

    if not phone:
        errors.append("Укажите номер телефона")
    elif not PHONE_PATTERN.match(phone):
        errors.append("Телефон указан в неверном формате")

    if email and not EMAIL_PATTERN.match(email):
        errors.append("E-mail указан в неверном формате")

    return errors


class ContactBook:
    """Хранилище контактов с операциями добавления, изменения и удаления."""

    def __init__(self):
        self._contacts = []

    def add(self, name, phone, email=""):
        errors = validate_contact(name, phone, email)
        if errors:
            raise ValueError("; ".join(errors))
        contact = {
            "name": name.strip(),
            "phone": phone.strip(),
            "email": email.strip(),
        }
        self._contacts.append(contact)
        return contact

    def update(self, index, name, phone, email=""):
        self._check_index(index)
        errors = validate_contact(name, phone, email)
        if errors:
            raise ValueError("; ".join(errors))
        self._contacts[index] = {
            "name": name.strip(),
            "phone": phone.strip(),
            "email": email.strip(),
        }
        return self._contacts[index]

    def delete(self, index):
        self._check_index(index)
        return self._contacts.pop(index)
    
    def get(self, index):
        self.check_index(index)
        return self._contacts[index]
    
    def all(self):
        return list(self._contacts)
    
    def find_by_name(self, query):
        query = query.strip().lower()
        if not query:
            return self.all()
        return [c for c in self._contacts if query in c["name"].lower()]
    
    def check_index(self, index):
        if not 0 <= index < len(self._contacts):
            raise IndexError("Контакт с таким номером не найден")
    
    def __len__(self):
        return len(self._contacts)