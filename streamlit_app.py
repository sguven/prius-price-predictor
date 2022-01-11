#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 13:48:40 2022

@author: serhat
"""

class prius_model_predict:    

    def price_predict(example_df):
        import pandas as pd
        from sklearn.compose import ColumnTransformer
        from sklearn.pipeline import Pipeline
        from sklearn.impute import SimpleImputer
        from sklearn.preprocessing import StandardScaler, OneHotEncoder
        from sklearn.linear_model import LinearRegression
        from sklearn.model_selection import train_test_split
        df = pd.read_csv('data.csv')
        df.rename(columns={"Unnamed: 0": "#"},inplace=True)
        df.set_index('#',inplace=True)
        X = df.iloc[:, [True, False, True, True, True, True, True, True,]]
        y = df.iloc[:,1:2]
        numeric_features = ["Years", "Mileage","Owner#"]
        numeric_transformer = Pipeline(steps=[("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())])
        categorical_features = ["Model", "Condition", "Usage Type" ,"Location"]
        categorical_transformer = OneHotEncoder(handle_unknown="ignore")    
        preprocessor = ColumnTransformer(transformers=[("num", numeric_transformer, numeric_features),("cat", categorical_transformer, categorical_features),])    
        clf = Pipeline(steps=[("preprocessor", preprocessor), ("classifier", LinearRegression())])    
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)    
        clf.fit(X_train, y_train)
        return clf.predict(example_df)
        

import streamlit as st
import pandas as pd



model =('Prius', 'Prius Two FWD', 'Prius Three', 'Prius Two', 
       'Prius Four FWD', 'Prius XLE FWD', 'Prius LE FWD',
       'Prius Persona Series', 'Prius Limited FWD', 'Prius Four',
       'Prius XLE AWD-e', 'Prius One FWD', 'Prius One', 'Prius Five',
       'Prius Touring FWD', 'Prius Four Touring FWD',
       'Prius 2020 Edition FWD', 'Prius L Eco FWD', 'Prius Three FWD',
       'Prius FWD', 'Prius Three Touring FWD', 'Prius LE AWD-e',
       'Prius Two Eco FWD', 'Prius Liftback FWD',
       'Prius Persona Series SE')

location = ('CA', 'HI', 'FL', 'ND', 'MN', 'KY', 'OR', 'PA', 'CO', 'UT', 'TN',
       'TX', 'OH', 'VA', 'NM', 'WA', 'NV', 'IA', 'IL', 'NC', 'GA', 'MA',
       'LA', 'AZ', 'IN', 'MS', 'MT', 'NY', 'CT', 'OK', 'NJ', 'NE',
       'AL', 'SC', 'MD', 'MI', 'KS', 'MO', 'WI', 'ID', 'VT', 'NH', 'RI',
       'WV', 'AR', 'WY', 'ME', 'SD')

condition = ('Accident check\nNo issues reported',
       'Accident check\n1Accident reported',
       'Accident check\nFrame damage reported',
       'Accident check\n3Accidents reported',
       'Accident check\n2Accidents reported',
       'Accident check\n4Accidents reported')

usage_type = ('Personal', 'Commercial')

st.text('Welcome')
st.text('Please enter the features of the vehicle you want to calculate the price of.')

model = st.selectbox('Model', model)
year = st.slider('Year', 2002, 2022)
mileage = st.slider('Mileage', 0, 275000)
owners = st.slider('Number of Prev. Owners', 0 , 10)
location = st.selectbox('Location', location)
usage_type = st.selectbox('usage_type', usage_type)
condition = st.selectbox(('Condition'), condition)
calculate = st.button('Calculate the Price')

d = {'Years': [int(year)], 'Model': [model], 'Mileage':[int(mileage)],
     'Condition': [condition],'Usage Type': [usage_type], 
     'Owner#': [int(owners)], 'Location': [location]}

df_input = pd.DataFrame(data=d)

calculate = True

if calculate:
    result = str(round(prius_model_predict.price_predict(df_input)[0][0],2)) + ' USD'
else:
    result = 'No Price'
    

st.text(result)


    


