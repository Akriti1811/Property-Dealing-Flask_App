from flask import Flask
import numpy as np 
import pandas as pd

from sklearn.impute import SimpleImputer # used for handling missing data
from sklearn.model_selection import train_test_split # used for splitting training and testing data
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error
from math import sqrt
from sklearn import neighbors


app=Flask(__name__)
@app.route("/")
def index():
    
    
    df=pd.read_csv(r"C:\Users\SHIVANI SINGH\Documents\Buy_house.csv")
    # df=pd.read_csv(r"C:\Users\SHIVANI SINGH\Documents\Rent_house.csv")
    
    correlation_matrix = df.corr()  
    # print(correlation_matrix)
    
    H=drop_fun(df)
    M=pd.get_dummies(H) # For categorical data
    
    y = M.iloc[:,3].values  #indepemdent variable
    M=M.drop("price",axis='columns')
    X = M.iloc[:,0:8].values # attributes to determine dependent variable 

    imputer = SimpleImputer(missing_values=np.nan, strategy='mean') #Handle missing data
    imputer = imputer.fit(X)
    X = imputer.transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
            
    g=best_value_of_k(X_train,y_train,X_test,y_test) #Best value of k to find number is neighbour
        
    neighbouring_prices(g,X,y)  #Function predicts price 
   
    return M.to_html() 


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
            print(m)
            t=m
    
    return t


def neighbouring_prices(g,X,y):
    Z = np.array([3,2,800,0,1,0,0,1])

    distances = np.linalg.norm(X - Z, axis='1')

    nearest_neighbor_ids = distances.argsort()[:g]
    # print(nearest_neighbor_ids)

    nearest_neighbor_price = y[nearest_neighbor_ids]
    print("neighbouring prices : ")
    print(nearest_neighbor_price)