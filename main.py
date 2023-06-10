# Gunnar Stubler - 001342614

import csv
from datetime import datetime, timedelta


# Function for calculating the distance between two location IDs from the distances.csv file.
def calculate_distance(location1, location2):
    if location1 > location2:
        distance = float(distances[location1 - 1][location2 - 1])
    else:
        distance = float(distances[location2 - 1][location1 - 1])
    return distance


# Chaining hash table class.
class HashTable:
    def __init__(self):
        self.table = []
        for i in range(10):
            self.table.append([])

    def insert(self, package_id, location_id, address, city, state, zipcode, weight, deadline, status, time_received,
               time_loaded, time_delivered):
        bucket = hash(package_id) % len(self.table)
        bucket_list = self.table[bucket]
        bucket_list.append(package)


# Package class.
class Package:
    def __init__(self, package_id, location_id, address, city, state, zipcode, weight, deadline, status, time_received):
        self.package_id = int(package_id)
        self.location_id = int(location_id)
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.weight = weight
        self.deadline = datetime.strptime(deadline, '%H:%M')
        self.status = status
        self.time_received = datetime.strptime(time_received, '%H:%M')


# Truck class.
class Truck:
    def __init__(self, truck_id):
        self.truck_id = int(truck_id)
        self.current_time = datetime.strptime('08:00', '%H:%M')
        self.current_location = 1
        self.distance_traveled = 0
        self.AVERAGE_SPEED = 18
        self.packages_on_truck = []
        self.next_package = Package

    # Copies a package from the all_packages hash table to the packages_on_truck list.
    def load_package(self, package_id):
        first = package_id % 10
        second = package_id // 10
        if first == 0:
            second = second - 1
        # Checks to see if packages_on_truck can hold more packages, then checks if the package has already been loaded
        # onto a truck.
        if len(self.packages_on_truck) < 16:
            if all_packages.table[first][second][8] != 'On truck':
                all_packages.table[first][second][8] = 'On truck'

                self.packages_on_truck.append(Package(all_packages.table[first][second][0],
                                                      all_packages.table[first][second][1],
                                                      all_packages.table[first][second][2],
                                                      all_packages.table[first][second][3],
                                                      all_packages.table[first][second][4],
                                                      all_packages.table[first][second][5],
                                                      all_packages.table[first][second][6],
                                                      all_packages.table[first][second][7],
                                                      all_packages.table[first][second][8],
                                                      all_packages.table[first][second][9]))
            else:
                print('Error: Cannot load package ' + str(all_packages.table[first][second][0]) +
                      ', package not at hub. Package status: ' + str(all_packages.table[first][second][8]))
        else:
            print('Error: Cannot load package ' + str(all_packages.table[first][second][0]) +
                  ', truck ' + str(self.truck_id) + ' full.')

    # Finds the next package to deliver by finding packages with the closest deadline, and then the closest delivery
    # distance among those:
    #   1) look for any package with the same delivery destination as the truck's current location:
    #           select this package for delivery
    #   2) find the earliest delivery deadline among the packages on the truck,
    #   3) add packages matching the earliest deadline to a separate list,
    #   4) within the separate list, find the package with the closest delivery destination from the current location:
    #           select this package for delivery
    #
    # PSEUDOCODE
    #
    # next_delivery algorithm:
    #   set next_deadline to 18:00
    #   set next_group to empty list
    #   set closest_distance to 999
    #   for each package on truck:
    #       if package's destination ID is the same as the truck's location ID:
    #           select package for next delivery
    #           return
    #
    #   for each package on truck:
    #       if package's deadline is sooner than next_deadline:
    #           set next_deadline's value to package's deadline
    #
    #   for each package on truck:
    #       if package's deadline matches the value stored in next_deadline:
    #           append package to next_group
    #
    #   for each package on truck:
    #       if package's distance to destination is less than the value stored in closest_distance:
    #           set closest_distance's value to package's distance to destination
    #           select package for next delivery
    #
    def next_delivery(self):
        next_deadline = datetime.strptime('18:00', '%H:%M')
        next_group = []
        closest_distance = 999

        # Iterates through packages_on_truck to check if any packages have the same destination as the truck's current
        # location.
        #
        # for each package on the truck:
        #   if the package's destination is the same as the current location:
        #       select this package as the next delivery
        #       return
        for x in self.packages_on_truck:
            if x.location_id == self.current_location:
                self.next_package = x
                return

        # Iterates through the packages_on_truck to find the closest deadline.
        #
        # for each package on the truck:
        #   if the package's delivery deadline is before the stored datetime in next_deadline:
        #       set next_deadline's value to this package's deadline
        for x in self.packages_on_truck:
            if x.deadline < next_deadline:
                next_deadline = x.deadline

        # Iterates through the packages_on_truck and adds packages with the same deadline as
        # next_deadline to a separate list.
        #
        # for each package on the truck:
        #   if the package's deadline is the same as the datetime value stored in next_deadline:
        #       add this package to a separate list called next_group
        for x in self.packages_on_truck:
            if x.deadline == next_deadline:
                next_group.append(x)

        # Iterates through next_group to find the closest delivery distance from the current location,
        # and marks the package with the closest distance as next_package.
        #
        # for each package in the separate list next_group:
        #   if the distance to the package's destination is less than the value stored in closest_distance:
        #       set closest_distance's value to the distance to this package's destination
        #       select this package as the next delivery
        for x in next_group:
            distance = calculate_distance(self.current_location, x.location_id)
            if distance < closest_distance:
                closest_distance = distance
                self.next_package = x

    # Delivers all packages by calling next_package at each location. Updates current_location, current_time, and
    # distance_traveled, after each delivery.
    def run_delivery(self, departure_time):
        departure_time = datetime.strptime(departure_time, '%H:%M')
        # Checks if the given departure_time is before current_time.
        if departure_time < self.current_time:
            print('Error: Departure time cannot be in the past.')
        else:
            self.current_time = departure_time
            # Finds each package loaded onto the truck within the all_packages HashTable and set the time_loaded
            # variable to self.current_time.
            for x in self.packages_on_truck:
                first = x.package_id % 10
                second = x.package_id // 10
                if first == 0:
                    second = second - 1
                all_packages.table[first][second][10] = str(self.current_time.time())

            print('Truck ' + str(self.truck_id) +
                  ' departing at ' + str(departure_time.time()) +
                  ' with ' + str(len(self.packages_on_truck)) + ' packages on board.')

            # Checks if any packages are remaining on the truck, and runs the next_delivery() algorithm to choose
            # the next package to deliver.
            while len(self.packages_on_truck) > 0:
                self.next_delivery()
                current_location = self.current_location
                next_location = self.next_package.location_id
                next_package = self.next_package

                # Checks if next_delivery() has the same destination as the previous one, so packages sent to the same
                # destination are delivered simultaneously, with no time delay between them.
                if current_location == next_location:
                    distance_from_last = 0
                    trip_time = timedelta(minutes=0)
                else:
                    distance_from_last = calculate_distance(current_location, next_location)
                    self.distance_traveled += distance_from_last
                    trip_time = timedelta(minutes=((distance_from_last / self.AVERAGE_SPEED) * 60))
                self.current_location = next_location
                self.current_time += trip_time

                first = next_package.package_id % 10
                second = next_package.package_id // 10
                if first == 0:
                    second = second - 1
                all_packages.table[first][second][8] = 'Delivered'
                all_packages.table[first][second][11] = str(self.current_time.time())

                print('   Current time: ' + str(self.current_time.time()) + ', ' +
                      'Current location: ' + str(self.current_location) +
                      ', Package delivered: ' + str(next_package.package_id) +
                      ', Distance from last location: ' + str(distance_from_last) + ' miles, ' +
                      'Total distance traveled: ' + str("%.1f" % self.distance_traveled) + ' miles, ' +
                      'Deliveries remaining: ' + str(len(self.packages_on_truck) - 1) + '.')

                if next_package.deadline < self.current_time:
                    print('LATE DELIVERY')
                self.packages_on_truck.remove(next_package)

            distance_to_hub = float(distances[self.current_location - 1][0])
            self.distance_traveled += distance_to_hub
            return_time = timedelta(minutes=((distance_to_hub / self.AVERAGE_SPEED) * 60))
            self.current_time += return_time

            print('Truck ' + str(self.truck_id) +
                  ' returned to hub at ' + str(self.current_time.time()) +
                  '. Total distance traveled: ' + str("%.1f" % self.distance_traveled) + ' miles.')
            print('')


