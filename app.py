from flask import Flask, request
from requests import post, get
from dotenv import load_dotenv
from os import environ
from flask_migrate import Migrate
from db import conexion
from models.groups import Group
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
conexion.init_app(app)
Migrate(app=app, db=conexion)


def send_discord_message(channel: str, date, download_link: str, playback_link: str, password: str):
    data = {
        'content': f'Hola 🤖 @everyone este es el link de la sesión de hoy **{date}** 🗓️! Recuerda que esta es la password: `{password}` 🔑',
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
    print(data)
    result = post(f'https://discord.com/api/channels/{channel}/messages',
                  json=data, headers={'Authorization': f'Bot {token}'})

    print(result.status_code)


@app.route('/webex-webhook', methods=['GET', 'POST'])
def webex_webhook():
    print('LLEGO DATA DEL WEBHOOK!')
    print(request.json)
    print('-----------')

    record_id = request.json.get('data').get('id')
    token = environ.get('WEBEX_TOKEN')
    result = get(f'https://webexapis.com/v1/recordings/{record_id}',
                 headers={'Authorization': f'Bearer {token}'})

    if (result.status_code == 401):
        print('Token del webex invalida')
        return {
            'message': 'ok'
        }, 204
    webex_data = result.json()
    name = webex_data.get('topic')
    # TEMPORAL
    name = name.split('-')[1]
    # TEMPORAL FIN
    print(name)

    group = conexion.session.query(Group).filter(
        Group.name.like(f"%{name}%")).first()

    if not group:
        return {
            'message': 'ok'
        }, 200

    fecha_webex = datetime.strptime(webex_data.get('createTime'),'%Y-%m-%dT%H:%M:%SZ')
    hora = fecha_webex.hour

    if hora - 5 < 0:
        fecha_webex = fecha_webex.replace(day= fecha_webex.day - 1)

    send_discord_message(
        group.channel, fecha_webex.strftime('%Y-%m-%d'), webex_data.get('downloadUrl'), webex_data.get('playbackUrl'), webex_data.get('password'))

    return {
        'message': 'ok'
    }, 204


@app.route('/login-webex', methods=['GET'])
def login_webex():
    print('login!')
    print(request.args)
    return {'message': 'ok'}, 200


@app.route('/')
def inicio():
    return {
        'message': 'Welcome to backend webex bot 🤖'
    }


if __name__ == '__main__':
    app.run(debug=True)
