import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from Shipment_Management import add_cargo_ui
from Customer_Management import main as customer_management_main

def add_cargo_shipment():
    add_cargo_ui()

def check_shipping_status():
    import Shipment_Search
    Shipment_Search.main()

def view_shipping_history():
    import Stack_shipping_history
    Stack_shipping_history.main()

def list_all_shipments():
    new_window = tk.Tk()
    new_window.title("List All Shipments")
    messagebox.showinfo("List All Shipments", "This will open the List All Shipments UI.", parent=new_window)
    new_window.mainloop()

def show_delivery_routes():
    import tree4
    tree4.main()

def open_customer_management():
    customer_management_main()

def center_window(window, width=600, height=400):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

root = tk.Tk()
root.title("Main GUI")
center_window(root, width=600, height=400)

ttk.Button(root, text="Add Cargo Shipment", command=add_cargo_shipment).pack(padx=10, pady=10)
ttk.Button(root, text="Check Shipping Status", command=check_shipping_status).pack(padx=10, pady=10)
ttk.Button(root, text="View Shipping History", command=view_shipping_history).pack(padx=10, pady=10)
ttk.Button(root, text="List All Shipments", command=list_all_shipments).pack(padx=10, pady=10)
ttk.Button(root, text="Show Delivery Routes", command=show_delivery_routes).pack(padx=10, pady=10)
ttk.Button(root, text="Customer Management", command=open_customer_management).pack(padx=10, pady=10)

root.mainloop()