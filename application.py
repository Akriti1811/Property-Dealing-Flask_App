from flask import Flask
import numpy as np 
import pandas as pd

from sklearn.impute import SimpleImputer # used for handling missing data
from sklearn.model_selection import train_test_split # used for splitting training and testing data
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error
from math import sqrt
from sklearn import neighbors

import pyodbc
import json
app = Flask(__name__)

conn = pyodbc.connect(  'Driver={SQL Server Native Client 11.0};'
             'Server=LAPTOP-EVDFGGHS\SQLEXPRESS;'
             'Database=Property_dealing;'
             'Trusted_Connection=yes;')

cursor = conn.cursor()

app=Flask(__name__)
@app.route("/")
def index():

    open_file=open('buy_input.json',"r")
    data_file=open_file.read()
    data=json.loads(data_file)
    
    if(data['variable']==0):
        df=pd.read_sql_query("SELECT * FROM dbo.Buy_house",conn)
    else:
        df=pd.read_sql_query("SELECT * FROM dbo.Rent_house",conn)
    
    # df=pd.read_sql_query("SELECT * FROM dbo.Buy_house",conn)
    # df=pd.read_sql_query("SELECT * FROM dbo.Rent_house",conn)
    # df=pd.read_csv(r"C:\Users\SHIVANI SINGH\Documents\Buy_house.csv")
    # df=pd.read_csv(r"C:\Users\SHIVANI SINGH\Documents\Rent_house.csv")
    
    correlation_matrix = df.corr()  
    # print(correlation_matrix)
    
    H=drop_fun(df)
    M=pd.get_dummies(H) # For categorical data
    y = M.iloc[:,3].values  #indepemdent variable
    M=M.drop("price",axis='columns')

    # attributes to determine dependent variable 
    if(data['variable']==0):
        X= M.iloc[:,0:8].values # for buy data 
    else:
        X = M.iloc[:,0:9].values # for rent data


    imputer = SimpleImputer(missing_values=np.nan, strategy='mean') #Handle missing data
    imputer = imputer.fit(X)
    X = imputer.transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
            
    g=best_value_of_k(X_train,y_train,X_test,y_test) #Best value of k to find number is neighbour
        
    mean_price=neighbouring_prices(g,X,y)  #Function predicts price 
    # data['predicted_price']=mean_price
    # g=open('buy_input.json',"w")
    # json.dump(data, g)
    # g.close()
    # print("o")
    # print(data['predicted_price'])

    # return H.to_html()
    return mean_price 
    


def drop_fun(L):
    M= L.drop("property_no",axis='columns')
    M= M.drop("city",axis='columns')
    M= M.drop("locality",axis='columns')

    M= M.drop("status",axis='columns')
    
    M=M.drop("parking",axis='columns')
    M=M.drop("user_id",axis='columns')
    # M= M.drop("furnishing",axis='columns')
    # M= M.drop("type",axis='columns')
    # M=M.drop("bhk",axis='columns')
    return M


def best_value_of_k(X_train,y_train,X_test,y_test):
    rmse_val = [] #to store rmse values for different k
    for k in range(20):

        k=k+1
        model=neighbors.KNeighborsRegressor(n_neighbors=k)
        model.fit(X_train, y_train)  #fit the model
        pred=model.predict(X_test) #make prediction on test set
        # print(model.score(X_test, y_test))
        error = sqrt(mean_squared_error(y_test,pred)) #calculate rmse
        rmse_val.append(error) #store rmse values
        # print('RMSE value for k= ' , k , 'is:', error)
        p=min(rmse_val)
        # print(p)
    for m in range(20):
        if(rmse_val[m]==p):
            # print(m)
            t=m
    
    return t


def neighbouring_prices(g,X,y):

    Z=input_data()
    # Z = np.array([3,3,900,1,0,0,0,1])  # for buy data
    # Z = np.array([3,2,1000,0,1,0,0,0,1])  # for rent data
    distances = np.linalg.norm(X - Z, axis='1')

    nearest_neighbor_ids = distances.argsort()[:g]
    # print(nearest_neighbor_ids)
    # print(type(nearest_neighbor_ids))
    nearest_neighbor_price = y[nearest_neighbor_ids]
    # print("neighbouring prices : ")
    means=np.mean(nearest_neighbor_price)
    # print(nearest_neighbor_price)
    return means

def input_data():
    open_file=open('buy_input.json',"r")
    data_file=open_file.read()
    data=json.loads(data_file)
    
    bathroom=0
    area=(int(data['bhk'])*270)
    if(data['bhk']==1):
        bathroom=1
    elif(data['bhk']==2):
            bathroom=2
    elif (data['bhk']>='3'):
            bathroom=3
    

    if(data['variable']==0):
        # print("buy")
        Z=np.array([3,2,9,1,0,1,0,1])
        
        if(data['furnishing']=='Full_furnished'):
            Z[3]=1
            Z[4]=0
            Z[5]=0
    
        elif(data['furnishing']=='Semi_furnished'):
            Z[3]=0
            Z[4]=1
            Z[5]=0
        
        elif(data['furnishing']=='Unfurnished'):

            Z[3]=0
            Z[4]=0
            Z[5]=1
         

        if(data['propert_y']=='Builder_Floor'):
            Z[6]=0
            Z[7]=1
            
        elif (data['propert_y']=='Apartment'):
            Z[6]=1
            Z[7]=0
        
    else:
        # print("rent")
        Z=np.array([3,2,9,1,0,1,0,1,0])

        if(data['furnishing']=='Full_furnished'):
            Z[3]=1
            Z[4]=0
            Z[5]=0
       
            
        elif(data['furnishing']=='Semi_furnished'):
            Z[3]=0
            Z[4]=1
            Z[5]=0

        
        elif(data['furnishing']=='Unfurnished'):
            Z[3]=0
            Z[4]=0
            Z[5]=1

        if(data['propert_y']=='Apartment'):
            Z[6]=1
            Z[7]=0
            Z[8]=0
        elif (data['propert_y']=='Builder_Floor'):
            Z[6]=0
            Z[7]=1
            Z[8]=0
        
        elif(data['propert_y']=='Lodging_Property'):
            Z[6]=0
            Z[7]=0
            Z[8]=1
    
    Z[0]=int(data['bhk'])
    Z[1]=bathroom
    Z[2]=area
    # print(Z)
    return Z
    
