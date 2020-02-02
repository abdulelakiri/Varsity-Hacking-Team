from flask import Flask
from webpage.routes import home, page_not_found

app = Flask(__name__)

app.register_blueprint(home)
app.register_error_handler(404, page_not_found)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port='8080',debug=True)