# Whats That Movie - Project 3 

Whats that Movie is a Python terminal application that runs on the Code Institute mock terminal on Heroku. 

It allows the user to signup, login, and add their favourite movies. The user can also Create, Read, Update and Delete their movie inputs. 

<img src="https://github.com/AdamVictory/Whatsthatmovie/blob/main/wireframescreenshots/resonsive.png">

Live link to app https://whatsthatmovie1.herokuapp.com/

## User Flow Diagram 

This User Flow Diagram displays the users flow of actions throughout the app and their options available to them. 

<img src="https://github.com/AdamVictory/Whatsthatmovie/blob/main/wireframescreenshots/Flowcharts.jpeg">

## Google Sheets data storage

This app stores user and movie data within Google Spreadsheets, It creates a new spreadsheet for every users entry. 

<img src="https://github.com/AdamVictory/Whatsthatmovie/blob/main/wireframescreenshots/googlesheets.png">

The live link to the Google Sheet is here: https://docs.google.com/spreadsheets/d/1Z8eItMjZa4e7WdAVj2OaFcxfHtXLPkeQsVGoD9tbslk/edit?usp=sharing


## Coding approach 

I used a procedural approach. The functionality is broken into functins, with variables or lists of data being passed from function to function. 

## User Journeys 

Below are the various different user journeys the user will view throughout using this app: 

### Register 

When the dashboard first opens, the user will have to create an account if they dont have one already. If they do they can also login here. The user can choose 'R' to register, 'L' to login if they have an account, and 'X' to quit. 

<img src="https://github.com/AdamVictory/Whatsthatmovie/blob/main/wireframescreenshots/dashboard.png">

If it is the users first time using this app they must create a username and password that is between 4 and 10 characters in length. They must also confirm their password to ensure they don't forget it. It also will tell the user if the username they have chosen already exists. Once this is validated they will proceed to the user dashnoard. 

<img src=">




## Deployment 

The below are the steps that were taken to deploy this project to Heroku: 

+ In my Gitppod termnial, I ran 'pip3 freeze > requirements.txt' to install all dependancies. 
+ Create an account with Heroku, login, select 'creatre new app' 
+ Go to settings, click revesl config vars button. 
+ Add two config vars, copy and paste Creds.json for the CREDS key, also enter value of 8000 for PORT key. 
+ Click "Add buildpack" , add pyhton and node.js in this order
+ Go to deploy tab, choose Github and connect to your resposistory 
+ Click deploy brand, and the app is now deployed. 



## Credits

+ PyFiglet was used for my intro text (https://pypi.org/project/pyfiglet/)
+ Tabulate was used to format tabular data within google sheets 
+ Code Institute - Gitpod tempate 
+ Heroku - Cloud Hosting platform 
+ Google Sheets - Acts as the backend by host data entered 
+ Gspread python package for spreadsheets (https://pypi.org/project/gspread/)
+ Google Auth python package (https://pypi.org/project/google-auth/)
