import os
os.environ['LC_ALL'] = 'en_US.UTF-8'
os.environ['LANG'] = 'en_US.UTF-8'

import psycopg2

try:
    conn = psycopg2.connect(
        dbname="bayern",
        user="oesterreich",
        password="T48R0JhMHfLRQj3i86Tv3810txboBkOI",
        host="dpg-cqmn0so8fa8c73afbo0g-a",
        port="5432"
    )
    print("Connection successful")
except Exception as e:
    print(f"Connection failed: {e}")