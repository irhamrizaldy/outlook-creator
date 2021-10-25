#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import json
import string
import random
import mysql.connector
import requests
from requests.structures import CaseInsensitiveDict
from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import calendar
from time import sleep
from faker import Faker

class Automate():
    def run(self,i):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
        #driver = webdriver.Chrome(chrome_options=chrome_options)
        driver = webdriver.Chrome('chromedriver.exe')
        driver.get("https://signup.live.com/")
        
        #button = driver.find_element_by_xpath("/html/body/section/div/div/div[2]/a[1]")
        #button.click()
        elem = driver.find_element_by_id("MemberName")
        email = elem.send_keys(Users[i]['username']+"@outlook.com")
        driver.find_element_by_id("iSignupAction").click()
        sleep(6)
        elem = driver.find_element_by_id("PasswordInput")
        pwd = elem.send_keys(Users[i]['password'])
        driver.find_element_by_id("iSignupAction").click()
        sleep(3)
        elem = driver.find_element_by_id("FirstName")
        fname = elem.send_keys(Users[i]['name'])
        elem = driver.find_element_by_id("LastName")
        lname = elem.send_keys(Users[i]['lastname'])
        driver.find_element_by_id("iSignupAction").click()
        sleep(3)
        select = Select(driver.find_element_by_id('Country'))
        country = select.select_by_visible_text(Users[i]['country'])
        select = Select(driver.find_element_by_id('BirthMonth'))
        month = select.select_by_visible_text(Users[i]['month'])
        select = Select(driver.find_element_by_id('BirthDay'))
        day = select.select_by_visible_text(Users[i]['day'])
        # select = Select(driver.find_element_by_id('BirthYear'))
        select = driver.find_element_by_id('BirthYear')
        year = select.send_keys(Users[i]['year'])
        # select.select_by_visible_text(Users[i]['year'])
        driver.find_element_by_id("iSignupAction").click()
        sleep(3)
        btnBack = WebDriverWait(driver, 300).until(ec.visibility_of_element_located((By.ID, "idBtn_Back")))
        btnBack.click()
        sleep(5)

        # insert json/data users to mysql
        file_json = open("Output.json")
        data = json.loads(file_json.read())

        # value of json
        fname = data['0']['name']
        lname = data['0']['lastname'] 
        email = data['0']['email']
        pwd = data['0']['password']
        day = data['0']['day']
        month = data['0']['month']
        year = data['0']['year']
        country = data['0']['country']

        # json post curl
        url = "https://reqbin.com/echo/post/json"
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers["Content-Type"] = "application/json"
        data = '{"login":'+email+',"password":"password112233"}'

        resp = requests.post(url, headers=headers, data=data)
        print("Data:", data)
        print("Status:", resp.status_code)

        # connection mysql
        db_connection = mysql.connector.connect (
            host = "localhost",
            user = "root",
            password = "",
            database = "outlook"
        )
        
        db_cursor = db_connection.cursor()
        outlook_insert_query = "INSERT INTO users (id, firstname, lastname, email, password, month, day, year, country) VALUES('', '"+fname+"', '"+lname+"', '"+email+"', '"+pwd+"', '"+month+"', '"+day+"', '"+year+"', '"+country+"')"

        db_cursor.execute(outlook_insert_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        # elem = driver.find_element_by_name("ConfirmPasswd")
        # elem.send_keys(Users[i]['password'])
        # elem.send_keys(Keys.RETURN)
        #driver.close()
    def __init__(self,Users):
        self.Users = Users
        for j in range(len(self.Users)):
            self.run(j)
            question1 = input("Enter y when you have completed registration>>>")
class randomData():
    numbers = string.digits
    letters = string.ascii_lowercase
    capletters = string.ascii_uppercase
    alphanumeric = letters + numbers + capletters
    symbols = string.punctuation
    months = calendar.month_name[1:13]
    dates =  [i for i in range(1,32) ]
    years =  [i for i in range(1990,2000) ]
    #mix = symbols + alphanumeric
    mix = alphanumeric
    outputfile = "Output.json"
    adjetives = ['Expert', 'Gran Master', 'Master', 'Senior', 'Ninja', 'Masine Learning', 'Data Visualisation']
    emaildomains = ['@outlook.com']
    #emaildomains = ['@hotmail.com', '@gmail.com', '@outlook.com', '@yahoo.com']
    fake = Faker()

    def __init__(self, intAmout, intPasswdLength, blnCreateCSV = 0):
        if blnCreateCSV:
            f = open(self.outputfile, "w")
            global Users
            Users = self.gendata(intAmout, intPasswdLength)
            f.write(json.dumps(Users))
            f.close()
            Automate(Users)
            print("{} generated in {}{}".format(self.outputfile, os.getcwd(), self.outputfile))
        else:
            Users = self.gendata(intAmout, intPasswdLength)
            Automate(Users)
            print(Users)

    def getnames(self, intAmount):
        """
        Select randomly names from the CSV file.

        Args:
            intAmount: Integer with the amount of last names to be selected.

        Returns:
            FinalNames: List with the names selected.
        """

        NamesFile = open(os.path.join(os.getcwd(),"Data","Names.csv"), 'r')
        Names = NamesFile.readlines()
        NamesFile.close()
        FinalNames = []
        for i in range(0, intAmount):
            RandomName = random.choice(Names).rstrip("\n")
            FinalNames.append(RandomName)
        return FinalNames

    def getlastnames(self, intAmount):
        """
        Select randomly Last Names from the CSV file.

        Args:
            intAmount: Integer with the amount of last names to be selected.

        Returns:
            FinalLastNames: List with the last names.
        """

        LastNameFile = open(os.path.join(os.getcwd(), "Data", "LastNames.csv"), 'r')
        LastNames = LastNameFile.readlines()
        LastNameFile.close()
        FinalLastNames = []
        for i in range(0, intAmount):
            RandomLastName = random.choice(LastNames).rstrip("\n")
            FinalLastNames.append(RandomLastName)
        return FinalLastNames

    def getpasswd(self, intPasswordLength):
        """
        Generate random passwords

        Args:
            intPasswordLength: Integer with the number of characters the password will have.

        Returns:
            Password: String with the password generated.
        """

        Password = ''
        for i in range(0, int(intPasswordLength)):
            char = random.choice(self.mix)
            Password += char
        return Password

    def gendata(self, intAmount, intPasswordLength):
        """
        Generate all user data like name, last name and password.

        Args:
            intAmount: Integer with the amount of data to be generated.
            intPasswordLength: Integer with the number of characters the password will have.

        Returns:
            Data: List with the names and last names.
        """

        NamesData = self.getnames(intAmount)
        LastNameData = self.getlastnames(intAmount)
        Data = {}
        for i in range(0, intAmount):
            username = str(NamesData[i][:3] + LastNameData[i][:3] + str(random.randint(100,10000))).lower()
            inner = {"name": "{}".format(NamesData[i]),
                     "lastname": "{}".format(LastNameData[i]),
                     "username": "{}".format(username),
                     "password": "{}".format(self.getpasswd(intPasswordLength)),
                     "email": "{}".format(username + random.choice(self.emaildomains)),
                     "month": "{}".format(random.choice(self.months)),
                     "day": "{}".format(random.choice(self.dates)),
                     "year": "{}".format(random.choice(self.years)),
                     "country": "{}".format(self.fake.country())}
            Data[i] = inner
        return Data


def main():
    #amount = int(input("Amount of users you want to generate?\n>>>"))
    #passwdlength = int(input("Password length for each password?\n>>>"))
    #question1 = input("Do you want to generate a file?\nYes/No\n>>>")
    #yesvalues = ("yes", "YES", "Yes", "Y", "y", "SI", "Si", "si", "S", "s")
    
    amount =1 # total number of accounts to be created
    passwdlength = 12 #password length

    #if question1 in yesvalues:
    if True:
        randomData(amount, passwdlength, blnCreateCSV=1)
    else:
        randomData(amount, passwdlength, blnCreateCSV=0)

if __name__ == "__main__":
    main()
