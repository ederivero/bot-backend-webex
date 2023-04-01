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


def send_discord_message(channel: str, download_link: str, playback_link: str, password: str):
    data = {
        'content': f'Hola 🤖 @everyone este es el link de la sesión de hoy! Recuerda que esta es la password: `{password}`',
        'components': [
            {
                'type': 1,
                'components': [
                    {
                        'type': 2,
                        'label': 'Descargar Grabación ⏬',
                        'style': 5,
                        'url': download_link
                    }
                ]

            },
            {
                'type': 1,
                'components': [
                    {
                        'type': 2,
                        'label': 'Visualizar Grabación 👀',
                        'style': 5,
                        'url': playback_link
                    }
                ]

            }
        ]
    }

    token = environ.get('DISCORD_TOKEN')

    post(f'https://discord.com/api/channels/{channel}/messages',
         json=data, headers={'Authorization': f'Bot {token}'})


@app.route('/webex-webhook', methods=['GET', 'POST'])
def webex_webhook():
    print('LLEGO DATA DEL WEBHOOK!')
    print(request.json)
    print('-----------')
    send_discord_message(
        '1091148055643959439', 'https://google.com', 'https://google.com', '123123123')
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