all_packages = HashTable()

# Populates hash table with .csv package data.
with open('packages.csv') as package_list:
    package_data = csv.reader(package_list)
    next(package_data)
    for package in package_data:
        package_id = int(package[0])
        location_id = int(package[1])
        address = package[2]
        city = package[3]
        state = package[4]
        zipcode = package[5]
        weight = package[6]
        deadline = package[7]
        status = package[8]
        time_received = package[9]
        time_loaded = package[10]
        time_delivered = package[11]

        all_packages.insert(package_id, location_id, address, city, state, zipcode, weight, deadline, status,
                            time_received, time_loaded, time_delivered)

# Parses data from distance table .csv file into a two-dimensional list.
with open('distances.csv') as distance_list:
    distance_data = csv.reader(distance_list)
    next(distance_data)
    distances = list(distance_data)


# Main menu for the user interface.
def main_menu():
    print('\n' + 'Total distance traveled by both trucks: ' + str((truck1.distance_traveled + truck2.distance_traveled))
          + ' miles.')
    print('\n' + 'Please choose an option:')
    print('1) Search for a specific package...')
    print('2) Return a report of all packages...')
    print('3) Exit...')
    data = input()

    if data == '1':
        search_menu()
    if data == '2':
        report_menu()
    if data == '3':
        exit()
    else:
        main_menu()


