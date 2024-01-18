import sqlite3
import pandas as pd

def export_all_tables_to_excel(db_file_path='management.db', excel_file_path='management.xlsx'):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file_path)

    # Get a list of all tables
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Excel writer engine
    excel_writer = pd.ExcelWriter(excel_file_path, engine='xlsxwriter')

    # Loop through all tables and export data to Excel
    for table in tables:
        table_name = table[0]
        query = f"SELECT * FROM {table_name};"
        df = pd.read_sql_query(query, conn)
        df.to_excel(excel_writer, sheet_name=table_name, index=False)

    # Save the Excel file
    excel_writer.close()
    conn.close()
