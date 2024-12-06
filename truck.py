import datetime

class Truck:
    """
    Represents a delivery truck, including its routing and delivery functionality.
    """

    def __init__(self, truck_number: int, location: str, time: datetime):
        """
        Initializes a Truck instance with the given parameters.

        Time Complexity: O(1) - Initialization involves setting up attributes, which are constant-time operations.
        """
        self.truck_number = truck_number
        self.location = location
        self.speed = 18  # Fixed speed
        self.miles = 0.0  # Initial mileage
        self.packages = []  # Packages assigned to the truck
        self.depart_time = time  # Departure time
        self.total_time_traveled = time  # Total time spent traveling

    def clear(self):
        """
        Resets the truck's state for reuse, clearing packages, mileage, and time data.
        
        Time Complexity: O(1) - Resetting attributes involves constant-time operations.
        """
        self.miles = 0.0
        self.packages.clear()  # Efficiently clears the list of packages
        self.location = "4001 South 700 East"  # Resets to the hub location
        self.total_time_traveled = self.depart_time  # Resets to the departure time

    def __repr__(self):
        """
        Provides a string representation of the Truck instance.

        Time Complexity: O(1) - Accessing and formatting instance attributes is constant time.
        """
        return f"""
        Truck Number: {self.truck_number},
        Location: {self.location}, 
        Speed: {self.speed},
        Mileage: {self.miles},
        Packages: {self.packages},
        Depart Time: {self.depart_time},
        Total Time Traveled: {self.total_time_traveled}"""
