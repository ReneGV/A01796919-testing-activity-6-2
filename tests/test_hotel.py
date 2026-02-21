#!/usr/bin/env python3
"""Unit tests for hotel.py – Hotel class."""

import unittest
from tests.helpers import clear_data
from src.hotel import Hotel


class TestHotel(unittest.TestCase):
    """Tests for the Hotel class."""

    def setUp(self):
        """Clear data before each test."""
        clear_data()

    def test_init_sets_attributes(self):
        """Hotel __init__ stores all five attributes correctly."""
        hotel = Hotel("H1", "Grand", "NYC", 10)
        self.assertEqual(hotel.hotel_id, "H1")
        self.assertEqual(hotel.name, "Grand")
        self.assertEqual(hotel.location, "NYC")
        self.assertEqual(hotel.total_rooms, 10)
        self.assertEqual(hotel.available_rooms, 10)

    def test_to_dict(self):
        """to_dict returns a dictionary with all expected keys."""
        data = Hotel("H1", "Grand", "NYC", 5).to_dict()
        self.assertEqual(data["hotel_id"], "H1")
        self.assertEqual(data["available_rooms"], 5)

    def test_from_dict(self):
        """from_dict reconstructs a Hotel with correct available_rooms."""
        raw = {"hotel_id": "H1", "name": "Grand",
               "location": "NYC", "total_rooms": 5, "available_rooms": 3}
        self.assertEqual(Hotel.from_dict(raw).available_rooms, 3)

    def test_create_hotel_success(self):
        """create_hotel returns a Hotel and saves it to the file."""
        hotel = Hotel.create_hotel("H1", "Grand", "NYC", 5)
        self.assertIsNotNone(hotel)
        ids = [h.hotel_id for h in Hotel.get_all_hotels()]
        self.assertIn("H1", ids)

    def test_create_hotel_duplicate(self):
        """create_hotel returns None when the ID already exists."""
        Hotel.create_hotel("H1", "Grand", "NYC", 5)
        self.assertIsNone(Hotel.create_hotel("H1", "Other", "LA", 3))

    def test_delete_hotel_success(self):
        """delete_hotel removes the hotel and returns True."""
        Hotel.create_hotel("H1", "Grand", "NYC", 5)
        self.assertTrue(Hotel.delete_hotel("H1"))
        ids = [h.hotel_id for h in Hotel.get_all_hotels()]
        self.assertNotIn("H1", ids)

    def test_delete_hotel_not_found(self):
        """delete_hotel returns False when the hotel does not exist."""
        self.assertFalse(Hotel.delete_hotel("NOPE"))

    def test_modify_hotel_name(self):
        """modify_hotel updates the name field."""
        Hotel.create_hotel("H1", "Grand", "NYC", 5)
        self.assertEqual(Hotel.modify_hotel("H1", name="Palace").name,
                         "Palace")

    def test_modify_hotel_location(self):
        """modify_hotel updates the location field."""
        Hotel.create_hotel("H1", "Grand", "NYC", 5)
        self.assertEqual(Hotel.modify_hotel("H1", location="LA").location,
                         "LA")

    def test_modify_hotel_total_rooms(self):
        """modify_hotel adjusts available_rooms when total_rooms changes."""
        Hotel.create_hotel("H1", "Grand", "NYC", 5)
        hotel = Hotel.modify_hotel("H1", total_rooms=10)
        self.assertEqual(hotel.total_rooms, 10)
        self.assertEqual(hotel.available_rooms, 10)

    def test_modify_hotel_not_found(self):
        """modify_hotel returns None when the hotel does not exist."""
        self.assertIsNone(Hotel.modify_hotel("NOPE", name="X"))

    def test_reserve_room_success(self):
        """reserve_room decrements available_rooms and returns True."""
        Hotel.create_hotel("H1", "Grand", "NYC", 2)
        self.assertTrue(Hotel.reserve_room("H1"))
        self.assertEqual(Hotel.get_hotel("H1").available_rooms, 1)

    def test_reserve_room_no_availability(self):
        """reserve_room returns False when no rooms are left."""
        Hotel.create_hotel("H1", "Grand", "NYC", 1)
        Hotel.reserve_room("H1")
        self.assertFalse(Hotel.reserve_room("H1"))

    def test_reserve_room_not_found(self):
        """reserve_room returns False when the hotel does not exist."""
        self.assertFalse(Hotel.reserve_room("NOPE"))

    def test_cancel_room_success(self):
        """cancel_room increments available_rooms and returns True."""
        Hotel.create_hotel("H1", "Grand", "NYC", 2)
        Hotel.reserve_room("H1")
        self.assertTrue(Hotel.cancel_room("H1"))
        self.assertEqual(Hotel.get_hotel("H1").available_rooms, 2)

    def test_cancel_room_already_full(self):
        """cancel_room returns False when all rooms are already free."""
        Hotel.create_hotel("H1", "Grand", "NYC", 2)
        self.assertFalse(Hotel.cancel_room("H1"))

    def test_cancel_room_not_found(self):
        """cancel_room returns False when the hotel does not exist."""
        self.assertFalse(Hotel.cancel_room("NOPE"))

    def test_get_all_hotels_empty(self):
        """get_all_hotels returns an empty list when no hotels exist."""
        self.assertEqual(Hotel.get_all_hotels(), [])

    def test_get_all_hotels_returns_all(self):
        """get_all_hotels returns every saved hotel."""
        Hotel.create_hotel("H1", "Grand", "NYC", 5)
        Hotel.create_hotel("H2", "Plaza", "LA", 10)
        hotels = Hotel.get_all_hotels()
        self.assertEqual(len(hotels), 2)
        ids = [h.hotel_id for h in hotels]
        self.assertIn("H1", ids)
        self.assertIn("H2", ids)


if __name__ == "__main__":
    unittest.main()
