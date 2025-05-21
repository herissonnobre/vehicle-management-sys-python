import csv

CSV_PATH = 'data/vehicle.csv'
COLD_PRESSURE = 32
HOT_PRESSURE = 34


def show_tire_pressure():
    """
    Read vehicle data from the CSV and display fixed pressure recommendations.
    """
    with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print("-" * 50)
            print(f"Vehicle: {row['brand']} {row['model']} {row['version']} ({row['plate']})")
            print(f"Recommended pressure (cold): {COLD_PRESSURE} psi")
            print(f"Recommended pressure (hot):  {HOT_PRESSURE} psi")
            print("-" * 50)


if __name__ == "__main__":
    show_tire_pressure()
