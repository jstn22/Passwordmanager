import db_connect
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet
import base64
import os

# AES-Schlüssel generieren (Speicher den Schlüssel sicher!)
KEY = base64.urlsafe_b64encode(os.urandom(32))
cipher = Fernet(KEY)

# Datenbankverbindung
conn = db_connect.db_connection()
cursor = conn.cursor(buffered=True)  # Verhindert "Unread result found"

# Sprachpakete
translations = {
    "de": {
        "welcome": "Willkommen zum Passwort-Manager!",
        "login": "Einloggen",
        "register": "Registrieren",
        "choose_option": "Wählen Sie eine Option: ",
        "username": "Benutzername: ",
        "password": "Passwort: ",
        "login_success": "Login erfolgreich!",
        "login_fail": "Falsches Passwort oder Benutzername.",
        "register_success": "Benutzer erfolgreich registriert!",
        "menu": "\n--- Menü ---",
        "save_password": "Neues Passwort speichern",
        "view_passwords": "Passwörter anzeigen",
        "update_password": "Passwort ändern",
        "delete_password": "Passwort löschen",
        "logout": "Ausloggen",
        "site_name": "Website/Dienst: ",
        "site_url": "URL (optional): ",
        "site_password": "Passwort für diese Seite: ",
        "password_saved": "Passwort gespeichert!",
        "no_passwords": "Keine Passwörter gespeichert.",
        "choose_language": "Sprache auswählen (de/en): "
    },
    "en": {
        "welcome": "Welcome to the Password Manager!",
        "login": "Login",
        "register": "Register",
        "choose_option": "Choose an option: ",
        "username": "Username: ",
        "password": "Password: ",
        "login_success": "Login successful!",
        "login_fail": "Incorrect password or username.",
        "register_success": "User successfully registered!",
        "menu": "\n--- Menu ---",
        "save_password": "Save new password",
        "view_passwords": "View saved passwords",
        "update_password": "Update password",
        "delete_password": "Delete password",
        "logout": "Logout",
        "site_name": "Website/Service: ",
        "site_url": "URL (optional): ",
        "site_password": "Password for this site: ",
        "password_saved": "Password saved!",
        "no_passwords": "No passwords stored.",
        "choose_language": "Choose language (de/en): "
    }
}

# Spracheinstellung
language = input(translations["de"]["choose_language"]).strip().lower()
if language not in ["de", "en"]:
    language = "de"  # Standard: Deutsch


# Verschlüsselung
def encrypt_password(password):
    return cipher.encrypt(password.encode()).decode()


def decrypt_password(encrypted_password):
    return cipher.decrypt(encrypted_password.encode()).decode()


# Benutzer-Login oder Registrierung
def login():
    print(translations[language]["login"])
    username = input(translations[language]["username"]).strip()
    password = input(translations[language]["password"]).strip()

    cursor.execute("SELECT id, password_hash FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.fetchall()

    if user:
        user_id, stored_password = user
        if check_password_hash(stored_password, password):
            print(translations[language]["login_success"])
            return user_id
    print(translations[language]["login_fail"])
    return None


# registrieren
def register():
    print(translations[language]["register"])
    username = input(translations[language]["username"]).strip()
    password = input(translations[language]["password"]).strip()

    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        print("Benutzername existiert bereits." if language == "de" else "Username already exists.")
        return None

    hashed_password = generate_password_hash(password)
    cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, hashed_password))
    conn.commit()
    print(translations[language]["register_success"])
    return cursor.lastrowid


# Passwort speichern
def add_password(user_id):
    site_name = input(translations[language]["site_name"]).strip()
    site_url = input(translations[language]["site_url"]).strip()
    site_password = input(translations[language]["site_password"]).strip()

    encrypted_password = encrypt_password(site_password)
    cursor.execute("INSERT INTO passwords (user_id, site_name, site_url, encrypted_password) VALUES (%s, %s, %s, %s)",
                   (user_id, site_name, site_url, encrypted_password))
    conn.commit()
    print(translations[language]["password_saved"])


# Passwörter anzeigen
def view_passwords(user_id):
    cursor.execute("SELECT site_name, site_url, encrypted_password FROM passwords WHERE user_id = %s", (user_id,))
    passwords = cursor.fetchall()

    if passwords:
        print(translations[language]["menu"])
        for pw in passwords:
            print(f"🔹 {pw[0]} ({pw[1]}) - {decrypt_password(pw[2])}")
    else:
        print(translations[language]["no_passwords"])


# Hauptmenü
def main():
    print(translations[language]["welcome"])
    print(f"1. {translations[language]['login']}")
    print(f"2. {translations[language]['register']}")

    choice = input(translations[language]["choose_option"])
    user_id = None

    if choice == '1':
        user_id = login()
    elif choice == '2':
        user_id = register()

    if user_id:
        while True:
            print(translations[language]["menu"])
            print(f"1. {translations[language]['save_password']}")
            print(f"2. {translations[language]['view_passwords']}")
            print("0. " + translations[language]["logout"])

            choice = input(translations[language]["choose_option"])

            if choice == '1':
                add_password(user_id)
            elif choice == '2':
                view_passwords(user_id)
            elif choice == '0':
                print(translations[language]["logout"])
                break

    cursor.close()
    conn.close()


# Starte das Programm
if __name__ == "__main__":
    main()
