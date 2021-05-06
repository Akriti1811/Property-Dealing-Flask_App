from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def buy():
    return render_template('buy.html')

@app.route("/rent")
def rent():
    return render_template('rent.html')

@app.route("/post")
def post():
    return render_template('post.html')

@app.route("/cardview")
def cardview():
    return render_template('cardview.html')
   
@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/signup")
def signup():
    return render_template('signup.html')

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)