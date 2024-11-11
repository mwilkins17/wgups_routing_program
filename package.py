class Package:
    """
    Represents a delivery package with all necessary details.
    """

    def __init__(self, package_id, address, deadline, city, zip_code, weight, status="at hub", delivery_time=None):
        # Unique identifier for the package
        self.package_id = package_id
        self.address = address
        self.deadline = deadline
        self.city = city
        self.zip_code = zip_code
        self.weight = weight
        self.status = status
        self.delivery_time = delivery_time