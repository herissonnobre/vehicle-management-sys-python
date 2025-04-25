from vehicle import register_vehicle, view_vehicle


def show_vehicle_menu():
    while True:
        print("\n--- Vehicle Menu ---")
        print("1. Register vehicle")
        print("2. View current vehicle")
        print("0. Back")

        choice = input("Choose an option: ")

        if choice == "1":
            register_vehicle()
        elif choice == "2":
            view_vehicle()
        elif choice == "0":
            break
        else:
            print("Invalid option. Please try again.")
