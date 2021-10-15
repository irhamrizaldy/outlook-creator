import json
import mysql.connector

file_json = open("Output.json")
data = json.loads(file_json.read())

# for i in range(len(data)):
#     print(f"Nama: {data[i]['email']}")

fname = data['0']['name']
lname = data['0']['lastname'] 
email = data['0']['email']
pwd = data['0']['password']
day = data['0']['day']
month = data['0']['month']
year = data['0']['year']
country = data['0']['country']
# print(f"Nama: {data['0']['email']}")
print (fname, lname, email, pwd, day, month, year, country)

db_connection = mysql.connector.connect (
    host = "localhost",
    user = "root",
    password = "",
    database = "outlook")

db_cursor = db_connection.cursor()

outlook_insert_query = "INSERT INTO users (id, firstname, lastname, email, password, month, day, year, country) VALUES('', '"+fname+"', '"+lname+"', '"+email+"', '"+pwd+"', '"+month+"', '"+day+"', '"+year+"', '"+country+"')"

db_cursor.execute(outlook_insert_query)
db_connection.commit()
print(db_cursor.rowcount, "Record Inserted")