import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

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

def create_shipping_history_table():
    conn = sqlite3.connect('shipping.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS shipping_history (
            shipping_id INTEGER PRIMARY KEY AUTOINCREMENT,
            shipping_date TEXT,
            delivery_status TEXT,
            delivery_time INTEGER,
            customer_id INTEGER,
            target_city_id INTEGER,
            FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
        )
    """)
    conn.commit()
    conn.close()

def fetch_customers():
    conn = sqlite3.connect('shipping.db')
    cursor = conn.cursor()
    cursor.execute("SELECT customer_id, name FROM customers")
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_cargo(shipping_date, delivery_status, delivery_time, customer_id, target_city_id):
    conn = sqlite3.connect('shipping.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO shipping_history (shipping_date, delivery_status, delivery_time, customer_id, target_city_id)
        VALUES (?, ?, ?, ?, ?)
    """, (shipping_date, delivery_status, delivery_time, customer_id, target_city_id))
    conn.commit()
    conn.close()

def delete_cargo(shipping_id):
    conn = sqlite3.connect('shipping.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM shipping_history WHERE shipping_id = ?", (shipping_id,))
    conn.commit()
    conn.close()

def center_window(window, width=400, height=300):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

def add_cargo_ui():
    def submit():
        shipping_date = entry_date.get()
        delivery_status = "Not delivered"
        delivery_time = int(entry_time.get())
        customer_id = int(customer_listbox.get(customer_listbox.curselection())[0])
        target_city_id = int(entry_city_id.get())
        if shipping_date and delivery_status and delivery_time and customer_id and target_city_id:
            add_cargo(shipping_date, delivery_status, delivery_time, customer_id, target_city_id)
            messagebox.showinfo("Success", "Cargo added successfully!")
            window.destroy()
        else:
            messagebox.showwarning("Input Error", "Please fill all fields.")

    window = tk.Tk()
    window.title("Add Cargo")
    window.configure(bg='white')
    center_window(window, width=500, height=400)

    ttk.Label(window, text="Date:", background='white').grid(row=0, column=0, padx=10, pady=10)
    entry_date = ttk.Entry(window)
    entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
    entry_date.grid(row=0, column=1, padx=10, pady=10)

    ttk.Label(window, text="Time:", background='white').grid(row=1, column=0, padx=10, pady=10)
    entry_time = ttk.Entry(window)
    entry_time.grid(row=1, column=1, padx=10, pady=10)

    ttk.Label(window, text="Target City ID:", background='white').grid(row=2, column=0, padx=10, pady=10)
    entry_city_id = ttk.Entry(window)
    entry_city_id.grid(row=2, column=1, padx=10, pady=10)

    ttk.Label(window, text="Select Customer:", background='white').grid(row=3, column=0, padx=10, pady=10)
    customer_listbox = tk.Listbox(window)
    linked_list = LinkedList()
    for customer in fetch_customers():
        linked_list.append(customer)
    for customer in linked_list.get_all_data():
        customer_listbox.insert(tk.END, customer)
    customer_listbox.grid(row=3, column=1, padx=10, pady=10)

    ttk.Button(window, text="Submit", command=submit).grid(row=4, column=0, columnspan=2, pady=10)

    window.mainloop()

def delete_cargo_ui():
    def submit():
        shipping_id = int(entry_id.get())
        if shipping_id:
            delete_cargo(shipping_id)
            messagebox.showinfo("Success", "Cargo deleted successfully!")
            window.destroy()
        else:
            messagebox.showwarning("Input Error", "Please enter a valid Shipping ID.")

    window = tk.Tk()
    window.title("Delete Cargo")
    window.configure(bg='white')
    center_window(window, width=500, height=400)

    ttk.Label(window, text="Shipping ID:", background='white').grid(row=0, column=0, padx=10, pady=10)
    entry_id = ttk.Entry(window)
    entry_id.grid(row=0, column=1, padx=10, pady=10)

    ttk.Button(window, text="Submit", command=submit).grid(row=1, column=0, columnspan=2, pady=10)

    window.mainloop()

def main():
    create_shipping_history_table()

    root = tk.Tk()
    root.title("Cargo Management")
    root.configure(bg='white')

    ttk.Button(root, text="Add Cargo", command=add_cargo_ui).pack(padx=10, pady=10)
    ttk.Button(root, text="Delete Cargo", command=delete_cargo_ui).pack(padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()