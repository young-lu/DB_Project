# original author: Luca Soldaini

# third party modules
from flask import (Flask, render_template, request, send_from_directory, redirect, make_response)

# project modules
import config
from logic import Database


# instanciate application and database object
app = Flask(__name__)
db = Database(config)

# configure the web app according to the config object
app.host = config.APP_HOST
app.port = config.APP_PORT
app.debug = config.APP_DEBUG

def load_current_user():
    userId = request.cookies.get('userID')
    if not userId: return None
    return db.get_user_by_id(userId)

@app.route('/', methods=['GET'])
def index():
    """Get the main page"""
    people = db.get_people()
    interests = db.get_interests()
    return render_template('index.html', people=people, interests=interests)


@app.route('/insert', methods=['POST'])
def insert():
    """Add the person"""
    firstname, lastname = request.form['firstname'], request.form['lastname']
    phone, age = request.form['phone'], request.form['age']

    # TODO: handle interests

    # insert person
    if db.insert_person(firstname, lastname, phone, age):
        return redirect('/')
    return "Error adding to list" # TODO: better error handling

@app.route('/logout', methods=['GET'])
def get_logout():
    # Clear the user cookie to log them out
    resp = make_response(redirect('/login'))
    resp.set_cookie('userID', '')
    return resp

# this triggers when you click the button in the html doc with action= login and method= POST
@app.route('/login', methods=['GET'])
def get_login():
    if load_current_user():
        # send user to home page if they are already logged in
        return redirect('/home')
    return render_template('login.html')

@app.route('/login', methods=['POST']) 
def post_login():
    username = request.form['username']
    password = request.form['password']
    user = db.get_user_by_credentials(username, password)
    if not user:
        # incorrect user id / password
        return redirect('/login')
    else:
        # Send the user to the home page and set a cookie to keep their session active
        # SECURITY NOTE: THIS IS NOT A GOOD WAY TO HANDLE USER AUTHORIZATION IN PRACTICE.
        # DO NOT DO THIS FOR A PRODUCTION WEBSITE (but it's good enough for this course project)
        resp = make_response(redirect('/home'))
        resp.set_cookie('userID', str(user['user_id']))
        return resp

@app.route('/home', methods=['GET'])
def get_home():
    user = load_current_user()
    if not user:
        # Not logged in
        return redirect('/login')
    return render_template('home.html', user=user)




@app.route('/resources/<path:path>')
def send_resources(path):
    return send_from_directory('resources', path)








if __name__ == '__main__':
    app.run()
