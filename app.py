import src.sql as sql
from flask import Flask
from src.listeners import listener


app = Flask(__name__)

app.register_blueprint(listener)

if __name__ == "__main__":
	app.run(port=8080)

