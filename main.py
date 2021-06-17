from flask import Flask, render_template, request, session, g, redirect, url_for
import pyodbc
import pandas as pd 
from pandas import DataFrame
import os
import json
import application

app = Flask(__name__)
app.secret_key = os.urandom(24)

conn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                         "Server=DESKTOP-PLT6RQC\SQLEXPRESS;"
                        #  "Server=LAPTOP-EVDFGGHS\SQLEXPRESS;"
                        #  "Server=DESKTOP-TS4AFA1;"
                         "Database=Property_dealing;"
                         "Trusted_Connection=yes;")

cursor = conn.cursor() 
 

@app.route("/",methods=["POST","GET"])
def buy():

    f=open('buy_input.json')  # using json file to store user input to be used by ML model
    data=f.read()
    ss=json.loads(data)
    f.close()
        
    pro_for="Sale"
    heading="BEST MATCHES"
    error=None
    if request.method == 'POST':
        city=request.form["city"]
        prop=request.form["property_type"]
        bhk=request.form["bhk"]
        locality=request.form["locality"]
        min_price=request.form["Min_price"]
        max_price=request.form["Max_price"]
        furnish=request.form["furnishing"]
        
        # Updating json file
        ss['city']=city
        ss['propert_y']=prop
        ss['bhk']=bhk
        ss['min_price']=min_price
        ss['max_price']=max_price
        ss['furnishing']=furnish
        ss['variable']=0
        g=open('buy_input.json',"w")
        json.dump(ss, g)
        g.close()
        # {"city":"c","propert_y":"prop","bhk":0,"min_price":0,"max_price":0,"furnishing":"furnish","variable":0,"predicted_price":0}
        predicted_price=(application.index())
        price=(int)(predicted_price[0])

        print("nearest id's:")

        for i in range (predicted_price[1].size):
            print(predicted_price[1][i])

        query= cursor.execute('''SELECT * FROM Property_dealing.dbo.Buy_house WHERE city = ? AND type = ? AND bhk = ? AND furnishing = ? AND price BETWEEN ? AND ? AND locality LIKE '%'+?+'%' ''',city, prop, bhk, furnish, min_price, max_price, locality)
        sql_query=query.fetchall() 
        if cursor.rowcount == 0:
            heading="NO MATCHES FOUND"
            error="true"
        return render_template('searchview.html',data=sql_query ,pro_for=pro_for ,heading=heading,error=error,price=price)
        cursor.close()
    return render_template('buy.html')

@app.route("/rent",methods=["POST","GET"])
def rent():
    
    f=open('buy_input.json')
    data=f.read()
    ss=json.loads(data)
    

    pro_for="Rent"
    heading="BEST MATCHES"
    error=None
    if request.method == "POST":
        r_city=request.form["city"]
        r_prop=request.form["property_type"]
        r_bhk=request.form["bhk"]
        r_locality=request.form["locality"]
        r_min_price=request.form["min_price"]
        r_max_price=request.form["max_price"]
        r_furnish=request.form["furnishing"]
        r_min_price=request.form["min_price"]
        r_max_price=request.form["max_price"]
         
        # Updating json file
        ss['city']=r_city
        ss['propert_y']=r_prop
        ss['bhk']=r_bhk
        ss['min_price']=r_min_price
        ss['max_price']=r_max_price
        ss['furnishing']=r_furnish
        ss['variable']=1
        g=open('buy_input.json',"w")
        json.dump(ss, g)
        g.close()

        predicted_price=(application.index())
        price=(int)(predicted_price[0])
        print("nearest id's:")

        for i in range (predicted_price[1].size):
            print(predicted_price[1][i])

        query= cursor.execute('''SELECT * FROM Property_dealing.dbo.Rent_house WHERE city = ? AND type = ? AND bhk = ? AND furnishing = ? AND price BETWEEN ? AND ? AND locality LIKE '%'+?+'%' ''',r_city, r_prop, r_bhk, r_furnish, r_min_price, r_max_price,r_locality)
        sql_query=query.fetchall() 
        if cursor.rowcount == 0:
            heading="NO MATCHES FOUND"
            error="true"        
        return render_template('searchview.html',data=sql_query ,pro_for=pro_for ,heading=heading,error=error,price=price)
        cursor.close()
    return render_template('rent.html')

