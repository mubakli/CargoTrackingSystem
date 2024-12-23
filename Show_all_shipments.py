
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

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
            SELECT shipping_id, shipping_date, delivery_status, delivery_time, customer_id, target_city_id
            FROM shipping_history
        """)
        rows = cursor.fetchall()
        conn.close()
        return rows
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
        return []

def on_closing():
    try:
        root.destroy()
        import MainGUI
        MainGUI.main()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while closing the application: {e}")

def show_all_shipments():
    global root
    try:
        root = tk.Tk()
        root.title("All Shipments")
        root.geometry("1200x800")  # Set the window size to 1200x800

        frame = ttk.Frame(root)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        tree = ttk.Treeview(frame, columns=("ID", "Date", "Status", "Time", "Customer ID", "Target City ID"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Date", text="Date")
        tree.heading("Status", text="Status")
        tree.heading("Time", text="Time")
        tree.heading("Customer ID", text="Customer ID")
        tree.heading("Target City ID", text="Target City ID")
        tree.pack(expand=True, fill="both")

        shipments = fetch_all_shipments()
        linked_list = LinkedList()
        for shipment in shipments:
            linked_list.append(shipment)

        for shipment in linked_list.get_all_data():
            tree.insert("", "end", values=shipment)

        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred in the main function: {e}")

if __name__ == "__main__":
    show_all_shipments()