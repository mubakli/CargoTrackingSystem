"""
Her müşteri için son gönderilen kargoları hızlıca sorgulamak için bir yığın (stack)
kullanılmalıdır.
İşlevler:
 Son gönderilen 5 kargoyu sorgulama.
 Yeni gönderim eklenmesi durumunda stack’e push işlemi yapılmalıdır.
 Eğer gönderim geçmişi boşsa, uygun bir hata mesajı döndürülmelidir.
Veriler shipping.db adlı SQLite veritabanında saklanıyor. Veriler buradan çekilmeli.
Saklandığı tablo adı shipping_history. Tablo şeması:
shipping_id INTEGER PRIMARY KEY
shipping_date TEXT
delivery_status TEXT
delivery_time INTEGER
customer_id INTEGER
Konsola aşağıdaki gibi bir çıktı verilmelidir:
Shipping ID: 101, Date: 2024-12-10, Status: Delivered, Time: 2
Shipping ID: 102, Date: 2024-12-11, Status: In Transit, Time: 3
"""

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
            raise ValueError("No shipping history available.")
        return self.stack

def fetch_shipping_history(customer_id):
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

def categorize_shipments(shipments):
    categories = {'Delivered': [], 'In Transit': [], 'Pending': []}
    for shipment in shipments:
        categories[shipment[2]].append(shipment)
    return categories

def display_shipping_history(customer_id):
    try:
        shipments = fetch_shipping_history(customer_id)
        categorized_shipments = categorize_shipments(shipments)

        for status, shipment_list in categorized_shipments.items():
            print(f"\n{status} Shipments:")
            for shipment in shipment_list:
                print(f"Shipping ID: {shipment[0]}, Date: {shipment[1]}, Time: {shipment[3]}, Target City ID: {shipment[4]}")
    except ValueError as e:
        print(e)

def show_customer_shipments(event):
    selected_item = customers_tree.selection()
    if not selected_item:
        return
    customer_id = customers_tree.item(selected_item, "values")[0]
    shipments_tree.delete(*shipments_tree.get_children())
    shipments = fetch_shipping_history(customer_id)
    for shipment in shipments:
        shipments_tree.insert("", "end", values=shipment)

def main():
    global customers_tree, shipments_tree

    # Tkinter UI
    root = tk.Tk()
    root.title("Shipping History")

    # Customer List
    frame_customers = ttk.Frame(root)
    frame_customers.pack(side="left", fill="both", expand=True)

    customers_tree = ttk.Treeview(frame_customers, columns=("ID", "Name"), show="headings")
    customers_tree.heading("ID", text="ID")
    customers_tree.heading("Name", text="Name")
    customers_tree.pack(expand=True, fill="both")

    # Load Customers
    conn = sqlite3.connect('shipping.db')
    cursor = conn.cursor()
    cursor.execute("SELECT customer_id, name FROM customers")
    for customer in cursor.fetchall():
        customers_tree.insert("", "end", values=customer)

    # Shipping History
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

    root.mainloop()
    conn.close()

if __name__ == "__main__":
    main()