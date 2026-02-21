#!/usr/bin/env python3
"""Unit tests for customer.py – Customer class."""

import unittest
from tests.helpers import clear_data
from src.customer import Customer, CustomerRepository


class TestCustomer(unittest.TestCase):
    """Tests for the Customer class."""

    def setUp(self):
        """Clear data before each test."""
        clear_data()

    def test_init_sets_attributes(self):
        """Customer __init__ stores all four attributes correctly."""
        c = Customer("C1", "Alice", "a@test.com", "555")
        self.assertEqual(c.customer_id, "C1")
        self.assertEqual(c.name, "Alice")
        self.assertEqual(c.email, "a@test.com")
        self.assertEqual(c.phone, "555")

    def test_to_dict(self):
        """to_dict returns a dictionary with all expected keys."""
        data = Customer("C1", "Alice", "a@test.com", "555").to_dict()
        self.assertEqual(data["name"], "Alice")

    def test_from_dict(self):
        """from_dict reconstructs a Customer correctly."""
        raw = {"customer_id": "C1", "name": "Alice",
               "email": "a@test.com", "phone": "555"}
        self.assertEqual(Customer.from_dict(raw).name, "Alice")

    def test_create_customer_success(self):
        """create_customer returns a Customer and saves it to the file."""
        c = CustomerRepository.create("C1", "Alice", "a@test.com", "555")
        self.assertIsNotNone(c)
        ids = [cu.customer_id for cu in CustomerRepository.get_all()]
        self.assertIn("C1", ids)

    def test_create_customer_duplicate(self):
        """create_customer returns None when the ID already exists."""
        CustomerRepository.create("C1", "Alice", "a@test.com", "555")
        self.assertIsNone(
            CustomerRepository.create("C1", "Bob", "b@test.com", "666")
        )

    def test_delete_customer_success(self):
        """delete_customer removes the customer and returns True."""
        CustomerRepository.create("C1", "Alice", "a@test.com", "555")
        self.assertTrue(CustomerRepository.delete("C1"))
        ids = [cu.customer_id for cu in CustomerRepository.get_all()]
        self.assertNotIn("C1", ids)

    def test_delete_customer_not_found(self):
        """delete_customer returns False when customer does not exist."""
        self.assertFalse(CustomerRepository.delete("NOPE"))

    def test_modify_customer_name(self):
        """modify_customer updates the name field."""
        CustomerRepository.create("C1", "Alice", "a@test.com", "555")
        self.assertEqual(
            CustomerRepository.modify("C1", name="Alicia").name, "Alicia"
        )

    def test_modify_customer_email(self):
        """modify_customer updates the email field."""
        CustomerRepository.create("C1", "Alice", "a@test.com", "555")
        self.assertEqual(
            CustomerRepository.modify("C1", email="new@test.com").email,
            "new@test.com"
        )

    def test_modify_customer_phone(self):
        """modify_customer updates the phone field."""
        CustomerRepository.create("C1", "Alice", "a@test.com", "555")
        self.assertEqual(
            CustomerRepository.modify("C1", phone="999").phone, "999"
        )

    def test_modify_customer_not_found(self):
        """modify_customer returns None when customer does not exist."""
        self.assertIsNone(CustomerRepository.modify("NOPE", name="X"))

    def test_get_all_customers_empty(self):
        """get_all_customers returns an empty list when no customers exist."""
        self.assertEqual(CustomerRepository.get_all(), [])

    def test_get_all_customers_returns_all(self):
        """get_all_customers returns every saved customer."""
        CustomerRepository.create("C1", "Alice", "a@test.com", "555")
        CustomerRepository.create("C2", "Bob", "b@test.com", "666")
        customers = CustomerRepository.get_all()
        self.assertEqual(len(customers), 2)
        ids = [c.customer_id for c in customers]
        self.assertIn("C1", ids)
        self.assertIn("C2", ids)

    def test_get_all_customers_returns_customer_objects(self):
        """get_all_customers returns a list of Customer instances."""
        CustomerRepository.create("C1", "Alice", "a@test.com", "555")
        customers = CustomerRepository.get_all()
        self.assertIsInstance(customers[0], Customer)


if __name__ == "__main__":
    unittest.main()
