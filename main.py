from tires.odometer import calculate_odometer_difference
from models.tire import Tire

original_tire = Tire(width=195, aspect_ratio=55, rim=15)
replacement_tire = Tire(width=185, aspect_ratio=60, rim=15)

result = calculate_odometer_difference(original_tire, replacement_tire)

print(f"Odometer difference: {result['difference_percentage']:.2f}%")

if result['direction'] == 'underreports':
    print(
        f"The odometer will underreport distance. For every 100 km on the odometer, "
        f"the actual distance is approximately {result['actual_distance_per_100km']:.2f} km."
    )
else:
    print(
        f"The odometer will overreport distance. For every 100 km on the odometer, "
        f"the actual distance is approximately {result['actual_distance_per_100km']:.2f} km."
    )