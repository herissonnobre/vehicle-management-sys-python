from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLabel, QComboBox, QPushButton, QMessageBox
)

from services.odometer import load_tires_from_csv, calculate_odometer_difference


class ShowOdometerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Odometer Correction Viewer")

        self.vehicles = load_tires_from_csv()
        if not self.vehicles:
            QMessageBox.critical(self, "Error", "No vehicle/tire data found.")
            self.close()
            return

        self.layout = QVBoxLayout()
        self.form_layout = QFormLayout()

        # Dropdown para selecionar veículo
        self.vehicle_combo = QComboBox()
        for label, _, _ in self.vehicles:
            self.vehicle_combo.addItem(label)

        # Labels de resultado
        self.direction_label = QLabel("-")
        self.percentage_label = QLabel("-")
        self.real_distance_label = QLabel("-")

        self.calc_button = QPushButton("Calculate")
        self.calc_button.clicked.connect(self.calculate_odometer_diff)

        self.form_layout.addRow("Select Vehicle:", self.vehicle_combo)
        self.form_layout.addRow("Odometer Direction:", self.direction_label)
        self.form_layout.addRow("Difference (%):", self.percentage_label)
        self.form_layout.addRow("Real Distance per 100km:", self.real_distance_label)

        self.layout.addLayout(self.form_layout)
        self.layout.addWidget(self.calc_button)

        self.setLayout(self.layout)

    def calculate_odometer_diff(self):
        index = self.vehicle_combo.currentIndex()
        _, original, current = self.vehicles[index]

        result = calculate_odometer_difference(original, current)

        self.direction_label.setText(f"{result.direction}")
        self.percentage_label.setText(f"{result.difference_percentage:.2f}%")
        self.real_distance_label.setText(f"{result.real_distance_per_100km:.2f} km")
