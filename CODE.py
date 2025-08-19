import datetime
import random
from typing import List, Dict, Optional
                      
class Driver:
    def __init__(self, name):
        self.name = name
        self.available = True
        self.rating = 5.0
        self.total_rides = 0
        self.total_rating = 0.0
    
    def update_rating(self, new_rating):
        self.total_rating += new_rating
        self.total_rides += 1
        self.rating = self.total_rating / self.total_rides

class User:
    _id_counter = 1
    
    def __init__(self, name, phone, email):
        self.id = User._id_counter
        User._id_counter += 1
        self.name = name
        self.phone = phone
        self.email = email

class Ride:
    _id_counter = 1
    
    def __init__(self, user, driver, pickup, drop, distance, ride_type="private"):
        self.ride_id = Ride._id_counter
        Ride._id_counter += 1
        self.user = user
        self.driver = driver
        self.pickup = pickup
        self.drop = drop
        self.distance = distance
        self.ride_type = ride_type
        self.fare = self.calculate_fare()
        self.status = "Ongoing"
        self.date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.rating = 0.0
    
    def calculate_fare(self):
        base_fare = 50.0
        per_km_rate = 15.0
        return base_fare + (self.distance * per_km_rate)

class SharedRide:
    _id_counter = 1
    
    def __init__(self, driver, pickup, drop, distance, max_passengers=4):
        self.shared_ride_id = SharedRide._id_counter
        SharedRide._id_counter += 1
        self.driver = driver
        self.pickup = pickup
        self.drop = drop
        self.distance = distance
        self.max_passengers = max_passengers
        self.current_passengers = []
        self.status = "Waiting"
        self.date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.individual_fare = self.calculate_shared_fare()
    
    def calculate_shared_fare(self):
        base_fare = 50.0
        per_km_rate = 15.0
        total_fare = base_fare + (self.distance * per_km_rate)
        return total_fare / max(1, len(self.current_passengers))
    
    def add_passenger(self, user):
        if len(self.current_passengers) < self.max_passengers:
            self.current_passengers.append(user)
            self.individual_fare = self.calculate_shared_fare()
            return True
        return False
    
    def is_full(self):
        return len(self.current_passengers) >= self.max_passengers
    
    def get_passenger_count(self):
        return len(self.current_passengers)

