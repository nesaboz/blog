from race_pb2 import Race, Driver
from vehicle_pb2 import Vehicle
import base64
import sys


def serialize_to_string(message):
    if message is None:
        return None
    serialized = message.SerializeToString()
    encoded = base64.b64encode(serialized).decode('utf-8')
    return encoded


def parse_from_string(message, encoded_str):
    if isinstance(encoded_str, str):
        # Decode base64 string to bytes
        decoded_bytes = base64.b64decode(encoded_str)
    # elif sys.version_info[0] < 3 and isinstance(encoded_str, unicode):
    #     # For Python 2, handle unicode strings
    #     decoded_bytes = base64.b64decode(encoded_str.encode('utf-8'))
    # else:
    #     return None
    message.ParseFromString(decoded_bytes)
    return message


# Function to add methods dynamically to a protobuf message
def add_methods(cls):
    def add_lap_time(self, lap_time):
        self.lap_times.append(lap_time)

    def get_average_lap_time(self):
        if not self.lap_times:
            return None
        return sum(self.lap_times) / len(self.lap_times)

    cls.add_lap_time = add_lap_time
    cls.get_average_lap_time = get_average_lap_time

# Extend the Race class with new methods
add_methods(Race)


# print(race_pb2.Race.add_lap_time)

# print('-----')
# print(vehicle_pb2.Vehicle.UNKNOWN)
# print('-----')

# # Access the enum descriptor
# category_enum = vehicle_pb2.Vehicle.Category.DESCRIPTOR
# # List all enum values
# enum_values = {enum_value.name: enum_value.number for enum_value in category_enum.values}

# print("Vehicle Category Enum Values:")
# for name, value in enum_values.items():
#     print(f"{name}: {value}")
    
# print('-----')



# Example usage
if __name__ == "__main__":
    driver = Driver(name="John Doe", nicknames=["Speedster", "The Flash"], age=30)


    race = Race(
        title="Grand Prix",
        driver=driver,
        total_laps=75,
        lap_times=[1.23, 1.45, 1.37, 1.50],
        vehicle= Vehicle(
            id="1234",
            category=Vehicle.CAR,
            specs={
                "color": "red",
                "engine": "V8",
                "transmission": "manual"
                }
            )
        )

    race.add_lap_time(1.55)
    avg_lap_time = race.get_average_lap_time()

    # Serialize to string
    serialized_race = serialize_to_string(race)

    # Deserialize from string
    deserialized_race = parse_from_string(Race(), serialized_race)
    print('--------')
    print('--------')
    print('AFTER DESERIALIZATION')
    print('--------')
    print('--------')

    # Print the data
    print(f"Race Title: {deserialized_race.title}")
    print(f"Driver Name: {deserialized_race.driver.name}")
    print(f"Total Laps: {deserialized_race.total_laps}")
    print(f"Lap Times: {deserialized_race.lap_times}")
    print(f"Average Lap Time: {deserialized_race.get_average_lap_time()}")
    print(f"Vehicle {deserialized_race.vehicle.id}")

    print('--------')
    
    vehicle_instance = deserialized_race.vehicle
    
    # Accessing the map field
    print("\nVehicle specs:")
    for key, value in vehicle_instance.specs.items():
        print(f"{key}: {value}")

    # Adding a new spec
    vehicle_instance.specs["fuel"] = "gasoline"
    print("\nUpdated Vehicle specs:")
    for key, value in vehicle_instance.specs.items():
        print(f"{key}: {value}")
        
    # Set the oneof field us_model
    vehicle_instance.us_model = "WRXP138762M"
    
    print('set only us_model')
    print(f'us_model: {vehicle_instance.us_model}')
    print(f'eu_model: {vehicle_instance.eu_model}')

    print('set only eu model')
    # Setting the oneof field eu_model will clear the us_model field
    vehicle_instance.eu_model = "WRXP578927L"
    print(f'us_model: {vehicle_instance.us_model}')
    print(f'eu_model: {vehicle_instance.eu_model}')
    print('note that us_model was removed')
