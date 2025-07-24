import sys
import traceback

from PyQt6.QtWidgets import QApplication

from gui.main_window import VehicleManagerApp


def main() -> None:
    def excepthook(exc_type, exc_value, exc_tb):
        print("".join(traceback.format_exception(exc_type, exc_value, exc_tb)))

    sys.excepthook = excepthook

    app = QApplication(sys.argv)
    window = VehicleManagerApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
