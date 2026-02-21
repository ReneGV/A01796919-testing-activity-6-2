#!/usr/bin/env python3
"""Shared test helper used by all test modules."""

from src.file_db import FileDB


def clear_data():
    """Reset all JSON data files to empty before each test."""
    FileDB.save_hotels_data({})
    FileDB.save_customers_data({})
    FileDB.save_reservations_data({})
