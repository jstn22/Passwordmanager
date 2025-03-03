import db_connect  # Importiere die Datenbankverbindung (deine Datei db_connect.py)

# Stelle die Verbindung zur Datenbank her
conn = db_connect.db_connection()
cursor = conn.cursor()

# Login-Teil: Benutzername und Passwort eingeben
username = input("Benutzername: ").strip()  # Eingabe des Benutzernamens
password = input("Passwort: ").strip()  # Eingabe des Passworts

# Suche nach dem Benutzer in der Datenbank (Tabelle: userdata)
cursor.execute("SELECT password FROM userdata WHERE username = %s", (username,))
user = cursor.fetchone()  # Hole den Benutzer und das Passwort

# Überprüfen, ob der Benutzer existiert und das Passwort stimmt
if user and password == user[0]:
    print("✅ Login erfolgreich!")  # Wenn das Passwort stimmt

    # Menü, das nach dem Login angezeigt wird
    while True:
        print("\n--- Menü ---")
        print("1. Neuen Benutzer hinzufügen")
        print("2. Passwort ändern")
        print("3. Mein Info anzeigen")
        print("4. Alle Benutzer anzeigen")
        print("5. Benutzer löschen")
        print("0. Beenden")

        # Eingabe der Auswahl
        choice = input("Wählen Sie eine Option: ")

        if choice == '1':
            # Option 1: Neuen Benutzer und Passwort hinzufügen
            new_username = input("Geben Sie den neuen Benutzernamen ein: ").strip()
            new_password = input("Geben Sie das neue Passwort ein: ").strip()

            # Überprüfen, ob der Benutzername schon existiert
            cursor.execute("SELECT * FROM userdata WHERE username = %s", (new_username,))
            existing_user = cursor.fetchone()

            if existing_user:
                print("❌ Benutzername existiert bereits.")
            else:
                cursor.execute("INSERT INTO userdata (username, password) VALUES (%s, %s)",
                               (new_username, new_password))
                conn.commit()  # Änderungen speichern
                print("✅ Neuer Benutzer wurde hinzugefügt!")

        elif choice == '2':
            # Option 2: Passwort ändern
            new_password = input("Geben Sie das neue Passwort ein: ").strip()
            cursor.execute("UPDATE userdata SET password = %s WHERE username = %s",
                           (new_password, username))
            conn.commit()  # Änderungen speichern
            print("✅ Passwort wurde geändert!")

        elif choice == '3':
            # Option 3: Mein Info anzeigen
            cursor.execute("SELECT username, password FROM userdata WHERE username = %s", (username,))
            user_data = cursor.fetchone()  # Hole die Benutzerdaten

            if user_data:
                print("\n--- Mein Info ---")
                print(f"Benutzername: {user_data[0]}")
                print(f"Passwort: {user_data[1]}")
            else:
                print("❌ Benutzer nicht gefunden.")

        elif choice == '4':
            # Option 4: Alle Benutzer anzeigen
            cursor.execute("SELECT username, password FROM userdata")

            # Hole alle Benutzer aus der Tabelle
            all_users = cursor.fetchall()  # Alle Datensätze abholen

            if all_users:
                print("\n--- Alle Benutzer ---")
                for user in all_users:
                    print(f"Benutzername: {user[0]}, Passwort: {user[1]}")
            else:
                print("❌ Keine Benutzer gefunden.")

        elif choice == '5':
            # Option 5: Benutzer löschen
            delete_username = input("Geben Sie den Benutzernamen des zu löschenden Benutzers ein: ").strip()

            # Überprüfen, ob der Benutzer existiert
            cursor.execute("SELECT * FROM userdata WHERE username = %s", (delete_username,))
            user_to_delete = cursor.fetchone()  # Hole den Benutzer zum Löschen

            if user_to_delete:
                cursor.execute("DELETE FROM userdata WHERE username = %s", (delete_username,))
                conn.commit()  # Änderungen speichern
                print(f"✅ Benutzer '{delete_username}' wurde gelöscht!")
            else:
                print(f"❌ Benutzer '{delete_username}' wurde nicht gefunden.")

        elif choice == '0':
            # Option 0: Programm beenden
            print("❌ Sie wurden ausgeloggt.")
            break  # Beendet die Schleife und geht zurück zum Login

        else:
            print("❌ Ungültige Auswahl. Bitte erneut versuchen.")

else:
    print("❌ Falscher Benutzername oder Passwort!")

# Verbindung zur Datenbank schließen
cursor.close()
conn.close()
