from flask import Flask
import numpy as np 
import pandas as pd
# from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer # used for handling missing data
from sklearn.model_selection import train_test_split # used for splitting training and testing data
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error
from math import sqrt
from sklearn import neighbors
# from sklearn.metrics import accuracy_score
# import matplotlib.pyplot as plt

app=Flask(__name__)
@app.route("/")
def index():
    
    # df = pd.read_csv(r"C:\Users\SHIVANI SINGH\Documents\bangluru_data_set1.csv")
    df=pd.read_csv(r"C:\Users\SHIVANI SINGH\Documents\delhi_dataset1.csv")
    # print(len(df))
 
    correlation_matrix = df.corr()
    # print(correlation_matrix)
   
    M=drop_fun(df)

    X = M.iloc[:,0:2].values # attributes to determine dependent variable 
    y = M.iloc[:,2].values  #indepemdent variable
    

    imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
    imputer = imputer.fit(X)
    X = imputer.transform(X)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=0)
 
    # knn_model = KNeighborsRegressor(n_neighbors=3)
    # knn_model.fit(X_train, y_train)
    # test_preds = knn_model.predict(X_test)
    # print(knn_model.score(knn_model.score(X_test=X_test, y_test=y_test)))

    # mse = mean_squared_error(y_train, test_preds)
    # rmse = sqrt(mse)
    # print(rmse)
    
    rmse_val = [] #to store rmse values for different k
    for k in range(20):

        k=k+1
        model=neighbors.KNeighborsRegressor(n_neighbors=k)
        model.fit(X_train, y_train)  #fit the model
        pred=model.predict(X_test) #make prediction on test set
        print(model.score(X_test, y_test))
        error = sqrt(mean_squared_error(y_test,pred)) #calculate rmse
        rmse_val.append(error) #store rmse values
        print('RMSE value for k= ' , k , 'is:', error)
        
        
    # print(X)

    # Z = np.array([3,1000])

    # distances = np.linalg.norm(X - Z, axis='1')

    # k = 5
    # nearest_neighbor_ids = distances.argsort()[:k]
    # print(nearest_neighbor_ids)

    # nearest_neighbor_price = y[nearest_neighbor_ids]
    # print(nearest_neighbor_price)

    # sum=0
    # for element in nearest_neighbor_price:
    #     sum=sum+element
    # avg=sum/5
    # print(avg)
    # print(sum)
    
    return M.to_html() 

def drop_fun(L):
    M= L.drop("property_no",axis='columns')
    M= M.drop("city",axis='columns')
    M= M.drop("locality",axis='columns')
    M= M.drop("furnishing",axis='columns')
    M= M.drop("status",axis='columns')
    M= M.drop("type",axis='columns')
    M=M.drop("bhk",axis='columns')
    M=M.drop("parking",axis='columns')

    return M

# def neighbour():
#     for K in range(20):
#     K = K+1
#     model = neighbors.KNeighborsRegressor(n_neighbors = K)

#     model.fit(x_train, y_train)  #fit the model
#     pred=model.predict(x_test) #make prediction on test set
#     error = sqrt(mean_squared_error(y_test,pred)) #calculate rmse
#     rmse_val.append(error) #store rmse values
#     print('RMSE value for k= ' , K , 'is:', error)