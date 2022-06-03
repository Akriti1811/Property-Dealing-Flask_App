# Property Dealing Web App

Objective

•	To provide a GUI for end-user who is looking for buying/ selling/ renting any housing asset.

•	Assist user in selecting the most suitable property based on his/her custom requirements through ML model.

Additional Features

•	To predict the price of the property so that the user can verify that the price asked by the owner is appreciable or not.

•	Suggesting the best property matches if there is no such property which has the exact same features as asked by the user.


OVERVIEW OF PROJECT

![image](https://user-images.githubusercontent.com/55645517/171822661-8a80513c-ffcd-4c72-ac7b-a7c5c2338246.png)

EXECUTION OF QUERY

![image](https://user-images.githubusercontent.com/55645517/171822600-b4e639ff-e8a2-4b9b-adb9-902c9a11598e.png)

ML MODEL

KNN ALGORITHM (K Nearest Neighbour)

In backend we are using KNN algorithm to predict the price of properties

IMPLEMENTATION AND OUTPUT

The home page of our web application “HOME SWEET HOME” consist of a navbar having 4 items named as Home, Post Property, Login and Sign Up. We also have a form to enter the details of the property the user wants to search.

![image](https://user-images.githubusercontent.com/55645517/171827253-5293f4be-f791-40a4-a47b-76eeda8b73d7.png)
![image](https://user-images.githubusercontent.com/55645517/171827301-42f17be3-550c-4812-a5d6-40af289e3979.png)
![image](https://user-images.githubusercontent.com/55645517/171828537-b0990c1e-e620-4daf-9b78-fb4861396c56.png)


Our home page consists of 2 sections, one for buy and another for rent. 

![image](https://user-images.githubusercontent.com/55645517/171827418-631ed16a-dc08-458b-a945-12edb342fe0a.png)

This is our Sign-Up page where new user can enter the details to register.

![image](https://user-images.githubusercontent.com/55645517/171827676-9fc90c89-88e7-4d5c-8223-55d2cad627d0.png)

This is our Login page where user enter the details to login.

![image](https://user-images.githubusercontent.com/55645517/171827950-94ec6ff7-0b31-4835-88fa-bf78d7507f9d.png)

User can change their details from ‘My Profile’.

![image](https://user-images.githubusercontent.com/55645517/171828009-127e4348-c7c5-4582-b687-320251728fcc.png)

User can see the Properties they posted for sale or rent. They can also delete the property posted by them.

![image](https://user-images.githubusercontent.com/55645517/171828202-39641791-9bd4-46a9-b458-d9726b830b52.png)

If the user has not posted any property.

![image](https://user-images.githubusercontent.com/55645517/171828786-bbed1c50-5db8-49b4-a62f-a3bee1029195.png)

User can also change the details of the property they posted.

![image](https://user-images.githubusercontent.com/55645517/171828117-c7440084-ef44-4287-917d-b3f9f243c2b8.png)

If the user wants to post new property.

![image](https://user-images.githubusercontent.com/55645517/171828878-8290cc92-d863-45ec-a5a1-f12832fce70c.png)

Now if user wants to search a property, then they have to fill the form according to their requirements.

Example 1. When the exact requirements of the user are fulfilled

![image](https://user-images.githubusercontent.com/55645517/171829078-6beed083-77c4-4889-8661-894cc4e25bd7.png)

Output of the previous search:

•	Predicted price of the property according to user requirements.

•	Best matched properties from the database.

![image](https://user-images.githubusercontent.com/55645517/171829162-9dfd9eb4-7292-43a6-baee-18c34c1d7fb1.png)

Property details after user choose ‘contact owner’ option.

![image](https://user-images.githubusercontent.com/55645517/171829262-105dd2a7-e80a-4496-83b8-983ffec0ec73.png)
![image](https://user-images.githubusercontent.com/55645517/171829302-7bae15d6-d746-414b-a91b-b0f430657bbc.png)

Example 2. When the exact requirements of the user are not fulfilled.

Output:

•	Predicted price of the property according to user requirements.

•	K nearest properties returned from the ML Model.

![image](https://user-images.githubusercontent.com/55645517/171829517-b7897a71-c3ac-4696-aa8c-f80fc445285f.png)

So, this was our web app, which is made with a purpose of making your home search easier, efficient and convenient. Hope the user find his dream house using this application.






