"""Utility functions for the software renderer."""

import os

import numpy as np


def ensure_directory(path: str):
    """Create a directory and all parent directories if they do not exist.

    Args:
        path: Directory path to create.
    """
    os.makedirs(path, exist_ok=True)


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp a scalar value to the range [min_val, max_val].

    Args:
        value: The value to clamp.
        min_val: Minimum bound.
        max_val: Maximum bound.

    Returns:
        The clamped value.
    """
    return max(min_val, min(max_val, value))


def degrees_to_radians(degrees: float) -> float:
    """Convert an angle from degrees to radians.

    Args:
        degrees: Angle in degrees.

    Returns:
        Angle in radians.
    """
    return degrees * np.pi / 180.0
