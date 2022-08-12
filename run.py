import gspread 
from google.oauth2.service_account import Credentials 


# The connection between applications and google sheets
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('WhatsThatMovie')

def user_login():
    """
    Function forwards username and password to the authenticate_user function.
    """
    while True:
        user_name = validate_login_input("username")
        user_pass = validate_login_input("password")
        
        if authenticate_user(user_name, user_pass):
            print(f"Logged in as user {user_name}!")
            user_dashboard(user_name)
            break

        print("Incorrect details, try again!")

def user_register():
    """
    Places the users input details into the google sheet
    """
    user_name = validate_signup_input("username")
    user_pass = validate_signup_input("password")

    while True: 
        user_pass_confirm = input("Confirm your password:\n")

        if user_pass_confirm == user_pass:
            print("Correct Password")
            break
        if user_pass_confirm != user_pass:
            print("Wrong Password")

    print(f"You have signed up and are logged in as user {user_name}!")





