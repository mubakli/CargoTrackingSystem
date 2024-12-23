import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

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

    def sort_by_delivery_time(self):
        if not self.head or not self.head.next:
            return

        sorted_list = LinkedList()
        current = self.head
        while current:
            next_node = current.next
            current.next = None
            sorted_list.sorted_insert(current)
            current = next_node
        self.head = sorted_list.head

    def sorted_insert(self, new_node):
        if not self.head or self.head.data[3] >= new_node.data[3]:
            new_node.next = self.head
            self.head = new_node
        else:
            current = self.head
            while current.next and current.next.data[3] < new_node.data[3]:
                current = current.next
            new_node.next = current.next
            current.next = new_node

def fetch_shipments():
    try:
        conn = sqlite3.connect('shipping.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT sh.shipping_id, sh.shipping_date, sh.delivery_status, sh.delivery_time, sh.customer_id, sh.target_city_id, c.name
            FROM shipping_history sh
            JOIN customers c ON sh.customer_id = c.customer_id
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

def display_sorted_shipments():
    try:
        shipments = fetch_shipments()
        linked_list = LinkedList()

        for shipment in shipments:
            linked_list.append(shipment)

        linked_list.sort_by_delivery_time()

        def toggle_delivered():
            nonlocal show_delivered
            show_delivered = not show_delivered
            update_treeview()

        def update_treeview():
            tree.delete(*tree.get_children())
            for shipment in linked_list.get_all_data():
                if show_delivered or shipment[2] != 'Delivered':
                    tree.insert("", "end", values=shipment)

        global root
        root = tk.Tk()
        root.title("Sorted Shipments by Delivery Time")
        root.geometry("1000x600")

        show_delivered = True

        tree = ttk.Treeview(root, columns=("ID", "Date", "Status", "Time", "Customer ID", "Target City ID", "Customer Name"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Date", text="Date")
        tree.heading("Status", text="Status")
        tree.heading("Time", text="Time")
        tree.heading("Customer ID", text="Customer ID")
        tree.heading("Target City ID", text="Target City ID")
        tree.heading("Customer Name", text="Customer Name")

        tree.column("ID", width=50)
        tree.column("Date", width=100)
        tree.column("Status", width=100)
        tree.column("Time", width=50)
        tree.column("Customer ID", width=100)
        tree.column("Target City ID", width=100)
        tree.column("Customer Name", width=150)

        tree.pack(expand=True, fill="both")

        toggle_button = ttk.Button(root, text="Toggle Delivered Shipments", command=toggle_delivered)
        toggle_button.pack(pady=10)

        update_treeview()

        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred in the main function: {e}")

if __name__ == "__main__":
    display_sorted_shipments()