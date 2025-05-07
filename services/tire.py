import csv

from models.tire import Tire

CSV_PATH = 'data/vehicle.csv'
DEFAULT_PRESSURE = 32  # pressão original (em psi)


def calculate_volume(tire: Tire) -> float:
    """
    Estimate a proportional volume for a tire based on its dimensions.

    Note: This is not the real physical volume, but a proportional value
    useful for comparing relative pressure changes when changing tire sizes.

    Args:
        tire (Tire): A tire object with width, aspect ratio, and rim size.

    Returns:
        float: Estimated proportional volume.
    """
    return tire.width * tire.aspect_ratio * (tire.rim * 25.4)


def calculate_adjusted_pressure(original_volume: float, current_volume: float,
                                original_pressure: float = DEFAULT_PRESSURE) -> float:
    """
    Calculate the adjusted tire pressure based on volume change.

    Args:
        original_volume (float): Volume of the original tire.
        current_volume (float): Volume of the current tire.
        original_pressure (float): Original reference pressure (psi).

    Returns:
        float: Adjusted pressure (psi).
    """
    return original_pressure * (original_volume / current_volume)


def show_tire_pressure_adjustments():
    """
    Read vehicle and tire data from the CSV and display adjusted pressure suggestions
    based on the new tire dimensions.
    """
    with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
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

            original_volume = calculate_volume(original)
            current_volume = calculate_volume(current)
            adjusted_pressure = calculate_adjusted_pressure(original_volume, current_volume)

            print("-" * 50)
            print(f"Vehicle: {row['brand']} {row['model']} {row['version']} ({row['plate']})")
            print(f"Original pressure estimate: {DEFAULT_PRESSURE} psi")
            print(f"Adjusted pressure for current tires: {adjusted_pressure:.1f} psi")
            print("-" * 50)
