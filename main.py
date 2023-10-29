import tkinter as tk
from tkinter import ttk
import sqlite3


class MainWindow(tk.Frame):
    """
    Класс главного окна
    """

    def __init__(self, root):
        super().__init__(root)
        self.root_win = root
        self.db = db
        self.init_window()

    def init_window(self):
        """
        Рисует элементы основного окна
        """
        toolbar = tk.Frame(bg='#d7d7d7', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # кнопка добавления нового сотрудника
        self.img_add = tk.PhotoImage(file='./img/add.png')
        btn_add = tk.Button(toolbar, text='Добавить', bg='#c7c7c7', bd=2, image=self.img_add,
                            command=self.open_add_employee_form)
        btn_add.pack(side=tk.LEFT)

        # кнопка редактирования сотрудника
        self.img_edit = tk.PhotoImage(file='./img/edit.png')
        btn_edit = tk.Button(toolbar, text='Редактировать', bg='#c7c7c7', bd=2, image=self.img_edit,
                             command=self.open_edit_employee_form)
        btn_edit.pack(side=tk.LEFT)

        # кнопка удаления сотрудника
        self.img_delete = tk.PhotoImage(file='./img/delete.png')
        btn_delete = tk.Button(toolbar, text='Удалить', bg='#c7c7c7', bd=2, image=self.img_delete,
                               command=self.delete_employee)
        btn_delete.pack(side=tk.LEFT)

        # поиск
        self.entry_fio_search = tk.Entry(toolbar)
        self.entry_fio_search.pack(side=tk.LEFT)
        btn_search = tk.Button(toolbar, text='Найти', bg='#c7c7c7', bd=2, command=self.search_employee)
        btn_search.pack(side=tk.LEFT)

        # таблица сотрудников
        self.employee_table = ttk.Treeview(self.root_win,
                                           columns=('id', 'fio', 'phone', 'email', 'salary'),
                                           height=45,
                                           show='headings')

        self.employee_table.column('id', width=47)
        self.employee_table.column('fio', width=300)
        self.employee_table.column('phone', width=150)
        self.employee_table.column('email', width=200)
        self.employee_table.column('salary', width=100)

        self.employee_table.heading('id', text='id')
        self.employee_table.heading('fio', text='ФИО')
        self.employee_table.heading('phone', text='Телефон')
        self.employee_table.heading('email', text='E-Mail')
        self.employee_table.heading('salary', text='Зарплата')
        self.employee_table.pack(side=tk.LEFT)

        self.show_records()

    def open_add_employee_form(self):
        """
        Открывает форму добавления нового сотрудника
        """
        EmployeeForm(self.root_win)

    def save_employee(self, fio, phone, email, salary):
        """
        Сохраняет данные формы в базу данных
        """
        self.db.insert_record(fio, phone, email, salary)
        self.show_records()

    def show_records(self):
        self.db.cur.execute('SELECT * FROM employees')
        [self.employee_table.delete(i) for i in self.employee_table.get_children()]
        [self.employee_table.insert('', 'end', values=i) for i in self.db.cur.fetchall()]

    def open_edit_employee_form(self):
        """
        Открывает форму редактирования сотрудника
        """
        sel = self.employee_table.item(self.employee_table.focus())
        values = sel.get('values')
        EmployeeForm(self.root_win, values[0], values[1], values[2], values[3], values[4])

    def update_employee(self, id, fio, phone, email, salary):
        """
        обновляет данные в БД
        """
        self.db.update_record(id, fio, phone, email, salary)
        self.show_records()

    def delete_employee(self):
        """
        Удаляет сотрудника
        """
        sel = self.employee_table.item(self.employee_table.focus())
        values = sel.get('values')
        self.db.delete_record(values[0])
        self.show_records()

    def search_employee(self):
        """
        Поиск сотрудника по ФИО
        """
        txt = self.entry_fio_search.get()
        if txt != "":
            for i in self.employee_table.get_children():
                if txt.lower() in self.employee_table.item(i).get('values')[1].lower():
                    self.employee_table.selection_set(i)


class EmployeeForm(tk.Toplevel):
    """
    Класс дочернего окна с данными сотрудника
    """

    def __init__(self, root, eid=None, fio='', phone='', email='', salary=''):
        super().__init__(root)
        self.init_window()
        self.view = app
        self.id = eid
        self.fio_var.set(fio)
        self.phone_var.set(phone)
        self.email_var.set(email)
        self.salary_var.set(salary)

    def init_window(self):
        self.title('Добавление сотрудника')
        self.geometry('400x200')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        label_fio = tk.Label(self, text='ФИО:')
        label_fio.place(x=50, y=20)
        label_phone = tk.Label(self, text='Телефон:')
        label_phone.place(x=50, y=50)
        label_email = tk.Label(self, text='E-Mail:')
        label_email.place(x=50, y=80)
        label_salary = tk.Label(self, text='Salary:')
        label_salary.place(x=50, y=110)

        self.fio_var = tk.StringVar()
        self.entry_fio = tk.Entry(self, textvariable=self.fio_var)
        self.entry_fio.place(x=150, y=20)

        self.phone_var = tk.StringVar()
        self.entry_phone = tk.Entry(self, textvariable=self.phone_var)
        self.entry_phone.place(x=150, y=50)

        self.email_var = tk.StringVar()
        self.entry_email = tk.Entry(self, textvariable=self.email_var)
        self.entry_email.place(x=150, y=80)

        self.salary_var = tk.StringVar()
        self.entry_salary = tk.Entry(self, textvariable=self.salary_var)
        self.entry_salary.place(x=150, y=110)

        btn_cancel = tk.Button(self, text='Отмена', command=self.destroy)
        btn_cancel.place(x=245, y=155)

        btn_add = tk.Button(self, text='Сохранить', command=self.save_form)
        btn_add.place(x=310, y=155)

    def save_form(self):
        if self.id is None:
            self.view.save_employee(self.entry_fio.get(),
                                    self.entry_phone.get(),
                                    self.entry_email.get(),
                                    self.entry_salary.get())
        else:
            self.view.update_employee(self.id,
                                      self.entry_fio.get(),
                                      self.entry_phone.get(),
                                      self.entry_email.get(),
                                      self.entry_salary.get())
        self.destroy()


class Db:
    """
    Класс базы данных
    """

    def __init__(self):
        self.conn = sqlite3.connect('company.db')
        self.cur = self.conn.cursor()
        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fio TEXT,
            phone TEXT,
            email TEXT,
            salary TEXT
        )
        ''')
        self.conn.commit()

    def insert_record(self, fio, phone, email, salary):
        self.cur.execute('''
        INSERT INTO employees (fio, phone, email, salary)
        VALUES(?,?,?,?) 
        ''', (fio, phone, email, salary))
        self.conn.commit()

    def update_record(self, id, fio, phone, email, salary):
        self.cur.execute(
            f"UPDATE employees SET fio='{fio}', phone='{phone}', email='{email}', salary='{salary}' WHERE id={id} ")
        self.conn.commit()

    def delete_record(self, id):
        self.cur.execute(
            f"DELETE FROM employees WHERE id={id} ")
        self.conn.commit()

# Запускаем программу
if __name__ == '__main__':
    root = tk.Tk()
    db = Db()
    app = MainWindow(root)
    root.title('Сотрудники компании')
    root.geometry('800x600')
    root.resizable(False, False)
    root.mainloop()
