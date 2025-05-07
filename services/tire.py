import csv

CSV_PATH = 'data/vehicle.csv'
DEFAULT_PRESSURE = 32  # pressão original (em psi)

def calculate_volume(width, aspect, rim):
    # Aproximação do volume do pneu (não é o volume real, mas serve para cálculo proporcional)
    return width * aspect * (rim * 25.4)  # rim em polegadas convertido para mm

def calculate_adjusted_pressure(original_volume, current_volume, original_pressure=DEFAULT_PRESSURE):
    return original_pressure * (original_volume / current_volume)

def show_tires_pressure():
    with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Extrai dados
            original_width = int(row['original_width'])
            original_aspect = int(row['original_aspect'])
            original_rim = int(row['original_rim'])

            current_width = int(row['current_width'])
            current_aspect = int(row['current_aspect'])
            current_rim = int(row['current_rim'])

            # Calcula volumes
            original_volume = calculate_volume(original_width, original_aspect, original_rim)
            current_volume = calculate_volume(current_width, current_aspect, current_rim)

            # Calcula nova pressão
            adjusted_pressure = calculate_adjusted_pressure(original_volume, current_volume)

            print(f"Veículo: {row['brand']} {row['model']} {row['version']} ({row['plate']})")
            print(f"Pressão original (estimada): {DEFAULT_PRESSURE} psi")
            print(f"Pressão ajustada para nova medida: {adjusted_pressure:.1f} psi\n")

