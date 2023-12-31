import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import sqlite3

class EmployeeManagmentApp:
    def __init__(self, master):
        self.master = master
        self.master.title('Employee Managment App')
        self.conn = sqlite3.connect('employees.db')
        self.create_table()
        self.tree = ttk.Treeview(master)
        self.tree["columns"] = ('ID', 'Name', 'Phone', 'Email', 'Salary')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="name")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Salary", text="salary")
        self.tree.pack(padx = 20, pady = 20)

        self.create_widgets()
        self.update_treeview()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees 
            (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name text,
            email text, 
            phone text
            salary INTEGER
            )
        ''')
        self.conn.commit()

    def create_widgets(self):
        self.add_button = tk.Button(self.master, text="Add Employee", command=self.add_employee)
        self.add_button.pack(pady = 10)
        self.update_button = tk.Button(self.master, text="Update Employee", command=self.update_employee)
        self.update_button.pack(pady = 10)
        self.delite_button = tk.Button(self.master, text="Delite Employee", command=self.delite_employee)
        self.delite_button.pack(pady=10)
        self.search_button = tk.Button(self.master, text="Search Employee", command=self.search_employee)
        self.search_button.pack(pady=10)
        self.undo_button = tk.Button(self.master, text="Undo Employee", command=self.undo_employee)
        self.undo_button.pack(pady=10)

        self.tree.bind("<Double-1>", self.on_double_click)

        self.last_action = None

    def add_employee(self):
        name = simpledialog.askstring('Input', 'Enter Employee name: ')
        phone = simpledialog.askstring('Input', 'Enter Employee phone: ')
        Email = simpledialog.askstring('Input', 'Enter Employee Email: ')
        salary = simpledialog.askstring('Input', 'Enter Employee salary: ')

        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO employees (name, phone, email, salary) VALUES (?, ?, ?, ?)',
                       (name, phone, Email, salary, ))
        self.conn.commit()
        self.update_treeview()
        self.last_action = 'add'

    def update_employee(self):
        emp_id = simpledialog.askstring('Input', 'Enter Employee ID: ')
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM employees WHERE id=?',
                       (emp_id))
        employee = cursor.fetchone()

        if employee:
            name = simpledialog.askstring('Input', 'Enter updated Employee name: ',
                                          initialvalue=employee[1])
            phone = simpledialog.askstring('Input', 'Enter updated Employee phone: ',
                                           initialvalue=employee[2])
            Email = simpledialog.askstring('Input', 'Enter updated Employee Email: ',
                                           initialvalue=employee[3])
            salary = simpledialog.askstring('Input', 'Enter updated Employee salary: ',
                                            initialvalue=employee[4])
            cursor.execute('UPDATE employees SET name=?, phone=?, Email=?, salary=?, WHERE emp_id',
                           (name, phone, Email, salary, emp_id))
            self.conn.commit()
            self.update_treeview()
            self.last_action = 'update'
        else:
            messagebox.showerror("Error", 'Employee nor found(((')

    def delite_employee(self):
        emp_id = simpledialog.askstring('Input', 'Enter Employee ID: ')
        cursor = self.conn.cursor()
        cursor.execute('DELITE FROM employees WHERE id=?',
                       (emp_id))
        self.conn.commit()
        self.update_treeview()
        self.last_action = 'delite'

    def search_employee(self):
        name = simpledialog.askstring('Input', 'Enter Employee name: ')
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM employees WHERE name=?',
                       (name))
        employees = cursor.fetchone()
        if employees:
            self.tree.delete(*self.tree.get_children())
            for employee in employees:
                self.tree.insert("", "end", values=employee)
        else:
            messagebox.showinfo("Info", 'No employee found with given name.')
    def update_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete()
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM employees')
        employees = cursor.fetchall()
        for employee in employees:
            self.tree.insert("", "end", values=employee)
    def on_double_click(self, event):
        item = self.tree.selection()[0]
        employee_id = self.tree.item(item, 'values')[0]
        messagebox.showinfo("Employee ID", f'Employee ID {employee_id}.')

    def undo_employee(self):
        if self.last_action == 'delite':
            messagebox.showinfo("Undo", f'Undo Delite Employee action.')
        elif self.last_action == 'update':
            messagebox.showinfo("Undo", f'Undo Update Employee action.')
        elif self.last_action == 'add':
            messagebox.showinfo("Undo", f'Undo Add Employee action.')
        else:
            messagebox.showinfo("Undo", f'No previos action.')

    def on_closing(self):
        self.conn.close()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeManagmentApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing())
    root.mainloop()



