import sqlite3
import random
from datetime import datetime, timedelta

from CustomerDataManagment import Customer

if __name__ == "__main__":
    # Create a new customer
    customer = Customer(1, "John Doe")
    customer.save_customer()

    # Add shipping records
    #customer.add_shipping(101, "2024-12-10", "Delivered", 2)
    #customer.add_shipping(102, "2024-12-05", "Pending", 5)
    #customer.add_shipping(103, "2024-12-12", "Delivered", 1)

    # Display shipping history (linked list)
    customer.display_shipping_history()

    # Reload the shipping history from the database
    print("\nReloading from the database:")
    customer.load_shipping_history()
    customer.display_shipping_history()










""""
# Veritabanı bağlantısını oluştur
conn = sqlite3.connect("CargoTrackingSystem.db", check_same_thread=False)
cursor = conn.cursor()

# Tablo oluşturma

cursor.execute(
CREATE TABLE IF NOT EXISTS Customers (
    CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
    FirstName TEXT NOT NULL,
    LastName TEXT NOT NULL
);
)

cursor.execute(
CREATE TABLE IF NOT EXISTS Shipments (
    ShipmentID INTEGER PRIMARY KEY AUTOINCREMENT,
    CustomerID INTEGER NOT NULL,
    ShipmentDate DATE NOT NULL,
    DeliveryStatus TEXT NOT NULL,
    DeliveryTime INTEGER NOT NULL,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);
)

# Basit Python arayüzü için gerekli kütüphaneler
import tkinter as tk
from tkinter import ttk, messagebox

# Linked List Sınıfı
class LinkedListNode:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        if not self.head:
            self.head = LinkedListNode(data)
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = LinkedListNode(data)

    def to_list(self):
        data_list = []
        current = self.head
        while current:
            data_list.append(current.data)
            current = current.next
        return data_list

# Fonksiyonlar

def show_customers_tab():
    for widget in customer_frame.winfo_children():
        widget.destroy()

    customer_list = ttk.Treeview(customer_frame, columns=("ID", "Ad", "Soyad"), show="headings")
    customer_list.heading("ID", text="Müşteri ID")
    customer_list.heading("Ad", text="Ad")
    customer_list.heading("Soyad", text="Soyad")

    cursor.execute("SELECT * FROM Customers")
    for row in cursor.fetchall():
        customer_list.insert("", "end", values=row)

    def on_customer_select(event):
        selected_item = customer_list.selection()[0]
        customer_details = customer_list.item(selected_item, 'values')
        show_customer_shipments_linked_list(customer_details[0])

    customer_list.bind("<Double-1>", on_customer_select)
    customer_list.pack(fill="both", expand=True)

def show_customer_shipments_linked_list(customer_id):
    customer_shipments_window = tk.Toplevel()
    customer_shipments_window.title(f"Müşteri {customer_id} Gönderi Geçmişi")

    # Gönderi geçmişini linked list ile çekme
    linked_list = LinkedList()
    cursor.execute("SELECT ShipmentID, ShipmentDate, DeliveryStatus, DeliveryTime FROM Shipments WHERE CustomerID = ?", (customer_id,))
    for row in cursor.fetchall():
        linked_list.append(row)

    # Linked list'teki verileri görüntüleme
    linked_list_view = tk.Text(customer_shipments_window, wrap="word")
    linked_list_view.pack(fill="both", expand=True)

    linked_list_view.insert("1.0", "Gönderi Geçmişi (Linked List):\n")
    current = linked_list.head
    while current:
        linked_list_view.insert("end", f"Gönderi ID: {current.data[0]}, Tarih: {current.data[1]}, Durum: {current.data[2]}, Süre: {current.data[3]} gün\n")
        current = current.next

def add_customer():
    def save_customer():
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        cursor.execute("INSERT INTO Customers (FirstName, LastName) VALUES (?, ?)", (first_name, last_name))
        conn.commit()
        messagebox.showinfo("Başarılı", "Müşteri başarıyla eklendi.")
        add_window.destroy()
        show_customers_tab()

    add_window = tk.Toplevel()
    add_window.title("Yeni Müşteri Ekle")

    tk.Label(add_window, text="Ad:").grid(row=0, column=0)
    first_name_entry = tk.Entry(add_window)
    first_name_entry.grid(row=0, column=1)

    tk.Label(add_window, text="Soyad:").grid(row=1, column=0)
    last_name_entry = tk.Entry(add_window)
    last_name_entry.grid(row=1, column=1)

    tk.Button(add_window, text="Ekle", command=save_customer).grid(row=2, column=0, columnspan=2)


def show_shipments_tab():
    pass


def add_shipment():
    def save_shipment():
        customer_id = customer_id_var.get()
        shipment_date = datetime.now().strftime('%Y-%m-%d')
        delivery_status = delivery_status_var.get()
        delivery_time = 3 if delivery_status == "Standart" else 2

        cursor.execute(
            "INSERT INTO Shipments (CustomerID, ShipmentDate, DeliveryStatus, DeliveryTime) VALUES (?, ?, ?, ?)",
            (customer_id, shipment_date, delivery_status, delivery_time)
        )
        conn.commit()
        messagebox.showinfo("Başarılı", "Gönderim başarıyla eklendi.")
        add_window.destroy()
        show_shipments_tab()

    add_window = tk.Toplevel()
    add_window.title("Yeni Gönderim Ekle")

    tk.Label(add_window, text="Müşteri Seç:").grid(row=0, column=0)
    customer_id_var = tk.StringVar()
    customer_menu = ttk.Combobox(add_window, textvariable=customer_id_var)
    cursor.execute("SELECT CustomerID, FirstName || ' ' || LastName FROM Customers")
    customer_menu['values'] = [f"{row[0]} - {row[1]}" for row in cursor.fetchall()]
    customer_menu.grid(row=0, column=1)

    tk.Label(add_window, text="Teslimat Tipi:").grid(row=1, column=0)
    delivery_status_var = tk.StringVar(value="Standart")
    ttk.Combobox(add_window, textvariable=delivery_status_var, values=["Standart", "Ekspres"]).grid(row=1, column=1)

    tk.Button(add_window, text="Ekle", command=save_shipment).grid(row=2, column=0, columnspan=2)

def prioritize_shipment():
    cursor.execute("SELECT ShipmentID FROM Shipments ORDER BY DeliveryTime ASC LIMIT 1")
    first_shipment = cursor.fetchone()
    if first_shipment:
        messagebox.showinfo("Kargo Önceliklendir", f"Kargo ID: {first_shipment[0]} ilk sırada depodan çıkmalıdır.")
    else:
        messagebox.showinfo("Kargo Önceliklendir", "Hiçbir gönderi bulunamadı.")

# Ana arayüz
root = tk.Tk()
root.title("Kargo Takip Sistemi")

# Sekme yapısı
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

customer_frame = tk.Frame(notebook)
customer_frame.pack(fill="both", expand=True)
notebook.add(customer_frame, text="Müşteriler")

shipment_frame = tk.Frame(notebook)
shipment_frame.pack(fill="both", expand=True)
notebook.add(shipment_frame, text="Gönderimler")

# Araç çubuğu
toolbar = tk.Frame(root)
toolbar.pack(side="top", fill="x")

customer_button = tk.Button(toolbar, text="Müşteri Ekle", command=add_customer)
customer_button.pack(side="left", padx=5, pady=5)

shipment_button = tk.Button(toolbar, text="Gönderi Ekle", command=add_shipment)
shipment_button.pack(side="left", padx=5, pady=5)

prioritize_button = tk.Button(toolbar, text="Kargo Önceliklendir", command=prioritize_shipment)
prioritize_button.pack(side="left", padx=5, pady=5)

# Varsayılan sekmeleri yükle
show_customers_tab()

root.mainloop()
"""