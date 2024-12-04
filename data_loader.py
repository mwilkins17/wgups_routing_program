from package import Package
from hash_table import HashTable
import csv

def load_distance_table() -> dict:
    """
    Loads the distance data from a CSV file and returns it as a list of lists.
    Each entry represents the distance between addresses in a distance matrix format.

    Time Complexity:
    - Reading the file: O(n), where n is the number of rows in the CSV file.
    - Converting to a list of lists: O(n), as it iterates through each row.
    Overall: O(n), where n is the number of rows in the CSV file.
    """
    with open("./csv/distances.csv", mode='r', encoding='utf-8-sig') as file:
        distance_data = csv.reader(file)  # O(n) to read all rows
        distance_list = list(distance_data)  # O(n) to convert rows to a list
    return distance_list  # Return the distance matrix as a list of lists


def load_address_data() -> list:
    """
    Loads address data from a CSV file and returns it as a list of lists.
    Each entry contains the details of an address, including its index, name, and location.

    Time Complexity:
    - Reading the file: O(a), where a is the number of rows in the addresses CSV.
    - Converting to a list of lists: O(a).
    Overall: O(a), where a is the number of rows in the addresses CSV file.
    """
    with open("./csv/addresses.csv") as address_csv:
        address_data = csv.reader(address_csv)  # O(a) to read all rows
        address_list = list(address_data)  # O(a) to convert rows to a list
    return address_list  # Return the list of addresses


def load_package_data() -> dict:
    """
    Loads package data from a CSV file and inserts each package into a hash table.

    Time Complexity:
    - Reading the file: O(p), where p is the number of rows (packages) in the CSV file.
    - Looping through rows to create Package instances: O(p).
    - Hash table insertion: O(1) per insertion (average case), O(p) for all packages.
    Overall: O(p), where p is the number of packages in the CSV file.
    """
    hash_table = HashTable()  # O(1) to initialize a hash table
    
    # Open and read the CSV file containing package details
    with open("./csv/packages.csv", mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)  # O(p) to iterate through rows in the CSV
        
        # Loop through each row in the CSV to create and insert Package objects
        for row in reader:  # O(p), where p is the number of packages
            package_id = int(row['PackageID'])  # O(1) to parse package ID
            # Create a Package instance using data from the current row
            package = Package(
                package_id=package_id,  # O(1)
                address=row['Address'],  # O(1)
                deadline=row['Deadline'],  # O(1)
                city=row['City'],  # O(1)
                state=row['State'],  # O(1)
                zip_code=row['Zip'],  # O(1)
                weight=float(row['Weight']),  # O(1)
                status=row.get('Status', 'at hub'),  # O(1)
                notes=row['Notes']  # O(1)
            )
            # Insert the package into the hash table using its package ID as the key
            hash_table.insert(package_id, package)  # O(1) per insertion (average case)
    
    return hash_table  # O(1) to return the hash table containing all packages
