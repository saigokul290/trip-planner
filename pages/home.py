import streamlit as st
import mysql.connector
import pandas as pd
from mysql.connector import Error
import random
import datetime as dt
page="""" 
<style>
[data-testid="stAppViewContainer"]{
background-image: url("https://wallpaperaccess.com/full/8405347.jpg");
 background-size: cover;
 }


</style>    
"""
st.markdown(page,unsafe_allow_html=True)
cnx = mysql.connector.connect(user='root', password='1234', host='localhost', database='trip_app')
cursor = cnx.cursor()
option = st.sidebar.selectbox("menu:",["login","sign up"])
import sqlite3


 

def Home():
    name=st.text_input('Enter your name')
    loc=st.text_input('Enter your location')
    maximum=st.text_input('Enter your budget')
    minimum=st.text_input("enter the minimum budget")
    x=st.multiselect("preferences:",['games','malls','resturents','hangouts'])
    
    if(st.checkbox("show")):
        
        cnx = mysql.connector.connect(user='root', password='1234', host='localhost', database='trip_app')
        cursor = cnx.cursor()
        part1 = []
        header = ''
        part2 = []
        summ = ''
        part3 = []
        tables = ''
        part4 = []
        cond = ''
        part5 = []
        coloumn_names=[]
        cond2 = ''
        final_string = ''
        loca=''
        if 'resturents' in x:
            part1.append("HOTELS.NAME,HOTELS.LOCATION,HOTELS.AVG_PRICE")
            part2.append("HOTELS.AVG_PRICE")
            part5.append("HOTELS.LOCATION")
            part3.append("HOTELS")
            part4.append("HOTELS.AVG_PRICE")
        
            coloumn_names.append("resturents name")
            coloumn_names.append("bus stop")
            coloumn_names.append("price")
        if 'games' in x:
            part1.append("GAMES.NAME,GAMES.PLACE,GAMES.PRICE")
            part2.append("GAMES.PRICE ")
            part3.append("GAMES")
            part5.append("GAMES.PLACE")
            part4.append("GAMES.PRICE")
            coloumn_names.append("game name")
            coloumn_names.append("game bus stop")
            coloumn_names.append("game price")
        if 'malls' in x:
            part1.append("MALLS.NAME,MALLS.PLACE,MALLS.AVG_PRICE")
            part2.append("MALLS.AVG_PRICE ")
            part3.append("MALLS")
            part5.append("MALLS.PLACE")
            
            part4.append("MALLS.AVG_PRICE")
            coloumn_names.append("malls name")
            coloumn_names.append("malls bus stop")
            coloumn_names.append("malls price")
        if 'hangouts' in x:
            part1.append("HANGOUTS.NAME,HANGOUTS.PLACE,HANGOUTS.PRICE")
            part2.append("HANGOUTS.PRICE ")
            part3.append("HANGOUTS")
            part4.append("HANGOUTS.PRICE")
            part5.append('HANGOUTS.PLACE')
            coloumn_names.append("hangouts name")
            coloumn_names.append("hangouts bus stop")
            coloumn_names.append("hangouts price")
            

        for i in range(len(part1)):
            if i != len(part1)-1:
                header = header + part1[i] + ','
            else:
                header = header + part1[i]
        for i in range(len(part2)):
            if i != len(part2)-1:
                summ = summ + part2[i] + '+'
            else:
                summ = summ + part2[i]
        for i in range(len(part3)):
            if i != len(part3)-1:
                tables = tables + part3[i] + ','
            else:
                tables = tables + part3[i]
        for i in range(len(part4)):
            if i != len(part4)-1:
                cond = cond + part4[i] + '+'
            else:
                cond = cond + part4[i]
        for i in range(len(part5)):
            if(i!=len(part4)):
                loca+=part5[i] + '='
            else:
                loca+=part5[i]
        loca1='='.join(part5)
                

        final_string = f'select {header},({summ}) from {tables} where ({cond}) < {int(maximum)-75} and ({cond})>{minimum} AND {loca1}'
    
     
       
        coloumn_names.append("total_price")
        cursor = cnx.cursor()
        result = None
        try:
            bus=[]
            cursor.execute(final_string)
            result = cursor.fetchall()
            df = pd.DataFrame(result, columns=coloumn_names)
            st.dataframe(df,width=90000)

            selected_index = st.selectbox("Select the row of your choice", df.index)
            if st.button("Submit"):
                selected_tuple = df.loc[selected_index]
                st.dataframe(selected_tuple)
                try:
                    bus.append(selected_tuple[1])
                    bus.append(selected_tuple[4])
                    bus.append(selected_tuple[7])
                    bus.append(selected_tuple[10])
                    bus.append(selected_tuple[13])
                except:
                   
                    for i in range(len(bus)):
                        try:
                            source=bus[i]
                            
                            destination=bus[i+1]
                        
                            bus_q=f"""
                                    SELECT bus_no
                                    FROM (
                                    SELECT bus_no, stops,
                                            ROW_NUMBER() OVER (ORDER BY bus_no) as row_num
                                    FROM bus
                                    WHERE stops LIKE "{source}" AND stops LIKE "{destination}"
                                    ) as matching_buses
                                    WHERE row_num = 1
                                    UNION
                                    SELECT bus_no
                                    FROM bus
                                    WHERE stops IN (
                                    SELECT DISTINCT stops
                                    FROM bus
                                    WHERE stops='{source}' <> stops='{destination}' AND stops LIKE '{source}' AND stops LIKE '{destination}'
                                    )
                                    GROUP BY bus_no;"""
                            cursor.execute(bus_q)
                            res = cursor.fetchall()
    
                        except:
                            continue  
                        
        except Error as err:
                print(f"Error: '{err}'")
                
                
                
                
                
                
                
                
def sign_up():
    
    username = st.sidebar.text_input("Username")
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type='password')
    password2 = st.sidebar.text_input("Confirm Password", type='password')
    if(st.sidebar.button("submit") ):
            # Check if passwords match
        if password != password2:
            st.error("Passwords do not match")
        else:
                # Insert new user into the MySQL database
            insert_query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (username, email, password))
            cnx.commit()
            st.success("Account created!")
           
    # Close the connection

if(option == "login"):
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type='password')

            # Check if user exists in the MySQL database
        select_query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(select_query, (username, password))
        results = cursor.fetchall()
        if st.sidebar.checkbox("Log in"):
            if results:
                st.success("Logged in!")
              
                Home()
            else:
                st.error("Incorrect username or password")
                




if(option=="sign up"):
    sign_up()
