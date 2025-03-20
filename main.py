import db_connect
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet
import base64
import os

# AES-Schlüssel generieren (Dieser sollte sicher gespeichert werden!)
KEY = base64.urlsafe_b64encode(os.urandom(32))
cipher = Fernet(KEY)

# Verbindung zur Datenbank herstellen
conn = db_connect.db_connection()
cursor = conn.cursor(buffered=True)  # Verhindert "Unread result found"

# Sprachoptionen
languages = {
    "de": {
        "welcome": "Willkommen zum Passwort-Manager!",
        "register": "Registrieren",
        "login": "Einloggen",
        "exit": "Beenden",
        "username": "Benutzername",
        "password": "Passwort",
        "invalid_choice": "Ungültige Auswahl, bitte erneut versuchen.",
        "already_exists": "Benutzername existiert bereits. Bitte einen anderen wählen.",
        "empty_fields": "Benutzername und Passwort dürfen nicht leer sein!",
        "registration_success": "Registrierung erfolgreich!",
        "login_success": "Login erfolgreich!",
        "login_fail": "Falscher Benutzername oder Passwort!",
        "attempts_left": "Versuche übrig.",
        "too_many_attempts": "Zu viele Fehlversuche. Programm wird beendet.",
        "main_menu": "--- Hauptmenü ---",
        "add_password": "1. Passwort für eine Webseite speichern",
        "view_passwords": "2. Gespeicherte Passwörter anzeigen",
        "logout": "0. Abmelden",
        "enter_website": "Webseiten-Name eingeben:",
        "enter_url": "Webseiten-URL (optional):",
        "password_saved": "Passwort erfolgreich gespeichert!",
        "no_passwords": "Keine gespeicherten Passwörter gefunden."
    },
    "en": {
        "welcome": "Welcome to the Password Manager!",
        "register": "Register",
        "login": "Login",
        "exit": "Exit",
        "username": "Username",
        "password": "Password",
        "invalid_choice": "Invalid choice, please try again.",
        "already_exists": "Username already exists. Please choose another.",
        "empty_fields": "Username and password cannot be empty!",
        "registration_success": "Registration successful!",
        "login_success": "Login successful!",
        "login_fail": "Incorrect username or password!",
        "attempts_left": "Attempts left.",
        "too_many_attempts": "Too many failed attempts. Program will exit.",
        "main_menu": "--- Main Menu ---",
        "add_password": "1. Save a password for a website",
        "view_passwords": "2. View saved passwords",
        "logout": "0. Logout",
        "enter_website": "Enter website name:",
        "enter_url": "Enter website URL (optional):",
        "password_saved": "Password saved successfully!",
        "no_passwords": "No saved passwords found."
    }
}

# Sprache wählen
def choose_language():
    while True:
        lang_choice = input("Sprache wählen | Choose language (de/en): ").strip().lower()
        if lang_choice in languages:
            return languages[lang_choice]
        print("Ungültige Auswahl / Invalid choice.")

lang = choose_language()

# Verschlüsselungsfunktionen
def encrypt_password(password):
    return cipher.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password):
    return cipher.decrypt(encrypted_password.encode()).decode()

# Registrierung
def register():
    while True:
        username = input(f"{lang['username']}: ").strip()
        password = input(f"{lang['password']}: ").strip()

        if not username or not password:
            print(lang["empty_fields"])
            continue

        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            print(lang["already_exists"])
            continue

        hashed_password = generate_password_hash(password)
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        print(lang["registration_success"])
        break

# Login mit maximal 3 Versuchen
def login():
    attempts = 3
    while attempts > 0:
        username = input(f"{lang['username']}: ").strip()
        password = input(f"{lang['password']}: ").strip()

        cursor.execute("SELECT id, password_hash FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user[1], password):
            print(lang["login_success"])
            return user[0]

        attempts -= 1
        print(f"{lang['login_fail']} {attempts} {lang['attempts_left']}")

    print(lang["too_many_attempts"])
    exit()

# Passwort speichern
def save_password(user_id):
    website = input(f"{lang['enter_website']} ").strip()
    url = input(f"{lang['enter_url']} ").strip()
    password = input(f"{lang['password']}: ").strip()

    if not website or not password:
        print(lang["empty_fields"])
        return

    encrypted_password = encrypt_password(password)
    cursor.execute("INSERT INTO passwords (user_id, website, url, password_hash) VALUES (%s, %s, %s, %s)",
                   (user_id, website, url, encrypted_password))
    conn.commit()
    print(lang["password_saved"])

# Gespeicherte Passwörter anzeigen
def view_passwords(user_id):
    cursor.execute("SELECT website, url, password_hash FROM passwords WHERE user_id = %s", (user_id,))
    passwords = cursor.fetchall()

    if not passwords:
        print(lang["no_passwords"])
        return

    print("\n--- Gespeicherte Passwörter ---")
    for site, url, encrypted_password in passwords:
        print(f"🔹 {site} ({url}) - {decrypt_password(encrypted_password)}")

# Hauptmenü
def main_menu(user_id):
    while True:
        print(f"\n{lang['main_menu']}")
        print(lang["add_password"])
        print(lang["view_passwords"])
        print(lang["logout"])

        choice = input("Option wählen: ").strip()

        if choice == "1":
            save_password(user_id)
        elif choice == "2":
            view_passwords(user_id)
        elif choice == "0":
            print("Abgemeldet.")
            exit()
        else:
            print(lang["invalid_choice"])

# Startmenü
def main():
    while True:
        print("\n--- Passwort-Manager ---")
        print("1. " + lang["register"])
        print("2. " + lang["login"])
        print("0. " + lang["exit"])

        choice = input("Option wählen: ").strip()

        if choice == "1":
            register()
        elif choice == "2":
            user_id = login()
            main_menu(user_id)
        elif choice == "0":
            print("Programm beendet.")
            exit()
        else:
            print(lang["invalid_choice"])

# Programm starten
print(lang["welcome"])
main()

# Datenbankverbindung schließen
cursor.close()
conn.close()
