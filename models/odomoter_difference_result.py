from dataclasses import dataclass


@dataclass
class OdometerDifferenceResult:
    original_diameter: float
    replacement_diameter: float
    difference_percentage: float
    direction: str
    real_distance_per_100km: float
