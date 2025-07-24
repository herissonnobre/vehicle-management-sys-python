from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, \
    QHeaderView, QFrame, QLabel, QPushButton, QTableWidgetItem

from gui.dialogs import (
    AddRefuelDialog,
    ShowConsumptionDialog,
    ShowOdometerDialog,
    ShowTirePressureDialog,
)
from services.fueling import read_refuels


class VehicleManagerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(
            "D:\\Users\\herisson\\documents\\profissional\\portfolio\\gestao-veicular-python\\assets\\icons\\favicon-32x32.png"))

        self.setWindowTitle("CMSys")
        self.setGeometry(100, 100, 1280, 800)  # Para telas Full HD

        self.layout = QVBoxLayout()

        # 1. Painéis de Informações (Total KM e Total Gasto)
        self.info_layout = QHBoxLayout()
        self.km_box = self.create_info_box("Total KM Percorrido", "0 km")
        self.cost_box = self.create_info_box("Total Gasto", "R$ 0,00")
        self.info_layout.addWidget(self.km_box)
        self.info_layout.addWidget(self.cost_box)

        self.layout.addLayout(self.info_layout)

        # 2. Tabela de abastecimentos
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Data", "Odômetro", "Combustível", "Total (R$)", "Preço/Litro", "Litros"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.layout.addWidget(self.table)

        # 3. Botões de ação
        self.button_layout = QHBoxLayout()
        self.add_button("Registrar Abastecimento", self.open_add_fueling_dialog)
        self.add_button("Mostrar Consumo", self.open_show_consumption_dialog)
        self.add_button("Mostrar Odômetro", self.open_show_odometer_dialog)
        self.add_button("Mostrar Pressão Pneus", self.open_show_tires_dialog)
        self.add_button("Sair", self.close)

        self.layout.addLayout(self.button_layout)

        self.setLayout(self.layout)
        self.refresh_data()

    def is_dark_theme(self) -> bool:
        palette = self.palette()
        bg_color = palette.color(QPalette.ColorRole.Window)
        return bg_color.value() < 128  # 0 (preto) a 255 (branco)

    def create_info_box(self, title: str, value: str):
        box = QFrame()
        box.setFrameShape(QFrame.Shape.StyledPanel)

        dark = self.is_dark_theme()
        print(dark)

        bg_color = "#2b2b2b" if dark else "#f0f0f0"
        border_color = "#444444" if dark else "#cccccc"
        text_color = "#ffffff" if dark else "#000000"
        value_color = "#00ffcc" if dark else "#003366"

        # Cores adaptadas para modo escuro
        box.setStyleSheet(f"""
                QFrame {{
                    background-color: {bg_color};
                    border: 1px solid {border_color};
                    padding: 20px;
                    border-radius: 8px;
                }}
            """)

        layout = QVBoxLayout()

        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(f"font-weight: bold; font-size: 16px; color: {text_color};")

        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_label.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {value_color};")

        box.value_label = value_label
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        box.setLayout(layout)
        return box

    def add_button(self, text, callback):
        btn = QPushButton(text)
        btn.setFixedHeight(40)
        btn.clicked.connect(callback)
        self.button_layout.addWidget(btn)

    def refresh_data(self):
        records = read_refuels()

        # Atualiza informações superiores
        total_km = 0
        total_spent = 0.0

        sorted_records = sorted(records, key=lambda r: r.odometer)
        if len(sorted_records) >= 2:
            total_km = sorted_records[-1].odometer - sorted_records[0].odometer

        for r in records:
            if r.total_value:
                total_spent += r.total_value

        self.km_box.value_label.setText(f"{total_km} km")
        self.cost_box.value_label.setText(f"R$ {total_spent:.2f}")

        # Atualiza tabela
        self.table.setRowCount(len(records))
        for row, r in enumerate(records):
            self.table.setItem(row, 0, QTableWidgetItem(r.date))
            self.table.setItem(row, 1, QTableWidgetItem(str(r.odometer)))
            self.table.setItem(row, 2, QTableWidgetItem(r.fuel_type))
            self.table.setItem(row, 3, QTableWidgetItem(f"{r.total_value:.2f}" if r.total_value else ""))
            self.table.setItem(row, 4, QTableWidgetItem(f"{r.price_per_liter:.2f}" if r.price_per_liter else ""))
            self.table.setItem(row, 5, QTableWidgetItem(f"{r.liters:.2f}" if r.liters else ""))

    def open_add_fueling_dialog(self):
        dialog = AddRefuelDialog(self)
        if dialog.exec():
            self.refresh_data()

    def open_show_consumption_dialog(self):
        dialog = ShowConsumptionDialog(self)
        dialog.exec()

    def open_show_odometer_dialog(self):
        dialog = ShowOdometerDialog(self)
        dialog.exec()

    def open_show_tires_dialog(self):
        dialog = ShowTirePressureDialog(self)
        dialog.exec()
