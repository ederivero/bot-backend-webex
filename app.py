from flask import Flask, request
from requests import post
from dotenv import load_dotenv
from os import environ
from flask_migrate import Migrate
from db import conexion
from models.groups import Group

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
conexion.init_app(app)
Migrate(app=app, db=conexion)


def send_discord_message(channel, link):
    data = {
        'content': 'Hola @everyone este es el link de la sesion de hoy!',
        'components': [
            {
                'type': 1,
                'components': [
                    {
                        'type': 2,
                        'label': 'Grabacion',
                        'style': 5,
                        'url': link
                    }
                ]

            }
        ]
    }

    token = environ.get('DISCORD_TOKEN')

    post(f'https://discord.com/api/channels/{channel}/messages',
         json=data, headers={'Authorization': f'Bot {token}'})


@app.route('/webex-webhook')
def webex_webhook():
    print('LLEGO DATA DEL WEBHOOK!')
    print(request.json)
    print('-----------')
    send_discord_message('1091148055643959439', 'https://google.com')
    return {
        'message': 'ok'
    }, 204


@app.route('/')
def inicio():
    return {
        'message': 'Welcome to backend webex bot 🤖'
    }


if __name__ == '__main__':
    app.run(debug=True)
