 # -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 13:33:44 2020

@author: Administrator
"""

from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin

import json
import pickle
import requests
import pandas as pd
import numpy as np

import flasgger
from flasgger import Swagger


app = Flask(__name__)
cors = CORS(app)

randomForest = pickle.load(open('flight_rf.pkl', 'rb'))
df= pd.read_excel('Data_Train.xlsx')

@app.route('/getAllDetails')
@cross_origin()
def getAllDetails():
    
    """Lets Authenticate the Bank Note
    ---
    parameters:
        - name: variance
          in: query
          type: number
          required: true
        - name: skewness
          in: query
          type: number
          required: true
        - name: curtosis
          in: query
          type: number
          required: true
        - name: entropy
          in: query
          type: number
          required: true
    responses:
        200:
            description: The output values
    """
    Airlines=  list(df['Airline'].dropna().unique())
    SourceCity= list(df['Source'].dropna().unique())
    DestinationCity= list(df['Source'].dropna().unique())
    Stops= list(df['Total_Stops'].dropna().unique())
    airlineData = [{'id':i,'airline':Airlines[i]} for i in range(len(Airlines))]
    sourceCityData = [{'id':i,'source':SourceCity[i]} for i in range(len(SourceCity))]
    destinationCityData = [{'id':i,'destination':DestinationCity[i]} for i in range(len(DestinationCity))]
    stopsData = [{'id':i,'stop':Stops[i]} for i in range(len(Stops))]
    return {'Airline':airlineData,'SourceCity':sourceCityData,'DestinationCity':destinationCityData,'Stops':stopsData}
   
@app.route("/predictPrice",methods=["GET","POST"])
@cross_origin(supports_credentials=True)
def predict_Price():
    data = json.loads(request.data)
    airline= data['Airline']
    source = data['SourceCity']
    destination = data['DestinationCity']
    stops= int(data['Stops'])
    departureDateTime = pd.to_datetime(data['DepartureDate'], format="%Y-%m-%dT%H:%M")
    departureDay = int(departureDateTime.day)
    departureMonth = int(departureDateTime.month)
    departureHour = int(departureDateTime.hour)
    departureMinute =int(departureDateTime.minute)
    arrivalDateTime = pd.to_datetime(data['ArrivalDate'], format="%Y-%m-%dT%H:%M")
    arrivalDay = int(arrivalDateTime.day)
    arrivalMonth = int(arrivalDateTime.month)
    arrivalHour = int(arrivalDateTime.hour)
    arrivalMinute =int(arrivalDateTime.minute)
    durationDateTime = departureDateTime - arrivalDateTime
    durationHour = durationDateTime.hour
    durationMinute = durationDateTime.minute
    Jet_Airways = 0
    IndiGo = 0
    Air_India = 0
    Multiple_carriers = 0
    SpiceJet = 0
    Vistara = 0
    GoAir = 0
    Multiple_carriers_Premium_economy = 0
    Jet_Airways_Business = 0
    Vistara_Premium_economy = 0
    Trujet = 0 
    if(airline=='Jet Airways'):
            Jet_Airways = 1
            

    elif (airline=='IndiGo'):
            
            IndiGo = 1
           
    elif (airline=='Air India'):
           
            Air_India = 1
           
    elif (airline=='Multiple carriers'):
           
            Multiple_carriers = 1
            
    elif (airline=='SpiceJet'):
           
            SpiceJet = 1
           
    elif (airline=='Vistara'):
            Vistara = 1
    elif (airline=='GoAir'):
           
            GoAir = 1
            
    elif (airline=='Multiple carriers Premium economy'):
           
            Multiple_carriers_Premium_economy = 1
         
    elif (airline=='Jet Airways Business'):
           
            Jet_Airways_Business = 1
          
    elif (airline=='Vistara Premium economy'):
           
            Vistara_Premium_economy = 1
           
            
    elif (airline=='Trujet'):
           
            Trujet = 1
    s_Delhi = 0
    s_Kolkata = 0
    s_Mumbai = 0
    s_Chennai = 0                
    if (source == 'Delhi'):
            s_Delhi = 1
            

    elif (source == 'Kolkata'):
           
            s_Kolkata = 1

    elif (source == 'Mumbai'):
            s_Mumbai = 1
            

    elif (source == 'Chennai'):
            
            s_Chennai = 1
    d_Cochin = 0
    d_Delhi = 0
    d_New_Delhi = 0
    d_Hyderabad = 0
    d_Kolkata = 0
    if (destination == 'Cochin'):
            d_Cochin = 1
        
    elif (destination == 'Delhi'):
            d_Delhi = 1

    elif (destination == 'New_Delhi'):
          
            d_New_Delhi = 1

    elif (destination == 'Hyderabad'):
           
            d_Hyderabad = 1
            
    elif (destination == 'Kolkata'):
            d_Kolkata = 1

    prediction=randomForest.predict([[
            stops,
            departureDay,
            departureMonth,
            departureHour,
            departureMinute,
            arrivalHour,
            arrivalMinute,
            durationHour,
            durationMinute,
            Air_India,
            GoAir,
            IndiGo,
            Jet_Airways,
            Jet_Airways_Business,
            Multiple_carriers,
            Multiple_carriers_Premium_economy,
            SpiceJet,
            Trujet,
            Vistara,
            Vistara_Premium_economy,
            s_Chennai,
            s_Delhi,
            s_Kolkata,
            s_Mumbai,
            d_Cochin,
            d_Delhi,
            d_Hyderabad,
            d_Kolkata,
            d_New_Delhi
        ]])

    output=round(prediction[0],2)
   
    return output

if __name__ == '__main__':
    app.run()

