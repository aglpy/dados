import os
width = os.get_terminal_size().columns - 1
import time
import boto3
import yaml
from data import streamer
from funcs import userify, hasher
import app

print("Conectando con el servidor...", end='\r')
creds = yaml.safe_load(open('credentials.yaml'))
ACCESS_KEY = creds.get('ACCESS_KEY')
SECRET_KEY = creds.get('SECRET_KEY')
ddb = boto3.resource('dynamodb', region_name='eu-west-3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
table = ddb.Table('dados')
print(" "*width, end='\r')

player = input('Alias: ')
print('Accediendo...', end='\r')
players = userify(streamer.get_data(table))
if player in players.keys():
    password = input('Contraseña: ')
    while hasher(password) != players.get(player):
        password = input('Contraseña incorrecta\nContraseña: ')
else:
    password = input('Registrando nuevo jugador\nContraseña: ')
    streamer.send(table, player, 0, 'null', hasher(password), 'null', 'null')

app.run_server(table, player)