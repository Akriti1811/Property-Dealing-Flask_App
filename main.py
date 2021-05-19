from flask import Flask, render_template
import pyodbc
import pandas as pd
app = Flask(__name__)

conn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                         "Server=DESKTOP-PLT6RQC\SQLEXPRESS;"
                         "Database=Property_dealing;"
                         "Trusted_Connection=yes;")

cursor = conn.cursor() 

@app.route("/")
def buy():
    return render_template('buy.html')

@app.route("/rent")
def rent():
    return render_template('rent.html')

@app.route("/post")
def post():
    return render_template('post.html')
       
@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/signup")
def signup():
    return render_template('signup.html')

@app.route("/buy_own_pro")
def buy_own_pro():
    pro_for="Sale"
    sql_query= pd.read_sql_query("SELECT * FROM Property_dealing.dbo.Buy_house WHERE type='Builder_Floor'",conn)
    return render_template('cardview.html',data=sql_query ,pro_for=pro_for)

@app.route("/buy_new_pro")
def buy_new_pro():
    pro_for="Sale"
    sql_query= pd.read_sql_query("SELECT * FROM Property_dealing.dbo.Buy_house WHERE type='Apartment'",conn)
    return render_template('cardview.html',data=sql_query ,pro_for=pro_for)

@app.route("/buy_ready")
def buy_ready():
    pro_for="Sale"
    sql_query= pd.read_sql_query("SELECT * FROM Property_dealing.dbo.Buy_house WHERE status='Ready_to_move'",conn)
    return render_template('cardview.html',data=sql_query ,pro_for=pro_for)

@app.route("/buy_furnished")
def buy_furnished():
    pro_for="Sale"
    sql_query= pd.read_sql_query("SELECT * FROM Property_dealing.dbo.Buy_house WHERE furnishing='Furnished'",conn)
    return render_template('cardview.html',data=sql_query ,pro_for=pro_for)

@app.route("/rent_own_pro")
def rent_own_pro():
    pro_for="Rent"
    sql_query= pd.read_sql_query("SELECT * FROM Property_dealing.dbo.Rent_house WHERE type='Builder_Floor'",conn)
    return render_template('cardview.html',data=sql_query ,pro_for=pro_for)

@app.route("/rent_new_pro")
def rent_new_pro():
    pro_for="Rent"
    sql_query= pd.read_sql_query("SELECT * FROM Property_dealing.dbo.Rent_house WHERE type='Apartment'",conn)
    return render_template('cardview.html',data=sql_query ,pro_for=pro_for)

@app.route("/rent_ready")
def rent_ready():
    pro_for="Rent"
    sql_query= pd.read_sql_query("SELECT * FROM Property_dealing.dbo.Rent_house WHERE status='Ready_to_move'",conn)
    return render_template('cardview.html',data=sql_query ,pro_for=pro_for)

@app.route("/rent_furnished")
def rent_furnished():
    pro_for="Rent"
    sql_query= pd.read_sql_query("SELECT * FROM Property_dealing.dbo.Rent_house WHERE furnishing='Furnished'",conn)
    return render_template('cardview.html',data=sql_query ,pro_for=pro_for)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
