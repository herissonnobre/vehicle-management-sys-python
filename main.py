"""

"""
from services.fueling import add_fueling, show_consumption
from services.odometer import show_odometer_difference
from services.tire import show_tires_pressure


def main():
    """

    :return: None
    :rtype: NoneType
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


if __name__ == "__main__":
    main()
