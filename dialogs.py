import tkinter as tk
from contacts_logic import validate_contact

ACCENT = "#2F678C"


def center_over_parent(window, parent):
    """Располагает окно window по центру относительно окна parent."""
    window.update_idletasks()
    px, py = parent.winfo_rootx(), parent.winfo_rooty()
    pw, ph = parent.winfo_width(), parent.winfo_height()
    w, h = window.winfo_width(), window.winfo_height()
    x = px + (pw - w) // 2
    y = py + (ph - h) // 2
    window.geometry(f"+{max(x, 0)}+{max(y, 0)}")


class ContactDialog(tk.Toplevel):
    """Модальное окно добавления или редактирования контакта.

    Результат сохраняется в self.result: словарь с данными
    при нажатии «Сохранить» или None при отмене.
    """

    def __init__(self, parent, title="Новый контакт", contact=None):
        super().__init__(parent)
        self.title(title)
        self.resizable(False, False)
        self.result = None

        contact = contact or {"name": "", "phone": "", "email": ""}
        self.name_var = tk.StringVar(value=contact["name"])
        self.phone_var = tk.StringVar(value=contact["phone"])
        self.email_var = tk.StringVar(value=contact["email"])

        self._build_ui()          # создание полей формы (см. приложение А)
        self._bind_events()

        # --- Делаем окно модальным ---
        self.transient(parent)
        center_over_parent(self, parent)
        self.grab_set()
        self.name_entry.focus_set()
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.wait_window(self)     # <-- блокирует код, открывший диалог

    def _bind_events(self):
        self.save_button.config(command=self.on_save)
        self.cancel_button.config(command=self.on_cancel)
        self.bind("<Return>", lambda event: self.on_save())
        self.bind("<Escape>", lambda event: self.on_cancel())

    def on_save(self):
        name = self.name_var.get()
        phone = self.phone_var.get()
        email = self.email_var.get()
        errors = validate_contact(name, phone, email)
        if errors:
            self.error_label.config(text="; ".join(errors))
            return
        self.result = {
            "name": name.strip(),
            "phone": phone.strip(),
            "email": email.strip(),
        }
        self.destroy()

    def on_cancel(self):
        self.result = None
        self.destroy()
    
    def _build_ui(self):
        form = tk.Frame(self, padx=20, pady=18)
        form.pack(fill="both", expand=True)

        tk.Label(form, text=self.title(), font=("Segoe UI Semibold", 13)
                 ).grid(row=0, column=0, columnspan=2,
                        sticky="w", pady=(0, 12))

        tk.Label(form, text="Имя").grid(row=1, column=0, sticky="w", pady=4)
        self.name_entry = tk.Entry(form, textvariable=self.name_var, width=26)
        self.name_entry.grid(row=1, column=1, pady=4)

        tk.Label(form, text="Телефон").grid(
            row=2, column=0, sticky="w", pady=4)
        self.phone_entry = tk.Entry(
            form, textvariable=self.phone_var, width=26)
        self.phone_entry.grid(row=2, column=1, pady=4)

        tk.Label(form, text="E-mail").grid(
            row=3, column=0, sticky="w", pady=4)
        self.email_entry = tk.Entry(
            form, textvariable=self.email_var, width=26)
        self.email_entry.grid(row=3, column=1, pady=4)

        self.error_label = tk.Label(form, text="", fg="#C82E3E",
                                    wraplength=260, justify="left")
        self.error_label.grid(row=4, column=0, columnspan=2,
                              sticky="w", pady=(6, 0))

        buttons = tk.Frame(form)
        buttons.grid(row=5, column=0, columnspan=2, sticky="e", pady=(14, 0))
        self.cancel_button = tk.Button(buttons, text="Отмена")
        self.cancel_button.pack(side="left", padx=(0, 8))
        self.save_button = tk.Button(buttons, text="Сохранить",
                                     bg=ACCENT, fg="white")
        self.save_button.pack(side="left")


class AboutDialog(tk.Toplevel):
    """Немодальное информационное окно «О программе»."""

    def __init__(self, parent):
        super().__init__(parent)
        self.title("О программе")
        self.resizable(False, False)

        frame = tk.Frame(self, padx=24, pady=20)
        frame.pack()
        tk.Label(frame, text="Записная книжка контактов",
                 font=("Segoe UI Semibold", 13)).pack(anchor="w")
        tk.Label(frame,
                 text="Учебное приложение · ОП.03 · ПР № 4").pack(anchor="w")
        tk.Button(frame, text="Закрыть",
                  command=self.destroy).pack(anchor="e", pady=(16, 0))

        # Модальность НЕ включаем: transient() и grab_set() отсутствуют
        center_over_parent(self, parent)
