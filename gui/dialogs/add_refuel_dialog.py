from PyQt6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox

from models.refuel import RefuelRecord
from services.fueling import read_refuels, write_refuels, CSV_PATH


class AddRefuelDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Register Refueling")

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.date_input = QLineEdit()
        self.date_input.setInputMask("0000-00-00")  # yyyy-mm-dd

        self.odometer_input = QLineEdit()
        self.fuel_type_input = QLineEdit()
        self.total_value_input = QLineEdit()
        self.price_per_liter_input = QLineEdit()
        self.liters_input = QLineEdit()

        form_layout.addRow("Date (YYYY-MM-DD):", self.date_input)
        form_layout.addRow("Odometer (km):", self.odometer_input)
        form_layout.addRow("Fuel Type:", self.fuel_type_input)
        form_layout.addRow("Total Value (R$):", self.total_value_input)
        form_layout.addRow("Price Per Liter (R$):", self.price_per_liter_input)
        form_layout.addRow("Liters (l):", self.liters_input)

        layout.addLayout(form_layout)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.save_data)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

        self.total_value_input.textChanged.connect(self.recalculate_fields)
        self.price_per_liter_input.textChanged.connect(self.recalculate_fields)
        self.liters_input.textChanged.connect(self.recalculate_fields)

    def get_float_or_none(self, text: str) -> float | None:
        text = text.strip().replace(",", ".")

        try:
            return float(text) if text else None
        except ValueError:
            return None

    def recalculate_fields(self):
        # Evita loops ao editar os campos programaticamente

        total = self.get_float_or_none(self.total_value_input.text())
        price = self.get_float_or_none(self.price_per_liter_input.text())
        liters = self.get_float_or_none(self.liters_input.text())

        new_total, new_price, new_liters = self.calculate_missing_field(total, price, liters)

        # Apenas preenche o campo que estava vazio
        if total is None and new_total is not None:
            self.total_value_input.blockSignals(True)
            self.total_value_input.setText(f"{new_total:.2f}")
            self.total_value_input.blockSignals(False)

        elif price is None and new_price is not None:
            self.price_per_liter_input.blockSignals(True)
            self.price_per_liter_input.setText(f"{new_price:.3f}")
            self.price_per_liter_input.blockSignals(False)

        elif liters is None and new_liters is not None:
            self.liters_input.blockSignals(True)
            self.liters_input.setText(f"{new_liters:.2f}")
            self.liters_input.blockSignals(False)

    def calculate_missing_field(self, total, price, liters):
        try:
            if total is None and price is not None and liters is not None:
                return price * liters, price, liters
            elif price is None and total is not None and liters is not None and liters != 0:
                return total, total / liters, liters
            elif liters is None and total is not None and price is not None and price != 0:
                return total, price, total / price
        except Exception:
            return None, None, None

        return None, None, None

    def save_data(self):
        try:
            record = RefuelRecord(
                date=self.date_input.text(),
                odometer=int(self.odometer_input.text()),
                fuel_type=self.fuel_type_input.text(),
                total_value=self.get_float_or_none(self.total_value_input.text()),
                price_per_liter=self.get_float_or_none(self.price_per_liter_input.text()),
                liters=self.get_float_or_none(self.liters_input.text())
            )

            record.complete_data()  # Calcula o campo faltante se necessário

            records = read_refuels()
            records.append(record)
            write_refuels(CSV_PATH, records)

            QMessageBox.information(self, "Success", "Fueling registered successfully.")
            self.accept()

        except ValueError as e:
            QMessageBox.critical(self, "Invalid Input", f"Check your input: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Unexpected error: {e}")
