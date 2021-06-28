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

conn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                         "Server=DESKTOP-PLT6RQC\SQLEXPRESS;"
                        # "Server=LAPTOP-EVDFGGHS\SQLEXPRESS;"
                        #  "Server=DESKTOP-TS4AFA1;"
                         "Database=Property_dealing;"
                         "Trusted_Connection=yes;")

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
    # print(df)
    area=df['area'].mean()
    
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
    
    # CONVERTING numpyarray INTO dataframe
    if(data['variable']==0):
        X=pd.DataFrame(X,columns=['bhk','bathroom','area','furnishing_Furnished','furnishing_Semi_furnished','furnishing_Unfurnished','type_Apartment','type_Builder_Floor'])
    else:
        X=pd.DataFrame(X,columns=['bhk','bathroom','area','furnishing_Furnished','furnishing_Semi_furnished','furnishing_Unfurnished','type_Apartment','type_Builder_Floor','type_Lodging_property'])

    y=pd.DataFrame(y,columns=['price'])

    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.32, random_state=0)
            
    g=best_value_of_k(X_train,y_train,X_test,y_test) #Best value of k to find number is neighbour
        
    
    ids=neighbouring_prices(g,X,y,area)    # GIVES NEAREST NEIGHBOUR ID'S
    
    nearest_negh_df=pd.DataFrame()  # EMPTY DATAFRAME

    for i in range(g):                  # STORE NEAREST NEIGHBOUR IN A DATAFRAME
        pf=df.iloc[ids[i]]
        temp=nearest_negh_df.append(pf,ignore_index=True)
        nearest_negh_df=temp
   
    means=nearest_negh_df['price'].mean()
    mn=nearest_negh_df['property_no']
   
    # return X.to_html()
    # return nearest_negh_df.to_html()
    return means,mn
    
    


def drop_fun(L):
    M= L.drop("property_no",axis='columns')
    M= M.drop("city",axis='columns')
    M= M.drop("locality",axis='columns')

    M= M.drop("status",axis='columns')
    
    M=M.drop("parking",axis='columns')
    M=M.drop("user_id",axis='columns')
    
    return M


def best_value_of_k(X_train,y_train,X_test,y_test):
    rmse_val = [] #to store rmse values for different k
    for k in range(20):
        k=k+1
        model=neighbors.KNeighborsRegressor(n_neighbors=k)
        model.fit(X_train, y_train)  #fit the model
        pred=model.predict(X_test) #make prediction on test set
        error = sqrt(mean_squared_error(y_test,pred)) #calculate rmse
        rmse_val.append(error) #store rmse values
        # print('RMSE value for k= ' , k , 'is:', error)

    p=min(rmse_val)
    # print(p)
    # print(model.score(X_test,y_test))
    for m in range(20):
        if(rmse_val[m]==p):
            print(m)
            t=m
    
    return t


def neighbouring_prices(g,X,y,area):

    Z=input_data(area)
    distances = np.linalg.norm(X - Z, axis='1')

    nearest_neighbour_ids = distances.argsort()[:g]
    # print( nearest_neighbour_ids)
    return nearest_neighbour_ids
    
    # nearest_neighbour_price = y[nearest_neighbour_ids]  
    # means=np.mean(nearest_neighbour_price)
    # return nearest_neighbour_ids
    # return means,nearest_neighbour_ids

def input_data(Area):
    open_file=open('buy_input.json')
    data_file=open_file.read()
    data=json.loads(data_file)
    
    bathroom=0
    area=(int(data['bhk'])*270)
    # area=Area/2
    if(data['bhk']==1):
        bathroom=1
    elif(data['bhk']==2):
            bathroom=2
    elif (data['bhk']>='3'):
            bathroom=3
    

    if(data['variable']==0):
        
        Z=np.array([3,2,9,1,0,1,0,1])
        
        if(data['furnishing']=='Furnished'):
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
    
        Z=np.array([3,2,9,1,0,1,0,1,0])

        if(data['furnishing']=='Furnished'):
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

    return Z
    
