from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../scripts'))

from etl_functions import (
    process_dim_customer,
    process_dim_room,
    process_dim_payment,
    process_dim_booking_channel,
    process_dim_date,
    process_fact_reservation
)


# Default DAG arguments
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# Define the DAG
with DAG(
    dag_id='etl_star_schema',
    default_args=default_args,
    description='ETL pipeline to generate star schema tables from hotel RDBMS CSVs',
    schedule_interval=None,  # manual trigger
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["hotel_dwh"]
) as dag:

    # Define tasks
    dim_customer_task = PythonOperator(
        task_id='process_dim_customer',
        python_callable=process_dim_customer
    )

    dim_room_task = PythonOperator(
        task_id='process_dim_room',
        python_callable=process_dim_room
    )

    dim_payment_task = PythonOperator(
        task_id='process_dim_payment',
        python_callable=process_dim_payment
    )

    dim_channel_task = PythonOperator(
        task_id='process_dim_booking_channel',
        python_callable=process_dim_booking_channel
    )

    dim_date_task = PythonOperator(
        task_id='process_dim_date',
        python_callable=process_dim_date
    )

    fact_reservation_task = PythonOperator(
        task_id='process_fact_reservation',
        python_callable=process_fact_reservation
    )

    # Set task dependencies
    [
        dim_customer_task,
        dim_room_task,
        dim_payment_task,
        dim_channel_task,
        dim_date_task
    ] >> fact_reservation_task
