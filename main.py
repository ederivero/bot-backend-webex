from flask import Flask

app = Flask(__name__)

@app.route('/')
def inicio():
    return {
        'message': 'Welcome to backend webex bot 🤖'
    }

if __name__ == '__main__':
    app.run(debug=True)