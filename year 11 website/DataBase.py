import sqlite3 as sql
import os
directory = __file__.removesuffix('\\DataBase.py')
path = f'{directory}\\DataBase\\Loser.db'
print(path)
connection = sql.connect(database=path, uri=True)
cursor = connection.cursor()
result = cursor.execute("SELECT vegetable FROM Die where status = 'Good'").fetchall()

print(result)

