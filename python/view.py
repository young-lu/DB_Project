# original author: Luca Soldaini

# third party modules
from flask import (Flask, render_template, request, send_from_directory, redirect, make_response)

# project modules
import config
import datetime
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


#fix this to fit our tables; probable here submit to user tble, add customer details on seperate page
@app.route('/insert', methods=['POST'])
def insert():
    """Add the person"""
    firstname, lastname = request.form['firstname'], request.form['lastname']
    phone = request.form['phone']
    ssn = request.form['ssn']
    dob = request.form['dob']
    gender = request.form['gender']
    children = request.form['children']
    married_prev= request.form['married_prev']
    interests = request.form.getlist("interests")
    seeking = request.form['seeking']
    if married_prev == 'true' :
        married_prev = 'Y'
    else:
        married_prev = 'N'
    status = 'open'
    username = request.form['username']
    password = request.form['password']
    role = 'Customer'
    # TODO: handle interests
    # insert person

    if db.insert_new_user(username,password,role):
        if db.insert_new_customer(ssn, firstname, lastname, username, dob, seeking, phone, gender, 
                    children, married_prev):
            for each in interests:
                db.insert_customer_interest(ssn, each)
            return redirect('/')
    return "Error adding to list" # TODO: better error handling

@app.route('/logout', methods=['GET'])
def get_logout():
    # Clear the user cookie to log them out
    resp = make_response(redirect('/login'))
    resp.set_cookie('userID', '')
    return resp

# this triggers when you click the button in the html doc with action= login and method= GET
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
