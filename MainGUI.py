import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from Shipment_Management import main as shipment_management_main
from Customer_Management import main as customer_management_main
from Shipment_priority import display_sorted_shipments

def open_shipment_management():
    try:
        root.withdraw()
        shipment_management_main()
        root.deiconify()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while opening Shipment Management: {e}")

def check_shipping_status():
    try:
        root.withdraw()
        import Shipment_Search
        Shipment_Search.main()
        root.deiconify()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while checking shipping status: {e}")

def view_shipping_history():
    try:
        root.withdraw()
        import Stack_shipping_history
        Stack_shipping_history.main()
        root.deiconify()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while viewing shipping history: {e}")

def list_all_shipments():
    try:
        root.withdraw()
        import Show_all_shipments
        Show_all_shipments.show_all_shipments()
        root.deiconify()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while listing all shipments: {e}")

def show_delivery_routes():
    try:
        root.withdraw()
        import Shipment_route
        Shipment_route.main()
        root.deiconify()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while showing delivery routes: {e}")

def open_customer_management():
    try:
        root.withdraw()
        customer_management_main()
        root.deiconify()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while opening Customer Management: {e}")

def show_sorted_shipments():
    try:
        root.withdraw()
        display_sorted_shipments()
        root.deiconify()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while displaying sorted shipments: {e}")

def center_window(window, width=600, height=400):
    try:
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while centering the window: {e}")

def on_closing():
    try:
        root.destroy()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while closing the application: {e}")

def main():
    global root
    try:
        root = tk.Tk()
        root.title("Main GUI")
        center_window(root)

        ttk.Button(root, text="Shipment Management", command=open_shipment_management).pack(pady=10)
        ttk.Button(root, text="Check Shipping Status", command=check_shipping_status).pack(pady=10)
        ttk.Button(root, text="View Shipping History", command=view_shipping_history).pack(pady=10)
        ttk.Button(root, text="List All Shipments", command=list_all_shipments).pack(pady=10)
        ttk.Button(root, text="Show Delivery Routes", command=show_delivery_routes).pack(pady=10)
        ttk.Button(root, text="Customer Management", command=open_customer_management).pack(pady=10)
        ttk.Button(root, text="Sorted Shipments by Delivery Time(Priority Queue)", command=show_sorted_shipments).pack(pady=10)

        root.protocol("WM_DELETE_WINDOW", on_closing)

        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred in the main function: {e}")

if __name__ == "__main__":
    main()