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
    # print('loading current user')
    userId = request.cookies.get('userID')

    if not userId: return None
    if request.cookies.get('role')== 'Customer':
        return db.get_customer_by_name(userId)

    return db.get_user_by_name(userId)


def load_user_ID():
    userId = request.cookies.get('userID')
    if not userId: return None
    return userId

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
        c = []
        for i in range(int(children)):
            c.append(' ')
        seeking = request.form['seeking']
        username = request.form['username']
        password = request.form['password']
        ec = request.form['eye_color']
        hc = request.form['hair_color']
        print('CHILDREN: {0}:'.format(children))

    except:
        print('ERROR inserting customer')
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
    if db.insert_user(username,password,role):
        if db.insert_customer(ssn, firstname, lastname, username, dob,
                            seeking, phone, gender, ec, hc, 0, married_prev):
            for each in interests:
                db.insert_customer_interest(ssn, each)

            # if int(children) > 0 :
            #     return render_template('customers-children.html')
            return redirect('/')
    return "Error adding to list" # TODO: better error handling

@app.route('/add_child', methods=['POST'])
def add_child() :
    user = load_current_user()
    ssn = user['ssn']
    age = request.form['age']
    at_home = request.form['at_home']
    count = db.get_children_count(ssn)
    print('count:')
    print(count )

    db.add_child(ssn,age,at_home, count + 1)

    return redirect('/home')

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
        resp.set_cookie('role', role)
        print("resp: {0}".format(resp))
        print()
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
    results= ""
    return render_template('query1.html', results=results)

# this is what happens when the user pushes enter on the query1 page.. actually perfom + display the query
@app.route('/query1', methods=['POST']) 
def post_query1():
    # check what the user wants to query 
    option_str = request.form['option_query1']
    number = request.form['number_dates']    
    # perform the query
    username=load_user_ID()
    results= db.getquery1(username, number, option)
    return render_template('query1.html', results=results)

# this is what happens when the user clicks on page for query 2
@app.route('/query2', methods=['GET'])
def get_query2():
    username=load_user_ID()
    results= db.getquery2(username)
    return render_template('query2.html', results=results)

# this is what happens when the user clicks on page for query 3
@app.route('/query3', methods=['GET'])
def get_query3():
    username=load_user_ID()
    results= db.getquery3(username)
    return render_template('query3.html', results=results)

# this is what happens when the user clicks on page for query 4
@app.route('/query4', methods=['GET'])
def get_query4():
    username=load_user_ID()
    results= db.getquery4(username)
    return render_template('query4.html', results=results)

# this is what happens when the user clicks on page for query 5
@app.route('/query5', methods=['GET'])
def get_query5():
    username=load_user_ID()
    results= db.getquery5(username)
    return render_template('query5.html', results=results)

# this is what happens when the user clicks on page for query 7
@app.route('/query7', methods=['GET'])
def get_query7():
    username=load_user_ID()
    results= db.getquery7(username)
    return render_template('query7.html', results=results)

# this is what happens when the user clicks on page for query 8a
@app.route('/query8a', methods=['GET'])
def get_query8a():
    username=load_user_ID()
    results= db.getquery8a(username)
    return render_template('query8a.html', results=results)

# this is what happens when the user clicks on page for query 8b
@app.route('/query8b', methods=['GET'])
def get_query8b():
    username=load_user_ID()
    results= db.getquery8b(username)
    return render_template('query8b.html', results=results)

# this is what happens when the user clicks on page for query 8c
@app.route('/query8c', methods=['GET'])
def get_query8c():
    username=load_user_ID()
    results= db.getquery8c(username)
    return render_template('query8c.html', results=results)

# this is what happens when the user clicks on page for query 8d
@app.route('/query8d', methods=['GET'])
def get_query8d():
    results= db.getquery8d()
    return render_template('query8d.html', results=results)

# this is what happens when the user clicks on page for query 8e
@app.route('/query8e', methods=['GET'])
def get_query8e():
    results= db.getquery8e()
    return render_template('query8e.html', results=results)

# this is what happens when the user clicks on page for query 8f
@app.route('/query8f', methods=['GET'])
def get_query8f():
    results= db.getquery8f()
    return render_template('query8f.html', results=results)



