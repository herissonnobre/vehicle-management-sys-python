"""
This module defines tire specifications used for vehicle odometer calculations.

The module provides the Tire dataclass which represents standard tire measurements
following conventional tire sizing notation. These measurements are essential for:

1. Representing tire dimensions (width, aspect ratio, rim diameter)
2. Calculating total tire diameter
3. Determining odometer accuracy when changing tire sizes
4. Computing actual distances traveled with non-standard tire sizes

The tire specifications defined here are used by the odometer module to calculate
how different tire sizes affect vehicle odometer readings and actual distances traveled.
"""
from dataclasses import dataclass


@dataclass
class Tire:
    """
    A class representing a tire with standard tire sizing measurements.

    Attributes:
        width (float): The tire's section width in millimeters
        aspect_ratio (float): The tire's aspect ratio as a percentage (height/width)
        rim (float): The wheel's diameter in inches
    """
    width: float        # in mm
    aspect_ratio: float # in percentage
    rim: float          # in inches

