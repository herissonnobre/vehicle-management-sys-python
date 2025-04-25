from menus.menu import show_main_menu
from menus.menu_fuel import show_fuel_menu
from menus.menu_tire import show_tire_menu
from menus.menu_vehicle import show_vehicle_menu


def main():
    while True:
        choice = show_main_menu()
        if choice == '1':
            show_fuel_menu()
        elif choice == '2':
            show_tire_menu()
        elif choice == '3':
            show_vehicle_menu()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
