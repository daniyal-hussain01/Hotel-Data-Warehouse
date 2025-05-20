import pandas as pd
import os

# Define paths inside Airflow container
CSV_INPUT_PATH = "/opt/airflow/csv_exports/"
CSV_OUTPUT_PATH = "/opt/airflow/output_data/"

def validate_and_save(df, filename):
    output_file = os.path.join(CSV_OUTPUT_PATH, filename)
    df.to_csv(output_file, index=False)

def process_dim_customer():
    df = pd.read_csv(os.path.join(CSV_INPUT_PATH, "customers.csv"))
    df = df[['customer_id', 'customer_name', 'gender', 'city']]
    df.dropna(inplace=True)
    validate_and_save(df, "dim_customer.csv")

def process_dim_room():
    df = pd.read_csv(os.path.join(CSV_INPUT_PATH, "rooms.csv"))
    df = df[['room_id', 'room_type']]
    df.dropna(inplace=True)
    validate_and_save(df, "dim_room.csv")

def process_dim_payment():
    df = pd.read_csv(os.path.join(CSV_INPUT_PATH, "payments.csv"))
    df = df[['payment_id', 'payment_type']]
    df.dropna(inplace=True)
    validate_and_save(df, "dim_payment.csv")

def process_dim_booking_channel():
    df = pd.read_csv(os.path.join(CSV_INPUT_PATH, "booking_channel.csv"))
    df = df[['booking_channel_id', 'booking_channel']]
    df.dropna(inplace=True)
    validate_and_save(df, "dim_booking_channel.csv")

def process_dim_date():
    date_range = pd.date_range(start='2024-01-01', end='2024-12-31')
    df = pd.DataFrame({'date': date_range})
    df['date_key'] = df['date'].dt.strftime('%Y%m%d').astype(int)
    df['day'] = df['date'].dt.day
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    df['day_name'] = df['date'].dt.day_name()
    df['week_number'] = df['date'].dt.isocalendar().week
    df['quarter'] = df['date'].dt.quarter
    df['is_weekend'] = df['day_name'].isin(['Saturday', 'Sunday'])
    df = df[['date_key', 'date', 'day', 'month', 'year', 'day_name', 'week_number', 'quarter', 'is_weekend']]
    validate_and_save(df, "dim_date.csv")

def process_fact_reservation():
    bookings = pd.read_csv(os.path.join(CSV_INPUT_PATH, "bookings.csv"))
    payments = pd.read_csv(os.path.join(CSV_INPUT_PATH, "payments_details.csv"))
    rooms = pd.read_csv(os.path.join(CSV_INPUT_PATH, "rooms.csv"))
    reviews = pd.read_csv(os.path.join(CSV_INPUT_PATH, "reviews.csv"))
    services = pd.read_csv(os.path.join(CSV_INPUT_PATH, "service_usage.csv"))
    dim_date = pd.read_csv(os.path.join(CSV_OUTPUT_PATH, "dim_date.csv"))

    bookings['check_in_date'] = pd.to_datetime(bookings['check_in_date'])
    dim_date['date'] = pd.to_datetime(dim_date['date'])
    bookings = bookings.merge(dim_date[['date', 'date_key']], left_on='check_in_date', right_on='date', how='left')

    service_agg = services.groupby('booking_id').agg(
        total_services_used=pd.NamedAgg(column='service_id', aggfunc='count'),
        total_service_amount=pd.NamedAgg(column='total_cost', aggfunc='sum')
    ).reset_index()

    df = bookings.merge(payments, on='booking_id', how='left') \
                 .merge(rooms[['room_id', 'price']], on='room_id', how='left') \
                 .merge(reviews[['booking_id', 'rating']], on='booking_id', how='left') \
                 .merge(service_agg, on='booking_id', how='left')

    df['total_services_used'] = df['total_services_used'].fillna(0).astype(int)
    df['total_service_amount'] = df['total_service_amount'].fillna(0)

    df = df.rename(columns={"booking_id": "reservation_id"})

    df = df[[
        'reservation_id',
        'customer_id',
        'room_id',
        'booking_channel_id',
        'payment_type_id',
        'date_key',
        'stay_length',
        'total_services_used',
        'total_service_amount',
        'amount',
        'rating'
    ]].dropna(subset=['reservation_id', 'customer_id', 'room_id', 'date_key'])

    validate_and_save(df, "fact_reservation.csv")
