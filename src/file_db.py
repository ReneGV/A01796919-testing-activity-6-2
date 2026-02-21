#!/usr/bin/env python3
"""Generic JSON file read/write utilities for persistent storage."""

import json
import os


def read_json(filepath):
    """Read a JSON file and return its contents as a dictionary."""
    if not os.path.exists(filepath):
        return {}
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(filepath, data):
    """Write a dictionary to a JSON file, creating directories if needed."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
