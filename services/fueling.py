"""
Fuel service module for reading, writing and managing refueling records.
"""
import csv
import logging
from datetime import datetime

from models.refuel import RefuelRecord

CSV_PATH = 'data/refuels.csv'


def read_refuels(file_path: str = CSV_PATH) -> list[RefuelRecord]:
    """
    Reads refuel records from a CSV file and returns them as RefuelRecord objects.
    """
    records = []
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    record = RefuelRecord(
                        date=row['date'],
                        odometer=int(row['odometer']) if row['odometer'] else 0,
                        fuel_type=row['fuel_type'],
                        total_value=float(row['total_value']) if row['total_value'] else None,
                        price_per_liter=float(row['price_per_liter']) if row['price_per_liter'] else None,
                        liters=float(row['liters']) if row['liters'] else None,
                    )
                    record.complete_data()
                    records.append(record)
                except (ValueError, KeyError) as e:
                    logging.warning(f"Skipping invalid row: {row} - Error: {e}")
    except FileNotFoundError:
        logging.warning(f"No existing refuel data found at {file_path}. Returning empty list.")
    return records


def write_refuels(file_path: str, records: list[RefuelRecord]) -> None:
    """
    Writes a list of RefuelRecord objects to a CSV file.
    """
    with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['date', 'odometer', 'fuel_type', 'total_value', 'price_per_liter', 'liters']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for r in records:
            writer.writerow({
                'date': r.date,
                'odometer': r.odometer,
                'fuel_type': r.fuel_type,
                'total_value': f'{r.total_value:.2f}' if r.total_value is not None else '',
                'price_per_liter': f'{r.price_per_liter:.2f}' if r.price_per_liter is not None else '',
                'liters': f'{r.liters:.2f}' if r.liters is not None else '',
            })


def add_fueling(csv_path: str = CSV_PATH) -> None:
    """
    Prompts the user for fueling information and stores it in the CSV.
    """
    print("\n--- Add Fueling ---")

    try:
        date_input = input("Date (YYYY-MM-DD): ")
        datetime.strptime(date_input, "%Y-%m-%d")  # Validate format

        odometer = int(input("Odometer reading (km): "))
        fuel_type = input("Fuel type: ")

        total_value_input = input("Total value of fueling: ")
        total_value = float(total_value_input) if total_value_input else None

        price_input = input("Price per liter: ")
        price_per_liter = float(price_input) if price_input else None

        liters_input = input("Fuel quantity (liters): ")
        liters = float(liters_input) if liters_input else None

        record = RefuelRecord(
            date=date_input,
            odometer=odometer,
            fuel_type=fuel_type,
            total_value=total_value,
            price_per_liter=price_per_liter,
            liters=liters
        )

        record.complete_data()

        records = read_refuels(CSV_PATH)
        records.append(record)
        write_refuels(CSV_PATH, records)

        print("Fueling added successfully!")
    except ValueError as e:
        print(f"Invalid input: {e}. Please try again.")


def show_consumption(csv_path: str = CSV_PATH) -> None:
    """
    Calculates and displays average fuel consumption (km/l).
    """
    records = read_refuels(csv_path)

    sorted_records = sorted([r for r in records if r.odometer and r.liters], key=lambda r: r.odometer)

    total_km = 0.0
    total_liters = 0.0

    for i in range(1, len(sorted_records)):
        prev = sorted_records[i - 1]
        curr = sorted_records[i]
        km = curr.odometer - prev.odometer

        if km > 0 and curr.liters:
            total_km += km
            total_liters += curr.liters

    if total_liters == 0:
        print("Not enough data to calculate average consumption.")
        return

    avg_consumption = total_km / total_liters

    print(f"Average consumption: {avg_consumption:.2f} km/l")