@app.route('/home', methods=['GET'])
def get_home():
    user = load_current_user()
    if not user:
        return redirect('/login')
    interests = db.get_interests()
    print(user)
    if user['role'] == 'Customer':
        myssn = user['ssn']
        my_matchIDs = []
        my_dates = db.get_dates(myssn)
        for each in (db.get_matches_by_ssn(myssn)) : 
            my_matchIDs.append(each['ssn'])
        return render_template('home.html', user=user, interests=interests, dates=my_dates)
    elif user['role'] == 'Specialist':
        return render_template('special-home.html', user=user,tables=db.show_tables())


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
    eye_color = request.form['eye_color']
    hair_color = request.form['hair_color']

    try:
        exact = request.form['exact']
    except:
        exact = 0

    if not exact:
        ssn_list = db.find_matches(ssn, interested_in, married,max_kids,min_age,max_age,interests,eye_color, hair_color)
    elif exact:
        ssn_list = db.find_exact_matches(ssn, interested_in, married,max_kids,min_age,max_age,interests,eye_color, hair_color)

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
    date = request.form['date']
    time = request.form['time']
    location = request.form['location']
    ID = int(db.get_largest_matchID()) + 1
    my_dates = db.get_dates(myssn)
    my_matches=[]
    for each in (db.get_matches_by_ssn(myssn)) : #finish this
        my_matches.append(each['ssn'])
    print(ID)

    if matchssn in my_matches :
        return render_template('home.html', interests=db.get_interests(), dates=my_dates, user=user, none_message="you are already matched with that user!\n\n")
        # if db.insert_new_date(time, date, location, db.get/
    elif (db.insert_new_match(myssn, matchssn, ID)) :
        if db.insert_new_date(time, date, location, ID) :
            # return render_template('home.html', interests=db.get_interests(), dates=my_dates, user=user,none_message="match made with {0}!\n".format(db.get_customer_by_ssn(matchssn)['first_name']))
            return redirect('/home')
    return render_template('home.html', interests=db.get_interests(), dates=my_dates, user=user, none_message="ERROR: problem adding match\n\n")

@app.route('/dates', methods=['POST'])
def manage_dates() :
    user = load_current_user()
    my_dates = db.get_dates(user['ssn'])


    return render_template('dates.html', dates=db.get_dates(user['ssn']), user= user )

@app.route('/dates', methods=['GET'])
def get_dates_page() :
    user = load_current_user()

    if not user:
        return redirect('/home')
    return render_template('dates.html', dates=db.get_dates(user['ssn']), user= user )


@app.route('/add_date', methods=['POST'])
def add_date() :
    user = load_current_user()

    rematch = request.form['radio_date'].split(',')
    rematchID  = rematch[0]
    rematch_ssn = rematch[1]
    date = request.form['date']
    time = request.form['time']
    location = request.form['location']

    if db.insert_new_date(time, date, location, rematchID) :
        return redirect('/dates')

    return render_template('dates.html', dates=db.get_dates(user['ssn']), user= user, none_message='ERROR adding date' )

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

@app.route('/get_special_insert', methods=['POST'])
def get_special_insert() :

    try:
        table = request.form['insert_table'].lower()
        # print('table: {0}'.format(table))
        dest = 'insert_{0}.html'.format(table)
        print(dest)
        return render_template('{0}'.format(dest))

    except:
        print('ERROR in get_special_insert')
        return redirect('/home')




###########################################
####### UPDATE + DELETE VIEWS GET #########
###########################################
# view for udpate-customer page
# @app.route('/update-customer', methods=['GET'])
# def update_customer_get():
#     statement
#     results= db.update(statement)
#     return render_template('update-customer.html', results=results)

# # view for update-customer-interests page
# @app.route('/update-customer-interests', methods=['GET'])
# def update_customer_interests_get():
#     username=load_user_ID()
#     results= db.update(statement)
#     return render_template('update-customer-interests.html', results=results)

# # view for update-customer-crimes page
# @app.route('/update-customer-crimes', methods=['GET'])
# def update_customer_crimes_get():
#     username=load_user_ID()
#     results= db.update(statement)
#     return render_template('update-customer-crimes.html', results=results)

# # view for update-customer-children
# @app.route('/update-customer-children', methods=['GET'])
# def update_customer_children_get():
#     username=load_user_ID()
#     results= db.update(statement)
#     return render_template('update-customer-children.html', results=results)

# # view for update-interests page
# @app.route('/update-interests', methods=['GET'])
# def update_interests_get():
#     username=load_user_ID()
#     results= db.update(statement)
#     return render_template('update-interests.html', results=results)

# # view for update-crime-options page
# @app.route('/update-crime-options', methods=['GET'])
# def update_crime_options_get():
#     username=load_user_ID()
#     results= db.update(statement)
#     return render_template('update-crime-options.html', results=results)

# # view for delete-customer page
# @app.route('/delete-customer', methods=['GET'])
# def delete_customer_get():
#     username=load_user_ID()
#     results= db.delete_sql(statement)
#     return render_template('delete-customer.html', results=results)

# # view for delete-customer-interests page
# @app.route('/delete-customer-interests', methods=['GET'])
# def delete_customer_interests_get():
#     username=load_user_ID()
#     results= db.delete_sql(statement)
#     return render_template('delete-customer-interests.html', results=results)

