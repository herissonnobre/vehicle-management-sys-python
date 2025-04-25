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
            - original_diameter (float)
            - replacement_diameter (float)
            - difference_percentage (float)
            - direction (str): 'underreports' or 'overreports'
            - real_distance_per_100km (float)
    """

    original_diameter = calculate_total_diameter(original)
    replacement_diameter = calculate_total_diameter(replacement)

    difference_percentage = ((replacement_diameter - original_diameter) / original_diameter) * 100
    direction = 'underreports' if difference_percentage > 0 else 'overreports'
    real_distance_per_100km  = 100 + difference_percentage

    return {
        'original_diameter': original_diameter,
        'replacement_diameter': replacement_diameter,
        'difference_percentage': round(abs(difference_percentage), 2),
        'direction': direction,
        'real_distance_per_100km': round(real_distance_per_100km, 2)
    }