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

        Time Complexity: O(size) - Initializing the hash table involves creating a list of fixed size.
        """
        self.size = size
        self.table = [None] * size  # O(size)

    def __str__(self):
        """
        Provides a string representation of all packages in the hash table.
        
        Returns:
        - A string containing all packages, each on a new line.

        Time Complexity: O(n), where n is the number of slots in the table. Each slot is iterated once.
        """
        package_list = str()
        for package in self.table:  # O(n)
            package_list += f"{package}\n"  # O(1) for string concatenation
        return package_list

    def _hash(self, key: int) -> int:
        """
        Private method to calculate the hash index for a given key.
        
        Parameters:
        - key: The package ID for which the hash index is generated.
        
        Returns:
        - An integer representing the index in the hash table where the key should be stored.

        Time Complexity: O(1) - The hash index is computed in constant time using the modulo operation.
        """
        return key % self.size  # O(1)

    def insert(self, package_id, package):
        """
        Inserts a package into the hash table using open addressing to handle collisions.
        
        Parameters:
        - package_id: Unique identifier of the package.
        - package: Package object containing all relevant package details.

        Time Complexity:
        - Best Case: O(1) - The slot is empty, and the package is inserted directly.
        - Worst Case: O(n) - In case of collisions, linear probing may traverse all slots.
        - Average Case: O(1) - With a good hash function and low load factor, collisions are rare.
        """
        index = self._hash(package_id)  # O(1)
        # Resolve collisions using linear probing
        while self.table[index] is not None:  # O(k), where k is the number of collisions
            if self.table[index].package_id == package_id:  # O(1) to compare IDs
                self.table[index] = package  # O(1) to update
                return
            index = (index + 1) % self.size  # O(1) to probe the next slot
        self.table[index] = package  # O(1) to insert

    def lookup(self, package_id):
        """
        Finds and returns a package from the hash table by its package_id.
        
        Parameters:
        - package_id: The unique identifier for the package to locate.
        
        Returns:
        - The Package object if found, otherwise None.

        Time Complexity:
        - Best Case: O(1) - The package is located in the first checked slot.
        - Worst Case: O(n) - Linear probing may traverse all slots if collisions occur.
        - Average Case: O(1) - With a good hash function and low load factor, collisions are rare.
        """
        index = self._hash(package_id)  # O(1)
        # Linear probing to find the package if collisions occurred
        while self.table[index] is not None:  # O(k), where k is the number of collisions
            if self.table[index].package_id == package_id:  # O(1) to compare IDs
                return self.table[index]  # O(1) to return the package
            index = (index + 1) % self.size  # O(1) to probe the next slot
        return None  # O(1) to return None if not found
