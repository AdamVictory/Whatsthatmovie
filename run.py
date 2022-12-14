import datetime
import gspread
from google.oauth2.service_account import Credentials 
import pyfiglet
from tabulate import tabulate

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

ascii_banner = pyfiglet.figlet_format("><> WHATS-THAT- MOVIE <><")
print(ascii_banner)


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

    # Write valid user details to new sheet and populate rows
    SHEET.add_worksheet(title=user_name, rows="100", cols="20")
    user_sheet = SHEET.worksheet(user_name)
    user_sheet.append_row(["Username", "Password", "Date Joined"])
    user_sheet.format('A1:C1', {'textFormat': {'bold': True}})
    user_sheet.append_row(
        [user_name, user_pass, str(datetime.datetime.now().date())])
    user_sheet.append_row([" ", " ", " ", " "])
    user_sheet.append_row(["Movie ID", "Movie Title", "Director", "Genre"])
    user_sheet.format('A3:D3', {'textFormat': {'bold': True}})

    user_dashboard(user_name)


def user_dashboard(user_name):
    """
    Function provides a dashboard for the user once logged in here they can update and delete a movie
    """
    print(f"Welcome to your dashboard, {user_name}")
    # Get all user data for this username
    user_data = SHEET.worksheet(user_name)
    user_movie_data = user_data.get_all_values()[3:]

    while True: 
        user_input = input(
            "Press 'B' to view movies, 'A' to add a movie, 'X' to logout:\n")
        if user_input in {"X", "x"}:
            print("You have logged out")
            init()
            break
        if user_input in ("B", "b"):
            view_all_movies(user_data, user_name, user_movie_data)
            break
        if user_input in {"A", "a"}:
            add_movie(user_name, user_data, user_movie_data)
            break
        print("Wrong choice, please type B, A or X")


def view_all_movies(user_data, user_name, user_movie_data):
    """
    This function allows the user to view all of their movies
    """
    if user_movie_data:
        print(tabulate(user_movie_data, headers=["ID", "Movie Title", "Director", "Genre", "Rating (1-5)"]))
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


def add_movie(user_name, user_data, user_movie_data):
    """
    Function creates a new record
    """
    while True: 
        movie_data = []
        movie_prompt_labels = ["title", "director", "genre"]
        for label in movie_prompt_labels:
            user_input = input(f"Add movie {label}:\n")
            movie_data.append(user_input)

        movie_data = watchlist_and_rating_input(movie_data)

        if "" not in movie_data:
            print("Data is correct")
            break
        print("You entered empty values! Try again")


# Assign Movie ID
    new_movie_id = assign_movie_id(user_movie_data)
    movie_data.insert(0, new_movie_id)

    user_data.append_row(movie_data)

    user_dashboard(user_name)


def edit_movie(user_data, user_movie_data, user_name):
    """
    This function allows the user to edit their movie records
    """
    while True: 
        movie_data = []
        user_input_id = input("Choose movie ID from list:\n")
        if user_input_id.isdigit() and check_movie_id(user_movie_data, user_input_id):

            movie_data = watchlist_and_rating_input(movie_data)

            new_list_of_movies = []
            for movie in user_movie_data:
                movie[0] = int(movie[0])
                movie[4] = True if movie[4] == 'TRUE' else False 
                movie[5] = int(movie[5])

                new_list_of_movies.append(movie)
                if int(movie[0]) == int(user_input_id):
                    movie[4] = movie_data[0]
                    movie[5] = movie_data[1]
                user_data.delete_rows(4, 20)
                # Write new list back to sheet 
                for movie in new_list_of_movies:
                    user_data.append_row(movie)
                user_data.add_rows(1)

                print("Movie updated, returning to dashboard")
                user_dashboard(user_name)
                
                break
            print("Movie ID does not exist")


def delete_movie(user_data, user_movie_data, user_name):
    """
    Function allowsd the user to delete an ID relating to a movie
    """
    while True: 
        user_input_id = input("Choose movie ID from above list:\n")
        if user_input_id.isdigit() and check_movie_id(user_movie_data, user_input_id):
            # delete the movie from data list
            new_list_of_movies = []
            for movie in user_movie_data:
                if int(movie[0]) != int(user_input_id):
                    # Id number is read back into app as string 
                    # so this converts back into integer
                    new_int_movie_id = int(movie[0])
                    movie.pop(0)
                    movie.insert(0, new_int_movie_id)
                    new_list_of_movies.append(movie)

            user_data.delete_rows(4, 20)
            # Write new list back to sheet 
            for movie in new_list_of_movies:
                user_data.append_row(movie)
            user_data.add_rows(1)

            # user_data.add_rows(1)

            # view_all_movies(user_data, user_name, user_movie_data)
            print("Movie deleted")
            user_dashboard(user_name)

            break
        print("That movie ID does not exist")


