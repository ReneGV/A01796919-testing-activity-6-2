#!/usr/bin/env python3
"""Customer class with simple file-based persistence."""

from src.file_db import read_json, write_json

DATA_FILE = "data/customers.json"


def load_customers_data():
    """Load customers from JSON file."""
    return read_json(DATA_FILE)


def save_customers_data(data):
    """Save customers to JSON file."""
    write_json(DATA_FILE, data)


class Customer:
    """Represents a customer with basic contact information."""

    def __init__(self, customer_id, name, email, phone):
        """Initialize a Customer instance."""
        self.customer_id = str(customer_id)
        self.name = str(name)
        self.email = str(email)
        self.phone = str(phone)

    def to_dict(self):
        """Return customer data as a dictionary."""
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
        }

    @classmethod
    def from_dict(cls, data):
        """Build a Customer object from a dictionary."""
        return cls(
            data["customer_id"],
            data["name"],
            data["email"],
            data["phone"],
        )

    @staticmethod
    def get_all_customers():
        """Return all customers as a list of Customer objects."""
        return [
            Customer.from_dict(data)
            for data in load_customers_data().values()
        ]

    @staticmethod
    def get_customer(customer_id):
        """Return a Customer by ID, or None if not found."""
        customer_id = str(customer_id)
        return next(
            (c for c in Customer.get_all_customers()
             if c.customer_id == customer_id),
            None
        )

    # --- CRUD operations ---

    @staticmethod
    def create_customer(customer_id, name, email, phone):
        """Create and save a new customer. Returns Customer or None."""
        customers = load_customers_data()
        customer_id = str(customer_id)

        if customer_id in customers:
            print(f"Error: Customer '{customer_id}' already exists.")
            return None

        customer = Customer(customer_id, name, email, phone)
        customers[customer_id] = customer.to_dict()
        save_customers_data(customers)
        print(f"Customer '{name}' created.")
        return customer

    @staticmethod
    def delete_customer(customer_id):
        """Delete a customer by ID. Returns True or False."""
        customers = load_customers_data()
        customer_id = str(customer_id)

        if customer_id not in customers:
            print(f"Error: Customer '{customer_id}' not found.")
            return False

        del customers[customer_id]
        save_customers_data(customers)
        print(f"Customer '{customer_id}' deleted.")
        return True

    @staticmethod
    def modify_customer(customer_id, name=None, email=None, phone=None):
        """Update one or more fields of a customer.

        Returns Customer or None.
        """
        customers = load_customers_data()
        customer_id = str(customer_id)

        if customer_id not in customers:
            print(f"Error: Customer '{customer_id}' not found.")
            return None

        customer = Customer.from_dict(customers[customer_id])

        if name is not None:
            customer.name = str(name)
        if email is not None:
            customer.email = str(email)
        if phone is not None:
            customer.phone = str(phone)

        customers[customer_id] = customer.to_dict()
        save_customers_data(customers)
        print(f"Customer '{customer_id}' updated.")
        return customer