@app.route("/post",methods=["POST","GET"])
def post():
    if g.loggedin:
        message=None
        if request.method == "POST":
            city=request.form["city"]
            prop_type=request.form["property_type"]
            bhk=request.form["bhk"]
            purpose=request.form["gridRadios"]
            locality=request.form["locality"]
            area=request.form["area"]
            price=request.form["price"]
            bathroom=request.form["bathroom"]
            parking=request.form["parking"]
            furnishing=request.form["furnishing"]
            status=request.form["status"]
            user_id=session['userid']
            message = "You have posted your property successfully!"   
            if prop_type=="Lodging_property":
                purpose="Rent"
            if purpose=="Sale":
                query= cursor.execute("SELECT MAX(property_no) FROM Property_dealing.dbo.Buy_house")
                last_no =query.fetchone()
                last=int(last_no[0])
                prop_no=last+1 
                cursor.execute('''INSERT INTO Property_dealing.dbo.Buy_house (property_no, city, bhk, bathroom, parking, area, locality, furnishing, price, status, type, user_id) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',prop_no, city, bhk, bathroom, parking, area, locality, furnishing, price, status, prop_type, user_id)
                conn.commit()
            else:
                query= cursor.execute("SELECT MAX(property_no) FROM Property_dealing.dbo.Rent_house")
                last_no =query.fetchone()
                last=int(last_no[0])
                prop_no=last+1 
                cursor.execute('''INSERT INTO Property_dealing.dbo.Rent_house (property_no, city, bhk, bathroom, parking, area, locality, furnishing, price, status, type, user_id) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',prop_no, city, bhk, bathroom, parking, area, locality, furnishing, price, status, prop_type, user_id)
                conn.commit()    
        return render_template('post.html', message=message)
    return redirect(url_for('login'))

@app.route("/profile",methods=["POST","GET"])
def profile():
    if g.loggedin:
        user_id=session['userid']
        message=None
        if request.method == "POST":
            name=request.form["Name"]
            Email=request.form["Email"]
            number=request.form["Number"]
            password=request.form["Password"]
            cursor.execute('''UPDATE Property_dealing.dbo.Users SET  name= ?, Email_id= ?, Phone_no= ?, password=? WHERE user_id= ?''', name, Email, number, password,user_id)
            conn.commit()
            message="Changes saved Successfully!"
        query= cursor.execute('''SELECT * FROM Property_dealing.dbo.Users WHERE  user_id= ? ''',user_id)
        sql_query=query.fetchone() 
        return render_template('profile.html',data=sql_query,message=message)
    return redirect(url_for('login'))  
       
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

@app.route("/logout")
def logout():
    session.pop('loggedin',None)
    session.pop('userid',None)
    return render_template("buy.html")

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

@app.route("/propview/<pro_for>/<user_id>", methods=['GET', 'POST'])
# @app.route("/propview/")
def propview(user_id=None,pro_for=None):
    if g.loggedin:
        if pro_for=='Sale':
            query= cursor.execute('''SELECT * FROM Property_dealing.dbo.Buy_house,Property_dealing.dbo.Users WHERE Property_dealing.dbo.Users.user_id=Property_dealing.dbo.Buy_house.user_id AND Property_dealing.dbo.Users.user_id= ? ''',user_id)
        else:
            query= cursor.execute('''SELECT * FROM Property_dealing.dbo.Rent_house,Property_dealing.dbo.Users WHERE Property_dealing.dbo.Users.user_id=Property_dealing.dbo.Rent_house.user_id AND Property_dealing.dbo.Users.user_id= ? ''',user_id)
        
        sql_query=query.fetchone() 
        return render_template('propview.html',data=sql_query,pro_for=pro_for)
    return redirect(url_for('login'))    

@app.before_request
def before_request():
    g.loggedin=None
    if 'loggedin' in session:
        g.loggedin = session['loggedin']


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
