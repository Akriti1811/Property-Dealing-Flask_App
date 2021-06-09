from flask import Flask, render_template, request, flash, session, g, redirect, url_for
import pyodbc
import pandas as pd 
from pandas import DataFrame
import os
app = Flask(__name__)
app.secret_key = os.urandom(24)

# conn = pyodbc.connect( 'Driver={SQL Server Native Client 11.0};'
#                         'Server=LAPTOP-EVDFGGHS\SQLEXPRESS;'
#                         'Database=Property_dealing;'
#                         'Trusted_Connection=yes;')
conn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                         "Server=DESKTOP-PLT6RQC\SQLEXPRESS;"
                         "Database=Property_dealing;"
                         "Trusted_Connection=yes;")

cursor = conn.cursor() 
 

@app.route("/",methods=["POST","GET"])
def buy():
    pro_for="Sale"
    heading="BEST MATCHES"
    if request.method == 'POST':
        city=request.form["city"]
        prop=request.form["property_type"]
        bhk=request.form["bhk"]
        min_price=request.form["Min_price"]
        max_price=request.form["Max_price"]
        query= cursor.execute('''SELECT * FROM Property_dealing.dbo.Buy_house WHERE city = ? AND type = ? AND bhk = ? AND price BETWEEN ? AND ? ''',city, prop, bhk, min_price, max_price)
        sql_query=query.fetchall()         
        return render_template('searchview.html',data=sql_query ,pro_for=pro_for ,heading=heading)
        cursor.close()
    return render_template('buy.html')

@app.route("/rent",methods=["POST","GET"])
def rent():
    pro_for="Rent"
    heading="BEST MATCHES"
    if request.method == "POST":
        r_city=request.form["city"]
        r_prop=request.form["property_type"]
        r_bhk=request.form["bhk"]
        r_min_price=request.form["min_price"]
        r_max_price=request.form["max_price"]
        query= cursor.execute('''SELECT * FROM Property_dealing.dbo.Rent_house WHERE city = ? AND type = ? AND bhk = ? AND price BETWEEN ? AND ? ''',r_city, r_prop, r_bhk, r_min_price, r_max_price)
        sql_query=query.fetchall()         
        return render_template('searchview.html',data=sql_query ,pro_for=pro_for ,heading=heading)
        cursor.close()
    return render_template('rent.html')

@app.route("/post",methods=["POST","GET"])
def post():
    message=None
    if request.method == "POST":
        city=request.form["city"]
        prop_type=request.form["property_type"]
        bhk=request.form["bhk"]
        purpose=request.form["gridRadios"]
        locality=request.form["locality"]
        price=request.form["price"]
        bathroom=request.form["bathroom"]
        parking=request.form["parking"]
        furnishing=request.form["furnishing"]
        status=request.form["status"]
        message = "You have posted your property successfully!"       
    return render_template('post.html', message=message)
       
@app.route("/login", methods=['GET', 'POST'])
def login():
    message = None
    error = None
    if request.method == 'POST' and 'Email' in request.form and 'Password' in request.form:
        Email = request.form['Email']
        password = request.form['Password']
        session.pop('loggedin',None)
        session.pop('userid',None)
        query= cursor.execute('''SELECT * FROM Property_dealing.dbo.Users WHERE email_id = ? AND password = ? ''',Email, password)
        account =query.fetchone()
        if account:
            session['loggedin'] = True
            session['userid'] = account[0]
            message = "Logged in successfully!"           
        else:
            error = "Error: Invalid Credentials. Please try again."

    return render_template('login.html', message=message,error=error)

# def login():                 #HARD-CODED login function                          
#     message = None
#     error = None
#     if request.method == 'POST':
#         if request.form['Email'] != 'admin' or request.form['Password'] != 'admin':
#             error = 'Error: Invalid Credentials. Please try again.'
#         else:
#             message = "Logged in successfully!"
#     return render_template('login.html', message=message,error=error)


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    message=None
    error=None
    if request.method == "POST":
        name=request.form["Name"]
        Email=request.form["Email"]
        number=request.form["Number"]
        password=request.form["Password"] 
        num= int(number)
        if num<1000000000 or num>9999999999:
            error= "Number not valid! Please check again."
        else:
            message="Signed-up Successfully!"
        query= cursor.execute("SELECT MAX(user_id) FROM Property_dealing.dbo.Users")
        last_id =query.fetchone()
        last=int(last_id[0])
        user_id=last+1  
        cursor.execute('''INSERT INTO Property_dealing.dbo.Users (user_id, name, Email_id, Phone_no, password) VALUES(?, ?, ?, ?, ?)''',user_id, name, Email, number, password)
        conn.commit()
    return render_template('signup.html',message=message, error=error)

