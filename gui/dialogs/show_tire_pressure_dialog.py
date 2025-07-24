import csv

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QScrollArea, QWidget, QMessageBox
)

CSV_PATH = 'data/vehicle.csv'
COLD_PRESSURE = 32
HOT_PRESSURE = 34


class ShowTirePressureDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tire Pressure Recommendations")
        self.setMinimumWidth(400)

        layout = QVBoxLayout()

        try:
            vehicles = self.load_vehicles_from_csv()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load data: {e}")
            self.close()
            return

        if not vehicles:
            QMessageBox.information(self, "Info", "No vehicle data found.")
            self.close()
            return

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)

        for v in vehicles:
            label = QLabel(
                f"<b>Vehicle:</b> {v['brand']} {v['model']} {v['version']} ({v['plate']})<br>"
                f"<b>Recommended pressure (cold):</b> {COLD_PRESSURE} psi<br>"
                f"<b>Recommended pressure (hot):</b> {HOT_PRESSURE} psi<br>"
                "<hr>"
            )
            label.setWordWrap(True)
            content_layout.addWidget(label)

        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)

        self.setLayout(layout)

    def load_vehicles_from_csv(self) -> list[dict]:
        with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            return list(reader)