class CabService:
    def __init__(self):
        self.drivers = []
        self.users = []
        self.rides = []
        self.shared_rides = []
        self.initialize_system()
    
    def initialize_system(self):
        """Initialize system with default drivers"""
        default_drivers = ["Alice Johnson", "Bob Smith", "Charlie Davis", "Diana Wilson", "Ethan Brown"]
        for name in default_drivers:
            self.add_driver(name)
    
    def add_driver(self, name):
        if len(self.drivers) < 10:
            self.drivers.append(Driver(name))
            print(f"Driver {name} added successfully!")
    
    def register_user(self):
        if len(self.users) >= 10:
            print("Maximum users reached!")
            return None
        
        name = input("Enter your name: ")
        phone = input("Enter your phone number: ")
        email = input("Enter your email: ")
        
        new_user = User(name, phone, email)
        self.users.append(new_user)
        print(f"Registration successful! Your user ID is: {new_user.id}")
        return new_user
    
    def login_user(self):
        try:
            user_id = int(input("Enter your user ID: "))
            for user in self.users:
                if user.id == user_id:
                    return user
            print("User not found!")
            return None
        except ValueError:
            print("Invalid ID format!")
            return None
    
    def find_available_driver(self):
        for driver in self.drivers:
            if driver.available:
                return driver
        return None
    
    def request_ride(self, user):
        if len(self.rides) >= 50:
            print("Maximum rides reached!")
            return
        
        driver = self.find_available_driver()
        if not driver:
            print("No available drivers at the moment. Please try again later.")
            return
        
        pickup = input("Enter pickup location: ")
        drop = input("Enter drop location: ")
        try:
            distance = float(input("Enter distance in km: "))
            if distance <= 0:
                print("Distance must be positive!")
                return
        except ValueError:
            print("Invalid distance format!")
            return
        
        new_ride = Ride(user, driver, pickup, drop, distance)
        self.rides.append(new_ride)
        driver.available = False
        
        print("\n=== Ride Confirmed ===")
        print(f"Ride ID: {new_ride.ride_id}")
        print(f"Driver: {driver.name}")
        print(f"Pickup: {pickup}")
        print(f"Drop: {drop}")
        print(f"Distance: {distance:.2f} km")
        print(f"Estimated Fare: Rs. {new_ride.fare:.2f}")
        print(f"Status: {new_ride.status}")
        print(f"Date: {new_ride.date}")
    
    def complete_ride(self, ride_id):
        for ride in self.rides:
            if ride.ride_id == ride_id and ride.status == "Ongoing":
                ride.status = "Completed"
                ride.driver.available = True
                ride.driver.total_rides += 1
                print(f"Ride {ride_id} completed successfully!")
                print(f"Total fare: Rs. {ride.fare:.2f}")
                return
        print("Ride not found or not ongoing!")
    
    def cancel_ride(self, ride_id):
        for ride in self.rides:
            if ride.ride_id == ride_id and ride.status == "Ongoing":
                ride.status = "Cancelled"
                ride.driver.available = True
                print(f"Ride {ride_id} cancelled successfully!")
                return
        print("Ride not found or not ongoing!")
    
    def rate_driver(self, ride_id, rating):
        for ride in self.rides:
            if ride.ride_id == ride_id and ride.status == "Completed" and ride.rating == 0.0:
                if 1.0 <= rating <= 5.0:
                    ride.rating = rating
                    ride.driver.update_rating(rating)
                    print(f"Thank you for rating driver {ride.driver.name} with {rating:.1f} stars!")
                    return
                else:
                    print("Rating must be between 1 and 5!")
                    return
        print("Ride not found, not completed, or already rated!")
    
    def display_ride_history(self, user):
        print(f"\n=== Ride History for {user.name} ===")
        found = False
        for ride in self.rides:
            if ride.user.id == user.id:
                found = True
                print(f"\nRide ID: {ride.ride_id}")
                print(f"Driver: {ride.driver.name}")
                print(f"Pickup: {ride.pickup}")
                print(f"Drop: {ride.drop}")
                print(f"Distance: {ride.distance:.2f} km")
                print(f"Fare: Rs. {ride.fare:.2f}")
                print(f"Status: {ride.status}")
                print(f"Date: {ride.date}")
                if ride.status == "Completed":
                    print(f"Rating: {ride.rating:.1f}/5.0")
                print("-" * 20)
        
        if not found:
            print("No rides found for this user.")
    
    def display_driver_info(self):
        print("\n=== All Drivers Information ===")
        for driver in self.drivers:
            print(f"\nDriver: {driver.name}")
            print(f"Available: {'Yes' if driver.available else 'No'}")
            print(f"Rating: {driver.rating:.1f}/5.0")
            print(f"Total Rides: {driver.total_rides}")
            print("-" * 20)
    
    def display_available_drivers(self):
        print("\n=== Available Drivers ===")
        found = False
        for driver in self.drivers:
            if driver.available:
                found = True
                print(f"Driver: {driver.name} (Rating: {driver.rating:.1f}/5.0)")
        
        if not found:
            print("No drivers available at the moment.")
    
    def display_admin_menu(self):
        while True:
            print("\n=== Admin Menu ===")
            print("1. Add New Driver")
            print("2. View All Drivers")
            print("3. View All Users")
            print("4. View All Rides")
            print("5. View All Shared Rides")
            print("6. Complete Shared Ride")  # <--- Added menu option
            print("7. Back to Main Menu")
            
            try:
                choice = int(input("Enter your choice: "))
                
                if choice == 1:
                    name = input("Enter driver name: ")
                    self.add_driver(name)
                elif choice == 2:
                    self.display_driver_info()
                elif choice == 3:
                    print("\n=== All Users ===")
                    for user in self.users:
                        print(f"ID: {user.id}, Name: {user.name}, Phone: {user.phone}, Email: {user.email}")
                elif choice == 4:
                    print("\n=== All Rides ===")
                    for ride in self.rides:
                        print(f"Ride ID: {ride.ride_id}, User: {ride.user.name}, Driver: {ride.driver.name}, Status: {ride.status}")
                elif choice == 5:
                    self.display_shared_rides()
                elif choice == 6:  # <--- Handle complete shared ride
                    try:
                        shared_ride_id = int(input("Enter shared ride ID to complete: "))
                        self.complete_shared_ride(shared_ride_id)
                    except ValueError:
                        print("Invalid shared ride ID format!")
                elif choice == 7:
                    break
                else:
                    print("Invalid choice! Please try again.")
            except ValueError:
                print("Invalid input! Please enter a number.")
    
    def create_shared_ride(self, user):
        if len(self.shared_rides) >= 20:
            print("Maximum shared rides reached!")
            return
        
        driver = self.find_available_driver()
        if not driver:
            print("No available drivers at the moment. Please try again later.")
            return
        
        pickup = input("Enter pickup location: ")
        drop = input("Enter drop location: ")
        try:
            distance = float(input("Enter distance in km: "))
            if distance <= 0:
                print("Distance must be positive!")
                return
        except ValueError:
            print("Invalid distance format!")
            return
        
        new_shared_ride = SharedRide(driver, pickup, drop, distance)
        new_shared_ride.add_passenger(user)
        self.shared_rides.append(new_shared_ride)
        driver.available = False
        
        print("\n=== Shared Ride Created ===")
        print(f"Shared Ride ID: {new_shared_ride.shared_ride_id}")
        print(f"Driver: {driver.name}")
        print(f"Pickup: {pickup}")
        print(f"Drop: {drop}")
        print(f"Distance: {distance:.2f} km")
        print(f"Your Fare: Rs. {new_shared_ride.individual_fare:.2f}")
        print(f"Passengers: {new_shared_ride.get_passenger_count()}/{new_shared_ride.max_passengers}")
        print(f"Status: {new_shared_ride.status}")
    
    def join_shared_ride(self, user):
        available_shared_rides = [sr for sr in self.shared_rides 
                                 if sr.status == "Waiting" and not sr.is_full()]
        
        if not available_shared_rides:
            print("No available shared rides to join!")
            return
        
        print("\n=== Available Shared Rides ===")
        for i, ride in enumerate(available_shared_rides, 1):
            print(f"{i}. Shared Ride ID: {ride.shared_ride_id}")
            print(f"   Driver: {ride.driver.name}")
            print(f"   Route: {ride.pickup} → {ride.drop}")
            print(f"   Distance: {ride.distance:.2f} km")
            print(f"   Current Passengers: {ride.get_passenger_count()}/{ride.max_passengers}")
            print(f"   Your Fare: Rs. {ride.individual_fare:.2f}")
            print("-" * 30)
        
        try:
            choice = int(input("Enter ride number to join (0 to cancel): "))
            if choice == 0:
                return
            
            if 1 <= choice <= len(available_shared_rides):
                selected_ride = available_shared_rides[choice - 1]
                if selected_ride.add_passenger(user):
                    print(f"Successfully joined shared ride {selected_ride.shared_ride_id}!")
                    print(f"Updated fare: Rs. {selected_ride.individual_fare:.2f}")
                    print(f"Total passengers: {selected_ride.get_passenger_count()}")
                    
                    if selected_ride.is_full():
                        selected_ride.status = "Ready"
                        print("Ride is now full and ready to depart!")
                else:
                    print("Failed to join ride - may be full!")
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid input format!")
    
    def display_shared_rides(self):
        print("\n=== All Shared Rides ===")
        if not self.shared_rides:
            print("No shared rides available.")
            return
        
        for ride in self.shared_rides:
            print(f"\nShared Ride ID: {ride.shared_ride_id}")
            print(f"Driver: {ride.driver.name}")
            print(f"Route: {ride.pickup} → {ride.drop}")
            print(f"Distance: {ride.distance:.2f} km")
            print(f"Status: {ride.status}")
            print(f"Passengers: {ride.get_passenger_count()}/{ride.max_passengers}")
            print(f"Individual Fare: Rs. {ride.individual_fare:.2f}")
            if ride.current_passengers:
                print("Passengers:")
                for passenger in ride.current_passengers:
                    print(f"  - {passenger.name}")
            print("-" * 30)
    
    # NEW: Complete shared ride
    def complete_shared_ride(self, shared_ride_id):
        for ride in self.shared_rides:
            if ride.shared_ride_id == shared_ride_id and ride.status in ("Ready", "Ongoing"):
                ride.status = "Completed"
                ride.driver.available = True
                ride.driver.total_rides += 1
                print(f"Shared Ride {shared_ride_id} completed successfully!")
                print(f"Total fare per passenger: Rs. {ride.individual_fare:.2f}")
                return
        print("Shared Ride not found or not ready/ongoing!")
    
    def display_user_menu(self, user):
        while True:
            print(f"\n=== User Menu ({user.name}) ===")
            print("1. Request New Ride")
            print("2. Request Shared Ride")
            print("3. Join Shared Ride")
            print("4. View Ride History")
            print("5. View Shared Rides")
            print("6. Complete Ride")
            print("7. Cancel Ride")
            print("8. Rate Driver")
            print("9. View Available Drivers")
            print("10. Complete Shared Ride")  # <--- Added menu option
            print("11. Logout")
            
            try:
                choice = int(input("Enter your choice: "))
                
                if choice == 1:
                    self.request_ride(user)
                elif choice == 2:
                    self.create_shared_ride(user)
                elif choice == 3:
                    self.join_shared_ride(user)
                elif choice == 4:
                    self.display_ride_history(user)
                elif choice == 5:
                    self.display_shared_rides()
                elif choice == 6:
                    try:
                        ride_id = int(input("Enter ride ID to complete: "))
                        self.complete_ride(ride_id)
                    except ValueError:
                        print("Invalid ride ID format!")
                elif choice == 7:
                    try:
                        ride_id = int(input("Enter ride ID to cancel: "))
                        self.cancel_ride(ride_id)
                    except ValueError:
                        print("Invalid ride ID format!")
                elif choice == 8:
                    try:
                        ride_id = int(input("Enter ride ID to rate: "))
                        rating = float(input("Enter rating (1-5): "))
                        self.rate_driver(ride_id, rating)
                    except ValueError:
                        print("Invalid input format!")
                elif choice == 9:
                    self.display_available_drivers()
                elif choice == 10:  # <--- Handle complete shared ride
                    try:
                        shared_ride_id = int(input("Enter shared ride ID to complete: "))
                        self.complete_shared_ride(shared_ride_id)
                    except ValueError:
                        print("Invalid shared ride ID format!")
                elif choice == 11:
                    break
                else:
                    print("Invalid choice! Please try again.")
            except ValueError:
                print("Invalid input! Please enter a number.")
    
    def display_main_menu(self):
        while True:
            print("\n=== CAB SERVICE MANAGEMENT SYSTEM ===")
            print("1. Register New User")
            print("2. User Login")
            print("3. Admin Panel")
            print("4. Exit")
            
            try:
                choice = int(input("Enter your choice: "))
                
                if choice == 1:
                    self.register_user()
                elif choice == 2:
                    user = self.login_user()
                    if user:
                        self.display_user_menu(user)
                elif choice == 3:
                    self.display_admin_menu()
                elif choice == 4:
                    print("Thank you for using our cab service!")
                    break
                else:
                    print("Invalid choice! Please try again.")
            except ValueError:
                print("Invalid input! Please enter a number.")

if __name__ == "__main__":
    service = CabService()
    print("Welcome to the Enhanced Cab Service Management System!")
    service.display_main_menu()
