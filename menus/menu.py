from menus.menu_fuel import show_fuel_menu
from menus.menu_tire import show_tire_menu
from menus.menu_vehicle import show_vehicle_menu


def show_main_menu():
    while True:
        print("\n=== Vehicle Management Menu ===")
        print("1. Fueling")
        print("2. Tires")
        print("3. Vehicle")
        print("0. Exit")

        choice = input("Choose an option: ")

        return choice