# UTILITY FUNCTIONS 


def validate_login_input(input_name):
   """
   Function means that users cannot submit empty values
   """
   while True:
       user_input_field = input(f"Enter your {input_name}:\n")

       if len(user_input_field) > 0: 
        return user_input_field
       if len(user_input_field) == 0:
        print(f"{input_name} can't be empty")


def validate_signup_input(input_name):
    """
    Function means that users can't submit empty values at sign up
    """
    while True:
        user_input_field = input(
            f'Choose a {input_name} (4-10 characters):\n')
        user_name_exists = check_username(user_input_field)

        if len(user_input_field) > 3 and len(user_input_field) < 11 and not user_name_exists:
            print(f"Your {input_name} {user_input_field} is valid!")
            return user_input_field
        if user_name_exists:
            print(f"{input_name} already exists, pick another")
        if len(user_input_field) > 0 and len(user_input_field) < 4: 
            print(f"{input_name} is too short")
        if len(user_input_field) > 10:
            print(f"{input_name} is too long")
        if len(user_input_field) == 0:
            print(f"{input_name} can't be empty")


def authenticate_user(user_name, user_pass):
    """
    Function takes the user details and compares them with the google sheet
    """
    # get list of current usernames from sheet 
    worksheet_objs = SHEET.worksheets()
    username_list = []
    for worksheet in worksheet_objs:
        username_list.append(worksheet.title)

    if user_name in username_list: 
        if check_password(user_name, user_pass): 
            return True

    else: 
        return False


def check_password(user_name, user_pass):
    """
    Function checks user password
    """
    user_sheet = SHEET.worksheet(user_name)
    user_data = user_sheet.get_all_values()
    user_data_row = user_data[1]
    user_password = user_data_row[1]
    if user_pass == user_password:
        return True
    return False


def check_username(user_name): 
    """
    Function that checks if username already exists
    """
    # get list of current usernames from sheet
    worksheet_objs = SHEET.worksheets()
    username_list = []
    for worksheet in worksheet_objs:
        username_list.append(worksheet.title)

    if user_name in username_list:
        return True
    return False


def check_movie_id(data, movie_id):
    """
    Function checks that the movie ID exists in the users list
    """
    movie_ids = []

    for movie in data: 
        movie_ids.append(int(movie[0]))

    if int(movie_id) in movie_ids: 
        return True 
    return False 


def assign_movie_id(user_movie_data): 
    """
    Function assigns the ID as 1 if no other movies present in list 
    """
    if not user_movie_data:
        return 1 
    else: 
        return int(user_movie_data[-1][0]) + 1


def watchlist_and_rating_input(movie_data):
    """
    This function allows the user to edit or add details to their movie record
    """
    while True: 
        watch_list_input = input("Have you watched this movie? Y or N:\n")
        if watch_list_input in {"Y", "y"}:
            while True: 
                rating_input = input("Please rate movie out of 5:\n")
                if rating_input.isdigit():
                    if int(rating_input) > 0 and int(rating_input) < 6: 
                        movie_data = movie_data + [True, int(rating_input)]
                        return movie_data
                print("Add a number between 1 and 5")
            break 
        if watch_list_input in {"N", "n"}:
            movie_data = movie_data + [False, 0]
            return movie_data
        print("Wrong choice, Choose Y or N")


def init():
    """
    Function starts application and asks for first movie"
    """
    print("Welcome to Whats That Movie! Never forget your favourite movies again")

    while True: 
        user_input = input(
            "Press 'L' to login, or 'R' to register, or 'X' to quit:\n")
        if user_input in {"L", "l"}: 
            user_login()
            break
        if user_input in {"R", "r"}: 
            user_register()
            break
        if user_input in {"X", "x"}: 
            print("Thank you for using WhatsThatMovie")
            quit()
        else:
            print("Wrong choice, type L, R OR X")


init()