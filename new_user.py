from db_connect import db_conection

db = db_conection()
cursor = db.cursor()

def add_item(username, password):
    cursor.execute('INSERT INTO userdata (username, password) VALUES (%s, %s)', (username, password))
    db.commit()

name = input("Username: ")
password = input("Passwort: ")

add_item(name, password)

print("User erfolgreich hinzugefügt")