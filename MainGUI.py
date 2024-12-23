import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from Shipment_Management import main as shipment_management_main
from Customer_Management import main as customer_management_main
from Shipment_priority import display_sorted_shipments

def open_shipment_management():
    shipment_management_main()

def check_shipping_status():
    import Shipment_Search
    Shipment_Search.main()

def view_shipping_history():
    import Stack_shipping_history
    Stack_shipping_history.main()

def list_all_shipments():
    import Show_all_shipments
    Show_all_shipments.show_all_shipments()

def show_delivery_routes():
    messagebox.showinfo("Info", "This feature is not yet implemented.")

def open_customer_management():
    customer_management_main()

def center_window(window, width=600, height=400):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

def show_sorted_shipments():
    display_sorted_shipments()

root = tk.Tk()
root.title("Main GUI")
center_window(root, width=600, height=400)

ttk.Button(root, text="Cargo Management", command=open_shipment_management).pack(padx=10, pady=10)
ttk.Button(root, text="Check Shipping Status", command=check_shipping_status).pack(padx=10, pady=10)
ttk.Button(root, text="View Shipping History(Stack)", command=view_shipping_history).pack(padx=10, pady=10)
ttk.Button(root, text="List All Shipments", command=list_all_shipments).pack(padx=10, pady=10)
ttk.Button(root, text="Show Delivery Routes", command=show_delivery_routes).pack(padx=10, pady=10)
ttk.Button(root, text="Customer Management", command=open_customer_management).pack(padx=10, pady=10)
ttk.Button(root, text="Show Sorted Shipments", command=show_sorted_shipments).pack(padx=10, pady=10)

root.mainloop()