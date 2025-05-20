import sqlite3
import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

# -----------------------------------
# STEP 0: Setup
# -----------------------------------
fake = Faker()
conn = sqlite3.connect("hotel_management.db")
cursor = conn.cursor()

# -----------------------------------
# STEP 1: Create Tables
# -----------------------------------
cursor.executescript("""
DROP TABLE IF EXISTS Customers;
DROP TABLE IF EXISTS Booking_Channel;
DROP TABLE IF EXISTS Payments;
DROP TABLE IF EXISTS Services;
DROP TABLE IF EXISTS Hotel_Facilities;
DROP TABLE IF EXISTS Rooms;
DROP TABLE IF EXISTS Bookings;
DROP TABLE IF EXISTS Payments_Details;
DROP TABLE IF EXISTS Service_Usage;
DROP TABLE IF EXISTS Reviews;
DROP TABLE IF EXISTS Staff;
DROP TABLE IF EXISTS Maintenance;

CREATE TABLE Customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    gender TEXT CHECK(gender IN ('Male', 'Female')),
    contact_number TEXT,
    dob DATE,
    city TEXT CHECK(city IN ('Lahore', 'Islamabad', 'Karachi', 'Quetta'))
);

CREATE TABLE Booking_Channel (
    booking_channel_id INTEGER PRIMARY KEY,
    booking_channel TEXT NOT NULL CHECK(booking_channel IN ('Online', 'Walk-in', 'Travel Agent', 'Phone Call'))
);

CREATE TABLE Payments (
    payment_id INTEGER PRIMARY KEY,
    payment_type TEXT NOT NULL CHECK(payment_type IN ('Online', 'Cash', 'Card'))
);

CREATE TABLE Services (
    service_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price REAL NOT NULL
);

CREATE TABLE Hotel_Facilities (
    facility_id INTEGER PRIMARY KEY,
    description TEXT NOT NULL
);

CREATE TABLE Rooms (
    room_id INTEGER PRIMARY KEY,
    room_number TEXT NOT NULL UNIQUE,
    room_type TEXT CHECK(room_type IN ('Single', 'Double', 'Suite')),
    price REAL CHECK(price IN (200, 400, 600))
);

CREATE TABLE Bookings (
    booking_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    room_id INTEGER,
    booking_channel_id INTEGER,
    check_in_date TEXT,
    check_out_date TEXT,
    stay_length INTEGER,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
    FOREIGN KEY (room_id) REFERENCES Rooms(room_id),
    FOREIGN KEY (booking_channel_id) REFERENCES Booking_Channel(booking_channel_id)
);

CREATE TABLE Payments_Details (
    payment_id INTEGER PRIMARY KEY,
    booking_id INTEGER UNIQUE,
    payment_type_id INTEGER,
    amount REAL,
    status TEXT CHECK(status IN ('Paid', 'Pending')),
    FOREIGN KEY (booking_id) REFERENCES Bookings(booking_id),
    FOREIGN KEY (payment_type_id) REFERENCES Payments(payment_id)
);

CREATE TABLE Service_Usage (
    usage_id INTEGER PRIMARY KEY,
    booking_id INTEGER,
    service_id INTEGER,
    quantity INTEGER,
    total_cost REAL,
    FOREIGN KEY (booking_id) REFERENCES Bookings(booking_id),
    FOREIGN KEY (service_id) REFERENCES Services(service_id)
);

CREATE TABLE Reviews (
    review_id INTEGER PRIMARY KEY,
    booking_id INTEGER,
    customer_id INTEGER,
    rating INTEGER CHECK(rating BETWEEN 1 AND 5),
    FOREIGN KEY (booking_id) REFERENCES Bookings(booking_id),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);

CREATE TABLE Staff (
    staff_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT NOT NULL,
    phone TEXT,
    salary REAL
);

CREATE TABLE Maintenance (
    maintenance_id INTEGER PRIMARY KEY,
    room_id INTEGER,
    maintenance_date TEXT,
    staff_id INTEGER,
    status TEXT CHECK(status IN ('Pending', 'In Progress', 'Completed')),
    FOREIGN KEY (room_id) REFERENCES Rooms(room_id),
    FOREIGN KEY (staff_id) REFERENCES Staff(staff_id)
);
""")

# -----------------------------------
# STEP 2: Insert Static Data
# -----------------------------------

# Customers
male_names = ["Ali", "Ahmed", "Hassan", "Usman", "Bilal", "Zaid", "Hamza", "Ahsan", "Fahad", "Tariq",
              "Imran", "Noman", "Shahid", "Naveed", "Waqar", "Farhan", "Kamran", "Amir", "Rizwan", "Sami",
              "Jawad", "Yasir", "Asad", "Kashif", "Zohaib", "Saad", "Rehan", "Umar", "Basit", "Adeel",
              "Anas", "Faizan", "Shahzaib", "Ammar", "Adnan"]

female_names = ["Ayesha", "Fatima", "Zainab", "Sana", "Hira", "Rabia", "Mehwish", "Kiran", "Mariam", "Areeba",
                "Mahnoor", "Iqra", "Laiba", "Huma", "Nimra"]

cities = ["Lahore", "Karachi", "Islamabad", "Quetta"]
customers = []

