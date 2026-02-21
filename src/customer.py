#!/usr/bin/env python3
"""Customer class with simple file-based persistence using FileDB."""

from dataclasses import dataclass
from src.file_db import FileDB


@dataclass
class Customer:
    """Represents a customer with basic contact information."""

    customer_id: str
    name: str
    email: str
    phone: str

    def __post_init__(self):
        """Normalize field types after dataclass initialization."""
        self.customer_id = str(self.customer_id)
        self.name = str(self.name)
        self.email = str(self.email)
        self.phone = str(self.phone)

    def to_dict(self):
        """Return a serializable dict representation of the Customer."""
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Customer instance from a mapping (e.g., loaded JSON)."""
        return cls(
            data["customer_id"],
            data["name"],
            data["email"],
            data["phone"],
        )


class CustomerRepository:
    """Repository for Customer persistence and lookup using FileDB."""

    @staticmethod
    def get_all():
        """Return all customers loaded from persistent storage."""
        return [
            Customer.from_dict(data)
            for data in FileDB.load_customers_data().values()
        ]

    @staticmethod
    def get(customer_id):
        """Return the Customer with the given `customer_id`, or None."""
        customer_id = str(customer_id)
        return next(
            (
                c
                for c in CustomerRepository.get_all()
                if c.customer_id == customer_id
            ),
            None,
        )

    @staticmethod
    def create(customer_id, name, email, phone):
        """Create and persist a new Customer, or return None on duplicate."""
        customers = FileDB.load_customers_data()
        customer_id = str(customer_id)

        if customer_id in customers:
            print(f"Error: Customer '{customer_id}' already exists.")
            return None
        customer = Customer(customer_id, name, email, phone)
        customers[customer_id] = customer.to_dict()
        FileDB.save_customers_data(customers)
        print(f"Customer '{name}' created.")
        return customer

    @staticmethod
    def delete(customer_id):
        """Delete a customer by id.

        Returns True on success, False otherwise.
        """
        customers = FileDB.load_customers_data()
        customer_id = str(customer_id)

        if customer_id not in customers:
            print(f"Error: Customer '{customer_id}' not found.")
            return False
        del customers[customer_id]
        FileDB.save_customers_data(customers)
        print(f"Customer '{customer_id}' deleted.")
        return True

    @staticmethod
    def modify(customer_id, name=None, email=None, phone=None):
        """Modify fields of an existing Customer and persist changes."""
        customers = FileDB.load_customers_data()
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
        FileDB.save_customers_data(customers)
        print(f"Customer '{customer_id}' updated.")
        return customer
