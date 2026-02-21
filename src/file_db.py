#!/usr/bin/env python3
"""Generic JSON file read/write utilities for persistent storage."""

import json
import os
from typing import Dict


def ensure_data_dir():
    """Ensure the `data` directory exists for JSON files."""
    os.makedirs("data", exist_ok=True)


def read_json(filepath):
    """Read JSON from `filepath` and return the parsed object."""
    if not os.path.exists(filepath):
        return {}
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(filepath, data):
    """Write `data` as JSON to `filepath` with a 4-space indent."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


class FileDB:
    """High-level file access for domain data files."""

    CUSTOMERS_FILE = "data/customers.json"
    HOTELS_FILE = "data/hotels.json"
    RESERVATIONS_FILE = "data/reservations.json"

    @staticmethod
    def load_customers_data() -> Dict:
        """Load and return the customers JSON mapping from storage."""
        ensure_data_dir()
        if not os.path.exists(FileDB.CUSTOMERS_FILE):
            return {}
        return read_json(FileDB.CUSTOMERS_FILE)

    @staticmethod
    def save_customers_data(data: Dict):
        """Persist the customers mapping to storage."""
        ensure_data_dir()
        write_json(FileDB.CUSTOMERS_FILE, data)

    @staticmethod
    def load_hotels_data() -> Dict:
        """Load and return the hotels JSON mapping from storage."""
        ensure_data_dir()
        if not os.path.exists(FileDB.HOTELS_FILE):
            return {}
        return read_json(FileDB.HOTELS_FILE)

    @staticmethod
    def save_hotels_data(data: Dict):
        """Persist the hotels mapping to storage."""
        ensure_data_dir()
        write_json(FileDB.HOTELS_FILE, data)

    @staticmethod
    def load_reservations_data() -> Dict:
        """Load and return the reservations JSON mapping from storage."""
        ensure_data_dir()
        if not os.path.exists(FileDB.RESERVATIONS_FILE):
            return {}
        return read_json(FileDB.RESERVATIONS_FILE)

    @staticmethod
    def save_reservations_data(data: Dict):
        """Persist the reservations mapping to storage."""
        ensure_data_dir()
        write_json(FileDB.RESERVATIONS_FILE, data)