# # view for delete-customer-crimes page
# @app.route('/delete-customer-crimes', methods=['GET'])
# def delete_customer_crimes_get():
#     username=load_user_ID()
#     results= db.delete_sql(statement)
#     return render_template('delete-customer-interests.html', results=results)

# # view for delete-customer-children page
# @app.route('/delete-customer-children', methods=['GET'])
# def delete_customer_children_get():
#     username=load_user_ID()
#     results= db.delete_sql(statement)
#     return render_template('delete-customer-children.html', results=results)

# # view for delete-interests page
# @app.route('/delete-interests', methods=['GET'])
# def delete_interests_get():
#     username=load_user_ID()
#     results= db.delete_sql(statement)
#     return render_template('delete-interests.html', results=results)

# # view for delete-crime page
# @app.route('/delete-crime', methods=['GET'])
# def delete_crime_get():
#     username=load_user_ID()
#     results= db.delete_sql(statement)
#     return render_template('delete-crime.html', results=results)



# ###########################################
# ####### UPDATE + DELETE VIEWS POST ########
# ###########################################

# ### LOGIC FOR UPDATE:   in the get views we will display all of the options for which ones to udpate and we will have a field for each
# ###                     option of what to update... we will need to implement checks to make sure the specialist doesnt cause errors 
# ###                     in the DB
# ###                     when they push enter, the post view will then use the selected one as the one to update
# ###                     Then, the update statements will be performed using the primary keys (AKA find all tuples containing that key)
# ###                     When performing this update, we will also make sure to update dependencies.


# ### LOGIC FOR DELETION: in the get views we will display all of the options and have check boxes next to them.
# ###                     then, the user will be able to delete those that they check
# ###                     when they push enter, the post view will then use those that were check-marked as the ones to delete
# ###                     The deletion statements will be performed using the primary keys (AKA find all tuples containing that key)
# ###                     When performing these deletions, we will also make sure to delete dependencies.

# # view for udpate-customer page
# @app.route('/update-customer', methods=['POST'])
# def update_customer_post():

#     results= db.update(statement)
#     return render_template('update-customer.html', results=results)

# # view for update-customer-interests page
# @app.route('/update-customer-interests', methods=['POST'])
# def update_customer_interests_post():
#     username=load_user_ID()
#     results= db.update(statement)
#     return render_template('update-customer-interests.html', results=results)

# # view for update-customer-crimes page
# @app.route('/update-customer-crimes', methods=['POST'])
# def update_customer_crimes_post():
#     username=load_user_ID()
#     results= db.update(statement)
#     return render_template('update-customer-crimes.html', results=results)

# # view for update-customer-children
# @app.route('/update-customer-children', methods=['POST'])
# def update_customer_children_post():
#     username=load_user_ID()
#     results= db.update(statement)
#     return render_template('update-customer-children.html', results=results)

# # view for update-interests page
# @app.route('/update-interests', methods=['POST'])
# def update_interests_post():
#     username=load_user_ID()
#     results= db.update(statement)
#     return render_template('update-interests.html', results=results)

# # view for update-crime-options page
# @app.route('/update-crime-options', methods=['POST'])
# def update_crime_options_post():
#     username=load_user_ID()
#     results= db.update(statement)
#     return render_template('update-crime-options.html', results=results)

# # view for delete-customer page
# @app.route('/delete-customer', methods=['POST'])
# def delete_customer_post():
#     username=load_user_ID()
#     results= db.delete_sql(statement)
#     return render_template('delete-customer.html', results=results)

# # view for delete-customer-interests page
# @app.route('/delete-customer-interests', methods=['POST'])
# def delete_customer_interests_post():
#     username=load_user_ID()
#     results= db.delete_sql(statement)
#     return render_template('delete-customer-interests.html', results=results)

# # view for delete-customer-crimes page
# @app.route('/delete-customer-crimes', methods=['POST'])
# def delete_customer_crimes_post():
#     username=load_user_ID()
#     results= db.delete_sql(statement)
#     return render_template('delete-customer-interests.html', results=results)

# # view for delete-customer-children page
# @app.route('/delete-customer-children', methods=['POST'])
# def delete_customer_children_post():
    
#     results= db.delete_sql(statement)
#     return render_template('delete-customer-children.html', results=results)

# # view for delete-interests page
# @app.route('/delete-interests', methods=['POST'])
# def delete_interests_post():
#     username=load_user_ID()
#     results= db.delete_sql(statement)
#     return render_template('delete-interests.html', results=results)

# # view for delete-crime page
# @app.route('/delete-crime', methods=['POST'])
# def delete_crime_post():
#     username=load_user_ID()
#     results= db.delete_sql(statement)
#     return render_template('delete-crime.html', results=results)

# @app.route('/resources/<path:path>')
# def send_resources(path):
#     return send_from_directory('resources', path)


if __name__ == '__main__':
    app.run()







