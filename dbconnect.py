import mysql.connector

db_connection = mysql.connector.connect (
    host = "localhost",
    user = "root",
    password = "",
    database = "outlook"
)

# create database cursor to perform sql operation
db_cursor = db_connection.cursor()

# create table for current database
db_cursor.execute("CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, firstname VARCHAR(255), lastname VARCHAR(255), username VARCHAR(255), password VARCHAR(255), email VARCHAR(255), month VARCHAR(255), day VARCHAR(255), year VARCHAR(255), country VARCHAR(255))")

# executing cursor with execute method and pass sql query
# db_cursor.execute("CREATE DATABASE outlook")

# get list of all databases
db_cursor.execute("SHOW DATABASES")

# print all databases
for table in db_cursor:
    print(table)