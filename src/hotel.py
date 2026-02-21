#!/usr/bin/env python3
"""Hotel class with simple file-based persistence using FileDB."""

from dataclasses import dataclass, field
from typing import Optional
from src.file_db import FileDB


@dataclass
class Hotel:
    """Represents a hotel with rooms that can be reserved."""

    hotel_id: str
    name: str
    location: str
    total_rooms: int
    available_rooms: Optional[int] = field(default=None)

    def __post_init__(self):
        """Normalize field types after dataclass initialization."""
        self.hotel_id = str(self.hotel_id)
        self.name = str(self.name)
        self.location = str(self.location)
        self.total_rooms = int(self.total_rooms)
        if self.available_rooms is None:
            self.available_rooms = self.total_rooms
        else:
            self.available_rooms = int(self.available_rooms)

    def to_dict(self):
        """Return a serializable dict representation of the Hotel."""
        return {
            "hotel_id": self.hotel_id,
            "name": self.name,
            "location": self.location,
            "total_rooms": self.total_rooms,
            "available_rooms": self.available_rooms,
        }

    @classmethod
    def from_dict(cls, data):
        """Reconstruct a Hotel instance from a mapping (e.g., loaded JSON)."""
        hotel = cls(
            data["hotel_id"],
            data["name"],
            data["location"],
            data["total_rooms"],
            data.get("available_rooms"),
        )
        return hotel


class HotelRepository:
    """Repository for Hotel persistence and lookup using FileDB.

    Provides the same API previously available as `Hotel` static methods.
    """

    @staticmethod
    def get_all():
        """Return all hotels loaded from persistent storage."""
        return [
            Hotel.from_dict(data)
            for data in FileDB.load_hotels_data().values()
        ]

    @staticmethod
    def get(hotel_id):
        """Return a Hotel by id, or None if not found."""
        hotel_id = str(hotel_id)
        return next(
            (
                h
                for h in HotelRepository.get_all()
                if h.hotel_id == hotel_id
            ),
            None,
        )

    @staticmethod
    def create(hotel_id, name, location, total_rooms):
        """Create and persist a new Hotel, or return None on duplicate."""
        hotels = FileDB.load_hotels_data()
        hotel_id = str(hotel_id)

        if hotel_id in hotels:
            print(f"Error: Hotel '{hotel_id}' already exists.")
            return None
        hotel = Hotel(hotel_id, name, location, total_rooms)
        hotels[hotel_id] = hotel.to_dict()
        FileDB.save_hotels_data(hotels)
        print(f"Hotel '{name}' created.")
        return hotel

    @staticmethod
    def delete(hotel_id):
        """Delete a hotel by id. Returns True on success, False otherwise."""
        hotels = FileDB.load_hotels_data()
        hotel_id = str(hotel_id)

        if hotel_id not in hotels:
            print(f"Error: Hotel '{hotel_id}' not found.")
            return False
        del hotels[hotel_id]
        FileDB.save_hotels_data(hotels)
        print(f"Hotel '{hotel_id}' deleted.")
        return True

    @staticmethod
    def modify(hotel_id, name=None, location=None, total_rooms=None):
        """Modify fields of an existing Hotel and persist changes."""
        hotels = FileDB.load_hotels_data()
        hotel_id = str(hotel_id)

        if hotel_id not in hotels:
            print(f"Error: Hotel '{hotel_id}' not found.")
            return None
        hotel = Hotel.from_dict(hotels[hotel_id])

        if name is not None:
            hotel.name = str(name)
        if location is not None:
            hotel.location = str(location)
        if total_rooms is not None:
            new_total = int(total_rooms)
            diff = new_total - hotel.total_rooms
            hotel.total_rooms = new_total
            hotel.available_rooms = max(0, hotel.available_rooms + diff)

        hotels[hotel_id] = hotel.to_dict()
        FileDB.save_hotels_data(hotels)
        print(f"Hotel '{hotel_id}' updated.")
        return hotel

    @staticmethod
    def reserve(hotel_id):
        """Reserve one room at the hotel; return True on success."""
        hotels = FileDB.load_hotels_data()
        hotel_id = str(hotel_id)

        if hotel_id not in hotels:
            print(f"Error: Hotel '{hotel_id}' not found.")
            return False
        hotel = Hotel.from_dict(hotels[hotel_id])

        if hotel.available_rooms <= 0:
            print(f"Error: No rooms available at '{hotel_id}'.")
            return False

        hotel.available_rooms -= 1
        hotels[hotel_id] = hotel.to_dict()
        FileDB.save_hotels_data(hotels)
        return True

    @staticmethod
    def cancel(hotel_id):
        """Cancel a room reservation for the hotel; return True on success."""
        hotels = FileDB.load_hotels_data()
        hotel_id = str(hotel_id)

        if hotel_id not in hotels:
            print(f"Error: Hotel '{hotel_id}' not found.")
            return False
        hotel = Hotel.from_dict(hotels[hotel_id])

        if hotel.available_rooms >= hotel.total_rooms:
            print(f"Error: Hotel '{hotel_id}' already at full capacity.")
            return False

        hotel.available_rooms += 1
        hotels[hotel_id] = hotel.to_dict()
        FileDB.save_hotels_data(hotels)
        return True
