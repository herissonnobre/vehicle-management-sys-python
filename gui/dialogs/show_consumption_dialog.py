from datetime import datetime, timedelta

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLabel, QComboBox, QPushButton, QMessageBox
)

from services.fueling import read_refuels, MAX_INTERVAL_KM
from services.odometer import load_tires_from_csv, calculate_odometer_difference


class ShowConsumptionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Fuel Consumption")

        self.layout = QVBoxLayout()
        self.form_layout = QFormLayout()

        self.period_combo = QComboBox()
        self.period_combo.addItems([
            "All time", "Last 7 days", "Last 15 days", "Last 30 days",
            "Last 90 days", "Last 180 days", "Last 365 days"
        ])

        self.fuel_type_combo = QComboBox()

        self.result_label = QLabel("Select period and fuel type to calculate.")

        self.calc_button = QPushButton("Calculate")
        self.calc_button.clicked.connect(self.calculate_consumption)

        self.form_layout.addRow("Period:", self.period_combo)
        self.form_layout.addRow("Fuel Type:", self.fuel_type_combo)

        self.layout.addLayout(self.form_layout)
        self.layout.addWidget(self.calc_button)
        self.layout.addWidget(self.result_label)

        self.setLayout(self.layout)

        self.load_fuel_types()

    def load_fuel_types(self):
        records = read_refuels()
        fuel_types = sorted({r.fuel_type for r in records if r.fuel_type})
        self.fuel_type_combo.addItem("All types")  # Representa None
        self.fuel_type_combo.addItems(fuel_types)

    def calculate_consumption(self):
        vehicles = load_tires_from_csv()
        if not vehicles:
            QMessageBox.warning(self, "Error", "No tire data found for odometer correction.")
            return

        _, original_tire, current_tire = vehicles[0]
        correction = calculate_odometer_difference(original_tire, current_tire)
        multiplier = correction.real_distance_per_100km / 100

        records = read_refuels()

        # Período
        period_choice = self.period_combo.currentIndex()
        today = datetime.today()
        date_threshold = {
            1: today - timedelta(days=7),
            2: today - timedelta(days=15),
            3: today - timedelta(days=30),
            4: today - timedelta(days=90),
            5: today - timedelta(days=180),
            6: today - timedelta(days=365),
        }.get(period_choice, None)

        # Combustível
        fuel_selected = self.fuel_type_combo.currentText()
        if fuel_selected == "All types":
            fuel_selected = None

        # Filtra registros
        filtered = [
            r for r in records
            if (fuel_selected is None or r.fuel_type == fuel_selected)
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

        if total_liters == 0:
            QMessageBox.information(self, "No Data", "Not enough data to calculate average consumption.")
            return

        corrected_km = total_km * multiplier
        avg = corrected_km / total_liters

        label = fuel_selected if fuel_selected else "all fuel types"
        period_label = self.period_combo.currentText()

        self.result_label.setText(f"Avg. consumption for {label} ({period_label}): {avg:.2f} km/l")
