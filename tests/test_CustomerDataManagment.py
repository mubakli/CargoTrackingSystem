import unittest
import sqlite3
from io import StringIO
import sys
from CustomerDataManagment import Customer  # Import the Customer class from your main code


class TestCustomer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # This method will run once before all tests to set up the database
        cls.db = sqlite3.connect(':memory:')  # Using an in-memory database for testing
        cls.customer = Customer(1, "John Doe")  # Create a customer instance with ID 1 and name
        cls.customer.connect = cls.db  # Assign the in-memory database to the customer instance
        cls.customer.create_tables()  # Ensure that the tables are created for the tests

    def setUp(self):
        # This method will run before each tests to clean up the database
        self.db.execute("DELETE FROM customers")  # Remove all customers before each tests
        self.db.execute("DELETE FROM shipping_history")  # Remove all shipping history before each tests

    def test_save_customer(self):
        # Test saving a customer to the database
        self.customer.save_customer()
        cursor = self.db.execute("SELECT * FROM customers WHERE customer_id = 1")
        customer = cursor.fetchone()
        self.assertIsNotNone(customer)  # Check if the customer is added to the database
        self.assertEqual(customer[1], "John Doe")  # Ensure the name is correct

    def test_add_shipping(self):
        # Test adding a shipping record for the customer
        self.customer.add_shipping(101, "2024-12-10", "Delivered", 2)
        cursor = self.db.execute("SELECT * FROM shipping_history WHERE shipping_id = 101")
        shipping = cursor.fetchone()
        self.assertIsNotNone(shipping)  # Ensure the shipping record is inserted
        self.assertEqual(shipping[1], "2024-12-10")  # Verify the shipping date

    def test_load_shipping_history(self):
        # Test loading the shipping history from the database
        self.customer.add_shipping(102, "2024-12-11", "In Transit", 3)
        self.customer.add_shipping(103, "2024-12-12", "Delivered", 4)

        # Load shipping history into the customer object
        self.customer.load_shipping_history()
        current = self.customer.shipping_history_head

        # Verify the linked list order by shipping date
        self.assertEqual(current.shipping_id, 102)  # First record should be with shipping_id 102
        self.assertEqual(current.next.shipping_id, 103)  # Second record should be with shipping_id 103

    def test_display_shipping_history(self):
        # Test displaying the shipping history
        self.customer.add_shipping(104, "2024-12-13", "Pending", 5)

        # Capture the printed output
        captured_output = StringIO()
        sys.stdout = captured_output  # Redirect stdout to capture print statements

        self.customer.display_shipping_history()  # Call the display method

        sys.stdout = sys.__stdout__  # Restore original stdout

        # Check if the output contains the expected customer ID and shipping info
        output = captured_output.getvalue()
        self.assertIn("Shipping history for customer:", output)
        self.assertIn("ID: 104", output)  # Ensure the shipping ID 104 is displayed

    def test_insert_duplicate_shipping_id(self):
        # Test handling of duplicate shipping_id
        self.customer.add_shipping(105, "2024-12-14", "Delivered", 6)
        self.customer.add_shipping(105, "2024-12-15", "Returned", 7)  # Duplicate shipping_id

        # Check if the shipping history is updated with the new delivery status
        cursor = self.db.execute("SELECT * FROM shipping_history WHERE shipping_id = 105")
        shipping = cursor.fetchone()
        self.assertEqual(shipping[2], "Returned")  # Ensure the delivery status was updated

    @classmethod
    def tearDownClass(cls):
        # This method will run once after all tests
        cls.db.close()


if __name__ == "__main__":
    unittest.main()
