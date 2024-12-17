"""
Kargo Durum Sorgulama (Sorting &amp; Searching)
Sistem, kargo durumlarını sorgulamak için sıralama ve arama algoritmalarını
kullanmalıdır.
 Teslim Edilmiş Kargolar:
o Kargo ID’ye göre binary search algoritması kullanılarak bulunmalıdır.
o Arama işlemi sırasında sorted list kullanılmalıdır.
 Teslim Edilmemiş Kargolar:

o Teslimat süresine göre merge sort veya quick sort kullanılarak
sıralanmalıdır.
o Sıralama işleminin zaman karmaşıklığı analiz edilmelidir.

Gönderiler shipping.db adlı SQLite veritabanında saklanıyor. Veriler buradan çekilmeli.
Saklandığı tablo adı shipments. Tablo şeması:
shipmentID INTEGER PRIMARY KEY
shipmentYear TEXT
shipmentMonth TEXT
shipmentDay TEXT
shipmentType TEXT
shipmentStatus TEXT
Konsola aşağıdaki gibi bir çıktı verilmelidir:
Delivered Shipments:
ID: 101, Date: 2024-12-10, Status: Delivered, Time: 2
Ayrıca zaman karmaşıklığı da analiz edilmeli.
Aynı zamanda teslim edilmemiş kargoların sıralanması için kullanılan algoritma
belirtilmelidir.
Ayrıca sıralama işlemi sırasında kullanılan veri yapısı da belirtilmelidir.
Ayrıca bir arayüz ile kullanıcıya kargo sorgulama imkanı sunulmalıdır.
"""


import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

