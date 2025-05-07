from dataclasses import dataclass
from typing import Optional


@dataclass
class RefuelRecord:
    date: str
    odometer: int
    fuel_type: str
    total_value: Optional[float] = None
    price_per_liter: Optional[float] = None
    liters: Optional[float] = None

    def complete_data(self):
        if self.total_value is None and self.price_per_liter is not None and self.liters is not None:
            self.total_value = round(self.price_per_liter * self.liters, 2)
        elif self.price_per_liter is None and self.total_value is not None and self.liters is not None:
            self.price_per_liter = round(self.total_value / self.liters, 2)
        elif self.liters is None and self.total_value is not None and self.price_per_liter is not None:
            self.liters = round(self.total_value / self.price_per_liter, 2)
