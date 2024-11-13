from datetime import timedelta

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
        """
        self.package_id = package_id
        self.delivery_address = address
        self.delivery_deadline = deadline
        self.delivery_city = city
        self.delivery_state = state
        self.delivery_zip_code = zip_code
        self.package_weight = weight
        self.notes = notes
        self.status = status
        self.truck = None
        self.depart_time = None
        self.delivery_time = None
    
    def __str__(self):
        """
        Returns a string representation of the package with detailed information.
        """
        return f"""
        Package ID: {self.package_id}
        Address: {self.delivery_address}
        Deadline: {self.delivery_deadline}
        City: {self.delivery_city}
        State: {self.delivery_state}
        Zip Code: {self.delivery_zip_code}
        Weight: {self.package_weight}
        Status: {self.status}
        Truck Number:{self.truck}
        Depart Time: {self.depart_time}
        Delivery Time: {self.delivery_time}
        Notes: {self.notes}"""
    
    # Change delivery status of package
    def update_status(self, time):
        if self.delivery_time < time:
            self.status = "delivered"
        elif self.depart_time <= time <= self.delivery_time:
            self.status = "en route"
            self.delivery_time = timedelta(0)
        else:
            self.status = "at hub"
            self.delivery_time = timedelta(0)
