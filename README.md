# Largest Banks ETL Pipeline

## Project Overview

A Python-based ETL (Extract, Transform, Load) pipeline that extracts data about the world's largest banks by market capitalization, transforms financial values into multiple currencies, and loads the results into CSV and SQLite database formats.

This project demonstrates practical skills in Web Scraping, Data Processing, Data Transformation, SQL, and Python automation.

## Technologies Used

- Python
- Pandas
- NumPy
- Requests
- BeautifulSoup
- SQLite
- CSV

## ETL Process

### 1. Extract

- Retrieve data from the archived Wikipedia page.
- Parse HTML content using BeautifulSoup.
- Extract bank names and market capitalization in USD.
- Convert market capitalization values into numeric data types.

### 2. Transform

- Load currency exchange rates from `exchange_rate.csv`.
- Convert market capitalization values from USD into:
  - GBP – British Pound
  - EUR – Euro
  - INR – Indian Rupee
- Round converted values to two decimal places.

### 3. Load

- Export the transformed dataset to `Largest_banks_data.csv`.
- Store the final dataset in an SQLite database named `Banks.db`.
- Create a database table named `Largest_banks`.

### 4. SQL Analysis

Execute SQL queries to:

- Retrieve all records from the database.
- Calculate the average market capitalization in GBP.
- Retrieve the names of the top five banks.

## Project Structure

```text
largest-banks-etl-pipeline/
│
├── banks_project.py
├── exchange_rate.csv
├── Largest_banks_data.csv
├── README.md
└── .gitignore
```

**Generated Files:**

The following files are created automatically when the Python script runs:

- `Banks.db` – SQLite database.
- `code_log.txt` – ETL execution log.

## How to Run

### 1. Install the required libraries

```bash
pip install pandas numpy requests beautifulsoup4
```

### 2. Make sure the following files are in the project directory

- `banks_project.py`
- `exchange_rate.csv`

### 3. Run the Python script

```bash
python banks_project.py
```

The script will execute the ETL pipeline and generate the output CSV file, SQLite database, and execution log.

## Key Skills Demonstrated

- Web Scraping
- ETL Pipeline Development
- Data Cleaning and Transformation
- Python Programming
- Pandas and NumPy
- SQL and SQLite
- Data Export and Database Loading
- Logging and Process Monitoring

## Author

**Mohammed Ahmed Badawy**

Data Analyst | Python | SQL | Power BI | Data Engineering

---

*This project was completed as part of the IBM Data Engineering learning track on Coursera.*
