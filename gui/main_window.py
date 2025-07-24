from PyQt6.QtWidgets import QWidget, QMessageBox, QPushButton, QVBoxLayout, QLabel

from gui.dialogs import (
    AddRefuelDialog,
    ShowConsumptionDialog,
    ShowOdometerDialog,
    ShowTirePressureDialog,
)


class VehicleManagerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vehicle Management")
        self.setGeometry(300, 300, 250, 150)

        self.layout = QVBoxLayout()

        self.label = QLabel('Vehicle Management Menu', self)
        self.layout.addWidget(self.label)

        self.btn_refuel = QPushButton('1. Register Refueling', self)
        self.btn_refuel.clicked.connect(self.open_add_fueling_dialog)
        self.layout.addWidget(self.btn_refuel)

        self.btn_consumption = QPushButton("2. Show Consumption", self)
        self.btn_consumption.clicked.connect(self.open_show_consumption_dialog)
        self.layout.addWidget(self.btn_consumption)

        self.btn_odometer = QPushButton("3. Show Odometer Comparative", self)
        self.btn_odometer.clicked.connect(self.open_show_odometer_dialog)
        self.layout.addWidget(self.btn_odometer)

        self.btn_tires = QPushButton("4. Show Tires Pressure", self)
        self.btn_tires.clicked.connect(self.open_show_tires_dialog)
        self.layout.addWidget(self.btn_tires)

        self.btn_exit = QPushButton("Exit", self)
        self.btn_exit.clicked.connect(self.close)
        self.layout.addWidget(self.btn_exit)

        self.setLayout(self.layout)

    def run_action(self, func):
        try:
            result = func()
            if result:
                QMessageBox.information(self, "Success", str(result))
        except Exception as e:
            QMessageBox.information(self, "Error", str(e))

    def open_add_fueling_dialog(self):
        dialog = AddRefuelDialog(self)
        dialog.exec()

    def open_show_consumption_dialog(self):
        dialog = ShowConsumptionDialog(self)
        dialog.exec()

    def open_show_odometer_dialog(self):
        dialog = ShowOdometerDialog(self)
        dialog.exec()

    def open_show_tires_dialog(self):
        dialog = ShowTirePressureDialog(self)
        dialog.exec()
