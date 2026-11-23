
import pandas as pd
import numpy as np
import requests
import sqlite3

from bs4 import BeautifulSoup
from datetime import datetime


# Configuration
url = 'https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks'

table_attribs = ['Name', 'MC_USD_Billion']

csv_path = './exchange_rate.csv'
output_csv = './Largest_banks_data.csv'

db_name = 'Banks.db'
table_name = 'Largest_banks'

log_file = 'code_log.txt'


# TASK 1: Logging
def log_progress(message):
    timestamp_format = '%Y-%h-%d-%H:%M:%S'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)

    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(timestamp + ' : ' + message + '\n')
log_progress('Preliminaries complete. Initiating ETL process')

# TASK 2: Extraction
def extract(url, table_attribs):

    headers = {'User-Agent': 'Mozilla/5.0'}

    response = requests.get(
        url,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.select_one(
        'table.wikitable.sortable.mw-collapsible'
    )

    if table is None:
        raise ValueError('Target table was not found.')

    rows = table.find_all('tr')

    bank_data = []

    for row in rows[1:]:

        col = row.find_all('td')

        if len(col) >= 3:

            bank_name = col[1].get_text(strip=True)

            market_cap = col[2].get_text(strip=True)

            market_cap = float(
                market_cap.replace(',', '').replace('\n', '').strip()
            )

            bank_data.append({
                'Name': bank_name,
                'MC_USD_Billion': market_cap
            })

    df = pd.DataFrame(bank_data, columns=table_attribs)

    return df


df = extract(url, table_attribs)

print(df)

log_progress(
    'Data extraction complete. Initiating Transformation process'
)


# TASK 3: Transformation
def transform(df, csv_path):

    exchange_rate_df = pd.read_csv(csv_path)

    exchange_rate = exchange_rate_df.set_index(
        'Currency'
    )['Rate'].to_dict()

    gbp_rate = float(exchange_rate['GBP'])
    eur_rate = float(exchange_rate['EUR'])
    inr_rate = float(exchange_rate['INR'])

    df['MC_GBP_Billion'] = [
        np.round(x * gbp_rate, 2)
        for x in df['MC_USD_Billion']
    ]

    df['MC_EUR_Billion'] = [
        np.round(x * eur_rate, 2)
        for x in df['MC_USD_Billion']
    ]

    df['MC_INR_Billion'] = [
        np.round(x * inr_rate, 2)
        for x in df['MC_USD_Billion']
    ]

    return df


df = transform(df, csv_path)

print(df)

print('5th largest bank in EUR:')
print(df['MC_EUR_Billion'][4])

log_progress(
    'Data transformation complete. Initiating Loading process'
)


# TASK 4: Loading to CSV
def load_to_csv(df, output_path):

    df.to_csv(output_path, index=False)


load_to_csv(df, output_csv)

log_progress('Data saved to CSV file')


# TASK 5: Loading to Database
sql_connection = sqlite3.connect(db_name)

log_progress('SQL Connection initiated')


def load_to_db(df, sql_connection, table_name):

    df.to_sql(
        table_name,
        sql_connection,
        if_exists='replace',
        index=False
    )


load_to_db(df, sql_connection, table_name)

log_progress(
    'Data loaded to Database as a table, Executing queries'
)


# TASK 6: Running SQL Queries
def run_query(query_statement, sql_connection):

    print('\nSQL Query:')
    print(query_statement)

    query_output = pd.read_sql_query(
        query_statement,
        sql_connection
    )

    print(query_output)

    log_progress(
        'SQL query executed: ' +
        ' '.join(query_statement.split())
    )


query_statement = 'SELECT * FROM Largest_banks'

run_query(query_statement, sql_connection)


query_statement = 'SELECT AVG(MC_GBP_Billion) FROM Largest_banks'

run_query(query_statement, sql_connection)


query_statement = 'SELECT Name FROM Largest_banks LIMIT 5'

run_query(query_statement, sql_connection)


# TASK 7: Completion
log_progress('Process Complete')

sql_connection.close()

log_progress('Server Connection closed')
