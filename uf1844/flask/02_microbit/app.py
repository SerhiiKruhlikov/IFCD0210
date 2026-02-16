from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/software/")
def software():
    return render_template('software.html')


@app.route("/firmware/")
def firmware():
    return render_template('firmware.html')


if __name__ == "__main__":
    app.run(debug=True)
