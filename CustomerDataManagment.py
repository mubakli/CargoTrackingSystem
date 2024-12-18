import sqlite3


class ShippingHistoryNode:
    def __init__(self, shipping_id, shipping_date, delivery_status, delivery_time):
        self.shipping_id = shipping_id
        self.shipping_date = shipping_date
        self.delivery_status = delivery_status
        self.delivery_time = delivery_time
        self.next = None


class Customer:
    def __init__(self, customer_id, name):
        self.customer_id = customer_id
        self.name = name
        self.shipping_history_head = None
        self.connect = sqlite3.connect('shared_database.db')  # Shared database
        self.create_tables()

    def create_tables(self):
        # Create tables for customers and their shipping history
        with self.connect:
            self.connect.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INTEGER PRIMARY KEY,
                name TEXT
            );
            """)
            self.connect.execute("""
            CREATE TABLE IF NOT EXISTS shipping_history (
                shipping_id INTEGER PRIMARY KEY,
                shipping_date TEXT,
                delivery_status TEXT,
                delivery_time INTEGER,
                customer_id INTEGER,
                FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
            );
            """)

    def save_customer(self):
        # Save the customer to the database
        with self.connect:
            self.connect.execute("""
            INSERT OR IGNORE INTO customers (customer_id, name)
            VALUES (?, ?)
            """, (self.customer_id, self.name))

    def add_shipping(self, shipping_id, shipping_date, delivery_status, delivery_time):
        # Add a shipping record to the linked list and database
        new_shipping = ShippingHistoryNode(shipping_id, shipping_date, delivery_status, delivery_time)

        if not self.shipping_history_head or self.shipping_history_head.shipping_date > shipping_date:
            new_shipping.next = self.shipping_history_head
            self.shipping_history_head = new_shipping
        else:
            current = self.shipping_history_head
            while current.next and current.next.shipping_date <= shipping_date:
                current = current.next
            new_shipping.next = current.next
            current.next = new_shipping

        with self.connect:
            self.connect.execute("""
            INSERT OR REPLACE INTO shipping_history (shipping_id, shipping_date, delivery_status, delivery_time, customer_id)
            VALUES (?, ?, ?, ?, ?)
            """, (shipping_id, shipping_date, delivery_status, delivery_time, self.customer_id))

    def load_shipping_history(self):
        # Load shipping history from the database
        cursor = self.connect.cursor()
        cursor.execute("""
        SELECT shipping_id, shipping_date, delivery_status, delivery_time
        FROM shipping_history
        WHERE customer_id = ?
        ORDER BY shipping_date ASC
        """, (self.customer_id,))
        rows = cursor.fetchall()
        self.shipping_history_head = None
        for row in rows:
            self.add_shipping(row[0], row[1], row[2], row[3])

    def display_shipping_history(self):
        # Display the shipping history from the linked list
        current = self.shipping_history_head
        if not current:
            print(f"No shipping history found for customer: {self.customer_id}")
            return
        print(f"Shipping history for customer: {self.customer_id}")
        while current:
            print(f"ID: {current.shipping_id}, Date: {current.shipping_date}, Status: {current.delivery_status}, Time: {current.delivery_time} days")
            current = current.next
