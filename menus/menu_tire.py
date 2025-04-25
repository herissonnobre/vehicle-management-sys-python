from services.odometer_calc import calculate_odometer_difference
from models.tire import Tire


def show_tire_menu():
    print("\n--- Tire Menu ---")
    print("Compare original vs new tire to check odometer difference")

    try:
        print("\nOriginal Tire")
        width = int(input("Width (mm): "))
        aspect_ratio = int(input("Aspect ratio (%): "))
        rim = int(input("Rim (inches): "))
        original = Tire(width=width, aspect_ratio=aspect_ratio, rim=rim)

        print("\nReplacement Tire")
        width = int(input("Width (mm): "))
        aspect_ratio = int(input("Aspect ratio (%): "))
        rim = int(input("Rim (inches): "))
        replacement = Tire(width=width, aspect_ratio=aspect_ratio, rim=rim)

        result = calculate_odometer_difference(original, replacement)

        print(f"\nOdometer {result['direction']} by {abs(result['difference_percentage']):.2f}%")
        print(f"When odometer shows 100km, real distance is: {result['real_distance_per_100km']:.2f} km")
    except ValueError:
        print("Invalid input. Please enter numbers only.")
