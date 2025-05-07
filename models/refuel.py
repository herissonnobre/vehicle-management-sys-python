from dataclasses import dataclass
from typing import Optional


@dataclass
class RefuelRecord:
    """
    Represents a refueling event with details about the transaction.

    Attributes:
        date (str): Date of the refueling in the format YYYY-MM-DD.
        odometer (int): Odometer reading at the time of refueling (in km).
        fuel_type (str): Type of fuel used (e.g., Gasoline, Diesel, etc.).
        total_value (Optional[float]): Total amount spent on the refueling.
        price_per_liter (Optional[float]): Price per liter of fuel.
        liters (Optional[float]): Quantity of fuel in liters.
    """
    date: str
    odometer: int
    fuel_type: str
    total_value: Optional[float] = None
    price_per_liter: Optional[float] = None
    liters: Optional[float] = None

    def __post_init__(self):
        """
        Validates that at least two of the three numerical fields (total_value,
        price_per_liter, liters) are provided so that the third can be calculated
        if missing.

        Raises:
            ValueError: If fewer than two of the three key numeric fields are provided.
        """
        if sum(v is not None for v in [self.total_value, self.price_per_liter, self.liters]) < 2:
            raise ValueError(
                "At least two of the fields (total_value, price_per_liter, liters) must be provided."
            )

    def complete_data(self):
        """
        Completes the missing numeric field (total_value, price_per_liter, or liters)
        by calculating it based on the other two provided fields.

        The method assumes that two out of the three fields are filled.
        The missing one will be calculated with precision up to two decimal places.
        """
        if self.total_value is None and self.price_per_liter is not None and self.liters is not None:
            self.total_value = round(self.price_per_liter * self.liters, 2)
        elif self.price_per_liter is None and self.total_value is not None and self.liters is not None:
            self.price_per_liter = round(self.total_value / self.liters, 2)
        elif self.liters is None and self.total_value is not None and self.price_per_liter is not None:
            self.liters = round(self.total_value / self.price_per_liter, 2)
