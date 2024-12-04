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

# Main function that runs the program, displays the menu, and handles user input
def main():
    # Loop to continuously display the main menu until the user decides to exit
    while True:
        # Load package data and store it in a hash table
        # Time Complexity: O(n), where n is the number of packages
        package_data = load_package_data()
        hash_table = package_data

        # Lookup each package by its ID in the hash table
        # Time Complexity: O(n), where n is the number of packages (1 to 40)
        for i in range(1, 41):
            package = hash_table.lookup(i)

        # Instantiate 3 truck objects with initial addresses and start times
        # Time Complexity: O(1) per truck, so O(3) = O(1)
        truck1 = Truck(1, '4001 South 700 East', timedelta(hours=8))
        truck1.packages = [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40]

        truck2 = Truck(2, '4001 South 700 East', timedelta(hours=9, minutes=5))
        truck2.packages = [3, 6, 12, 17, 18, 21, 22, 23, 24, 26, 27, 33, 35, 36, 38, 39]

        truck3 = Truck(3, '4001 South 700 East', timedelta(hours=10, minutes=20))
        truck3.packages = [2, 4, 5, 7, 8, 9, 10, 11, 25, 28, 32]

        # Begin package delivery for each truck
        # Time Complexity: O(m1 + m2 + m3), where m1, m2, and m3 are the number of packages on each truck
        # Assuming total packages delivered = n, the overall complexity is O(n)
        truck1.deliver_packages(package_data)
        truck2.deliver_packages(package_data)
        truck3.deliver_packages(package_data)

        # Define a regex pattern to validate time in HH:MM:SS format
        # Time Complexity: O(1) for matching a single time string
        time_pattern = r"^(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d$"

        # Display menu options for the user
        print("""
            Welcome to WGUPS!\n
            \nPlease type one of the following numbers:
                1. Print All Package Final Delivery Status and Total Mileage
                2. Lookup a Single Package Status by a Specific Time
                3. Lookup All Package Delivery Status by a Specific Time 
                4. Exit the Program
            """
            )

        # Handle user input for menu selection
        ans = input("Which option would you like to select?:  ")
        if ans == '1':
            # Print final delivery status for all packages and total mileage for trucks
            # Time Complexity: O(n) for looking up each package and printing statuses
            for i in range(1, 41):
                package = hash_table.lookup(i)  # O(1) lookup per package
                package.status = 'delivered'
                update_package_9(package, timedelta(hours=17))  # O(1) for package 9
                print(package)
            mileage = truck1.miles + truck2.miles + truck3.miles  # O(1) for mileage calculation
            print(f"\n\nThe total mileage for all trucks is {round(mileage, 2)}.")

        elif ans == '2':
            # Allow user to lookup a single package by ID and time
            while True:
                print("If you want to go back to the main menu at any time, enter 'q'")
                user_package_id = input("Please enter a valid package ID (1-40): ")
                # Validate package ID
                if user_package_id.isnumeric():
                    if int(user_package_id) < 1 or int(user_package_id) > 40:
                        print("\n##############################")
                        print("That was not a valid number.")
                        print("##############################\n")
                    else:
                        # Get time input from user and update package status accordingly
                        user_time = input("Please enter a valid time in the form (HH:MM:SS): ")
                        if re.match(time_pattern, user_time):  # O(1) for regex match
                            h, m, s = user_time.split(":")
                            time = timedelta(hours=int(h), minutes=int(m), seconds=int(s))  # O(1)
                            package = hash_table.lookup(int(user_package_id))  # O(1)
                            package.update_status(time)  # O(1) per package
                            update_package_9(package, time)  # O(1) for package 9
                            print(package)
                        elif user_time == 'q':
                            print("\nRedirecting back to main menu...")
                            break
                        else:
                            print("\n##############################")
                            print("That was an invalid input format.")
                            print("##############################\n")
                            
                elif user_package_id == 'q':
                    print("\nRedirecting back to main menu...")
                    break
                else:
                    print("\n##############################")
                    print("That was not a valid number. Please try again.")
                    print("##############################\n")

        elif ans == '3':
            # Lookup and display status for all packages at a specific time
            while True:
                print("\nIf you want to go back to the main menu at any time, enter 'q'")
                user_time = input("Please enter a valid time in the form (HH:MM:SS): ")

                # Validate time format and update package statuses
                if re.match(time_pattern, user_time):  # O(1) for regex match
                    h, m, s = user_time.split(":")
                    time = timedelta(hours=int(h), minutes=int(m), seconds=int(s))  # O(1)
                    for i in range(1, 41):  # O(n)
                        package = hash_table.lookup(i)  # O(1) lookup
                        package.update_status(time)  # O(1)
                        update_package_9(package=package, time=time)  # O(1) for package 9
                        print(package)
                elif user_time == 'q':
                    print("\nRedirecting back to main menu...")
                    break
                else:
                    print("\n##############################")
                    print("That was an invalid input format.")
                    print("##############################\n")

        elif ans == '4':
            # Exit the program
            # Time Complexity: O(1)
            print("\nThank you for using WGUPS. Goodbye!\n")
            exit()
        else:
            # Handle invalid menu selection
            # Time Complexity: O(1)
            print("\n##############################")
            print("That was an invalid answer.")
            print("##############################")

# Function to update address for package 9 at specific times
# Time Complexity: O(1), as this operation only checks and updates a single package
def update_package_9(package, time):
    if package.package_id == 9:
        if time < timedelta(hours=10, minutes=20):
            package.delivery_address = '300 State St'
            package.delivery_zip_code = 84103
            package.notes = package.notes.replace(". Address fixed at 10:20:00", "")
        else:
            package.delivery_address = '410 S State St'
            package.delivery_zip_code = 84111
            package.notes = package.notes + ". Address fixed at 10:20:00"

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

# Entry point for the program
if __name__ == "__main__":
    main()
