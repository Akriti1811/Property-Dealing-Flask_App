from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def buy():
    return render_template('buy.html')

@app.route("/rent")
def rent():
    return render_template('rent.html')

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)