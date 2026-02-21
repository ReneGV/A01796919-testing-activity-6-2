#!/usr/bin/env python3
"""Shared test helper used by all test modules."""

from src.hotel import save_hotels_data
from src.customer import save_customers_data
from src.reservation import save_reservations_data


def clear_data():
    """Reset all JSON data files to empty before each test."""
    save_hotels_data({})
    save_customers_data({})
    save_reservations_data({})
