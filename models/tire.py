"""
This module defines tire specifications used for vehicle odometer and pressure calculations.

It provides the Tire dataclass which represents conventional tire measurements. These are used for:

1. Representing tire dimensions (width, aspect ratio, rim diameter)
2. Calculating tire diameter and volume
3. Estimating odometer reading differences
4. Adjusting tire pressure when changing tire sizes
"""
from dataclasses import dataclass


@dataclass
class Tire:
    """
    A class representing a tire with standard sizing measurements.

    Attributes:
        width (int): The tire's section width in millimeters.
        aspect_ratio (int): The tire's aspect ratio as a percentage (height/width).
        rim (int): The wheel's diameter in inches.
    """
    width: int  # in mm
    aspect_ratio: int  # in percentage
    rim: int  # in inches
