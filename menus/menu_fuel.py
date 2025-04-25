from models.refuel import RefuelRecord
from services.fuel_log import read_refuels, write_refuels

CSV_PATH = 'data/refuels.csv'


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
    date = input("Date (YYYY-MM-DD): ")
    odometer = int(input("Odometer reading (km): "))
    fuel_type = input("Fuel type: ")

    total_value_input = input("Total value of fueling: ")
    total_value = float(total_value_input) if total_value_input else None

    price_input = input("Price per liter: ")
    price_per_liter = float(price_input) if price_input else None

    liters_input = input("Fuel quantity (liters): ")
    liters = float(liters_input) if liters_input else None

    record = RefuelRecord(
        date=date,
        odometer=odometer,
        fuel_tipe=fuel_type,
        total_value=total_value,
        price_per_liter=price_per_liter,
        liters=liters
    )

    record.complete_data()

    records = read_refuels(CSV_PATH)
    records.append(record)
    write_refuels(CSV_PATH, records)

    print("Fueling added successfully!")


def list_fuelings():
    print("\n--- Fueling List ---")
    try:
        records = read_refuels(CSV_PATH)
        if not records:
            print("No fueling records found.")
        else:
            for r in records:
                print(f"{r.date} | {r.odometer} km | {r.fuel_tipe} | "
                      f"R${r.total_value:.2f} | R${r.price_per_liter:.2f}/L | {r.liters:.2f} L")
    except FileNotFoundError:
        print("No fueling records found.")
