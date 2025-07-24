"""
Fuel service module for reading, writing and managing refueling records.
"""
import csv
import logging
from datetime import datetime, timedelta
from pathlib import Path

from PyQt6.QtWidgets import QDialogButtonBox, QLineEdit, QFormLayout, QVBoxLayout, QMessageBox, QDialog

from models.refuel import RefuelRecord
from services.odometer import load_tires_from_csv, calculate_odometer_difference

CSV_PATH = Path("data/refuels.csv")
MAX_INTERVAL_KM = 1000


class AddFuelingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Register Refueling")

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Campos de entrada
        self.date_input = QLineEdit()
        self.odometer_input = QLineEdit()
        self.fuel_type_input = QLineEdit()
        self.total_value_input = QLineEdit()
        self.price_per_liter_input = QLineEdit()
        self.liters_input = QLineEdit()

        form_layout.addRow("Date (YYYY-MM-DD):", self.date_input)
        form_layout.addRow("Odometer (km):", self.odometer_input)
        form_layout.addRow("Fuel type:", self.fuel_type_input)
        form_layout.addRow("Total value:", self.total_value_input)
        form_layout.addRow("Price per liter:", self.price_per_liter_input)
        form_layout.addRow("Liters:", self.liters_input)

        layout.addLayout(form_layout)

        # Botões OK / Cancelar
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.save_data)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)


def read_refuels(file_path: str | Path = CSV_PATH) -> list[RefuelRecord]:
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


def write_refuels(file_path: str | Path, records: list[RefuelRecord]) -> None:
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
        csvfile.flush()


def add_fueling() -> None:
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

        records = read_refuels()
        records.append(record)
        write_refuels(CSV_PATH, records)

        print("Fueling added successfully!")
    except ValueError as e:
        print(f"Invalid input: {e}. Please try again.")

    def save_data(self):
        try:
            record = RefuelRecord(
                date=self.date_input.text(),
                odometer=int(self.odometer_input.text()),
                fuel_type=self.fuel_type_input.text(),
                total_value=float(self.total_value_input.text()) if self.total_value_input.text() else None,
                price_per_liter=float(self.price_per_liter_input.text()) if self.price_per_liter_input.text() else None,
                liters=float(self.liters_input.text()) if self.liters_input.text() else None
            )
            record.complete_data()

            records = read_refuels()
            records.append(record)
            write_refuels(CSV_PATH, records)

            QMessageBox.information(self, "Success", "Fueling registered successfully.")
            self.accept()

        except ValueError as e:
            QMessageBox.critical(self, "Invalid Input", f"Please check the values: {e}")


def show_consumption(csv_path: str = CSV_PATH) -> None:
    """
    Calculates and displays average fuel consumption (km/l).
    """
    vehicles = load_tires_from_csv()
    if not vehicles:
        print("No tire data found to apply odometer correction.")
        return

    _, original_tire, current_tire = vehicles[0]
    odometer_correction = calculate_odometer_difference(original_tire, current_tire)
    correction_multiplier = odometer_correction.real_distance_per_100km / 100

    records = read_refuels(csv_path)

    fuel_types = sorted({r.fuel_type for r in records if r.fuel_type})

    if not fuel_types:
        print("No fuel types found in the records.")
        return

    print("Select a period:")
    print("0. All time")
    print("1. Last 7 days")
    print("2. Last 15 days")
    print("3. Last 30 days")
    print("4. Last 90 days (quarter)")
    print("5. Last 180 days (semester)")
    print("6. Last 365 days (year)")

    try:
        period_choice = int(input("Enter the corresponding number: "))
    except ValueError:
        print("Invalid period selection.")
        return

    today = datetime.today()
    date_threshold = None

    if period_choice == 1:
        date_threshold = today - timedelta(days=7)
    elif period_choice == 2:
        date_threshold = today - timedelta(days=15)
    elif period_choice == 3:
        date_threshold = today - timedelta(days=30)
    elif period_choice == 4:
        date_threshold = today - timedelta(days=90)
    elif period_choice == 5:
        date_threshold = today - timedelta(days=180)
    elif period_choice == 6:
        date_threshold = today - timedelta(days=365)

    print("Select a fuel type:")
    print("0. All types")
    for idx, ft in enumerate(fuel_types, start=1):
        print(f"{idx}. {ft}")

    try:
        choice = int(input("Enter the corresponding number: "))
        if choice == 0:
            selected_fuel = None  # No filter
        else:
            selected_fuel = fuel_types[choice - 1]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return

    filtered = [
        r for r in records
        if (selected_fuel is None or r.fuel_type == selected_fuel)
           and r.odometer and r.liters
           and (not date_threshold or datetime.strptime(r.date, "%Y-%m-%d") >= date_threshold)
    ]

    sorted_records = sorted(filtered, key=lambda r: r.odometer)

    total_km = 0.0
    total_liters = 0.0

    for i in range(len(sorted_records) - 1):
        curr = sorted_records[i]
        next_fueling = sorted_records[i + 1]
        km = next_fueling.odometer - curr.odometer

        if 0 < km <= MAX_INTERVAL_KM and curr.liters:
            total_km += km
            total_liters += curr.liters
        elif km > 1000:
            logging.info(f"Ignored interval: {curr.odometer} -> {next_fueling.odometer} ({km} km)")

    if total_liters == 0:
        print("Not enough data to calculate average consumption.")
        return

    corrected_km = total_km * correction_multiplier

    avg_consumption = corrected_km / total_liters

    period_labels = {
        0: "all time",
        1: "last 7 days",
        2: "last 15 days",
        3: "last 30 days",
        4: "last 90 days",
        5: "last 180 days",
        6: "last 365 days",
    }

    fuel_label = selected_fuel if selected_fuel else "all fuel types"

    period_label = period_labels.get(period_choice, "custom period")

    print(f"Average consumption for {fuel_label} ({period_label}): {avg_consumption:.2f} km/l")
