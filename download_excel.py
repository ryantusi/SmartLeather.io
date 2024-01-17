import sqlite3
import pandas as pd

def export_data_to_excel():
    # Connect to the SQLite database
    conn = sqlite3.connect('management.db')  # Replace 'your_database.db' with the actual name of your SQLite database
    cursor = conn.cursor()

    # Fetch all table names from the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Create a Pandas Excel writer using the 'xlsxwriter' engine
    excel_writer = pd.ExcelWriter('exported_data.xlsx', engine='openpyxl')

    # Iterate through each table and write it to the Excel file
    for table in tables:
        table_name = table[0]
        query = f"SELECT * FROM {table_name};"
        df = pd.read_sql_query(query, conn)
        df.to_excel(excel_writer, sheet_name=table_name, index=False)

    # Close the Pandas Excel writer and the SQLite connection
    excel_writer.save()
    conn.close()

export_data_to_excel()