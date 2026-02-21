#!/usr/bin/env python3
"""Reservation class with simple file-based persistence."""

import uuid

from src.file_db import read_json, write_json
from src.hotel import Hotel
from src.customer import Customer

DATA_FILE = "data/reservations.json"


def load_reservations_data():
    """Load reservations from JSON file."""
    return read_json(DATA_FILE)


def save_reservations_data(data):
    """Save reservations to JSON file."""
    write_json(DATA_FILE, data)


class Reservation:
    """Links a customer to a hotel room."""

    def __init__(self, reservation_id, customer_id, hotel_id,
                 status="active"):
        """Initialize a Reservation instance."""
        self.reservation_id = str(reservation_id)
        self.customer_id = str(customer_id)
        self.hotel_id = str(hotel_id)
        self.status = str(status)

    def to_dict(self):
        """Return reservation data as a dictionary."""
        return {
            "reservation_id": self.reservation_id,
            "customer_id": self.customer_id,
            "hotel_id": self.hotel_id,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data):
        """Build a Reservation object from a dictionary."""
        return cls(
            data["reservation_id"],
            data["customer_id"],
            data["hotel_id"],
            data.get("status", "active"),
        )

    @staticmethod
    def get_all_reservations():
        """Return all reservations as a list of Reservation objects."""
        return [
            Reservation.from_dict(data)
            for data in load_reservations_data().values()
        ]

    # --- Operations ---

    @staticmethod
    def create_reservation(customer_id, hotel_id):
        """Create a reservation. Returns Reservation or None."""
        customer_id = str(customer_id)
        hotel_id = str(hotel_id)

        known_customers = {c.customer_id for c in Customer.get_all_customers()}
        if customer_id not in known_customers:
            print(f"Error: Customer '{customer_id}' not found.")
            return None

        known_hotels = {h.hotel_id for h in Hotel.get_all_hotels()}
        if hotel_id not in known_hotels:
            print(f"Error: Hotel '{hotel_id}' not found.")
            return None

        if not Hotel.reserve_room(hotel_id):
            return None

        reservation_id = str(uuid.uuid4())
        reservation = Reservation(reservation_id, customer_id, hotel_id)
        reservations = load_reservations_data()
        reservations[reservation_id] = reservation.to_dict()
        save_reservations_data(reservations)
        print(f"Reservation '{reservation_id}' created.")
        return reservation

    @staticmethod
    def cancel_reservation(reservation_id):
        """Cancel a reservation and free the hotel room.

        Returns True or False.
        """
        reservations = load_reservations_data()
        reservation_id = str(reservation_id)

        if reservation_id not in reservations:
            print(f"Error: Reservation '{reservation_id}' not found.")
            return False

        reservation = Reservation.from_dict(reservations[reservation_id])

        if reservation.status == "cancelled":
            print(
                f"Error: Reservation '{reservation_id}' is already cancelled."
            )
            return False

        reservation.status = "cancelled"
        reservations[reservation_id] = reservation.to_dict()
        save_reservations_data(reservations)
        Hotel.cancel_room(reservation.hotel_id)
        print(f"Reservation '{reservation_id}' cancelled.")
        return True

    @staticmethod
    def get_reservation(reservation_id):
        """Look up a reservation by ID. Returns Reservation or None."""
        reservations = load_reservations_data()
        reservation_id = str(reservation_id)

        if reservation_id not in reservations:
            print(f"Error: Reservation '{reservation_id}' not found.")
            return None

        return Reservation.from_dict(reservations[reservation_id])
