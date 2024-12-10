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

# Main function
def main():
    """
    Main function to run the WGUPS Routing Program.

    Process Flow:
    1. Load package data, distance matrix, and address data from respective CSV files.
    2. Create and initialize three trucks with their IDs, start locations, and start times.
    3. Assign specific packages to each truck based on predefined package IDs.
    4. Optimize delivery for each truck using the Nearest Neighbor Algorithm.
    5. Provide a menu for user interaction with four main options:
        - View final delivery status of all packages and total mileage.
        - Lookup the delivery status of a single package at a specified time.
        - View delivery statuses of all packages at a specified time.
        - Exit the program.
    6. Validate user input for menu selections, package IDs, and time formats.
    7. Process user requests and loop until the user chooses to exit.

    Time Complexity:
    - Data Loading: O(n), where n is the total size of the CSV files.
    - Delivery: O(t^2), where t is the number of packages per truck.
    - Menu Loop: O(1) to O(n), depending on user interaction.
    """
    # Load data
    package_data = load_package_data()
    distance_matrix = load_distance_table()
    address_list = [row[2] for row in load_address_data()]

    # Initialize trucks
    truck1 = Truck(1, '4001 South 700 East', timedelta(hours=8))
    truck2 = Truck(2, '4001 South 700 East', timedelta(hours=9, minutes=5))
    truck3 = Truck(3, '4001 South 700 East', timedelta(hours=10, minutes=20))

    # Assign packages
    truck1.packages = [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40]
    truck2.packages = [3, 6, 12, 17, 18, 21, 22, 23, 24, 26, 27, 33, 35, 36, 38, 39]
    truck3.packages = [2, 4, 5, 7, 8, 9, 10, 11, 25, 28, 32]

    # Deliver packages
    nearest_neighbor_delivery(truck1, package_data, distance_matrix, address_list)
    nearest_neighbor_delivery(truck2, package_data, distance_matrix, address_list)
    nearest_neighbor_delivery(truck3, package_data, distance_matrix, address_list)

    # Define time pattern
    time_pattern = r"^(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d$"

    # Menu loop
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
            # Print final delivery status and total mileage
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
                        print(package)
                    print("\n")
                else:
                    print("\nInvalid time format. Please try again (e.g., 08:35:00).")

        elif ans == '4':
            # Exit the program
            print("\nThank you for using WGUPS. Goodbye!\n")
            exit()
        else:
            print("\nInvalid choice. Please try again.")


def calculate_distance(address1, address2, distance_matrix, address_list):
    """
    Calculates the distance between two addresses.

    Process Flow:
    1. Find the indices of the two addresses in the address list.
    2. Use these indices to access the corresponding distance in the distance matrix.
    3. Handle cases where the distance is not directly available (use the reverse distance).

    Time Complexity: O(n), where n is the size of the address list.
    """
    index1 = address_list.index(address1)
    index2 = address_list.index(address2)
    distance = distance_matrix[index1][index2]
    return float(distance if distance else distance_matrix[index2][index1])


def update_package_9(package, time):
    """
    Dynamically updates the address for package #9.

    Process Flow:
    1. Check if the package ID is 9.
    2. Update the delivery address and zip code based on the current time.
    3. Add or update notes if necessary.

    Time Complexity: O(1).
    """
    if package.package_id == 9:
        if time < timedelta(hours=10, minutes=20):
            package.delivery_address = '300 State St'
            package.delivery_zip_code = 84103
            package.notes = package.notes.replace(". Address fixed at 10:20:00", "")
        else:
            package.delivery_address = '410 S State St'
            package.delivery_zip_code = 84111
            if ". Address fixed at 10:20:00" not in package.notes:
                package.notes += ". Address fixed at 10:20:00"


def nearest_neighbor_delivery(truck, package_data, distance_matrix, address_list):
    """
    Implements the Nearest Neighbor Algorithm for package delivery.

    Process Flow:
    1. Retrieve all packages assigned to the truck.
    2. While there are undelivered packages:
        a. Find the nearest package by calculating distances from the truck's current location.
        b. Update the truck's location, mileage, and time traveled.
        c. Mark the package as delivered and update its status.
    3. Repeat until all packages are delivered.

    Time Complexity: O(t^2), where t is the number of packages assigned to the truck.
    """
    not_delivered = [package_data.lookup(package_id) for package_id in truck.packages]
    truck.packages.clear()

    while not_delivered:
        nearest_package = None
        shortest_distance = float('inf')

        for package in not_delivered:
            package.reset_package()
            update_package_9(package, truck.total_time_traveled)
            distance = calculate_distance(truck.location, package.delivery_address, distance_matrix, address_list)
            if distance < shortest_distance:
                shortest_distance = distance
                nearest_package = package

        truck.packages.append(nearest_package.package_id)
        not_delivered.remove(nearest_package)
        truck.miles += shortest_distance
        truck.total_time_traveled += timedelta(hours=shortest_distance / truck.speed)
        truck.location = nearest_package.delivery_address
        nearest_package.delivery_time = truck.total_time_traveled
        nearest_package.depart_time = truck.depart_time
        nearest_package.status = "Delivered"
        nearest_package.truck = truck.truck_number


def load_distance_table():
    """
    Loads the distance matrix.

    Process Flow:
    1. Open the distance CSV file.
    2. Read all rows and convert them into a list of lists.

    Time Complexity: O(n), where n is the number of rows in the CSV file.
    """
    with open("./csv/distances.csv", mode='r', encoding='utf-8-sig') as file:
        distance_data = csv.reader(file)
        distance_list = list(distance_data)
    return distance_list


def load_address_data():
    """
    Loads the address list.

    Process Flow:
    1. Open the address CSV file.
    2. Read all rows and convert them into a list of lists.

    Time Complexity: O(n), where n is the number of rows in the CSV file.
    """
    with open("./csv/addresses.csv") as address_csv:
        address_data = csv.reader(address_csv)
        address_list = list(address_data)
    return address_list


def load_package_data():
    """
    Loads package data into a hash table.

    Process Flow:
    1. Initialize a hash table to store package data.
    2. Open the package CSV file and read rows one by one.
    3. For each row, create a Package object and insert it into the hash table.

    Time Complexity: O(n), where n is the number of packages.
    """
    hash_table = HashTable()
    with open("./csv/packages.csv", mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            package_id = int(row['PackageID'])
            package = Package(
                package_id=package_id,
                address=row['Address'],
                deadline=row['Deadline'],
                city=row['City'],
                state=row['State'],
                zip_code=row['Zip'],
                weight=float(row['Weight']),
                status=row.get('Status', 'at hub'),
                notes=row['Notes']
            )
            hash_table.insert(package_id, package)
    return hash_table


if __name__ == "__main__":
    main()