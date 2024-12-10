class Package:
    """
    Represents a delivery package with all necessary details.
    """

    def __init__(self, package_id, address, deadline, city, state, zip_code, weight, notes, status):
        """
        Initializes a Package instance with all required attributes.

        Parameters:
        - package_id: Unique identifier for the package.
        - address: The delivery address for the package.
        - deadline: The deadline by which the package must be delivered.
        - city: City of the delivery address.
        - state: State of the delivery address.
        - zip_code: Zip code for the delivery address.
        - weight: Weight of the package in pounds.
        - notes: Any special instructions or notes about the package.
        - status: Current status of the package (default is 'at hub').
        - delivery_time: Time at which the package is delivered (default is None, to be set upon delivery).

        Time Complexity: O(1) - Initializing an object involves constant time operations.
        """
        # Assigning attributes to the package instance
        self.package_id = package_id
        self.delivery_address = address
        self.delivery_deadline = deadline
        self.delivery_city = city
        self.delivery_state = state
        self.delivery_zip_code = zip_code
        self.package_weight = weight
        self.notes = notes
        self.status = status

        # Additional attributes related to delivery
        self.truck = None  # Truck assigned to deliver the package
        self.depart_time = None  # Time the package departs the hub
        self.delivery_time = None  # Time the package is delivered
    
    def __str__(self):
        """
        Returns a string representation of the package with detailed information.

        Time Complexity: O(1) - The string representation involves accessing instance attributes,
        which are constant-time operations.
        """
        pkg_str = str()
        str_1 = f"Package ID: {self.package_id}, Address: {self.delivery_address}, Deadline: {self.delivery_deadline}"
        str_2 = f" City: {self.delivery_city}, State: {self.delivery_state}, Zip Code: {self.delivery_zip_code},"
        str_3 = f" Weight: {self.package_weight}, Status: {self.status}, Truck Number: {self.truck},"
        str_4 = f" Depart Time: {self.depart_time}, Delivery Time: {self.delivery_time}, Notes: {self.notes}"
        return (str_1 + str_2 + str_3 + str_4)
    
    def update_status(self, time):
        """
        Updates the status of the package based on the current time.

        Parameters:
        - time: A timedelta object representing the current time.

        Status Updates:
        - "delivered": If the package's delivery time is earlier than the current time.
        - "en route": If the package has departed but not yet been delivered.
        - "at hub": If the package is still at the hub.

        Time Complexity: O(1) - The status update involves a series of constant-time comparisons
        and attribute updates.
        """
        if self.delivery_time and self.delivery_time < time:
            # Package has been delivered
            self.status = "delivered"
        elif self.depart_time and self.depart_time <= time <= self.delivery_time:
            # Package is currently being delivered
            self.status = "en route"
            self.delivery_time = None
        else:
            # Package is still at the hub
            self.status = "at hub"
            self.truck = None  # Truck assigned to deliver the package
            self.depart_time = None  # Time the package departs the hub
            self.delivery_time = None  # Time the package is delivered

    def reset_package(self):
        self.truck = None  # Truck assigned to deliver the package
        self.depart_time = None  # Time the package departs the hub
        self.delivery_time = None  # Time the package is delivered
        self.status = 'at hub'