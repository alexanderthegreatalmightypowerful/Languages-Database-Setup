import os
import threading

def requests():
    os.system('cmd /k "pip install requests_oauthlib"')

def flask_cors():
    os.system('cmd /k "pip install flask_cors"')

threading.Thread(target = flask_cors).start()
threading.Thread(target = requests).start()

os.system('cmd /k "pip install cryptography"')