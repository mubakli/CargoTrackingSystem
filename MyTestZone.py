import sqlite3
import random
import string
import tkinter as tk
from tkinter import ttk, messagebox

# Veritabanı bağlantısı
connection = sqlite3.connect('CargoTrackingSystem_CustomerDatabase.db')
cursor = connection.cursor()

# Tkinter uygulama
root = tk.Tk()
root.title("Kargo Yönetim Sistemi")

# Sekme oluşturma
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# Kargolar sekmesi
frame_shipments = ttk.Frame(notebook)
notebook.add(frame_shipments, text="Kargolar")

# Kişiler sekmesi
frame_customers = ttk.Frame(notebook)
notebook.add(frame_customers, text="Kişiler")

# Önceliklendirme sekmesi
frame_prioritize = ttk.Frame(notebook)
notebook.add(frame_prioritize, text="Önceliklendirme")

# Kargolar detay ve rota sekmesi
frame_details = ttk.Frame(notebook)
notebook.add(frame_details, text="Kargo Detayları")
details_label = tk.Label(frame_details, text="Detaylar", anchor="w", justify="left")
details_label.pack(side="left", fill="both", expand=True)
route_canvas = tk.Canvas(frame_details, bg="white")
route_canvas.pack(side="right", fill="both", expand=True)

# Kargolar sekmesindeki liste
shipments_tree = ttk.Treeview(frame_shipments, columns=("ID", "Gün Sayısı", "Durum"), show="headings")
shipments_tree.heading("ID", text="ID")
shipments_tree.heading("Gün Sayısı", text="Gün Sayısı")
shipments_tree.heading("Durum", text="Durum")
shipments_tree.pack(expand=True, fill="both")

# Kargoları yükle
cursor.execute("SELECT shipmentID, (julianday('now') - julianday(shipmentYear || '-' || shipmentMonth || '-' || shipmentDay)) AS days_left, shipmentStatus FROM shipments ORDER BY days_left ASC")
for shipment in cursor.fetchall():
    shipments_tree.insert("", "end", values=shipment)

# Kargo detayları ve rota gösterme
def show_shipment_details(event):
    selected_item = shipments_tree.selection()
    if not selected_item:
        return
    shipment_id = shipments_tree.item(selected_item, "values")[0]
    cursor.execute("SELECT * FROM shipments WHERE shipmentID = ?", (shipment_id,))
    shipment_details = cursor.fetchone()
    if shipment_details:
        details = f"ID: {shipment_details[0]}\nAdres ID: {shipment_details[1]}\nYıl: {shipment_details[2]}\nAy: {shipment_details[3]}\nGün: {shipment_details[4]}\nTip: {shipment_details[5]}\nDurum: {shipment_details[6]}"
        details_label.config(text=details)

shipments_tree.bind("<Double-1>", show_shipment_details)

# Kişiler sekmesindeki liste
customers_tree = ttk.Treeview(frame_customers, columns=("ID", "Ad"), show="headings")
customers_tree.heading("ID", text="ID")
customers_tree.heading("Ad", text="Ad")
customers_tree.pack(expand=True, fill="both")

# Kişileri yükle
cursor.execute("SELECT customerID, name FROM customerInformation")
for customer in cursor.fetchall():
    customers_tree.insert("", "end", values=customer)

# Müşteriye ait kargoları listeleme
def show_customer_shipments(event):
    selected_item = customers_tree.selection()
    if not selected_item:
        return
    customer_id = customers_tree.item(selected_item, "values")[0]
    shipments_tree.delete(*shipments_tree.get_children())
    cursor.execute("SELECT shipmentID, (julianday('now') - julianday(shipmentYear || '-' || shipmentMonth || '-' || shipmentDay)) AS days_left, shipmentStatus FROM shipments WHERE shipmentAdressID = ?", (customer_id,))
    for shipment in cursor.fetchall():
        shipments_tree.insert("", "end", values=shipment)

customers_tree.bind("<Double-1>", show_customer_shipments)

# Önceliklendirme sekmesindeki liste
prioritize_tree = ttk.Treeview(frame_prioritize, columns=("ID", "Gün Sayısı", "Durum"), show="headings")
prioritize_tree.heading("ID", text="ID")
prioritize_tree.heading("Gün Sayısı", text="Gün Sayısı")
prioritize_tree.heading("Durum", text="Durum")
prioritize_tree.pack(expand=True, fill="both")

cursor.execute("SELECT shipmentID, (julianday('now') - julianday(shipmentYear || '-' || shipmentMonth || '-' || shipmentDay)) AS days_left, shipmentStatus FROM shipments ORDER BY days_left ASC")
for shipment in cursor.fetchall():
    prioritize_tree.insert("", "end", values=shipment)

# Önceliklendirme fonksiyonu
def prioritize_shipment():
    selected_item = prioritize_tree.selection()
    if not selected_item:
        messagebox.showwarning("Hata", "Lütfen bir kargo seçin.")
        return
    shipment_id = prioritize_tree.item(selected_item, "values")[0]
    cursor.execute("UPDATE shipments SET shipmentType = -1 WHERE shipmentID = ?", (shipment_id,))
    connection.commit()
    messagebox.showinfo("Başarılı", "Kargo önceliklendirildi.")

prioritize_button = ttk.Button(frame_prioritize, text="Kargoyu Önceliklendir", command=prioritize_shipment)
prioritize_button.pack(pady=20)

root.mainloop()

# Veritabanı bağlantısını kapat
connection.close()