for i, name in enumerate(male_names, start=1):
    customers.append((i, name, "Male", fake.msisdn()[:11], fake.date_of_birth(minimum_age=19, maximum_age=75).isoformat(), random.choice(cities)))

for i, name in enumerate(female_names, start=36):
    customers.append((i, name, "Female", fake.msisdn()[:11], fake.date_of_birth(minimum_age=19, maximum_age=75).isoformat(), random.choice(cities)))

cursor.executemany("INSERT INTO Customers VALUES (?, ?, ?, ?, ?, ?);", customers)

# Booking Channels
cursor.executemany("INSERT INTO Booking_Channel VALUES (?, ?);", [
    (1, "Online"), (2, "Walk-in"), (3, "Travel Agent"), (4, "Phone Call")
])

# Payments
cursor.executemany("INSERT INTO Payments VALUES (?, ?);", [
    (1, "Online"), (2, "Cash"), (3, "Card")
])

# Services (without Wi-Fi)
cursor.executemany("INSERT INTO Services VALUES (?, ?, ?);", [
    (1, "Laundry", 100), (2, "Room Service", 200),
    (3, "Spa", 500), (4, "Gym", 150)
])

# Hotel Facilities
cursor.executemany("INSERT INTO Hotel_Facilities VALUES (?, ?);", [
    (1, "Swimming Pool"), (2, "Gymnasium"),
    (3, "Conference Room"), (4, "Restaurant"), (5, "Parking Area")
])

# Rooms
rooms = []
room_types = [("Single", 200), ("Double", 400), ("Suite", 600)]
room_id = 1
for rtype, price in room_types:
    for i in range(10):
        room_number = f"{rtype[:2].upper()}{i+1:02d}"  # Unique per type
        rooms.append((room_id, room_number, rtype, price))
        room_id += 1
cursor.executemany("INSERT INTO Rooms VALUES (?, ?, ?, ?);", rooms)

# -----------------------------------
# STEP 3: Staff and Maintenance
# -----------------------------------
roles = ["Cleaner", "Technician", "Receptionist", "Manager"]
staff_data = [(i, fake.name(), random.choice(roles), fake.msisdn()[:11], round(random.uniform(25000, 70000), 2)) for i in range(1, 16)]
cursor.executemany("INSERT INTO Staff VALUES (?, ?, ?, ?, ?);", staff_data)

maintenance_data = []
for i in range(1, 21):
    maintenance_data.append((
        i,
        random.randint(1, 30),
        fake.date_between_dates(datetime(2024, 1, 1), datetime(2024, 12, 31)).isoformat(),
        random.randint(1, 15),
        random.choice(["Pending", "In Progress", "Completed"])
    ))
cursor.executemany("INSERT INTO Maintenance VALUES (?, ?, ?, ?, ?);", maintenance_data)

# -----------------------------------
# STEP 4: Bookings
# -----------------------------------
def rand_date():
    start = datetime(2024, 1, 1)
    return start + timedelta(days=random.randint(0, 364))

bookings = []
for bid in range(1, 4201):
    check_in = rand_date()
    stay = random.randint(1, 7)
    bookings.append((
        bid,
        random.randint(1, 50),
        random.randint(1, 30),
        random.randint(1, 4),
        check_in.isoformat(),
        (check_in + timedelta(days=stay)).isoformat(),
        stay
    ))
cursor.executemany("INSERT INTO Bookings VALUES (?, ?, ?, ?, ?, ?, ?);", bookings)

# -----------------------------------
# STEP 5: Service Usage
# -----------------------------------
service_prices = {1: 100, 2: 200, 3: 500, 4: 150}
usage_id = 1
usage_data = []
service_totals = {}

for b in range(1, 4201):
    num_services = random.randint(0, 3)
    selected = random.sample(list(service_prices.items()), num_services)
    for sid, price in selected:
        qty = random.randint(1, 5)
        total = qty * price
        usage_data.append((usage_id, b, sid, qty, total))
        service_totals[b] = service_totals.get(b, 0) + total
        usage_id += 1

cursor.executemany("INSERT INTO Service_Usage VALUES (?, ?, ?, ?, ?);", usage_data)

# -----------------------------------
# STEP 6: Payments
# -----------------------------------
room_prices = {room[0]: room[3] for room in rooms}
payments = []
for b in bookings:
    booking_id = b[0]
    room_price = room_prices.get(b[2], 0)
    total_amount = (room_price * b[6]) + service_totals.get(booking_id, 0)
    payments.append((
        booking_id,
        booking_id,
        random.randint(1, 3),
        round(total_amount, 2),
        random.choice(["Paid", "Pending"])
    ))
cursor.executemany("INSERT INTO Payments_Details VALUES (?, ?, ?, ?, ?);", payments)

# -----------------------------------
# STEP 7: Reviews
# -----------------------------------
reviews = []
review_id = 1
for b in bookings:
    if random.random() < 0.65:
        reviews.append((review_id, b[0], b[1], random.randint(1, 5)))
        review_id += 1
cursor.executemany("INSERT INTO Reviews VALUES (?, ?, ?, ?);", reviews)

# -----------------------------------
# STEP 8: Finalize
# -----------------------------------
conn.commit()
conn.close()
print("✅ All data inserted into hotel_management.db successfully!")
