from datetime import datetime, timedelta
from data_loader import load_distance_table, load_address_data, load_package_data
from hash_table import HashTable

class Truck:
    """
    Represents a delivery truck, including its routing and delivery functionality.
    """

    def __init__(self, truck_number:int, location:str, time:datetime):
        """
        Initializes a Truck instance with the given parameters.
        
        Parameters:
        - truck_number: A unique identifier for the truck.
        - location: The starting location for the truck.
        - time: The truck's departure time.
        
        Other attributes include:
        - speed: Fixed speed of 18 mph.
        - miles: Total miles traveled, initially set to 0.
        - packages: List of package IDs assigned to the truck.
        - depart_time: The truck's initial departure time.
        - total_time_traveled: Tracks the cumulative time spent traveling.
        """
        self.truck_number = truck_number
        self.location = location 
        self.speed = 18
        self.miles = 0.0 
        self.packages = []
        self.depart_time = time
        self.total_time_traveled = time
    
    def __repr__(self):
            """
            Provides a string representation of the Truck instance, detailing its capacity, 
            speed, mileage, location, packages, departure time, truck number, and travel time.
            """
            return f"""
            Capacity: {self.capacity},
            Speed: {self.speed},
            Mileage: {self.miles},
            Location: {self.location}, 
            Packages: {self.packages},
            Depart Time: {self.depart_time},
            Truck Number: {self.truck_number},
            Total Time Traveled: {self.total_time_traveled}"""

    def deliver_packages(self, package_data) -> None:
        """
        Manages the package delivery process for the truck.
        
        1. Loads package data and address data.
        2. Builds an address index map to access address indices quickly.
        3. Iteratively finds the closest package destination, updates truck's mileage,
           and marks each package's delivery time.
        """
        # Load all package and address data
        address_data = load_address_data()
        address_index_map = self.create_address_to_index_map(address_data)
        
        # Prepare a list of packages to deliver by retrieving each package’s details
        packages_to_deliver = []
        for package_id in self.packages:
            package = package_data.lookup(package_id)
            packages_to_deliver.append(package)

        # Reset the truck's package list to store packages in delivery order
        self.packages = []

        # Loop through packages, selecting the nearest one for delivery
        while packages_to_deliver:
            min_distance = float("inf")

            # Find the nearest package destination to the truck's current location
            for package in packages_to_deliver:
                # Calculate the distance from the current location to this package's address
                distance = self.distance_bt_two_addresses(
                    address_index_map[self.location],
                    address_index_map[package.delivery_address]
                )
                # Update the nearest package if this distance is the shortest
                if distance < min_distance:
                    min_distance = distance
                    next_package = package

            # Remove the nearest package from the list and mark it as delivered
            packages_to_deliver.remove(next_package)
            self.packages.append(next_package.package_id)  # Track delivery order


            # Update truck’s miles, travel time, and location after delivery
            self.miles += min_distance
            self.total_time_traveled += timedelta(hours=min_distance/self.speed)
            self.location = next_package.delivery_address

            # Set the delivery time for this package
            next_package.depart_time = self.depart_time
            next_package.delivery_time = self.total_time_traveled
            next_package.truck = self.truck_number

    def distance_bt_two_addresses(self, address1: int, address2: int) -> float:
        """
        Returns the distance between two addresses using their indices in the distance matrix.
        """
        distance_data = load_distance_table()
        distance = distance_data[address1][address2]
        if distance == '':
            distance = distance_data[address2][address1]
        return float(distance)
    
    def create_address_to_index_map(self, address_data: list) -> dict[str, int]:
        """
        Creates a dictionary that maps each address to its respective index
        in the distance matrix.
        
        Parameters:
        - address_data: List of addresses with indices.
        
        Returns:
        - A dictionary mapping each address name to its matrix index.
        """
        address_to_idx = {}
        # Loop through address data and map each address to its index
        for address in address_data:
            index = int(address[0])  # Index of the address in the matrix
            address_name = address[2]  # Address name
            address_to_idx[address_name] = index  # Map address name to index
        return address_to_idx
    