# Search function that displays each package with matching data in the corresponding field based on the user input.
def search_function(value):
    data = input()
    data_found = 0
    for x in range(len(all_packages.table)):
        for y in range(len(all_packages.table[x])):
            # Prints relevant package data for entries matching the search input.
            if all_packages.table[x][y][value] == data:
                print('\n' + 'Package ID: ' + all_packages.table[x][y][0])
                print('Address: ' + all_packages.table[x][y][2])
                print('City: ' + all_packages.table[x][y][3])
                print('State: ' + all_packages.table[x][y][4])
                print('Zipcode: ' + all_packages.table[x][y][5])
                print('Weight: ' + all_packages.table[x][y][6])
                print('Deadline: ' + all_packages.table[x][y][7])
                print('Status: ' + all_packages.table[x][y][8])
                print('Received: ' + all_packages.table[x][y][9])
                print('Loaded: ' + all_packages.table[x][y][10])
                print('Delivered: ' + all_packages.table[x][y][11])
                data_found = 1
    # Prints a message if no matching entries are found.
    if data_found == 0:
        print('\n' + 'No matching records found.')

    print('\n' + '1) Return to search menu...')
    print('2) Return to main menu...')
    data = input()

    if data == '1':
        search_menu()
    if data == '2':
        main_menu()
    else:
        main_menu()


# Search menu for the user interface.
def search_menu():
    print('\n' + 'Please choose an attribute to search by, or return to the main menu:')
    print('1) ID')
    print('2) Address')
    print('3) City')
    print('4) Zipcode')
    print('5) Weight')
    print('6) Deadline')
    print('7) Status')
    print('\n' + '8) Return to main menu...')
    data = input()
    if data == '1':
        print('\n' + 'Please provide a package ID number:')
        search_function(0)
    if data == '2':
        print('\n' + 'Please provide a delivery address:')
        search_function(2)
    if data == '3':
        print('\n' + 'Please provide a destination city:')
        search_function(3)
    if data == '4':
        print('\n' + 'Please provide a destination zipcode:')
        search_function(5)
    if data == '5':
        print('\n' + 'Please provide a weight value:')
        search_function(6)
    if data == '6':
        print('\n' + 'Please provide a delivery deadline:')
        search_function(7)
    if data == '7':
        print('\n' + 'Please provide a delivery status:')
        search_function(8)
    if data == '8':
        main_menu()
    else:
        main_menu()


