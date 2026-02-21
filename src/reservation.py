#!/usr/bin/env python3
"""Reservation class with simple file-based persistence using FileDB."""

import uuid
from dataclasses import dataclass
from src.file_db import FileDB
from src.hotel import HotelRepository
from src.customer import CustomerRepository


@dataclass
class Reservation:
    """Links a customer to a hotel room."""

    reservation_id: str
    customer_id: str
    hotel_id: str
    status: str = "active"

    def __post_init__(self):
        """Normalize field types after dataclass initialization."""
        self.reservation_id = str(self.reservation_id)
        self.customer_id = str(self.customer_id)
        self.hotel_id = str(self.hotel_id)
        self.status = str(self.status)

    def to_dict(self):
        """Return a serializable dict representation of the Reservation."""
        return {
            "reservation_id": self.reservation_id,
            "customer_id": self.customer_id,
            "hotel_id": self.hotel_id,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Reservation from a mapping (e.g., loaded JSON)."""
        return cls(
            data["reservation_id"],
            data["customer_id"],
            data["hotel_id"],
            data.get("status", "active"),
        )


class ReservationRepository:
    """Repository for Reservation persistence and operations."""

    @staticmethod
    def get_all():
        """Return all reservations loaded from persistent storage."""
        data_values = FileDB.load_reservations_data().values()
        return [Reservation.from_dict(data) for data in data_values]

    @staticmethod
    def create(customer_id, hotel_id):
        """Create a new reservation if customer and hotel exist.

        Returns the Reservation on success, or None.
        """
        customer_id = str(customer_id)
        hotel_id = str(hotel_id)

        known_customers = {c.customer_id for c in CustomerRepository.get_all()}
        if customer_id not in known_customers:
            print(f"Error: Customer '{customer_id}' not found.")
            return None

        known_hotels = {h.hotel_id for h in HotelRepository.get_all()}
        if hotel_id not in known_hotels:
            print(f"Error: Hotel '{hotel_id}' not found.")
            return None

        if not HotelRepository.reserve(hotel_id):
            return None

        reservation_id = str(uuid.uuid4())
        reservation = Reservation(reservation_id, customer_id, hotel_id)
        reservations = FileDB.load_reservations_data()
        reservations[reservation_id] = reservation.to_dict()
        FileDB.save_reservations_data(reservations)
        print(f"Reservation '{reservation_id}' created.")
        return reservation

    @staticmethod
    def cancel(reservation_id):
        """Cancel a reservation and restore a room on success."""
        reservations = FileDB.load_reservations_data()
        reservation_id = str(reservation_id)

        if reservation_id not in reservations:
            print(f"Error: Reservation '{reservation_id}' not found.")
            return False

        reservation = Reservation.from_dict(reservations[reservation_id])

        if reservation.status == "cancelled":
            msg = (
                f"Error: Reservation '{reservation_id}' "
                "is already cancelled."
            )
            print(msg)
            return False

        reservation.status = "cancelled"
        reservations[reservation_id] = reservation.to_dict()
        FileDB.save_reservations_data(reservations)
        HotelRepository.cancel(reservation.hotel_id)
        print(f"Reservation '{reservation_id}' cancelled.")
        return True

    @staticmethod
    def get(reservation_id):
        """Return the Reservation with `reservation_id`, or None if missing."""
        reservations = FileDB.load_reservations_data()
        reservation_id = str(reservation_id)

        if reservation_id not in reservations:
            print(f"Error: Reservation '{reservation_id}' not found.")
            return None

        return Reservation.from_dict(reservations[reservation_id])
