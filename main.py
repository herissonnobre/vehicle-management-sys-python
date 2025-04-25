# original_tire = Tire(width=195, aspect_ratio=55, rim=15)
# replacement_tire = Tire(width=185, aspect_ratio=60, rim=15)
from models.tire import Tire
from services.odometer_calc import calculate_odometer_difference

CSV_PATH = 'data/refuels.csv'

def run_odometer_comparison():
    print("\n--- Odometer Comparison ---")
    print("Enter original tire specifications:")
    original = Tire(
        width=int(input("Width (mm): ")),
        aspect_ratio=int(input("Aspect ratio (%): ")),
        rim=int(input("Rim (inches): "))
    )

    print("\nEnter replacement tire specifications:")
    replacement = Tire(
        width=int(input("Width (mm): ")),
        aspect_ratio=int(input("Aspect ratio (%): ")),
        rim=int(input("Rim (inches): "))
    )

    result = calculate_odometer_difference(original, replacement)

    print("\n--- Comparison Result ---")
    print(f"Original diameter: {result['original_diameter']} mm")
    print(f"Replacement diameter: {result['replacement_diameter']} mm")
    print(f"Difference: {result['difference_percentage']}%")
    print(f"Odometer {result['direction']}")
    print(f"Real distance per 100 km shown on odometer: {result['real_distance_per_100km']} km\n")

def show_main_menu():
    print("\n--- Main Menu ---")
    print("1. Fuel Menu")
    print("2. Tire Menu")
    print("0. Exit")
    return input("Choose an option: ")

def show_fuel_menu():
    while True:
        print("\n--- Fuel Menu ---")
        print("1. Add Fueling")
        print("2. List Fuelings")
        print("0. Back to Main Menu")
        choice = input("Choose an option: ")

        if choice == '1':
            add_fueling()
        elif choice == '2':
            list_fuelings()
        elif choice == '0':
            break
        else:
            print("Invalid option. Please try again.")


def add_fueling():
    print("\n--- Add Fueling ---")
    # Gather fueling information from the user
    date = input("Date (YYYY-MM-DD): ")
    odometer = float(input("Odometer reading (km): "))
    fuel_type = input("Fuel type: ")

    total_value_input = input("Total value of fueling: ")
    total_value = float(total_value_input) if total_value_input else None

    fuel_price_input = input("Price per liter: ")
    fuel_price = float(fuel_price_input) if fuel_price_input else None

    quantity_input = input("Fuel quantity (liters): ")
    quantity = float(quantity_input) if quantity_input else None

    # Calculate values if needed
    if total_value and fuel_price:
        quantity = total_value / fuel_price
    elif total_value and quantity:
        fuel_price = total_value / quantity
    elif quantity and fuel_price:
        total_value = quantity * fuel_price

    # Save the fueling (in CSV or any other format, you can adjust this later)
    with open(CSV_PATH, 'a') as file:
        file.write(f"{date},{odometer},{fuel_type},{total_value},{fuel_price},{quantity}\n")

    print("Fueling added successfully!")


def list_fuelings():
    print("\n--- Fueling List ---")
    try:
        with open(CSV_PATH, 'r') as file:
            lines = file.readlines()
            for line in lines:
                print(line.strip())
    except FileNotFoundError:
        print("No fueling records found.")

def main():
    while True:
        choice = show_main_menu()
        if choice == '1':
            show_fuel_menu()
        elif choice == '2':
            print("\n--- Tire Menu ---")
            print("1. Compare Odometer Readings")
            print("0. Back to Main Menu")
            tire_choice = input("Choose an option: ")
            if tire_choice == '1':
                run_odometer_comparison()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()