# Report menu for the user interface.
def report_menu():
    print('\n' + 'Please enter a time (ex: 15:42) to check the status of all packages at that given time, or ' +
          '\n' + '1) Check the status of a SINGLE package at a specific time...'
          '\n' + '2) Return to the main menu...')
    data = input()

    if data == '2':
        main_menu()
    elif data == '1':
        print('\n' + 'Please enter a package number: ')
        package = int(input())
        first = package % 10
        second = package // 10
        if first == 0:
            second = second - 1
        print('\n' + 'Please enter a time (ex: 15:42) to check the status of the package at that given time: ')
        data = input()
        try:
            if datetime.strptime(data, '%H:%M') < datetime.strptime(all_packages.table[first][second][9], '%H:%M'):
                print('Package ID: ' + all_packages.table[first][second][0] +
                      ', Address: ' + all_packages.table[first][second][2] +
                      ', City: ' + all_packages.table[first][second][3] +
                      ', State: ' + all_packages.table[first][second][4] +
                      ', Zipcode: ' + all_packages.table[first][second][5] +
                      ', Weight: ' + all_packages.table[first][second][6] +
                      ', Deadline: ' + all_packages.table[first][second][7] +
                      ', Status: Not yet received by hub.')
            # Checks if the input time is prior to the package being loaded onto the truck.
            elif datetime.strptime(data, '%H:%M') < datetime.strptime(all_packages.table[first][second][10],
                                                                      '%H:%M:%S'):
                print('Package ID: ' + all_packages.table[first][second][0] +
                      ', Address: ' + all_packages.table[first][second][2] +
                      ', City: ' + all_packages.table[first][second][3] +
                      ', State: ' + all_packages.table[first][second][4] +
                      ', Zipcode: ' + all_packages.table[first][second][5] +
                      ', Weight: ' + all_packages.table[first][second][6] +
                      ', Deadline: ' + all_packages.table[first][second][7] +
                      ', Status: Received by hub at ' +
                      str(datetime.strptime(all_packages.table[first][second][9], '%H:%M').time()) + '.')
            # Checks if the input time is prior to the package being delivered.
            elif datetime.strptime(data, '%H:%M') < datetime.strptime(all_packages.table[first][second][11],
                                                                      '%H:%M:%S'):
                print('Package ID: ' + all_packages.table[first][second][0] +
                      ', Address: ' + all_packages.table[first][second][2] +
                      ', City: ' + all_packages.table[first][second][3] +
                      ', State: ' + all_packages.table[first][second][4] +
                      ', Zipcode: ' + all_packages.table[first][second][5] +
                      ', Weight: ' + all_packages.table[first][second][6] +
                      ', Deadline: ' + all_packages.table[first][second][7] +
                      ', Status: Out for delivery at ' +
                      str(datetime.strptime(all_packages.table[first][second][10], '%H:%M:%S').time()) + '.')
            # Checks if the input time is after the package's delivery time.
            elif datetime.strptime(data, '%H:%M') > datetime.strptime(all_packages.table[first][second][11],
                                                                      '%H:%M:%S'):
                print('Package ID: ' + all_packages.table[first][second][0] +
                      ', Address: ' + all_packages.table[first][second][2] +
                      ', City: ' + all_packages.table[first][second][3] +
                      ', State: ' + all_packages.table[first][second][4] +
                      ', Zipcode: ' + all_packages.table[first][second][5] +
                      ', Weight: ' + all_packages.table[first][second][6] +
                      ', Deadline: ' + all_packages.table[first][second][7] +
                      ', Status: Delivered at ' +
                      str(datetime.strptime(all_packages.table[first][second][11], '%H:%M:%S').time()) + '.')
        except IndexError:
            print('\n' + 'Error: Package not found.')
            report_menu()
        except ValueError:
            print('\n' + 'Error: Time format must be HH:MM.')
            report_menu()
    else:
        try:
            for x in range(len(all_packages.table)):
                for y in range(len(all_packages.table[x])):
                    # Checks if the input time is prior to the package being received.
                    if datetime.strptime(data, '%H:%M') < datetime.strptime(all_packages.table[x][y][9], '%H:%M'):
                        print('Package ID: ' + all_packages.table[x][y][0] +
                              ', Address: ' + all_packages.table[x][y][2] +
                              ', City: ' + all_packages.table[x][y][3] +
                              ', State: ' + all_packages.table[x][y][4] +
                              ', Zipcode: ' + all_packages.table[x][y][5] +
                              ', Weight: ' + all_packages.table[x][y][6] +
                              ', Deadline: ' + all_packages.table[x][y][7] +
                              ', Status: Not yet received by hub.')
                    # Checks if the input time is prior to the package being loaded onto the truck.
                    elif datetime.strptime(data, '%H:%M') < datetime.strptime(all_packages.table[x][y][10], '%H:%M:%S'):
                        print('Package ID: ' + all_packages.table[x][y][0] +
                              ', Address: ' + all_packages.table[x][y][2] +
                              ', City: ' + all_packages.table[x][y][3] +
                              ', State: ' + all_packages.table[x][y][4] +
                              ', Zipcode: ' + all_packages.table[x][y][5] +
                              ', Weight: ' + all_packages.table[x][y][6] +
                              ', Deadline: ' + all_packages.table[x][y][7] +
                              ', Status: Received by hub at ' +
                              str(datetime.strptime(all_packages.table[x][y][9], '%H:%M').time()) + '.')
                    # Checks if the input time is prior to the package being delivered.
                    elif datetime.strptime(data, '%H:%M') < datetime.strptime(all_packages.table[x][y][11], '%H:%M:%S'):
                        print('Package ID: ' + all_packages.table[x][y][0] +
                              ', Address: ' + all_packages.table[x][y][2] +
                              ', City: ' + all_packages.table[x][y][3] +
                              ', State: ' + all_packages.table[x][y][4] +
                              ', Zipcode: ' + all_packages.table[x][y][5] +
                              ', Weight: ' + all_packages.table[x][y][6] +
                              ', Deadline: ' + all_packages.table[x][y][7] +
                              ', Status: Out for delivery at ' +
                              str(datetime.strptime(all_packages.table[x][y][10], '%H:%M:%S').time()) + '.')
                    # Checks if the input time is after the package's delivery time.
                    elif datetime.strptime(data, '%H:%M') > datetime.strptime(all_packages.table[x][y][11], '%H:%M:%S'):
                        print('Package ID: ' + all_packages.table[x][y][0] +
                              ', Address: ' + all_packages.table[x][y][2] +
                              ', City: ' + all_packages.table[x][y][3] +
                              ', State: ' + all_packages.table[x][y][4] +
                              ', Zipcode: ' + all_packages.table[x][y][5] +
                              ', Weight: ' + all_packages.table[x][y][6] +
                              ', Deadline: ' + all_packages.table[x][y][7] +
                              ', Status: Delivered at ' +
                              str(datetime.strptime(all_packages.table[x][y][11], '%H:%M:%S').time()) + '.')
        # Displays an error message if the user input does not match the required time format.
        except ValueError:
            print('\n' + 'Error: Time format must be HH:MM.')
            report_menu()

    print('\n' + '1) Return to report menu...')
    print('2) Return to main menu...')
    data = input()

    if data == '1':
        report_menu()
    if data == '2':
        main_menu()
    else:
        main_menu()


