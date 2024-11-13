from package import Package

class HashTable:
    """
    Implements a hash table for storing and managing packages efficiently.
    """

    def __init__(self, size=40):
        """
        Initializes the hash table with a specified size.
        
        Parameters:
        - size: The number of slots in the hash table, default is 40.
        
        Attributes:
        - table: A list of fixed size initialized with `None`, representing the hash table.
        """
        self.size = size
        self.table = [None] * size  # Initialize the hash table with empty slots

    def __str__(self):
        """
        Provides a string representation of all packages in the hash table.
        
        Returns:
        - A string containing all packages, each on a new line.
        """
        package_list = str()
        for package in self.table:
            package_list += f"{package}\n"
        return package_list

    def _hash(self, key: int) -> int:
        """
        Private method to calculate the hash index for a given key.
        
        Parameters:
        - key: The package ID for which the hash index is generated.
        
        Returns:
        - An integer representing the index in the hash table where the key should be stored.
        """
        return key % self.size

    def insert(self, package_id, package):
        """
        Inserts a package into the hash table using open addressing to handle collisions.
        
        Parameters:
        - package_id: Unique identifier of the package.
        - package: Package object containing all relevant package details.
        """
        index = self._hash(package_id)  # Compute the hash index
        # Resolve collisions using linear probing
        while self.table[index] is not None:
            if self.table[index].package_id == package_id:
                self.table[index] = package  # Update existing package
                return
            index = (index + 1) % self.size  # Move to the next slot if occupied
        self.table[index] = package  # Insert the package when an empty slot is found

    def lookup(self, package_id):
        """
        Finds and returns a package from the hash table by its package_id.
        
        Parameters:
        - package_id: The unique identifier for the package to locate.
        
        Returns:
        - The Package object if found, otherwise None.
        """
        index = self._hash(package_id)  # Get the index for the package_id
        # Linear probing to find the package if collisions occurred
        while self.table[index] is not None:
            if self.table[index].package_id == package_id:
                return self.table[index]  # Return the package if found
            index = (index + 1) % self.size  # Move to the next slot if not found
        return None  # Return None if the package was not found in the table