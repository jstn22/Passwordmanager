import mysql.connector

def db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Standardbenutzer in XAMPP
        password="",  # Standardmäßig ist kein Passwort gesetzt
        database="passwort_manager"  # Name der erstellten Datenbank
    )
