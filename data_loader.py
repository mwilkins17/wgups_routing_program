from package import Package
from hash_table import HashTable
import csv
import datetime

def load_distance_table() -> dict:
    """
    Loads the distance data from a CSV file and returns it as a list of lists.
    Each entry represents the distance between addresses in a distance matrix format.
    """
    with open("./csv/distances.csv", mode='r', encoding='utf-8-sig') as file:
        distance_data = csv.reader(file)  # Read the distance data
        distance_list = list(distance_data)  # Convert the data to a list of lists
    return distance_list  # Return the distance matrix as a list of lists


def load_address_data() -> list:
    """
    Loads address data from a CSV file and returns it as a list of lists.
    Each entry contains the details of an address, including its index, name, and location.
    """
    with open("./csv/addresses.csv") as address_csv:
        address_data = csv.reader(address_csv)  # Read the address data
        address_list = list(address_data)  # Convert the data to a list of lists
    return address_list  # Return the list of addresses


def load_package_data() -> dict:
    """
    Loads package data from a CSV file and inserts each package into a hash table.
    
    Returns:
    - A HashTable object containing all packages, where each package can be looked up by its ID.
    """
    hash_table = HashTable()  # Initialize a new hash table to store packages
    
    # Open and read the CSV file containing package details
    with open("./csv/packages.csv", mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)  # Use DictReader to map data from CSV to dictionary keys
        
        # Loop through each row in the CSV to create and insert Package objects
        for row in reader:
            package_id = int(row['PackageID'])  # Get the package ID from the CSV
            # Create a Package instance using data from the current row
            package = Package(
                package_id=package_id,
                address=row['Address'],  # Delivery address
                deadline=row['Deadline'],  # Delivery deadline
                city=row['City'],  # City for delivery
                state=row['State'],  # State for delivery
                zip_code=row['Zip'],  # Zip code for delivery
                weight=float(row['Weight']),  # Package weight
                status=row.get('Status', 'at hub'),  # Initial status (default is 'at hub')
                notes=row['Notes']  # Additional notes or delivery instructions
            )
            # Insert the package into the hash table using its package ID as the key
            hash_table.insert(package_id, package)
    
    return hash_table  # Return the hash table containing all packages
