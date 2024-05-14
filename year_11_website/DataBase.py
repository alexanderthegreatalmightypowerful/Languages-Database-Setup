"""Alexander Krakowiak - sql data reciever
Usage of this code as ones own property is prohibited as sighend in the agreement form before
using this software."""

import sqlite3 as sql
import os
from flask import Flask, render_template, redirect, url_for,request
from flask import make_response, jsonify, Response
from flask_cors import CORS
import json
app = Flask(__name__)
CORS(app)
directory = __file__.removesuffix('\\DataBase.py')
path = f'{directory}\\DataBase\\CodingLanguages.db'
print(path)
connection = sql.connect(database=path, uri=True)
cursor = connection.cursor()

new_data_tabel = False
new_data = ''


def get_tabel_data(inp):
    global path
    inp = str(inp).replace('\n', '')
    connection = sql.connect(database=path, uri=True)
    cursor = connection.cursor()
    try:
        if not inp.endswith(';'):
            inp += ';'
        result = cursor.execute(inp).fetchall()
        columns = [i[0] for i in cursor.description]
        print_line = ''

        data = {}
        table_rows = []
        column_data = []

        for column in columns:
            print_line += f'{str(column)}{" " * (15 - len(str(column)))} | '
            data[str(column)] = []
            column_data.append(str(column))
        print(table_rows)

        print_line += f'\n{("_" * 18) * len(columns)}\n'
        colum_name = -1
        for item in result:
            table_rows.append([])
            colum_name += 1
            for words in item:
                #table_rows.append([])
                print_line += f'{str(words)}{" " * (15 - len(str(words)))} | '
                #data[column_data[colum_name]].append(str(words))
                table_rows[colum_name].append(str(words))

            print_line += '\n'
            print(colum_name)

        print(print_line)
        print(table_rows)
        
        return {'columns' : columns, 'data' : data, 'rows' : table_rows}
    except Exception as e:
        print(e)
        return {'columns' : None, 'data' : 'there is no data', 'rows' : None}


@app.route('/get_data', methods=['POST'])
def get_data():
    print(request.form)
    data = request.form.get('data')
    print('DATA:' , data)
    #result = data
    new_data = get_tabel_data(data)
    #new_data = {'data' : new_data['data']}
    return jsonify(new_data)

"""
while True:
    inp = input('What would you like to see: ')
    try:
        if not inp.endswith(';'):
            inp += ';'
        result = cursor.execute(inp).fetchall()
        columns = [i[0] for i in cursor.description]
        print_line = ''
        for column in columns:
            print_line += f'{str(column)}{" " * (15 - len(str(column)))} | '
        print_line += f'\n{("_" * 18) * len(columns)}\n'
        for item in result:
            for words in item:
                print_line += f'{str(words)}{" " * (15 - len(str(words)))} | '
            print_line += '\n'
        print(print_line)
    except Exception as e:
        print(e)
"""
"""
Select Languages.name from Languages
Join Owner On Owner.id = Languages.owner_id
Where Owner.name = "Dennis Ritchie";
"""
#Select Languages.name from Languages Join Owner On Owner.id = Languages.owner_id Where Owner.name = "Dennis Ritchie";

#Select Languages.name from Languages Join Type On Type.id = Languages.language_type_id Where Type.name = "scripting";

if __name__ == "__main__":
    app.run(debug = True)