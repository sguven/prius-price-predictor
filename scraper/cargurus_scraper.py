#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 28 20:01:12 2021

"""

#IMPORTING LIBRARIES

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
import numpy as np
import pandas as pd
import streamlit as st
#DEFINING FUNCTION to ELIMINATE POPUPS
'''
def Clearpopups(): 
    try:
        driver.find_element_by_xpath('/html/body/div[10]/div/button/svg').click()
    except:
        try:
            driver.find_element_by_xpath('/html/body/div[10]/div/div[2]/button[1]').click()
        except:
            pass
'''

#OPENING WEBDRIVER IN SERVICE MODE

#s=Service('/usr/local/bin/chromedriver')
#driver = webdriver.Chrome(service=s)
#driver.get('https://cargurus.com')
#WebDriverWait(driver, 2)



#ENTERING THE INFORMATIONS SUCH AS MAKE, MODEL, ZIPCODE


#DEFINING EMPTY LIST OBJECTS TO COLLECT AND APPEND DATA



'''
THIS LOOP IS DESIGNED TO COLLECT ALL INFORMATION IN 650 PAGES
IT FIRST GETS THE LIST PAGE AND COLLECT ALL LINKS, THEN GET ALL LINKS AND COLLECT DATA
AFTER COMPLETING COLLECTION, IT CLICKS THE NEXT BUTTON AND DO THE SAME FOR THE NEXT PAGE
'''
def collect_pages():   
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
    driver.get('https://cargurus.com')
    WebDriverWait(driver, 2)
    Clearpopups()
    Select(driver.find_element(By.XPATH, '//*[@id="carPickerUsed_makerSelect"]')).select_by_index(34)
    Select(driver.find_element_by_xpath('//*[@id="carPickerUsed_modelSelect"]')).select_by_index(21)
    driver.find_element_by_xpath('//*[@id="dealFinderZipUsedId_dealFinderForm"]').send_keys('08873')
    driver.find_element_by_xpath('//*[@id="dealFinderForm_0"]').click()
    WebDriverWait(driver, 2)
    headers = []
    vehicle_detail1 = []
    vehicle_detail2 = []
    vehicle_history = []
    table2_right = []
    table2_left = []
    Select(driver.find_element_by_xpath('//*[@id="distance"]')).select_by_index(8)
    driver.find_element_by_xpath('//*[@id="react-tabs-5"]/form/button').click()
    Clearpopups()
    i = 0
    while i < 650:
        Clearpopups()
        driver.implicitly_wait(3)
        links = [i.get_attribute('href') for i in driver.find_elements(By.XPATH,"//a[contains(@class, '_ajVSv wcSLm2')]")]
        for link in links:
            try:
                driver.get(link)    
                headers.append(driver.find_element_by_xpath('//*[@id="cargurus-listing-search"]/div[1]/div[3]/div[1]/h1').text)        
                vehicle_detail1.append([i.text for i in driver.find_elements_by_class_name('R_TThv')])
                table2_right.append([i.text for i in driver.find_elements(By.CLASS_NAME, 'tSbcGe')])
                table2_left.append([i.text for i in driver.find_elements(By.CLASS_NAME, 'wv1MO3')])
                vehicle_history.append([i.text for i in driver.find_elements(By.CLASS_NAME, 'pqHdTW')])
            except:
                print('smt wrong')
        Clearpopups()
        driver.find_element_by_xpath('//*[@id="cargurus-listing-search"]/div/div[1]/button').click()
        Clearpopups()
        driver.find_element_by_css_selector("button[data-cg-ft='page-navigation-next-page']").click()
        i = i + 1
#COMBINING DATA AND CREATING DATA FRAME
    i=0
    while i < len(table2_right):
        if len(table2_right[i])==len(table2_left[i]):
            vehicle_detail2.append(pd.DataFrame(table2_right[i],table2_left[i]))
            i = i + 1
        else:
            del table2_right[i][-1]

    df_main = pd.DataFrame()        
#'Vin','Make','Model','Year','Milage','ZipCode','Owner#','Condition','UsageType'
#maybe you need to put a if statement to check the lenght of lists
    df_main['Vin'] = [i.loc['VIN:'].to_string(index = False) for i in vehicle_detail2]
    df_main['Years'] = [int(i.split(' ')[0]) for i in headers]
    df_main['Price'] = [int(i.split(' ')[-1].replace('$','').replace(',','')) for i in headers]
    df_main['Make'] = [i.split(' ')[1] for i in headers]
    df_main['Model'] = [' '.join(i.split(' ')[2:-2]) for i in headers]
    df_main['Mileage'] = [int(i.loc['Mileage:'].to_string(index = False).replace(' miles','').replace(',','')) for i in vehicle_detail2]

    df_vehicle_history = pd.DataFrame(vehicle_history)

    df_main['Owner#'] = df_vehicle_history[2]
    df_main['Condition'] = df_vehicle_history[1]
    df_main['Usage Type'] = df_vehicle_history[3]

#because there were frames not having location info we created a loop to fill non-data frames
#df_main['Location12'] = [i.loc['Location:'].to_string() for i in vehicle_detail2]

    location_to_append=[]
    for i in vehicle_detail2:
        try:    
            location_to_append.append(i.loc['Location:'].to_string(index = False))
        except:
            location_to_append.append(str(''))

    #to try to get state info
    location_to_import =[]
    for i in location_to_append:
        try:
            location_to_import.append(i.split(',')[1][:3][1:])
        except:  
            location_to_import.append(str(''))


    df_main['Location'] = location_to_import

    df_main['Owner#'] = df_main['Owner#'].replace({'One owner' : 1,'2 Owners':2 ,
                                                   '4 Owners':4, '3 Owners':3,
                                                   '5 Owners':5,'6 Owners':6,
                                                   '8 Owners':8})

    return df_main


df = collect_pages()

@st.cache
def convert_df(df):
   return df.to_csv().encode('utf-8')


csv = convert_df(df)

st.download_button(
   "Press to Download",
   csv,
   "file.csv",
   "text/csv",
   key='download-csv'
)
