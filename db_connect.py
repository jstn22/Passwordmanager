import mysql.connector

def db_conection():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="user"
    )



