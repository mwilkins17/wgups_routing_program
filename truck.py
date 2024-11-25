from datetime import datetime, timedelta
from data_loader import load_distance_table, load_address_data, load_package_data
from hash_table import HashTable

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
    
    def __repr__(self):
        """
        Provides a string representation of the Truck instance.

        Time Complexity: O(1) - Accessing and formatting instance attributes is constant time.
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

        Time Complexity:
        - Loading data: O(a), where a is the number of addresses.
        - Address-to-index mapping: O(a), where a is the number of addresses.
        - Package retrieval: O(p), where p is the number of packages assigned to the truck.
        - Delivery loop:
          - Outer loop (over packages): O(p), where p is the number of packages.
          - Inner loop (finding nearest package): O(p) per iteration.
          - Total complexity for the loop: O(p^2).
        Overall: O(a + p^2), where `a` is the number of addresses and `p` is the number of packages.
        """
        # Load all package and address data
        address_data = load_address_data()  # O(a)
        address_index_map = self.create_address_to_index_map(address_data)  # O(a)
        
        # Prepare a list of packages to deliver
        packages_to_deliver = []
        for package_id in self.packages:  # O(p)
            package = package_data.lookup(package_id)  # O(1) per lookup
            packages_to_deliver.append(package)

        # Reset the truck's package list to store packages in delivery order
        self.packages = []

        # Loop through packages, selecting the nearest one for delivery
        while packages_to_deliver:  # O(p) iterations
            min_distance = float("inf")

            # Find the nearest package destination
            for package in packages_to_deliver:  # O(p) per iteration
                distance = self.distance_bt_two_addresses(
                    address_index_map[self.location],  # O(1)
                    address_index_map[package.delivery_address]  # O(1)
                )
                if distance < min_distance:  # O(1)
                    min_distance = distance  # O(1)
                    next_package = package  # O(1)

            # Remove the nearest package and mark it as delivered
            packages_to_deliver.remove(next_package)  # O(p)
            self.packages.append(next_package.package_id)  # O(1)

            # Update truck’s miles, travel time, and location
            self.miles += min_distance  # O(1)
            self.total_time_traveled += timedelta(hours=min_distance/self.speed)  # O(1)
            self.location = next_package.delivery_address  # O(1)

            # Set the delivery time for this package
            next_package.depart_time = self.depart_time  # O(1)
            next_package.delivery_time = self.total_time_traveled  # O(1)
            next_package.truck = self.truck_number  # O(1)

    def distance_bt_two_addresses(self, address1: int, address2: int) -> float:
        """
        Returns the distance between two addresses using their indices in the distance matrix.

        Time Complexity: O(1) - Accessing the distance from the matrix is constant time.
        """
        distance_data = load_distance_table()  # Assumed preloaded matrix
        distance = distance_data[address1][address2]
        if distance == '':
            distance = distance_data[address2][address1]
        return float(distance)  # O(1)

    def create_address_to_index_map(self, address_data: list) -> dict[str, int]:
        """
        Creates a dictionary that maps each address to its respective index
        in the distance matrix.

        Time Complexity: O(a), where a is the number of addresses.
        """
        address_to_idx = {}
        for address in address_data:  # O(a)
            index = int(address[0])  # O(1)
            address_name = address[2]  # O(1)
            address_to_idx[address_name] = index  # O(1)
        return address_to_idx
