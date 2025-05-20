import sqlite3
import pandas as pd
import os

# -----------------------------------
# STEP 1: Connect to the database
# -----------------------------------
db_path = "hotel_management.db"
conn = sqlite3.connect(db_path)

# -----------------------------------
# STEP 2: List of all tables to export
# -----------------------------------
tables = [
    "Customers",
    "Booking_Channel",
    "Payments",
    "Services",
    "Hotel_Facilities",
    "Rooms",
    "Bookings",
    "Payments_Details",
    "Service_Usage",
    "Reviews",
    "Staff",
    "Maintenance"
]

# -----------------------------------
# STEP 3: Export each table to CSV
# -----------------------------------
output_dir = "csv_exports"
os.makedirs(output_dir, exist_ok=True)

for table in tables:
    df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
    filename = f"{output_dir}/{table.lower()}.csv"
    df.to_csv(filename, index=False)
    print(f"✅ Exported: {filename}")

# -----------------------------------
# STEP 4: Finish
# -----------------------------------
conn.close()
print("\n✅ All tables exported successfully to 'csv_exports/' folder.")
