"""
This module provides functions to calculate tire diameters and their effects on odometer readings.

The module contains utilities to:
- Calculate the total diameter of a tire based on its specifications
- Determine how different tire sizes affect odometer readings
- Calculate actual distances traveled when using non-standard tire sizes
"""
import csv

from models.odomoter_difference_result import OdometerDifferenceResult
from models.tire import Tire

CSV_PATH = 'data/vehicle.csv'


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


def calculate_odometer_difference(original: Tire, replacement: Tire) -> OdometerDifferenceResult:
    """
    Compare original and replacement tire diameters to determine odometer discrepancy.

    Args:
        original (Tire): The original tire.
        replacement (Tire): The replacement tire.

    Returns:
        OdometerDifferenceResult: Object with detailed comparison results.
    """
    original_diameter = calculate_total_diameter(original)
    replacement_diameter = calculate_total_diameter(replacement)

    difference_percentage = ((replacement_diameter - original_diameter) / original_diameter) * 100
    direction = 'underreports' if difference_percentage > 0 else 'overreports'
    real_distance_per_100km = 100 + difference_percentage

    return OdometerDifferenceResult(
        original_diameter=round(original_diameter, 2),
        replacement_diameter=round(replacement_diameter, 2),
        difference_percentage=round(abs(difference_percentage), 2),
        direction=direction,
        real_distance_per_100km=round(real_distance_per_100km, 2)
    )


def load_tires_from_csv(filepath: str = CSV_PATH) -> list[tuple[str, Tire, Tire]]:
    """
    Load tire data from a CSV file and create Tire objects for each vehicle.

    Args:
        filepath (str): Path to the CSV file.

    Returns:
        list of tuple: Each tuple contains a label and two Tire objects (original and current).
    """
    vehicles = []
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            label = f"{row['brand']} {row['model']} {row['plate']} ({row['year']})"
            original = Tire(
                width=int(row['original_width']),
                aspect_ratio=int(row['original_aspect']),
                rim=int(row['original_rim'])
            )
            current = Tire(
                width=int(row['current_width']),
                aspect_ratio=int(row['current_aspect']),
                rim=int(row['current_rim'])
            )
            vehicles.append((label, original, current))
    return vehicles


def show_odometer_differences_from_file(filepath: str = CSV_PATH):
    """
    Print the odometer difference results for each vehicle listed in the CSV.

    Args:
        filepath (str): Path to the CSV file.
    """
    vehicles = load_tires_from_csv(filepath)

    for label, original, current in vehicles:
        result = calculate_odometer_difference(original, current)

        print(f"\nVehicle: {label}")
        print(f"Odometer {result.direction} by {result.difference_percentage:.2f}%")
        print(f"When odometer shows 100km, real distance is: {result.real_distance_per_100km:.2f} km")
