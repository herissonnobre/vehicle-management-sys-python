"""
Module
"""
import csv

from models.refuel import RefuelRecord

CSV_PATH = 'data/refuels.csv'


def read_refuels(file_path: str) -> list[RefuelRecord]:
    """
    Reads refuel records from a CSV file and parses each record into a
    `RefuelRecord` object. The method expects the CSV file to have specific
    column headers (`date`, `odometer`, `fuel_type`, `total_value`,
    `price_per_liter`, `liters`) for proper parsing of data. The parsed
    data is returned as a list of `RefuelRecord` objects.

    :param file_path: Path to the CSV file containing refuel data to be read.
    :type file_path: str
    :return: A list of `RefuelRecord` objects parsed from the CSV file.
    :rtype: list[RefuelRecord]
    """
    records = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            record = RefuelRecord(
                date=row['date'],
                odometer=int(float(row['odometer'])),
                fuel_tipe=row['fuel_type'],
                total_value=float(row['total_value']) if row['total_value'] else None,
                price_per_liter=float(row['price_per_liter']) if row['price_per_liter'] else None,
                liters=float(row['liters']) if row['liters'] else None,
            )
            record.complete_data()
            records.append(record)
    return records


def write_refuels(file_path: str, records: list[RefuelRecord]):
    """

    :param file_path:
    :param records:
    """
    with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['date', 'odometer', 'fuel_type', 'total_value', 'price_per_liter', 'liters']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for r in records:
            writer.writerow({
                'date': r.date,
                'odometer': r.odometer,
                'fuel_type': r.fuel_tipe,
                'total_value': f'{r.total_value:.2f}' if r.total_value is not None else '',
                'price_per_liter': f'{r.price_per_liter:.2f}' if r.price_per_liter is not None else '',
                'liters': f'{r.liters:.2f}' if r.liters is not None else '',
            })


def add_fueling():
    """
    Prompts the user to input details regarding a fueling event, creates a RefuelRecord object
    with the data provided, and subsequently appends it to the existing list of records stored
    in a CSV file. Ensures that data fields are validated and completed as necessary before
    saving the information.

    This function facilitates the management and tracking of fuel consumption by allowing users
    to add and persist detailed records of refueling events.

    :raises ValueError: If any of the required inputs is invalid or cannot be processed correctly.
    :raises IOError: If there is an issue with accessing or writing to the CSV file.
    """
    print("\n--- Add Fueling ---")
    date = input("Date (YYYY-MM-DD): ")
    odometer = int(input("Odometer reading (km): "))
    fuel_type = input("Fuel type: ")

    total_value_input = input("Total value of fueling: ")
    total_value = float(total_value_input) if total_value_input else None

    price_input = input("Price per liter: ")
    price_per_liter = float(price_input) if price_input else None

    liters_input = input("Fuel quantity (liters): ")
    liters = float(liters_input) if liters_input else None

    record = RefuelRecord(
        date=date,
        odometer=odometer,
        fuel_tipe=fuel_type,
        total_value=total_value,
        price_per_liter=price_per_liter,
        liters=liters
    )

    record.complete_data()

    records = read_refuels(CSV_PATH)
    records.append(record)
    write_refuels(CSV_PATH, records)

    print("Fueling added successfully!")


def show_consumption() -> None:
    """

    :return:
    """
    records = read_refuels(CSV_PATH)

    sorted_records = sorted([r for r in records if r.odometer and r.liters], key=lambda r: r.odometer)

    total_km = 0.0
    total_liters = 0.0

    for i in range(1, len(sorted_records)):
        prev = sorted_records[i - 1]
        curr = sorted_records[i]
        km = curr.odometer - prev.odometer

        # Ignora registros com quilometragem inválida
        if km > 0 and curr.liters:
            total_km += km
            total_liters += curr.liters

    avg_consumption = total_km / total_liters

    if total_liters == 0:
        avg_consumption = 0.00

    print(f"Consumo médio: {avg_consumption:.2f} km/l")
    return None
