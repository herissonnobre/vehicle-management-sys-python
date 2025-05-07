import pytest
from models.refuel import RefuelRecord
from services.fueling import calculate_average_consumption


def test_calculate_average_consumption_with_valid_data():
    records = [
        RefuelRecord(date="2023-01-01", odometer=10000, fuel_tipe="Gasoline", liters=50),
        RefuelRecord(date="2023-01-15", odometer=10500, fuel_tipe="Gasoline", liters=25),
        RefuelRecord(date="2023-02-01", odometer=11000, fuel_tipe="Gasoline", liters=30),
    ]
    result = calculate_average_consumption(records)
    assert result == pytest.approx(20.0, rel=1e-2)


def test_calculate_average_consumption_with_no_liters():
    records = [
        RefuelRecord(date="2023-01-01", odometer=10000, fuel_tipe="Gasoline"),
        RefuelRecord(date="2023-01-15", odometer=10500, fuel_tipe="Gasoline", liters=25),
    ]
    result = calculate_average_consumption(records)
    assert result == pytest.approx(20.0, rel=1e-2)


def test_calculate_average_consumption_with_zero_liters():
    records = [
        RefuelRecord(date="2023-01-01", odometer=10000, fuel_tipe="Gasoline", liters=0),
        RefuelRecord(date="2023-01-15", odometer=10500, fuel_tipe="Gasoline", liters=25),
    ]
    result = calculate_average_consumption(records)
    assert result == pytest.approx(20.0, rel=1e-2)


def test_calculate_average_consumption_with_invalid_km():
    records = [
        RefuelRecord(date="2023-01-01", odometer=10000, fuel_tipe="Gasoline", liters=50),
        RefuelRecord(date="2023-01-15", odometer=9900, fuel_tipe="Gasoline", liters=25),
    ]
    result = calculate_average_consumption(records)
    assert result == pytest.approx(0.0, rel=1e-2)


def test_calculate_average_consumption_with_empty_records():
    records = []
    result = calculate_average_consumption(records)
    assert result == 0.0


def test_calculate_average_consumption_with_missing_odometer():
    records = [
        RefuelRecord(date="2023-01-01", odometer=10000, fuel_tipe="Gasoline", liters=50),
        RefuelRecord(date="2023-01-15", odometer=None, fuel_tipe="Gasoline", liters=25),
    ]
    result = calculate_average_consumption(records)
    assert result == 0.0
