import sqlite3
import tkinter as tk
from tkinter import ttk

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

def fetch_all_shipments():
    try:
        conn = sqlite3.connect('shipping.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT sh.shipping_id, sh.shipping_date, sh.delivery_status, sh.delivery_time, sh.customer_id, sh.target_city_id, c.name
            FROM shipping_history sh
            JOIN customers c ON sh.customer_id = c.customer_id
        """)
        rows = cursor.fetchall()
        return rows
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        conn.close()

def show_all_shipments():
    shipments = fetch_all_shipments()
    linked_list = LinkedList()

    for shipment in shipments:
        linked_list.append(shipment)

    window = tk.Tk()
    window.title("All Shipments")
    window.geometry("1400x600")  # Adjusted window size

    tree = ttk.Treeview(window, columns=("ID", "Date", "Status", "Time", "Customer ID", "Target City ID", "Customer Name"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Date", text="Date")
    tree.heading("Status", text="Status")
    tree.heading("Time", text="Time")
    tree.heading("Customer ID", text="Customer ID")
    tree.heading("Target City ID", text="Target City ID")
    tree.heading("Customer Name", text="Customer Name")

    # Set column widths
    tree.column("ID", width=100)
    tree.column("Date", width=150)
    tree.column("Status", width=150)
    tree.column("Time", width=100)
    tree.column("Customer ID", width=150)
    tree.column("Target City ID", width=150)
    tree.column("Customer Name", width=200)

    tree.pack(expand=True, fill="both")

    # Insert shipments
    for shipment in linked_list.get_all_data():
        tree.insert("", "end", values=shipment)

    window.mainloop()

if __name__ == "__main__":
    show_all_shipments()