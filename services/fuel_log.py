import csv

from models.refuel import RefuelRecord


def read_refuels(file_path: str) -> list[RefuelRecord]:
    records = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            record = RefuelRecord(
                date=row['date'],
                odometer=int(float(row['odometer'])),
                fuel_tipe=row['fuel_type'],
                total_value=float(row['total_value']) if row['total_value'] else None,
                price_per_liter=float(row['price_per_liter']) if row['price_per_liter'] else None,
                liters=float(row['liters']) if row['liters'] else None,
            )
            record.complete_data()
            records.append(record)
    return records

def write_refuels(file_path: str, records: list[RefuelRecord]):
    with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames= ['date', 'odometer', 'fuel_type', 'total_value', 'price_per_liter', 'liters']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for r in records:
            writer.writerow({
                'date': r.date,
                'odometer': r.odometer,
                'fuel_type': r.fuel_tipe,
                'total_value': f'{r.total_value:.2f}' if r.total_value is not None else '',
                'price_per_liter': f'{r.price_per_liter:.2f}' if r.price_per_liter is not None else '',
                'liters': f'{r.liters:.2f}' if r.liters is not None else '',
            })