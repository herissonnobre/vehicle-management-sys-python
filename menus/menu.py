from services.fueling import add_fueling, show_consumption
from services.odometer import show_odometer_difference
from services.tire import show_tires_pressure


def show_main_menu():
    """
    Displays the main menu for vehicle management and handles the user's choice.

    The function presents a menu with options to manage different aspects of vehicle
    data such as refueling, consumption, odometer comparison, and tire pressure. The
    user is prompted to select an option, and the corresponding functionality is executed.
    If an invalid option is selected, the user is prompted to try again. The menu remains
    active until the user selects the option to exit.

    :raises ValueError: If an invalid input is provided when choosing an option.
    """
    while True:
        print("\n=== Vehicle Management Menu ===")
        print("1. Register Refueling")
        print("2. Show Consumption")
        print("3. Show Odometer Comparative")
        print("4. Show Tires Pressure")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == "0":
            print("Exiting the program.")
            break
        elif choice == "1":
            add_fueling()
        elif choice == "2":
            show_consumption()
        elif choice == "3":
            show_odometer_difference()
        elif choice == "4":
            show_tires_pressure()
        else:
            print("Invalid option. Please try again.")