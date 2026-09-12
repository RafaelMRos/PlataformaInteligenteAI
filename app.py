from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "API de Inteligência Artificial funcionando!"


if __name__ == "__main__":
    app.run(debug=True)