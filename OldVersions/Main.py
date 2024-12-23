from CustomerDataManagment import Customer
from CargoPriority import GlobalPriorityQueue


def main():
    # Example Customer
    customer = Customer(1, "John Doe")
    customer2 = Customer(2, "Elon Musk")
    customer3 = Customer(3, "Steve Jobs")
    customer4 = Customer(4, "Martin Brown")
    customer.save_customer()

    # Add shipping history for the customer
    customer.add_shipping(101, "2024-12-01", "Delivered", 3)
    customer.add_shipping(102, "2024-12-05", "In Transit", 5)
    customer2.add_shipping(103, "2024-12-07", "Delivered", 1)
    customer3.add_shipping(104, "2024-12-09", "In Transit", 9)
    customer4.add_shipping(105, "2024-12-03", "Delivered", 7)
    customer2.add_shipping(106, "2024-12-02", "In Transit", 2)
    customer3.add_shipping(107, "2024-12-10", "In Transit", 1)

    # Global Priority Queue - Automatically populate from shipping history
    priority_queue = GlobalPriorityQueue()
    priority_queue.populate_from_shipping_history()  # Fetch data automatically
    priority_queue.display_queue()

    # Process the next cargo
    processed = priority_queue.process_next_cargo()
    if processed:
        print("\nProcessed Cargo:")
        print(processed)

    # Display queue after processing
    print("\nQueue After Processing:")
    priority_queue.display_queue()


if __name__ == "__main__":
    main()
