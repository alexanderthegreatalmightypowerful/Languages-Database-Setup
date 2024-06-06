"""Alexander Krakowiak - sql data reciever
Usage of this code as ones own property is prohibited as sighend in the agreement form before
using this software."""

"""This Code is a internal server for recieving and transmiting data requets\
    from the data base website"""

import sqlite3 as sql
import os
from flask import Flask, render_template, redirect, url_for,request
from flask import make_response, jsonify, Response
from flask_cors import CORS
import json
from requests_oauthlib import OAuth2Session
import ctypes
import hashlib
import cryptography
from cryptography.fernet import Fernet
import pickle
import hmac



app = Flask(__name__)
CORS(app)

directory = __file__.removesuffix('\\DataBase.py')
path = f'{directory}\\DataBase\\CodingLanguages.db'
print(path)
connection = sql.connect(database=path, uri=True)
cursor = connection.cursor()

new_data_tabel = False
new_data = ''

def get_tabel_data(inp): #function to get data
    global path
    inp = str(inp).replace('\n', '')
    connection = sql.connect(database=path, uri=True) # have to reconnect to database as it needs to be in the same thread as the flask thread
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

        for column in columns: # split columns
            print_line += f'{str(column)}{" " * (15 - len(str(column)))} | '
            data[str(column)] = []
            column_data.append(str(column))
        print(table_rows)

        print_line += f'\n{("_" * 18) * len(columns)}\n'
        colum_name = -1
        for item in result: # sort data into rows
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
        return {'columns' : ['N/A'], 'data' : 'there is no data', 'rows' : {'N/A':'N/A'}}


@app.route('/get_data', methods=['POST'])
def get_data(): # request reciever
    print(request.form)
    data = request.form.get('data')
    print('DATA:' , data)
    #result = data
    new_data = get_tabel_data(data)
    #new_data = {'data' : new_data['data']}
    return jsonify(new_data)

#oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=["openid", "email", "profile"])


#hashing_data = {"Thew" : 'alex_smells', "Miguel" : "alex_smells2", "eggyolk" : 'i_dont_smell', "user" : "1234"}

hashing_usernames = ["Thew", "Miguel", "eggyolk", "user"]
hashed_data = {}
hashed_tokens = {}
unhashed_user_names = {}
hashed_keys = {}
"""
for key in hashing_data.keys():
    #for value in hashing_data.values():
        value = hashing_data[key]
        keyc = Fernet.generate_key()
        f = Fernet(keyc)
        token = f.encrypt(key.encode())

        #
        valuec = Fernet.generate_key()
        v = Fernet(valuec)
        valuetoken = v.encrypt(value.encode())

        hashed_data[token] = valuetoken
        hashed_tokens[f] = None

        hashed_tokens[key] = [token, valuetoken]
        hashed_keys[key] = [keyc.decode(), valuec.decode()]
        

print('hashed_data')

with open('hashed_folder\\hashed1.py', 'w') as writer:
    writer.write("hashed_data = " + str(hashed_data))


with open('hashed_folder\\pickled.py', 'w') as writer:
    writer.write('hashed_tokens = '  + str(pickle.dumps(hashed_tokens)) + '\n')
    writer.write('hashed_keys = ' + str(pickle.dumps(hashed_keys)))
    #pickle.dumps
"""

from hashed_folder.hashed1 import *
from hashed_folder.pickled import *


def check_data_validation(username, password):
    tokens = pickle.loads(hashed_tokens)
    #keys = hashed_keys
    keys = pickle.loads(hashed_keys)
    #print(tokens, keys)
    for item in keys.keys():
        decoded_username = Fernet(str(keys[item][0])).decrypt(tokens[item][0])
        decoded_username = decoded_username.decode()
        print(decoded_username, username)
        if hmac.compare_digest(username, decoded_username):
            decoded_password = Fernet(str(keys[item][1])).decrypt(tokens[item][1])
            decoded_password = decoded_password.decode()
            print(decoded_password)
            if hmac.compare_digest(decoded_password, password):
                return True
            else:
                return False
    return False


@app.route('/sign_in', methods = ['POST', 'GET'])
def sign_in():
    #authorization_url, state = oauth.authorization_url(authorization_base_url, access_type='offline', prompt='consent')
    #data = {'url' : redirect}
    print("Reuest sign in")
    name = request.form.get('Name')
    pas = request.form.get('Password')
    data = {}
    data['check'] = check_data_validation(name, pas);
    return jsonify(data)


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

#Select Languages.name, Owner.name from Languages Join Owner On Owner.id = Languages.owner_id Where Owner.name = "Dennis Ritchie";

if __name__ == "__main__":
    app.run(debug = True)

    #AIzaSyDRtO9uewM5eIvsWzUEBx3O6I3aMhnHLBI