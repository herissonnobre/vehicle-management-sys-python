def main() -> None:
    """Runs the vehicle management CLI menu."""
    from services.fueling import add_fueling, show_consumption
    from services.tire import show_tire_pressure_adjustments
    from services.odometer import show_odometer_differences_from_file

    options = {
        "1": add_fueling,
        "2": show_consumption,
        "3": show_odometer_differences_from_file,
        "4": show_tire_pressure_adjustments,
    }

    try:
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

            action = options.get(choice)
            if action:
                action()
            else:
                print("Invalid option. Please try again.")
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting...")


if __name__ == "__main__":
    main()
