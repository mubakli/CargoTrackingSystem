import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

def print_linked_list(linked_list):
    current = linked_list.head
    while current:
        print(current.data)
        current = current.next

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def get_all_data(self):
        data_list = []
        current = self.head
        while current:
            data_list.append(current.data)
            current = current.next
        return data_list

    def delete_node(self, key):
        temp = self.head
        if temp is not None:
            if temp.data[0] == key:
                self.head = temp.next
                temp = None
                return
        while temp is not None:
            if temp.data[0] == key:
                break
            prev = temp
            temp = temp.next
        if temp == None:
            return
        prev.next = temp.next
        temp = None

def create_customers_table():
    try:
        conn = sqlite3.connect('shipping.db')
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        """)
        conn.commit()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
    finally:
        conn.close()

def add_customer(name, linked_list):
    try:
        conn = sqlite3.connect('shipping.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO customers (name) VALUES (?)", (name,))
        conn.commit()
        cursor.execute("SELECT last_insert_rowid()")
        customer_id = cursor.fetchone()[0]
        linked_list.append((customer_id, name))
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
    finally:
        conn.close()

def delete_customer(customer_id):
    try:
        conn = sqlite3.connect('shipping.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM customers WHERE customer_id = ?", (customer_id,))
        conn.commit()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
    finally:
        conn.close()

def fetch_customers():
    try:
        conn = sqlite3.connect('shipping.db')
        cursor = conn.cursor()
        cursor.execute("SELECT customer_id, name FROM customers")
        rows = cursor.fetchall()
        return rows
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
        return []
    finally:
        conn.close()

def center_window(window, width=400, height=300):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

def add_customer_ui(linked_list):
    def submit():
        name = entry_name.get()
        if name:
            add_customer(name, linked_list)
            messagebox.showinfo("Success", "Customer added successfully!")
            window.destroy()
        else:
            messagebox.showwarning("Input Error", "Please enter a name.")

    window = tk.Tk()
    window.title("Add Customer")
    window.configure(bg='white')
    center_window(window)

    label_name = ttk.Label(window, text="Name:", background='white', foreground='black')
    label_name.grid(row=0, column=0, padx=10, pady=10)
    entry_name = ttk.Entry(window)
    entry_name.grid(row=0, column=1, padx=10, pady=10)

    button_submit = ttk.Button(window, text="Submit", command=submit, style="TButton")
    button_submit.grid(row=1, column=0, columnspan=2, pady=10)

    style = ttk.Style()
    style.configure("TButton", background='white', foreground='black')

    window.mainloop()

def delete_customer_ui(linked_list):
    def submit():
        selected_item = customer_listbox.curselection()
        if selected_item:
            customer_id = customer_listbox.get(selected_item)[0]
            delete_customer(customer_id)
            linked_list.delete_node(customer_id)
            messagebox.showinfo("Success", "Customer deleted successfully!")
            window.destroy()
        else:
            messagebox.showwarning("Input Error", "Please select a customer.")

    window = tk.Tk()
    window.title("Delete Customer")
    window.configure(bg='white')
    center_window(window)

    customer_listbox = tk.Listbox(window)
    for customer in linked_list.get_all_data():
        customer_listbox.insert(tk.END, customer)
    customer_listbox.grid(row=0, column=0, padx=10, pady=10)

    button_submit = ttk.Button(window, text="Submit", command=submit, style="TButton")
    button_submit.grid(row=1, column=0, columnspan=2, pady=10)

    style = ttk.Style()
    style.configure("TButton", background='white', foreground='black')

    window.mainloop()

def on_closing():
    try:
        root.destroy()
        import MainGUI
        MainGUI.main()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while closing the application: {e}")

def main():
    try:
        create_customers_table()

        global root
        root = tk.Tk()
        root.title("Customer Management")
        root.configure(bg='white')
        center_window(root, width=600, height=400)

        linked_list = LinkedList()
        for customer in fetch_customers():
            linked_list.append(customer)

        button_add_customer = ttk.Button(root, text="Add Customer", command=lambda: add_customer_ui(linked_list), style="TButton")
        button_add_customer.pack(padx=10, pady=10)

        button_delete_customer = ttk.Button(root, text="Delete Customer", command=lambda: delete_customer_ui(linked_list), style="TButton")
        button_delete_customer.pack(padx=10, pady=10)

        button_print_linked_list = ttk.Button(root, text="Print Linked List", command=lambda: print_linked_list(linked_list), style="TButton")
        button_print_linked_list.pack(padx=10, pady=10)

        style = ttk.Style()
        style.configure("TButton", background='white', foreground='black')

        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred in the main function: {e}")

if __name__ == "__main__":
    main()