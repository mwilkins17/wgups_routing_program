# hash_table.py

from package import Package

class HashTable:
    """
    Implements a hash table for storing and managing packages efficiently.
    """

    def __init__(self, size=40):
        # Initializes the hash table with a set size
        self.size = size
        self.table = [None] * size

    def _hash_key(self, key:int) -> int:
        """private method that generates a index (bucket) by
        taking the key mod size of the list and returning that
        value"""
        return key % self.size

    def insert(self, package_id, address, deadline, city, zip_code, weight, status="at hub", delivery_time=None):
        """
        Inserts a package with all relevant details into the hash table.
        """
        package = Package(package_id, address, deadline, city, zip_code, weight, status, delivery_time)
        index = self.hash_function(package_id)
        while self.table[index] is not None:
            if self.table[index].package_id == package_id:
                self.table[index] = package
                return
            index = (index + 1) % self.size
        self.table[index] = package

    def remove(self, package_id):
        """
        Removes a package from the hash table by package_id and rehashes if necessary.
        """
        index = self.hash_function(package_id)
        while self.table[index] is not None:
            if self.table[index].package_id == package_id:
                removed_package = self.table[index]
                self.table[index] = None
                next_index = (index + 1) % self.size
                while self.table[next_index] is not None:
                    rehashed_package = self.table[next_index]
                    self.table[next_index] = None
                    self.insert(
                        rehashed_package.package_id,
                        rehashed_package.address,
                        rehashed_package.deadline,
                        rehashed_package.city,
                        rehashed_package.zip_code,
                        rehashed_package.weight,
                        rehashed_package.status,
                        rehashed_package.delivery_time
                    )
                    next_index = (next_index + 1) % self.size
                return removed_package
            index = (index + 1) % self.size
        return None