@app.route("/buy_own_pro")
def buy_own_pro():
    pro_for="Sale"
    heading="Owner Properties"
    sql_query= pd.read_sql_query("SELECT * FROM Property_dealing.dbo.Buy_house WHERE type='Builder_Floor'",conn)
    return render_template('cardview.html',data=sql_query ,pro_for=pro_for ,heading=heading)

@app.route("/buy_new_pro")
def buy_new_pro():
    pro_for="Sale"
    heading="New Projects"
    sql_query= pd.read_sql_query("SELECT * FROM Property_dealing.dbo.Buy_house WHERE type='Apartment'",conn)
    return render_template('cardview.html',data=sql_query ,pro_for=pro_for ,heading=heading)

@app.route("/buy_ready")
def buy_ready():
    pro_for="Sale"
    heading="Ready to Move-in Properties"
    sql_query= pd.read_sql_query("SELECT * FROM Property_dealing.dbo.Buy_house WHERE status='Ready_to_move'",conn)
    return render_template('cardview.html',data=sql_query ,pro_for=pro_for ,heading=heading)

@app.route("/buy_furnished")
def buy_furnished():
    pro_for="Sale"
    heading="Furnished Properties"
    sql_query= pd.read_sql_query("SELECT * FROM Property_dealing.dbo.Buy_house WHERE furnishing='Furnished'",conn)
    return render_template('cardview.html',data=sql_query ,pro_for=pro_for ,heading=heading)

@app.route("/rent_own_pro")
def rent_own_pro():
    pro_for="Rent"
    heading="Owner Properties"
    sql_query= pd.read_sql_query("SELECT * FROM Property_dealing.dbo.Rent_house WHERE type='Builder_Floor'",conn)
    return render_template('cardview.html',data=sql_query ,pro_for=pro_for ,heading=heading)

@app.route("/rent_new_pro")
def rent_new_pro():
    pro_for="Rent"
    heading="New Projects"  
    sql_query= pd.read_sql_query("SELECT * FROM Property_dealing.dbo.Rent_house WHERE type='Apartment'",conn)
    return render_template('cardview.html',data=sql_query ,pro_for=pro_for ,heading=heading)

@app.route("/rent_ready")
def rent_ready():
    pro_for="Rent"
    heading="Immediately Available Properties"
    sql_query= pd.read_sql_query("SELECT * FROM Property_dealing.dbo.Rent_house WHERE status='Ready_to_move'",conn)
    return render_template('cardview.html',data=sql_query ,pro_for=pro_for ,heading=heading)

@app.route("/rent_furnished")
def rent_furnished():
    pro_for="Rent"
    heading="Furnished Properties"
    sql_query= pd.read_sql_query("SELECT * FROM Property_dealing.dbo.Rent_house WHERE furnishing='Furnished'",conn)
    return render_template('cardview.html',data=sql_query ,pro_for=pro_for ,heading=heading)

@app.route("/rent_lodging")
def rent_lodging():
    pro_for="Rent"
    heading="Lodging Properties"
    sql_query= pd.read_sql_query("SELECT * FROM Property_dealing.dbo.Rent_house WHERE type='Lodging_property'",conn)
    return render_template('cardview.html',data=sql_query ,pro_for=pro_for ,heading=heading)

@app.route("/propview")
def propview():
    error=None
    if g.loggedin:
        return render_template('propview.html')
   # sql_query= pd.read_sql_query("SELECT * FROM Property_dealing.dbo.Rent_house INNER JOIN Property_dealing.dbo.Users ON Rent_house.user_id=Users.user_id WHERE user_id='id'",conn)
    return redirect(url_for('login'))

@app.before_request
def before_request():
    g.loggedin=None
    if 'loggedin' in session:
        g.loggedin = session['loggedin']


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
