
# WGUPS Routing Program

Mason Wilkins

## Overview

This program, created as part of Mason Wilkins' coursework for Western Governors University, implements a routing solution for the WGUPS package delivery service. It leverages a hash table to store package data and utilizes multiple trucks to optimize delivery routes and track package statuses. The program allows users to view the final delivery status of all packages, query specific packages by time, and track the total mileage for delivery trucks.

## Project Details

- **Course**: Western Governors University
- **Project**: NHP3 Task 2: WGUPS Routing Program Implementation
- **Language**: Python
- **Key Concepts**: Hash tables, Nearest Neighbor Algorithm, Date and Time Handling, User Interaction

## Features

1. **Package Delivery Simulation**  
   - Loads package data into a hash table.
   - Simulates package delivery using three trucks with predefined routes and start times.
   - Assigns specific packages to each truck based on delivery priorities and location constraints.

2. **User Options**  
   - **View All Package Statuses**: Displays the final delivery status of all packages and the total mileage of all trucks.
   - **Package Status Lookup**: Allows querying the status of a single package at a specified time, showing if it is "at hub," "en route," or "delivered."
   - **All Package Statuses at Specific Time**: Shows the delivery status of all packages at a specified time, allowing the user to view the progress of deliveries across trucks.

3. **Real-Time Status Updates**  
   - Provides up-to-date status for each package based on user-specified times.
   - Tracks total mileage across all trucks to maintain a summary of distance traveled.

4. **Address Update for Specific Package**  
   - Handles mid-route address changes, as exemplified by Package ID 9, whose delivery address is updated at a specific time (10:20:00), showcasing adaptability to dynamic routing needs.

### Required Screenshots for Submission
For course submission, screenshots showing package statuses should be taken at the following times:
   - Between 8:35 a.m. and 9:25 a.m.
   - Between 9:35 a.m. and 10:25 a.m.
   - Between 12:03 p.m. and 1:12 p.m.

## Installation

1. *Clone the Repository*
   `bash
   git clone <https://github.com/mwilkins17/wgups_routing_program.git>
   cd wgups-routing-program
   `

2. **Run the Program**
   Ensure Python 3.9+ is installed and execute the main program.
   ```bash
   python main.py
   ```

## Usage

Upon running the program, users will be presented with several options:

**View All Package Statuses**: Displays the final delivery status of all packages and the total mileage of all trucks.
- **Package Status Lookup**: Allows querying the status of a package at a specific time, showing if it is "at hub," "en route," or "delivered."
**All Package Statuses at Specific Time**: Shows the delivery status of all packages at a specified time, allowing the user to view the progress of deliveries across trucks.

## Algorithm and Data Structure Details

### Nearest Neighbor Algorithm

The program’s routing logic is built on the **nearest neighbor algorithm**, which selects the closest next destination to the truck’s current location until all packages are delivered. This approach is straightforward and efficient for real-time delivery management. The algorithm prioritizes simplicity and scalability to handle the WGUPS constraints effectively.

### Alternative Algorithms Considered

1. **Bellman-Ford Algorithm**  
   Determines the shortest paths from a start location to each other location in a graph. Useful for complex graphs with variable edge weights.

2. **Dijkstra's Algorithm**  
   Calculates the shortest paths from a start vertex to all other vertices in a graph with non-negative edge weights. Ideal for stable routing applications with fixed distances.

For more details on these algorithms, see the [References](#references) section.

### Data Structures

The **hash table** data structure serves as the primary method for storing package data. Each package ID acts as a key, making lookup times efficient with average \(O(1)\) complexity. The hash table uses chaining to handle collisions, ensuring reliable data retrieval even with a large number of packages.

#### Other Data Structures Considered

1. **Dictionary**: A Python `dict` provides similar functionality to a hash table, offering efficient key-based access without requiring custom hashing.
2. **Binary Search Tree (BST)**: Would allow ordered access based on package attributes like delivery time but would introduce higher retrieval times than a hash table.

## Scalability and Adaptability

The program is designed to be highly adaptable. By using a modular structure and efficient data structures, it can scale to handle more packages and support other service areas or cities if WGUPS expands. The hash table ensures efficient data handling even with larger datasets, and the routing algorithm can be adapted to incorporate more complex logic if needed, such as dynamic updates or real-time traffic data.

## Future Improvements

If revisiting this project, the following enhancements are recommended:

- **Hybrid Routing Approach**: Integrate a 2-opt optimization step to refine the nearest neighbor route, reducing overall mileage.
- **Dynamic Routing Adjustments**: Incorporate real-time data (e.g., traffic updates or priority changes) for adaptive route reoptimization.
- **Multi-Threading for Parallel Delivery Simulation**: Optimize by routing multiple trucks simultaneously, improving performance for larger datasets.

## References

- Zybooks Section 5.9: "Dijkstra's Shortest Path Algorithm." *Data Structures and Algorithms II*. Retrieved from [https://learn.zybooks.com/zybook/WGUC950Template2023/chapter/5/section/9](https://learn.zybooks.com/zybook/WGUC950Template2023/chapter/5/section/9)

- Zybooks Section 5.10: "Bellman-Ford Shortest Path Algorithm." *Data Structures and Algorithms II*. Retrieved from [https://learn.zybooks.com/zybook/WGUC950Template2023/chapter/5/section/10](https://learn.zybooks.com/zybook/WGUC950Template2023/chapter/5/section/10)
