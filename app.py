"""app.py — главное окно приложения «Записная книжка контактов»."""

import tkinter as tk
from tkinter import messagebox

from contacts_logic import ContactBook
from dialogs import AboutDialog, ContactDialog


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Записная книжка контактов")
        self.root.geometry("480x460")

        self.book = ContactBook()
        self.about_window = None

        self._build_ui()
        self._bind_events()
        self.book.add("Иванов Иван", "+7 916 123-45-67", "ivanov@mail.ru")
        self.book.add("Петрова Анна", "+7 903 555-11-22", "")
        self.refresh_list()

    def _build_ui(self):
        self.listbox = tk.Listbox(self.root)
        self.listbox.pack(fill="both", expand=True, padx=20, pady=10)

        buttons = tk.Frame(self.root)
        buttons.pack(fill="x", padx=20, pady=10)
        self.add_button = tk.Button(buttons, text="Добавить")
        self.add_button.pack(side="left")
        self.edit_button = tk.Button(buttons, text="Изменить")
        self.edit_button.pack(side="left", padx=6)
        self.delete_button = tk.Button(buttons, text="Удалить")
        self.delete_button.pack(side="left")
        self.about_button = tk.Button(buttons, text="О программе")
        self.about_button.pack(side="right")

    def _bind_events(self):
        self.add_button.config(command=self.on_add_click)
        self.edit_button.config(command=self.on_edit_click)
        self.delete_button.config(command=self.on_delete_click)
        self.about_button.config(command=self.on_about_click)
        self.listbox.bind("<Double-Button-1>", self.on_edit_click)

    def on_add_click(self, event=None):
        dialog = ContactDialog(self.root, title="Новый контакт")
        if dialog.result is not None:
            self.book.add(**dialog.result)
            self.refresh_list()

    def on_edit_click(self, event=None):
        index = self._selected_index()
        if index is None:
            messagebox.showinfo("Редактирование", "Выберите контакт в списке")
            return
        contact = self.book.get(index)
        dialog = ContactDialog(self.root, title="Изменить контакт",
                               contact=contact)
        if dialog.result is not None:
            self.book.update(index, **dialog.result)
            self.refresh_list()

    def on_delete_click(self):
        index = self._selected_index()
        if index is None:
            messagebox.showinfo("Удаление", "Выберите контакт в списке")
            return
        contact = self.book.get(index)
        question = f"Удалить контакт «{contact['name']}»?"
        if messagebox.askyesno("Удаление", question):
            self.book.delete(index)
            self.refresh_list()

    def on_about_click(self):
        if self.about_window is not None and self.about_window.winfo_exists():
            self.about_window.lift()
            self.about_window.focus_set()
            return
        self.about_window = AboutDialog(self.root)

    def _selected_index(self):
        selection = self.listbox.curselection()
        return selection[0] if selection else None

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for contact in self.book.all():
            label = f"{contact['name']}   —   {contact['phone']}"
            self.listbox.insert(tk.END, label)


def main():
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()