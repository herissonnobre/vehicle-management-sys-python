import csv
import os
from models.tire import Tire

VEHICLE_FILE = "data/vehicle.csv"


def register_vehicle():
    print("\n--- Register Vehicle ---")
    brand = input("Brand: ")
    model = input("Model: ")
    version = input("Version: ")
    plate = input("License plate: ")
    year = input("Year: ")

    print("\nOriginal tire")
    orig_width = input("Width (mm): ")
    orig_ratio = input("Aspect ratio (%): ")
    orig_rim = input("Rim (in): ")

    print("\nCurrent tire")
    curr_width = input("Width (mm): ")
    curr_ratio = input("Aspect ratio (%): ")
    curr_rim = input("Rim (in): ")

    os.makedirs("data", exist_ok=True)

    with open(VEHICLE_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            brand, model, version, plate, year,
            orig_width, orig_ratio, orig_rim,
            curr_width, curr_ratio, curr_rim
        ])

    print("Vehicle registered successfully.")


def view_vehicle():
    if not os.path.exists(VEHICLE_FILE):
        print("No vehicle registered yet.")
        return

    with open(VEHICLE_FILE, mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Ignora o cabeçalho

        row = next(reader, None)  # Lê a segunda linha (dados do veículo)

        if row:
            (
                brand, model, version, plate, year,
                orig_width, orig_ratio, orig_rim,
                curr_width, curr_ratio, curr_rim
            ) = row

            print("\n--- Current Vehicle ---")
            print(f"Brand: {brand}")
            print(f"Model: {model}")
            print(f"Version: {version}")
            print(f"Plate: {plate}")
            print(f"Year: {year}")

            print("\nOriginal tire:")
            print(f"  Width: {orig_width} mm")
            print(f"  Aspect Ratio: {orig_ratio} %")
            print(f"  Rim: {orig_rim} in")

            print("Current tire:")
            print(f"  Width: {curr_width} mm")
            print(f"  Aspect Ratio: {curr_ratio} %")
            print(f"  Rim: {curr_rim} in")
        else:
            print("Vehicle data is missing or corrupted.")
