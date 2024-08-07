import race_pb2

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
add_methods(race_pb2.Race)


print(race_pb2.Race.add_lap_time)

# Example usage
if __name__ == "__main__":
    driver = race_pb2.Driver(name="John Doe", nicknames=["Speedster", "The Flash"], age=30)


    race = race_pb2.Race(
        title="Grand Prix",
        driver=driver,
        total_laps=75,
        lap_times=[1.23, 1.45, 1.37, 1.50],
    )

    race.add_lap_time(1.55)
    avg_lap_time = race.get_average_lap_time()

    # Serialize to string
    serialized_race = race.SerializeToString()

    # Deserialize from string
    deserialized_race = race_pb2.Race()
    deserialized_race.ParseFromString(serialized_race)

    # Print the data
    print(f"Race Title: {deserialized_race.title}")
    print(f"Driver Name: {deserialized_race.driver.name}")
    print(f"Total Laps: {deserialized_race.total_laps}")
    print(f"Lap Times: {deserialized_race.lap_times}")
    print(f"Average Lap Time: {avg_lap_time}")
