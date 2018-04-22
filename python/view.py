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
    return db.get_user_by_name(userId)

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
    user = load_current_user()
    if user:
        # send user to home page if they are already logged in
        return redirect('/home')
    people = db.get_people()
    return render_template('login.html', users=people)


@app.route('/login', methods=['POST']) 
def post_login():
    username = request.form['username']
    password = request.form['password']
    role = request.form['role']
    user = db.get_user_by_credentials(username, password, role)
    if not user:
        # incorrect user id / password
        print("NO_USER")
        return redirect('/login')   
    else:
        # Send the user to the home page and set a cookie to keep their session active
        # SECURITY NOTE: THIS IS NOT A GOOD WAY TO HANDLE USER AUTHORIZATION IN PRACTICE.
        # DO NOT DO THIS FOR A PRODUCTION WEBSITE (but it's good enough for this course project)
        resp = app.make_response(redirect('/home'))
        resp.set_cookie('userID', username)
        return resp
        # if (role=="Customer"):
        #     return render_template('home.html', username=username, password=password,role=role)
        # elif (role=="Specialist"):
        #     return render_template('special-home.html', username=username, password=password,role=role)
        # elif (role=="Entry-level"):
        #     return render_template('entry-home.html', username=username, password=password,role=role)


# this is what happens when the user pushes the link to query1
@app.route('/query1', methods=['GET'])
def get_query1():
    return render_template('query1.html')

# this is what happens when the user pushes enter on the query1 page.. actually perfom + display the query
@app.route('/query1', methods=['POST']) 
def post_query1():
    # check what the user wants to query 
    option_str = request.form['option_query1']
    number = request.form['number_dates']    
    # perform the query
    str_return= db.get_query1(number, option)
    return render_template('query1.html', strings_to_output=str_return)


@app.route('/home', methods=['GET'])
def get_home():
    user = load_current_user()
    print(user)
    if not user:
        # Not logged in
        return redirect('/login')
    return render_template('home.html', user=user)

if __name__ == '__main__':
    app.run()