truck1 = Truck(1)
truck2 = Truck(2)

truck1.load_package(13)
truck1.load_package(14)
truck1.load_package(15)
truck1.load_package(16)
truck1.load_package(19)
truck1.load_package(20)
truck1.load_package(21)
truck1.load_package(34)
truck1.load_package(39)
truck1.load_package(29)
truck1.load_package(7)
truck1.load_package(40)
truck1.load_package(1)
truck1.load_package(30)
truck1.load_package(37)
truck1.load_package(8)
truck1.run_delivery('08:00')

truck2.load_package(3)
truck2.load_package(6)
truck2.load_package(18)
truck2.load_package(25)
truck2.load_package(31)
truck2.load_package(36)
truck2.load_package(38)
truck2.load_package(26)
truck2.load_package(32)
truck2.load_package(5)
truck2.load_package(2)
truck2.load_package(33)
truck2.load_package(17)
truck2.run_delivery('09:05')

truck1.load_package(27)
truck1.load_package(35)
truck1.load_package(10)
truck1.load_package(24)
truck1.load_package(9)
truck1.load_package(28)
truck1.load_package(11)
truck1.load_package(23)
truck1.load_package(12)
truck1.load_package(22)
truck1.load_package(4)
truck1.run_delivery('10:20')

main_menu()
