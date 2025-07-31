Placeholder readme probably for the schema


To clone, download github desktop and login
Hit file on the top left corner and hit clone repository
Select the local folder you want the repository saved to and select this repo to clone

Notes:
Make sure to check the github for any changes and pull those changes onto local by hitting repository at the top of github
desktop and press pull

Make sure you always push any changes and make notes on what you did (github desktop wont even let you push without a description anyways)

Running python application:
# Step 1: Setup virtual environment
python3 -m venv venv

# Step 2: Activate it
source venv/bin/activate (Mac)
venv\Scripts\activate (Windows)

# Step 3: Install dependencies
pip install -r packages.txt

# Step 4: Run app
In project directory run:
export FLASK_APP=main.py (Mac)
set FLASK_APP=main.py (Windows)
flask run

/templates is where HTML will be stored and UI for the application
main.py is application where we will add our logic to our database
We will need a .db file to be able to connect with Python
packages.txt is all of the packages needed to install to run app