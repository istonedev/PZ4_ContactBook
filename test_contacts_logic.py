import unittest
from contacts_logic import ContactBook, validate_contact


class TestValidateContact(unittest.TestCase):
    def test_valid_contact_has_no_errors(self):
        errors = validate_contact(
            "Иванов Иван", "+7 916 123-45-67", "ivanov@mail.ru")
        self.assertEqual(errors, [])
    
    def test_empty_name_is_error(self):
        errors = validate_contact("", "+7 916 123-45-67", "")
        self.assertIn("Укажите имя контакта", errors)

    def test_invalid_email_is_error(self):
        errors = validate_contact(
            "Иванов Иван", "+7 916 123-45-67", "не-email")
        self.assertTrue(any("E-mail" in e for e in errors))


class TestContactBookUpdateDelete(unittest.TestCase):

    def setUp(self):
        self.book = ContactBook()
        self.book.add("Иванов Иван", "+7 916 123-45-67")
        self.book.add("Петрова Анна", "+7 903 555-11-22")

    def test_update_changes_contact(self):
        self.book.update(0, "Иванов Пётр", "+7 916 000-00-00")
        self.assertEqual(self.book.get(0)["name"], "Иванов Пётр")

    def test_delete_removes_contact(self):
        self.book.delete(index)
        self.assertEqual(len(self.book), 1)

    def test_update_invalid_index_raises_error(self):
        with self.assertRaises(IndexError):
            self.book.update(99, "Имя", "+7 916 123-45-67")


if __name__ == "__main__":
    unittest.main(verbosity=2)