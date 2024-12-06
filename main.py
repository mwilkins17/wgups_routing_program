from truck import Truck
from datetime import timedelta
from hash_table import HashTable
from package import Package
import re, csv

"""
Name: Mason Wilkins
Student ID: 012254545
Western Governors University
NHP3 — NHP3 Task 2: WGUPS Routing Program Implementation
"""

# Function to calculate distance between two addresses
def calculate_distance(address1, address2, distance_matrix, address_list):
    """
    Calculates the distance between two addresses based on the distance matrix.
    """
    index1 = address_list.index(address1)
    index2 = address_list.index(address2)
    distance = distance_matrix[index1][index2]
    return float(distance if distance else distance_matrix[index2][index1])

# Function to update address for package 9 at specific times
def update_package_9(package, time):
    """
    Dynamically updates the address for package #9 based on the current time.
    Ensures the note is added only once.
    """
    if package.package_id == 9:
        if time < timedelta(hours=10, minutes=20):
            package.delivery_address = '300 State St'
            package.delivery_zip_code = 84103
            package.notes = package.notes.replace(". Address fixed at 10:20:00", "")
        else:
            package.delivery_address = '410 S State St'
            package.delivery_zip_code = 84111
            # Only add the note if it doesn't already exist
            if ". Address fixed at 10:20:00" not in package.notes:
                package.notes += ". Address fixed at 10:20:00"

# Nearest Neighbor Algorithm for package delivery
def nearest_neighbor_delivery(truck, package_data, distance_matrix, address_list):
    """
    Implements the Nearest Neighbor Algorithm for truck deliveries.
    Dynamically determines the next closest package destination for optimal routing.
    Updates the truck number for each delivered package.
    """
    not_delivered = [package_data.lookup(package_id) for package_id in truck.packages]
    truck.packages.clear()  # Clear and reorder packages dynamically

    while not_delivered:
        nearest_package = None
        shortest_distance = float('inf')

        # Find the nearest package
        for package in not_delivered:
            # Update address for package #9 dynamically
            update_package_9(package, truck.total_time_traveled)

            distance = calculate_distance(truck.location, package.delivery_address, distance_matrix, address_list)
            if distance < shortest_distance:
                shortest_distance = distance
                nearest_package = package

        # Deliver the nearest package
        truck.packages.append(nearest_package.package_id)
        not_delivered.remove(nearest_package)
        truck.miles += shortest_distance
        truck.total_time_traveled += timedelta(hours=shortest_distance / truck.speed)
        truck.location = nearest_package.delivery_address
        nearest_package.delivery_time = truck.total_time_traveled
        nearest_package.depart_time = truck.depart_time
        nearest_package.status = "Delivered"
        nearest_package.truck = truck.truck_number  # Update truck number

# Main function
def main():
    """
    Main function to run the WGUPS Routing Program.
    """
    # Load package, distance, and address data
    package_data = load_package_data()
    distance_matrix = load_distance_table()
    address_list = [row[2] for row in load_address_data()]  # Extract address column

    # Initialize trucks
    truck1 = Truck(1, '4001 South 700 East', timedelta(hours=8))
    truck2 = Truck(2, '4001 South 700 East', timedelta(hours=9, minutes=5))
    truck3 = Truck(3, '4001 South 700 East', timedelta(hours=10, minutes=20))

    # Assign packages to trucks
    truck1.packages = [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40]
    truck2.packages = [3, 6, 12, 17, 18, 21, 22, 23, 24, 26, 27, 33, 35, 36, 38, 39]
    truck3.packages = [2, 4, 5, 7, 8, 9, 10, 11, 25, 28, 32]

    # Deliver packages using Nearest Neighbor Algorithm
    nearest_neighbor_delivery(truck1, package_data, distance_matrix, address_list)
    nearest_neighbor_delivery(truck2, package_data, distance_matrix, address_list)
    nearest_neighbor_delivery(truck3, package_data, distance_matrix, address_list)

    # Define a regex pattern to validate time in HH:MM:SS format
    time_pattern = r"^(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d$"

    # Display menu options for the user
    while True:
        print("""
            Welcome to WGUPS!

            Please type one of the following numbers:
                1. Print All Package Final Delivery Status and Total Mileage
                2. Lookup a Single Package Status by a Specific Time
                3. Lookup All Package Delivery Status by a Specific Time 
                4. Exit the Program
            """)

        ans = input("Which option would you like to select?:  ")
        if ans == '1':
            # Print final delivery status for all packages and total mileage
            for i in range(1, 41):
                package = package_data.lookup(i)
                print(package, "\n")
            total_mileage = truck1.miles + truck2.miles + truck3.miles
            print(f"\n\nThe total mileage for all trucks is {round(total_mileage, 2)}.")

        elif ans == '2':
            # Lookup a single package status at a specific time
            while True:
                print("If you want to go back to the main menu at any time, enter 'q'")
                user_package_id = input("Enter a valid Package ID (1-40): ")
                if user_package_id == 'q':
                    break
                if user_package_id.isnumeric() and 1 <= int(user_package_id) <= 40:
                    package_id = int(user_package_id)
                    user_time = input("Enter time in HH:MM:SS format: ")
                    if re.match(time_pattern, user_time):
                        h, m, s = map(int, user_time.split(":"))
                        current_time = timedelta(hours=h, minutes=m, seconds=s)
                        package = package_data.lookup(package_id)
                        update_package_9(package, current_time)
                        package.update_status(current_time)
                        print(package, "\n")
                    else:
                        print("\nInvalid time format. Please try again (e.g., 08:35:00).")
                else:
                    print("\nInvalid Package ID. Please try again.")

        elif ans == '3':
            # Lookup all package statuses at a specific time
            while True:
                user_time = input("Enter time in HH:MM:SS format (or 'q' to quit): ")
                if user_time == 'q':
                    break
                if re.match(time_pattern, user_time):
                    h, m, s = map(int, user_time.split(":"))
                    current_time = timedelta(hours=h, minutes=m, seconds=s)
                    for i in range(1, 41):
                        package = package_data.lookup(i)
                        update_package_9(package, current_time)
                        package.update_status(current_time)
                        print(package, "\n")
                else:
                    print("\nInvalid time format. Please try again (e.g., 08:35:00).")

        elif ans == '4':
            print("\nThank you for using WGUPS. Goodbye!\n")
            exit()
        else:
            print("\nInvalid choice. Please try again.")

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

if __name__ == "__main__":
    main()
