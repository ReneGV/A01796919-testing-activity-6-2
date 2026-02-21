#!/usr/bin/env python3
"""Hotel class with simple file-based persistence."""

import json
import os

DATA_FILE = "data/hotels.json"


def load_hotels_data():
    """Load hotels from JSON file."""
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_hotels_data(data):
    """Save hotels to JSON file."""
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


class Hotel:
    """Represents a hotel with rooms that can be reserved."""

    def __init__(self, hotel_id, name, location, total_rooms):
        """Initialize a Hotel instance."""
        self.hotel_id = str(hotel_id)
        self.name = str(name)
        self.location = str(location)
        self.total_rooms = int(total_rooms)
        self.available_rooms = int(total_rooms)

    def to_dict(self):
        """Return hotel data as a dictionary."""
        return {
            "hotel_id": self.hotel_id,
            "name": self.name,
            "location": self.location,
            "total_rooms": self.total_rooms,
            "available_rooms": self.available_rooms,
        }

    @classmethod
    def from_dict(cls, data):
        """Build a Hotel object from a dictionary."""
        hotel = cls(
            data["hotel_id"],
            data["name"],
            data["location"],
            data["total_rooms"],
        )
        hotel.available_rooms = int(data["available_rooms"])
        return hotel

    def display(self):
        """Print hotel details to the console."""
        print(f"ID       : {self.hotel_id}")
        print(f"Name     : {self.name}")
        print(f"Location : {self.location}")
        print(
            f"Rooms    : {self.available_rooms}/{self.total_rooms} available"
        )

    @staticmethod
    def get_all_hotels():
        """Return all hotels as a list of Hotel objects."""
        return [
            Hotel.from_dict(data)
            for data in load_hotels_data().values()
        ]

    # --- CRUD operations ---

    @staticmethod
    def create_hotel(hotel_id, name, location, total_rooms):
        """Create and save a new hotel. Returns Hotel or None."""
        hotels = load_hotels_data()
        hotel_id = str(hotel_id)

        if hotel_id in hotels:
            print(f"Error: Hotel '{hotel_id}' already exists.")
            return None

        hotel = Hotel(hotel_id, name, location, total_rooms)
        hotels[hotel_id] = hotel.to_dict()
        save_hotels_data(hotels)
        print(f"Hotel '{name}' created.")
        return hotel

    @staticmethod
    def delete_hotel(hotel_id):
        """Delete a hotel by ID. Returns True or False."""
        hotels = load_hotels_data()
        hotel_id = str(hotel_id)

        if hotel_id not in hotels:
            print(f"Error: Hotel '{hotel_id}' not found.")
            return False

        del hotels[hotel_id]
        save_hotels_data(hotels)
        print(f"Hotel '{hotel_id}' deleted.")
        return True

    @staticmethod
    def display_hotel(hotel_id):
        """Print details of one hotel. Returns Hotel or None."""
        hotels = load_hotels_data()
        hotel_id = str(hotel_id)

        if hotel_id not in hotels:
            print(f"Error: Hotel '{hotel_id}' not found.")
            return None

        hotel = Hotel.from_dict(hotels[hotel_id])
        hotel.display()
        return hotel

    @staticmethod
    def modify_hotel(hotel_id, name=None, location=None, total_rooms=None):
        """Update one or more fields of a hotel. Returns Hotel or None."""
        hotels = load_hotels_data()
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
        save_hotels_data(hotels)
        print(f"Hotel '{hotel_id}' updated.")
        return hotel

    @staticmethod
    def reserve_room(hotel_id):
        """Reduce available rooms by 1. Returns True or False."""
        hotels = load_hotels_data()
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
        save_hotels_data(hotels)
        return True

    @staticmethod
    def cancel_room(hotel_id):
        """Increase available rooms by 1. Returns True or False."""
        hotels = load_hotels_data()
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
        save_hotels_data(hotels)
        return True
