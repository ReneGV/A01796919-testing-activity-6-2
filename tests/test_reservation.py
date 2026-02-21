#!/usr/bin/env python3
"""Unit tests for reservation.py – Reservation class."""

import unittest
from tests.helpers import clear_data
from src.hotel import HotelRepository
from src.customer import CustomerRepository
from src.reservation import Reservation, ReservationRepository


class TestReservation(unittest.TestCase):
    """Tests for the Reservation class."""

    def setUp(self):
        """Clear data and create one hotel and one customer for each test."""
        clear_data()
        HotelRepository.create("H1", "Grand", "NYC", 3)
        CustomerRepository.create("C1", "Alice", "a@test.com", "555")

    def test_init_sets_attributes(self):
        """Reservation __init__ stores all four attributes correctly."""
        r = Reservation("R1", "C1", "H1")
        self.assertEqual(r.reservation_id, "R1")
        self.assertEqual(r.customer_id, "C1")
        self.assertEqual(r.hotel_id, "H1")
        self.assertEqual(r.status, "active")

    def test_init_custom_status(self):
        """Reservation __init__ accepts a custom status value."""
        r = Reservation("R1", "C1", "H1", status="cancelled")
        self.assertEqual(r.status, "cancelled")

    def test_to_dict(self):
        """to_dict returns a dictionary with the correct status."""
        data = Reservation("R1", "C1", "H1").to_dict()
        self.assertEqual(data["status"], "active")

    def test_from_dict(self):
        """from_dict reconstructs a Reservation correctly."""
        raw = {"reservation_id": "R1", "customer_id": "C1",
               "hotel_id": "H1", "status": "active"}
        self.assertEqual(Reservation.from_dict(raw).reservation_id, "R1")

    def test_from_dict_default_status(self):
        """from_dict defaults status to 'active' when key is absent."""
        raw = {"reservation_id": "R1", "customer_id": "C1",
               "hotel_id": "H1"}
        self.assertEqual(Reservation.from_dict(raw).status, "active")

    def test_create_reservation_success(self):
        """create_reservation returns a Reservation and reduces room count."""
        r = ReservationRepository.create("C1", "H1")
        self.assertIsNotNone(r)
        self.assertEqual(HotelRepository.get("H1").available_rooms, 2)

    def test_create_reservation_customer_not_found(self):
        """create_reservation returns None when the customer is missing."""
        self.assertIsNone(ReservationRepository.create("NOPE", "H1"))

    def test_create_reservation_hotel_not_found(self):
        """create_reservation returns None when the hotel is missing."""
        self.assertIsNone(ReservationRepository.create("C1", "NOPE"))

    def test_create_reservation_no_rooms(self):
        """create_reservation returns None when the hotel has no rooms."""
        HotelRepository.create("H2", "Tiny", "LA", 1)
        HotelRepository.reserve("H2")
        self.assertIsNone(ReservationRepository.create("C1", "H2"))

    def test_cancel_reservation_success(self):
        """cancel_reservation marks it cancelled and restores the room."""
        r = ReservationRepository.create("C1", "H1")
        self.assertTrue(ReservationRepository.cancel(r.reservation_id))
        self.assertEqual(HotelRepository.get("H1").available_rooms, 3)

    def test_cancel_reservation_not_found(self):
        """cancel_reservation returns False when ID does not exist."""
        self.assertFalse(ReservationRepository.cancel("NOPE"))

    def test_cancel_reservation_already_cancelled(self):
        """cancel_reservation returns False when already cancelled."""
        r = ReservationRepository.create("C1", "H1")
        ReservationRepository.cancel(r.reservation_id)
        self.assertFalse(ReservationRepository.cancel(r.reservation_id))

    def test_get_reservation_success(self):
        """get_reservation returns the correct Reservation object."""
        r = ReservationRepository.create("C1", "H1")
        found = ReservationRepository.get(r.reservation_id)
        self.assertIsNotNone(found)
        self.assertEqual(found.customer_id, "C1")

    def test_get_reservation_not_found(self):
        """get_reservation returns None when ID does not exist."""
        self.assertIsNone(ReservationRepository.get("NOPE"))

    def test_get_all_reservations_empty(self):
        """get_all_reservations returns empty list when none exist."""
        self.assertEqual(ReservationRepository.get_all(), [])

    def test_get_all_reservations_returns_all(self):
        """get_all_reservations returns every saved reservation."""
        r1 = ReservationRepository.create("C1", "H1")
        r2 = ReservationRepository.create("C1", "H1")
        reservations = ReservationRepository.get_all()
        self.assertEqual(len(reservations), 2)
        ids = [r.reservation_id for r in reservations]
        self.assertIn(r1.reservation_id, ids)
        self.assertIn(r2.reservation_id, ids)


if __name__ == "__main__":
    unittest.main()
