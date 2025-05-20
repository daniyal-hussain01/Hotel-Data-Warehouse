# 🏨 Hotel Data Warehouse Project

This project implements a data warehouse solution for a hotel management system using SQLite, Python, Apache Airflow, and Docker. The ETL pipeline transforms raw relational data into a star schema, enabling future analytics and dashboarding.

---

## 📂 Project Structure

```

hotel\_project/
├── csv\_exports/          # Raw CSVs exported from SQLite (RDBMS)
├── output\_data/          # Cleaned, transformed CSVs (Star Schema)
├── dags/                 # Airflow DAG for ETL pipeline
├── scripts/              # Scripts for schema creation and data insertion
├── hotel\_management.db   # SQLite database with hotel data
├── docker-compose.yml    # Docker setup for Apache Airflow
├── insert\_data.py        # Inserts data into SQLite
├── export\_to\_csv.py      # Exports RDBMS tables to CSV
├── Project Report.docx   # Project documentation
├── WorkFlow\_Snapshots.pdf # Screenshots of Airflow pipeline
├── README.md             # You're reading this file!
├── requirements.txt      # Python package list

````

---

## ⚙️ How to Run the Project

### 1. Clone the Repository and Set Up Virtual Environment
```bash
git clone https://github.com/yourusername/hotel-dwh-project.git
cd hotel-dwh-project
python -m venv venv
.\venv\Scripts\activate      # On Windows
pip install -r requirements.txt
````

### 2. Start Airflow with Docker

```bash
docker-compose down --volumes --remove-orphans
docker-compose up airflow-init
docker-compose up
```

### 3. Trigger ETL DAG

* Open your browser: [http://localhost:8080](http://localhost:8080)
* Login (default: airflow / airflow)
* Trigger the DAG manually

---

## 📈 Outputs

* Final transformed CSVs in `output_data/` (for data warehouse)
* Screenshots in `WorkFlow_Snapshots.pdf`
* Database schema diagrams: `hotel_erd.png` and `hotel_star_schema.png`

---

## 🔧 Tools & Technologies

* Python 3.x
* SQLite
* Apache Airflow
* Docker
* Faker (for sample data)
* pandas

---

## 📄 Authors

* Syed Muhammad Meesum Abbas
* Syed Daniyal Hussain
  (MS Data Science – Institute of Business Administration)


