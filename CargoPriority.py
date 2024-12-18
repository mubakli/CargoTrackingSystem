import sqlite3
import heapq

class GlobalPriorityQueue:
    def __init__(self,):
        self.queue = []  # In-memory heap
        self.connect = sqlite3.connect("priority.db") # Use the same database connection
        self.create_priority_queue_table()

    def create_priority_queue_table(self):
        # Create the priority queue table within the same database
        with self.connect:
            self.connect.execute("""
            CREATE TABLE IF NOT EXISTS priority_queue (
                shipping_id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                delivery_time INTEGER,
                status TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
            );
            """)

    def add_cargo(self, shipping_id, customer_id, delivery_time, status):
        # Add cargo to the in-memory queue and database
        heapq.heappush(self.queue, (delivery_time, shipping_id, customer_id, status))
        with self.connect:
            self.connect.execute("""
            INSERT OR REPLACE INTO priority_queue (shipping_id, customer_id, delivery_time, status)
            VALUES (?, ?, ?, ?)
            """, (shipping_id, customer_id, delivery_time, status))

    def load_queue(self):
        # Load all cargos from the database into the in-memory queue
        cursor = self.connect.cursor()
        cursor.execute("""
        SELECT delivery_time, shipping_id, customer_id, status
        FROM priority_queue
        """)
        rows = cursor.fetchall()
        self.queue = []
        for row in rows:
            heapq.heappush(self.queue, (row[0], row[1], row[2], row[3]))

    def process_next_cargo(self):
        if self.queue:
            # Remove the highest priority cargo from the heap and database
            delivery_time, shipping_id, customer_id, status = heapq.heappop(self.queue)
            with self.connect:
                self.connect.execute("""
                DELETE FROM priority_queue
                WHERE shipping_id = ?
                """, (shipping_id,))
            return {
                "shipping_id": shipping_id,
                "customer_id": customer_id,
                "delivery_time": delivery_time,
                "status": status
            }
        else:
            return None

    def display_queue(self):
        # Display the in-memory queue
        print("Global Priority Queue:")
        for delivery_time, shipping_id, customer_id, status in self.queue:
            print(f"Customer ID: {customer_id}, Shipping ID: {shipping_id}, Delivery Time: {delivery_time}, Status: {status}")








"""WİTH OUT DATABASE CODE"""
"""
class PriorityQueue:
    def __init__(self):
        self.queue = []

    def add_cargo(self, shipping_id, delivery_time, status):
        # Use delivery_time as the priority (min-heap by default)
        heapq.heappush(self.queue, (delivery_time, shipping_id, status))

    def process_next_cargo(self):
        if self.queue:
            delivery_time, shipping_id, status = heapq.heappop(self.queue)
            return {
                "shipping_id": shipping_id,
                "delivery_time": delivery_time,
                "status": status
            }
        else:
            return None

    def display_queue(self):
        print("Priority Queue:")
        for delivery_time, shipping_id, status in self.queue:
            print(f"ID: {shipping_id}, Delivery Time: {delivery_time}, Status: {status}")
"""