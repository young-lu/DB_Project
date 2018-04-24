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

# def get_customer_dates(ssn) :
#     userId = request.cookies.get('userID')
#     if not userId: return None
#     my_matchIDs = []
#     my_dates = []

#     for each in (db.get_matches_by_ssn(ssn)):
#         my_matchIDs.append(each['matchID'])

#     date_list = (db.get_dates(ssn, my_matchIDs))
#     return date_list

def get_date_names(dates) :
    try:
        names = []
        for each in dates:
            names.append((db.get_customer_by_ssn(each['ssn']))['first_name'])
        return names
    except: 
        return 0

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
    try:
        firstname, lastname = request.form['firstname'], request.form['lastname']
        phone = request.form['phone']
        ssn = request.form['ssn']
        dob = request.form['dob']
        gender = request.form['gender']
        children = request.form['children']
        seeking = request.form['seeking']
        username = request.form['username']
        password = request.form['password']
    except:
        return redirect('/')

    try: 
        married_prev= request.form['married_prev']
        if married_prev:
            married_prev = 'Y'
    except:
        married_prev = 'N'

    interests = request.form.getlist("interests")
    status = 'open'
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
    interests = db.get_interests()
    myssn = user['ssn']
    my_matchIDs = []
    my_matches = []
    my_dates = db.get_dates(myssn)
    # print(my_dates)

    for each in (db.get_matches_by_ssn(myssn)) : #finish this
        my_matchIDs.append(each['ssn'])

    print(my_matchIDs)
    # for each in my_matchIDs :
    #     match_list = db.get_customers_by_match_id(each)
    #     for each in match_list:
    #         my_matches.append(each['ssn'])

    # for each in my_matchIDs :

    if not user:
        return redirect('/login')
    return render_template('home.html', user=user, interests=interests, dates=my_dates)


@app.route('/find_match', methods=['POST'])
def find_match():
    user = load_current_user()
    ssn = user['ssn']
    interested_in = user['interested_in']
    married = request.form.get('married')
    max_kids = request.form['max_kids']
    max_age = request.form['max_age']
    min_age = request.form['min_age']
    interests = request.form.getlist("interest")
    my_dates = db.get_dates(ssn)


    try:
        exact = request.form['exact']
    except:
        exact = 0

    if not exact:
        ssn_list = db.find_matches(ssn, interested_in, married,max_kids,min_age,max_age,interests)
    elif exact:
        ssn_list = db.find_exact_matches(ssn, interested_in, married,max_kids,min_age,max_age,interests)

    if not ssn_list:
        return render_template('home.html',interests=db.get_interests(),dates=my_dates, user=user,none_message="\nSorry, you did not match with anyone!\n")

    matches = []
    for ssn in ssn_list:
        matches.append(db.get_customer_by_ssn(ssn['ssn']))

    return render_template('match.html',matches=matches)


@app.route('/match', methods=['POST'])
def make_match():
    user = load_current_user()
    myssn = user['ssn']
    matchssn = request.form['match']
    # print('MAKE_MATCH() {0}'.format(request.form['date']))
    # print('MAKE_MATCH() {0}'.format(request.form['time']))
    date = request.form['date']
    time = request.form['time']
    location = request.form['location']
    ID = int(db.get_largest_matchID()) + 1
    my_dates = db.get_dates(myssn)
    my_matches=[]

    for each in (db.get_matches_by_ssn(myssn)):
        printe(each['ssn'])

    # print(db.get_match_id(myssn,matchssn))

    if matchssn in my_matches :
        # return render_template('home.html', interests=db.get_interests(), dates=my_dates, user=user, none_message="you are already matched with that user!\n\n")
        if db.insert_new_date(time, date, location, db.get)
    elif (db.insert_new_match(myssn, matchssn, ID)) :
        if db.insert_new_date(time, date, location, ID) :
            return render_template('home.html', interests=db.get_interests(), dates=my_dates, user=user,none_message="match made with {0}!\n".format(db.get_customer_by_ssn(matchssn)['first_name']))
    return render_template('home.html', interests=db.get_interests(), dates=my_dates, user=user, none_message="ERROR: problem adding match\n\n")

@app.route('/dates', methods=['POST'])
def manage_dates() :
    user = load_current_user()
    my_dates = db.get_dates(user['ssn'])

    return render_template('dates.html', dates=db.get_dates(user['ssn']), user= user )

@app.route('/review_date', methods=['POST'])
def review_date():
    user = load_current_user()
    review = request.form['review']

    date = request.form['radio_date']
    matchID = date.split(',')[0]
    date_num = date.split(',')[1]

    if db.submit_date(user['ssn'], review, matchID, date_num):
        return render_template('home.html', interests=db.get_interests(), dates=db.get_dates(user['ssn']), user=user,none_message='Date review submitted')

    return render_template('dates.html', dates=db.get_dates(user['ssn']), user= user, none_message='ERROR submitting date review' )

# @app.route('/resources/<path:path>')
# def send_resources(path):
#     return send_from_directory('resources', path)


if __name__ == '__main__':
    app.run()
