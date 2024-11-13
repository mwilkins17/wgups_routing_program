from truck import Truck
from datetime import timedelta
from data_loader import load_package_data
import re

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
        package_data = load_package_data()
        hash_table = package_data

        # Lookup each package by its ID in the hash table
        for i in range(1, 41):
            package = hash_table.lookup(i)


        # Instantiate 3 truck objects with initial addresses and start times
        truck1 = Truck(1, '4001 South 700 East', timedelta(hours=8))
        truck1.packages = [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40]

        truck2 = Truck(2, '4001 South 700 East', timedelta(hours=9, minutes=5))
        truck2.packages = [3, 6, 12, 17, 18, 21, 22, 23, 24, 26, 27, 33, 35, 36, 38, 39]

        truck3 = Truck(3, '4001 South 700 East', timedelta(hours=10, minutes=20))
        truck3.packages = [2, 4, 5, 7, 8, 9, 10, 11, 25, 28, 32]

        # Begin package delivery for each truck
        truck1.deliver_packages(package_data)
        truck2.deliver_packages(package_data)
        truck3.deliver_packages(package_data)

        # Define a regex pattern to validate time in HH:MM:SS format
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
            for i in range(1, 40):
                package = hash_table.lookup(i)
                package.status = 'delivered'
                update_package_9(package, timedelta(hours=17))
                print(package)
            mileage = truck1.miles + truck2.miles + truck3.miles
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
                        if re.match(time_pattern, user_time):
                            h, m, s = user_time.split(":")
                            time = timedelta(hours=int(h), minutes=int(m), seconds=int(s))
                            package = hash_table.lookup(int(user_package_id))
                            package.update_status(time)
                            update_package_9(package, time)
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
                total_packages_loaded = 0
                truck1_packages = {}
                truck2_packages = {}
                truck3_packages = {}
                print("\nIf you want to go back to the main menu at any time, enter 'q'")
                user_time = input("Please enter a valid time in the form (HH:MM:SS): ")

                # Validate time format and update package statuses
                if re.match(time_pattern, user_time):
                    h, m, s = user_time.split(":")
                    time = timedelta(hours=int(h), minutes=int(m), seconds=int(s))
                    for i in range(1, 41):
                        package = hash_table.lookup(i)
                        package.update_status(time)
                        update_package_9(package=package, time=time)
                        if package.status != 'delivered':
                            total_packages_loaded += 1
                            if package.truck == 1:
                                truck1_packages[str(package.package_id)] = truck1_packages.get(
                                    str(package.package_id), 
                                    "Departed @ " + str(package.depart_time) + ", " +
                                    package.status + f", delivery @ {package.delivery_time}")
                            if package.truck == 2:
                                truck2_packages[str(package.package_id)] = truck2_packages.get(
                                    str(package.package_id), 
                                    "Departed @ " + str(package.depart_time) + ", " +
                                    package.status + f", delivery @ {package.delivery_time}")
                            if package.truck == 3:
                                truck3_packages[str(package.package_id)] = truck3_packages.get(
                                    str(package.package_id), 
                                    "Departed @ " + str(package.depart_time) + ", " +
                                    package.status + f", delivery @ {package.delivery_time}")
                    print(f"\n\nTotal Packages Loaded on trucks at {user_time}: {total_packages_loaded}")
                    for key, value in truck1_packages.items():
                        print(f"Truck 1, Package_number: {key}, Package Status: {value}")
                    for key, value in truck2_packages.items():
                        print(f"Truck 2, Package_number: {key}, Package Status: {value}")
                    for key, value in truck3_packages.items():
                        print(f"Truck 3, Package_number: {key}, Package Status: {value}")
                elif user_time == 'q':
                    print("\nRedirecting back to main menu...")
                    break
                else:
                    print("\n##############################")
                    print("That was an invalid input format.")
                    print("##############################\n")

        elif ans == '4':
            # Exit the program
            print("\nThank you for using WGUPS. Goodbye!\n")
            exit()
        else:
            # Handle invalid menu selection
            print("\n##############################")
            print("That was an invalid answer.")
            print("##############################")

# Function to update address for package 9 at specific times
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

# Entry point for the program
if __name__ == "__main__":
    main()