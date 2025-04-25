"""
This module provides functions to calculate tire diameters and their effects on odometer readings.

The module contains utilities to:
- Calculate the total diameter of a tire based on its specifications
- Determine how different tire sizes affect odometer readings
- Calculate actual distances traveled when using non-standard tire sizes
"""

from models.tire import Tire


def calculate_total_diameter(tire: Tire) -> float:
    """
    Calculate the total diameter of a tire in millimeters.

    Args:
        tire (Tire): A Tire object containing width, aspect ratio and rim measurements

    Returns:
        float: The total diameter of the tire in millimeters
    """
    sidewall_height = tire.width * (tire.aspect_ratio / 100)
    rim_in_mm = tire.rim * 25.4
    return 2 * sidewall_height + rim_in_mm

def calculate_odometer_difference(original: Tire, replacement: Tire) -> dict:
    """
    Calculate the difference in odometer readings when replacing tires of different sizes.

    This function compares the diameters of original and replacement tires to determine
    how the odometer readings will be affected. A larger replacement tire will cause
    the odometer to underreport distances, while a smaller one will cause it to overreport.

    Args:
        original (Tire): The original tire specifications
        replacement (Tire): The replacement tire specifications

    Returns:
        dict: A dictionary containing:
            - difference_percentage (float): The percentage difference in diameter
            - direction (str): Either 'underreports' or 'overreports'
            - actual_distance_per_100km (float): The actual distance traveled per 100km shown on odometer
    """

    original_diameter = calculate_total_diameter(original)
    replacement_diameter = calculate_total_diameter(replacement)

    difference_percentage = ((replacement_diameter - original_diameter) / original_diameter) * 100
    direction = 'underreports' if difference_percentage > 0 else 'overreports'
    actual_distance_per_100km = 100 + difference_percentage

    return {
        'difference_percentage': difference_percentage,
        'direction': direction,
        'actual_distance_per_100km': actual_distance_per_100km,
    }