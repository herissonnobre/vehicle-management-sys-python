from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QApplication, QDialog

from services.fueling import AddFuelingDialog
from services.fueling import show_consumption
from services.odometer import show_odometer_differences_from_file
from services.tire import show_tire_pressure


class VehicleManagerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Vehicle Management')
        self.setGeometry(300, 300, 250, 150)

        self.layout = QVBoxLayout()

        self.label = QLabel('Vehicle Management Menu', self)
        self.layout.addWidget(self.label)

        self.btn_refuel = QPushButton('1. Register Refueling', self)
        self.btn_refuel.clicked.connect(self.open_add_fueling_dialog)
        self.layout.addWidget(self.btn_refuel)

        self.btn_consumption = QPushButton("2. Show Consumption", self)
        self.btn_consumption.clicked.connect(lambda: self.run_action(show_consumption))
        self.layout.addWidget(self.btn_consumption)

        self.btn_odometer = QPushButton("3. Show Odometer Comparative", self)
        self.btn_odometer.clicked.connect(lambda: self.run_action(show_odometer_differences_from_file))
        self.layout.addWidget(self.btn_odometer)

        self.btn_tires = QPushButton("4. Show Tires Pressure", self)
        self.btn_tires.clicked.connect(lambda: self.run_action(show_tire_pressure))
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
        dialog = AddFuelingDialog(self)
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            print("Abastecimento registrado com sucesso.")
        else:
            print("Registro cancelado.")


def main() -> None:
    import sys
    import traceback

    def excepthook(exc_type, exc_value, exc_tb):
        print("".join(traceback.format_exception(exc_type, exc_value, exc_tb)))

    sys.excepthook = excepthook

    app = QApplication(sys.argv)
    window = VehicleManagerApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
