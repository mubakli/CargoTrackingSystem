import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

class ShippingStack:
    def __init__(self):
        self.stack = []
        self.max_size = 5

    def push(self, shipping):
        if len(self.stack) >= self.max_size:
            self.stack.pop(0)
        self.stack.append(shipping)

    def get_last_shipments(self):
        if not self.stack:
            return []
        return self.stack

shipping_stack = ShippingStack()

def fetch_shipping_history(customer_id):
    try:
        conn = sqlite3.connect('shipping.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT shipping_id, shipping_date, delivery_status, delivery_time, target_city_id
            FROM shipping_history
            WHERE customer_id = ?
            ORDER BY shipping_date DESC
            LIMIT 5
        """, (customer_id,))
        rows = cursor.fetchall()
        conn.close()
        return rows
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
        return []

def categorize_shipments(shipments):
    categories = {'Delivered': [], 'In Transit': [], 'Pending': []}
    for shipment in shipments:
        categories[shipment[2]].append(shipment)
    return categories

def display_shipping_history(customer_id):
    try:
        shipments = fetch_shipping_history(customer_id)
        if not shipments:
            messagebox.showinfo("No Shipments", "This person has no shipments.")
            return
        categorized_shipments = categorize_shipments(shipments)
        for status, shipment_list in categorized_shipments.items():
            print(f"{status}: {shipment_list}")
    except ValueError as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def show_customer_shipments(event):
    try:
        selected_item = customers_tree.selection()
        if not selected_item:
            return
        customer_id = customers_tree.item(selected_item, "values")[0]
        shipments_tree.delete(*shipments_tree.get_children())
        shipments = fetch_shipping_history(customer_id)
        if not shipments:
            messagebox.showinfo("No Shipments", "This person has no shipments.")
        else:
            for shipment in shipments:
                shipments_tree.insert("", "end", values=shipment)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def on_closing():
    try:
        root.destroy()
        import MainGUI
        MainGUI.main()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while closing the application: {e}")

def main():
    global customers_tree, shipments_tree, root
    try:
        root = tk.Tk()
        root.title("Shipping History")

        frame_customers = ttk.Frame(root)
        frame_customers.pack(side="left", fill="both", expand=True)

        customers_tree = ttk.Treeview(frame_customers, columns=("ID", "Name"), show="headings")
        customers_tree.heading("ID", text="ID")
        customers_tree.heading("Name", text="Name")
        customers_tree.pack(expand=True, fill="both")

        conn = sqlite3.connect('shipping.db')
        cursor = conn.cursor()
        cursor.execute("SELECT customer_id, name FROM customers")
        for customer in cursor.fetchall():
            customers_tree.insert("", "end", values=customer)
        conn.close()

        frame_shipments = ttk.Frame(root)
        frame_shipments.pack(side="right", fill="both", expand=True)

        shipments_tree = ttk.Treeview(frame_shipments, columns=("ID", "Date", "Status", "Time", "Target City ID"), show="headings")
        shipments_tree.heading("ID", text="ID")
        shipments_tree.heading("Date", text="Date")
        shipments_tree.heading("Status", text="Status")
        shipments_tree.heading("Time", text="Time")
        shipments_tree.heading("Target City ID", text="Target City ID")
        shipments_tree.pack(expand=True, fill="both")

        customers_tree.bind("<Double-1>", show_customer_shipments)

        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred in the main function: {e}")

if __name__ == "__main__":
    main()