def create_shipping_history_table():
    conn = sqlite3.connect('shipping.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS shipping_history (
            shipping_id INTEGER PRIMARY KEY,
            shipping_date TEXT,
            delivery_status TEXT,
            delivery_time INTEGER,
            customer_id INTEGER
        )
    """)
    conn.commit()
    conn.close()

def fetch_shipping_history(customer_id):
    conn = sqlite3.connect('shipping.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT shipping_id, shipping_date, delivery_status, delivery_time, customer_id
        FROM shipping_history
        WHERE customer_id = ?
        ORDER BY shipping_date DESC
    """, (customer_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def fetch_undelivered_shipments(customer_id=None):
    conn = sqlite3.connect('shipping.db')
    cursor = conn.cursor()
    if customer_id:
        cursor.execute("""
            SELECT shipping_id, shipping_date, delivery_status, delivery_time, customer_id
            FROM shipping_history
            WHERE customer_id = ? AND delivery_status != 'Delivered'
            ORDER BY delivery_time
        """, (customer_id,))
    else:
        cursor.execute("""
            SELECT shipping_id, shipping_date, delivery_status, delivery_time, customer_id
            FROM shipping_history
            WHERE delivery_status != 'Delivered'
            ORDER BY delivery_time
        """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def binary_search(shipments, shipment_id):
    left, right = 0, len(shipments) - 1
    while left <= right:
        mid = (left + right) // 2
        if shipments[mid][0] == shipment_id:
            return shipments[mid]
        elif shipments[mid][0] < shipment_id:
            left = mid + 1
        else:
            right = mid - 1
    return None

def merge_sort(shipments):
    if len(shipments) > 1:
        mid = len(shipments) // 2
        left_half = shipments[:mid]
        right_half = shipments[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i][3] < right_half[j][3]:
                shipments[k] = left_half[i]
                i += 1
            else:
                shipments[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            shipments[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            shipments[k] = right_half[j]
            j += 1
            k += 1
    return shipments

def quick_sort(shipments):
    if len(shipments) <= 1:
        return shipments
    pivot = shipments[len(shipments) // 2]
    left = [x for x in shipments if x[3] < pivot[3]]
    middle = [x for x in shipments if x[3] == pivot[3]]
    right = [x for x in shipments if x[3] > pivot[3]]
    return quick_sort(left) + middle + quick_sort(right)

def display_delivered_shipments(shipments):
    delivered_shipments = [s for s in shipments if s[2] == 'Delivered']
    delivered_shipments.sort(key=lambda x: x[0])  # Sort by shipping_id
    return delivered_shipments

def display_undelivered_shipments(shipments, sort_algorithm):
    undelivered_shipments = [s for s in shipments if s[2] != 'Delivered']
    if sort_algorithm == "Merge Sort":
        sorted_shipments = merge_sort(undelivered_shipments)
    elif sort_algorithm == "Quick Sort":
        sorted_shipments = quick_sort(undelivered_shipments)
    return sorted_shipments

def search_delivered_shipment():
    shipment_id = int(entry_delivered_shipment_id.get())
    result = binary_search(delivered_shipments, shipment_id)
    if result:
        messagebox.showinfo("Shipment Found", f"ID: {result[0]}, Date: {result[1]}, Status: {result[2]}, Time: {result[3]}")
    else:
        messagebox.showwarning("Not Found", "Shipment not found.")

def search_undelivered_shipment():
    shipment_id = int(entry_undelivered_shipment_id.get())
    sorted_shipments = display_undelivered_shipments(undelivered_shipments, "Merge Sort")  # Default to Merge Sort
    result = binary_search(sorted_shipments, shipment_id)
    if result:
        messagebox.showinfo("Shipment Found", f"ID: {result[0]}, Date: {result[1]}, Status: {result[2]}, Time: {result[3]}")
    else:
        messagebox.showwarning("Not Found", "Shipment not found.")

def show_undelivered_shipments():
    selected_item = customers_tree.selection()
    if selected_item:
        customer_id = customers_tree.item(selected_item, "values")[0]
    else:
        customer_id = None
    shipments_tree.delete(*shipments_tree.get_children())
    shipments = fetch_undelivered_shipments(customer_id)
    sorted_shipments = display_undelivered_shipments(shipments, "Merge Sort")  # Default to Merge Sort
    for shipment in sorted_shipments:
        shipments_tree.insert("", "end", values=shipment)

def show_customer_shipments(event):
    selected_item = customers_tree.selection()
    if not selected_item:
        return
    customer_id = customers_tree.item(selected_item, "values")[0]
    shipments_tree.delete(*shipments_tree.get_children())
    shipments = fetch_shipping_history(customer_id)
    for shipment in shipments:
        shipments_tree.insert("", "end", values=shipment)

def reset_selection():
    customers_tree.selection_remove(customers_tree.selection())
    show_undelivered_shipments()

# Create the shipping_history table if it does not exist
create_shipping_history_table()

# Fetch shipments from database
customer_id = 1  # Example customer_id
shipments = fetch_shipping_history(customer_id)
delivered_shipments = display_delivered_shipments(shipments)
undelivered_shipments = display_undelivered_shipments(shipments, "Merge Sort")

# Tkinter UI
root = tk.Tk()
root.title("Shipment Status Query")

frame_search_delivered = ttk.Frame(root)
frame_search_delivered.pack(side="top", fill="x", padx=10, pady=10)

label_delivered_shipment_id = ttk.Label(frame_search_delivered, text="Enter Delivered Shipment ID:")
label_delivered_shipment_id.pack(side="left")

entry_delivered_shipment_id = ttk.Entry(frame_search_delivered)
entry_delivered_shipment_id.pack(side="left", padx=5)

button_search_delivered = ttk.Button(frame_search_delivered, text="Search Delivered", command=search_delivered_shipment)
button_search_delivered.pack(side="left", padx=5)

frame_search_undelivered = ttk.Frame(root)
frame_search_undelivered.pack(side="top", fill="x", padx=10, pady=10)

label_undelivered_shipment_id = ttk.Label(frame_search_undelivered, text="Enter Undelivered Shipment ID:")
label_undelivered_shipment_id.pack(side="left")

entry_undelivered_shipment_id = ttk.Entry(frame_search_undelivered)
entry_undelivered_shipment_id.pack(side="left", padx=5)

button_search_undelivered = ttk.Button(frame_search_undelivered, text="Search Undelivered", command=search_undelivered_shipment)
button_search_undelivered.pack(side="left", padx=5)

frame_undelivered = ttk.Frame(root)
frame_undelivered.pack(side="top", fill="both", expand=True, padx=10, pady=10)

button_show_undelivered = ttk.Button(frame_undelivered, text="Show Undelivered Shipments", command=show_undelivered_shipments)
button_show_undelivered.pack(side="left", padx=5)

button_reset_selection = ttk.Button(frame_undelivered, text="Reset Selection", command=reset_selection)
button_reset_selection.pack(side="left", padx=5)

shipments_tree = ttk.Treeview(frame_undelivered, columns=("ID", "Date", "Status", "Time"), show="headings")
shipments_tree.heading("ID", text="ID")
shipments_tree.heading("Date", text="Date")
shipments_tree.heading("Status", text="Status")
shipments_tree.heading("Time", text="Time")
shipments_tree.pack(expand=True, fill="both")

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

customers_tree.bind("<Double-1>", show_customer_shipments)

root.mainloop()
conn.close()