import datetime
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

    # Insert valid user details to google sheets 
    SHEET.add_worksheet(title=user_name, rows="100", cols="20")
    user_sheet = SHEET.worksheet(user_name)
    user_sheet.append_row(["Username", "Password", "Date Joined"])
    user_sheet.format('A1:C1', {'text-format': {'bold': True}})
    user_sheet.append_row(
        [user_name, user_pass, str(datetime.datetime.now().date())])
    user_sheet.append_row([" ", " ", " ", " "])
    user_sheet.append_row(["Movie ID", "Movie Title", "Director", "Genre"])
    user_sheet.format('A3:D3', {'textFormat': {'bold': True}})

    user_dashboard(user_name)

def user_dashboard(user_name):
    """
    Function provides a dashboard for the user once logged in here they can add, update and delete a movie
    """
    print(f"Welcome to your dashboard, {user_name}")
    user_data = SHEET.worksheet(user_name)
    user_movie_data = user_data.get_all_values()[3:]

    while True: 
        user_input = input(
            "Type 'B' to view Movies, 'A' to add a movie, 'X' to logout:\n")
        if user_input in {"X", "x"}:
            print("You have logged out")
            init()
            break
        if user_input in ("B", "b"):
            view_all_movies(user_name, user_data, user_movie_data)
            break
        print("Wrong choice, please type B, A or X")


    def view_all_movies(user_data, user_name, user_movie_data):
        """
        This function allows the user to view all of their movies
        """
        if user_movie_data:
            print(tabulate(user_movie_data, headers=["ID", "Movie Title", "Director", "Genre", "Rating (1-5)" ]))
            while True:
                print("Want to update movie details?")
                user_input = input(
                    "Press E to edit, D to delete, or R to return to dashboard\n")

                if user_input in {"R", "r"}:
                    user_dashboard(user_name)
                if user_input in {"E", "e"}:
                    edit_movie(user_data, user_movie_data, user_name)
                    break
                if user_input in {"D", "d"}:
                    delete_movie(user_data, user_movie_data, user_name)
                    break
                print("Wrong choice")
            else: 
                print("No movies added")
                user_dashboard(user_name)






