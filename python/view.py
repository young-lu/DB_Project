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
    people = db.get_users()
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
        seeking = request.form['seeking']
        username = request.form['username']
        password = request.form['password']
        ec = request.form['eye_color']
        hc = request.form['hair_color']

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
    people = db.get_users()
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
@app.route('/query_dropdown', methods=['GET'])
def get_query_menu():
    return render_template('queries_drop_down.html')


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




################################################################
#############      begin views for insertion       #############
################################################################

# this is what happens when the user pushes the link to query1
# @app.route('/insert_interest', methods=['GET'])
# def insert_interest():
#     results= ""
#     return render_template('insert_interest.html', results=results)

# # this is what happens when the user pushes enter on the query1 page.. actually perfom + display the query
# @app.route('/insert_interest', methods=['POST']) 
# def post_query1():
#     # check what the user wants to insert -- need to have a category and an interest

#     # *******ADD HERE TO DO********

#     # perform the insertion
#     # takes args interest and category
#     db.insert_interest(interest, category)
#     return render_template('insert_interest.html', results=results)


################################################################
#############       end views for insertion        #############
################################################################







@app.route('/home', methods=['GET'])
def get_home():
    user = load_current_user()
    if not user:
        return redirect('/login')
    interests = db.get_interests()
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
        return render_template('home.html', interests=db.get_interests(), dates=my_dates, user=user, 
                                none_message="you are already matched with that user!\n\n")
    elif (db.insert_match(myssn, matchssn, ID)) :
        if db.insert_date(time, date, location, ID) :
            # return render_template('home.html', interests=db.get_interests(), dates=my_dates, user=user,none_message="match made with {0}!\n".format(db.get_customer_by_ssn(matchssn)['first_name']))
            return redirect('/home')
    return render_template('home.html', interests=db.get_interests(), dates=my_dates, 
                            user=user, none_message="ERROR: problem adding match\n\n")

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

    if db.insert_date(time, date, location, rematchID) :
        return redirect('/dates')

    return render_template('dates.html', dates=db.get_dates(user['ssn']), user= user, none_message='ERROR adding date' )

@app.route('/review_date', methods=['POST'])
def review_date():
    user = load_current_user()
    review = request.form['review']

    date = request.form['radio_date']
    matchID = date.split(',')[0]
    date_num = date.split(',')[1]
    print(matchID)
    print(date_num)

    if db.submit_date(user['ssn'], review, matchID, date_num):
        return render_template('home.html', interests=db.get_interests(), dates=db.get_dates(user['ssn']), 
                                user=user,none_message='Date review submitted')

    return render_template('dates.html', dates=db.get_dates(user['ssn']), user= user, 
                            none_message='ERROR submitting date review')

@app.route('/get_special_insert', methods=['POST'])
def get_special_insert() :
    table = request.form['insert_table'].lower()
    print('table: {0}'.format(table))
    dest = '/specialist-insert/insert_{0}.html'.format(table)
    people=[]
    for each in db.get_all_customers():
        people.append(each)
    crimes = db.get_all_crimes()
    interests= db.get_interests()
    matches = db.get_all_matches()
    dates = db.get_all_date_pairs()
    # for each in dates:
    #     print('\n')
    #     print(each)

    return render_template('{0}'.format(dest), people=people, crimes=crimes, 
                            matches=matches, interests=interests, dates=dates)
    print('ERROR in get_special_insert')
    return redirect('/home')

@app.route('/special_insert_user', methods=['POST'])
def special_insert_user() :
    try:
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        db.insert_user(username, password, role)
        # print('special insert success')
        return redirect('/home')
    except:
        print("SPECIAL INSERT ERROR")
        return render_template('special-home.html', user=load_current_user(),tables=db.show_tables())

@app.route('/special_insert_role', methods=['POST'])
def special_insert_role() :
    try:
        role = request.form['role']
        db.insert_role(role)
        return redirect('/home')
    except:
        print("SPECIAL INSERT ERROR")
        return render_template('special-home.html', user=load_current_user(),tables=db.show_tables())


@app.route('/special_insert_matches', methods=['POST'])
def special_insert_matches() :
    try:
        ssn1 = request.form['ssn1']
        ssn2 = request.form['ssn2']
        mid = int(db.get_largest_matchID()) + 1
        my_dates = db.get_dates(ssn1)
        my_matches=[]
        for each in (db.get_matches_by_ssn(ssn1)) : #finish this
            my_matches.append(each['ssn'])
        if ssn2 in my_matches :
            return render_template('special-home.html', user=load_current_user(),tables=db.show_tables())
        
        db.insert_match(ssn1, ssn2, mid)
        return redirect('/home')

    except:
        print("SPECIAL INSERT ERROR")
        return render_template('special-home.html', user=load_current_user(),tables=db.show_tables())

@app.route('/special_insert_crime', methods=['POST'])
def special_insert_crime() :
    try:
        crime = request.form['crime']
        db.insert_crime(crime)
        return redirect('/home')
    except :
        print("SPECIAL INSERT ERROR")
        return render_template('special-home.html', user=load_current_user(),tables=db.show_tables())

@app.route('/special_insert_customer_crimes', methods=['POST'])
def special_insert_customer_crime() :
    try:
        ssn = request.form['customer']
        crime = request.form['crime']
        db.insert_customer_crime(ssn,crime)
        return redirect('/home')
    except :
        print("SPECIAL CUSTOMER_CRIMES INSERT ERROR")
        return render_template('special-home.html', user=load_current_user(),tables=db.show_tables())

@app.route('/special_insert_customer_interests', methods=['POST'])
def special_insert_customer_interests():
    try:
        interest = request.form['interest']
        ssn = request.form['customer']

        db.insert_customer_interest(ssn, interest)
        return redirect('/home')
    except:
        print("SPECIAL CUSTOMER_interests INSERT ERROR")
        return render_template('special-home.html', user=load_current_user(),tables=db.show_tables())

@app.route('/special_insert_customer', methods=['POST'])
def special_insert_customer() :
    try:
        firstname, lastname = request.form['firstname'], request.form['lastname']
        phone = request.form['phone']
        ssn = request.form['ssn']
        dob = request.form['dob']
        gender = request.form['gender']
        seeking = request.form['seeking']
        username = request.form['username']
        password = request.form['password']
        ec = request.form['eye_color']
        hc = request.form['hair_color']
        try: 
            married_prev= request.form['married_prev']
            if married_prev:
                married_prev = 'Y'
        except:
            married_prev = 'N'

        db.insert_user(username,password,"Customer")
        db.insert_customer(ssn, firstname, lastname, username, dob,
                            seeking, phone, gender, ec, hc, 0, married_prev)
        return redirect('/home')

    except:
        print("SPECIAL Customer INSERT ERROR")
        return render_template('special-home.html', user=load_current_user(),tables=db.show_tables())

@app.route('/special_insert_customers_children', methods=["POST"])    
def special_insert_customers_children() :
    try:
        ssn = request.form['customer']
        age = request.form['age']
        at_home = request.form['at_home']
        count = db.get_children_count(ssn)
        db.add_child(ssn,age,at_home, count + 1)
        return redirect('/home')
    except: 
        print("SPECIAL Customers Children INSERT ERROR")
        return render_template('special-home.html', user=load_current_user(),tables=db.show_tables())

@app.route('/special_insert_interests', methods=['POST'])
def special_insert_interests() :
    try: 
        interest = request.form['interest']
        category = request.form['category']
        db.insert_interest(interest, category)
        return redirect('/home')
    except :
        print("SPECIAL interests INSERT ERROR")
        return render_template('special-home.html', user=load_current_user(),tables=db.show_tables())

@app.route('/special_insert_dates', methods=['POST'])
def special_insert_dates() :
    try :
        matchID = request.form['matchID']
        date = request.form['date']
        time = request.form['time']
        location = request.form['location']
        db.insert_date(time, date, location, matchID) 
        return redirect('/home')
    except:
        print("SPECIAL dates INSERT ERROR")
        return render_template('special-home.html', user=load_current_user(),tables=db.show_tables())

@app.route('/special_insert_datesuccess', methods=['POST'])
def special_insert_datesuccess() :
    try:
        date = request.form['radio_date'].split(',')
        date_num = date[0]
        mid = date[1]
        ssn1 = date[2]
        ssn2 = date[3]

        review_ssn1 = request.form['review_ssn1']
        review_ssn2 = request.form['review_ssn2']

        db.submit_date(ssn1, review_ssn1, mid, date_num)
        db.submit_date(ssn2, review_ssn2,mid, date_num)
        return redirect('/home')
    except:
        print("SPECIAL DateSuccess INSERT ERROR")
        return render_template('special-home.html', user=load_current_user(),tables=db.show_tables())



###########################################
####### UPDATE + DELETE VIEWS GET #########
###########################################

#view for update_customer page
@app.route('/update_customer', methods=['GET'])
def update_customer_get():
    results= db.return_tuples('Customers')
    return render_template('update_customer.html', results=results)

# view for update-customer page
@app.route('/update_customer', methods=['POST'])
def update_customer_post():
    # first get which customer to change by ssn 
    ssn = request.form['customer']
    kwargs_to_pass= {}
    if request.form['first_name']:
        first_name= request.form['first_name']
        # add it to the kwargs
        kwargs_to_pass['first_name']=  first_name

    if request.form['last_name']:
        last_name= request.form['last_name']
        # add it to the kwargs
        kwargs_to_pass['last_name']=  last_name

    if request.form['username']:
        username= request.form['username']
        # add it to the kwargs
        kwargs_to_pass['username']=  username

    if request.form['phone']:
        phone= request.form['phone']
        # add it to the kwargs
        kwargs_to_pass['phone']=  phone

    if request.form['DOB']!='1000-01-01':
        DOB= request.form['DOB']
        # add it to the kwargs
        kwargs_to_pass['DOB']=  DOB

    if request.form['eye_color'] != "no_change":
        eye_color= request.form['eye_color']
        kwargs_to_pass['eye_color']=  eye_color

    if request.form['hair_color']!= "no_change":
        hair_color= request.form['hair_color']
        # add it to the kwargs
        kwargs_to_pass['hair_color']= hair_color

    if request.form['gender'] != "no_change":
        gender= request.form['gender']
        # add it to the kwargs
        kwargs_to_pass['gender']= gender

    if request.form['interested_in'] != "no_change":
        interested_in= request.form['interested_in']
        kwargs_to_pass['interested_in']=interested_in

    if request.form['children_count']:
        children_count= request.form['children_count']
        kwargs_to_pass['children_count']= children_count

    if request.form['married_prev'] != "no_change":
        married_prev= request.form['married_prev']
        kwargs_to_pass['married_prev']= married_prev

    if request.form['criminal'] != "no_change":
        criminal= request.form['criminal']
        kwargs_to_pass['criminal']=criminal

    if request.form['account_opened']!='1000-01-01' :
        account_opened= request.form['account_opened']
        kwargs_to_pass['account_opened']=account_opened

    if request.form['account_closed']!= '1000-01-01':
        account_closed= request.form['account_closed']
        kwargs_to_pass['account_closed']= account_closed
        
    if request.form['status'] != "no_change":
        status= request.form['status']
        kwargs_to_pass['status']= status
    for key in kwargs_to_pass.keys():
        print(key)
    db.update_customer(ssn, **kwargs_to_pass)  # update the customer 

    results= db.return_tuples('Customers')
    return render_template('update_customer.html', results=results)



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


# # views for delete_interest page
@app.route('/delete_interest', methods=['GET'])
def delete_interest_get():
    results= db.return_tuples('Interests')
    return render_template('delete_interest.html', to_delete= results)

@app.route('/delete_interest', methods=['POST'])
def delete_interest_post():
    results= db.return_tuples('Interests')
    interest = request.form['interest']
    db.delete_interest(interest)
    message= "Deletion of interest "+interest+ " has been performed."
    print(message)
    results= db.return_tuples('Interests')
    return render_template('delete_interest.html', msg= message)

# # views for delete_customer page
@app.route('/delete_customer', methods=['GET'])
def delete_customer_get():
    results= db.return_tuples('Customers')
    return render_template('delete_customer.html', to_delete= results)

@app.route('/delete_customer', methods=['POST'])
def delete_customer_post():
    ssn = request.form['customer']
    db.delete_customer(ssn)
    message= "Deletion of person with ssn "+ssn+ " has been performed."
    print(message)
    results= db.return_tuples('Customers')
    return render_template('delete_customer.html', to_delete=results, msg= message)

#     def delete_customer_interest(self, ssn, interest): # delete a customer interest

# # views for delete_customer_interest page
@app.route('/delete_customer_interest', methods=['GET'])
def delete_customer_interest_get():
    results= db.return_tuples('Customer_Interests')
    return render_template('delete_customer_interest.html', to_delete= results)

@app.route('/delete_customer_interest', methods=['POST'])
def delete_customer_interest_post():
    ssn_interest = request.form['customer']
    new_dict= ssn_interest.split('|')
    ssn= new_dict[0]
    interest= new_dict[1]
    db.delete_customer_interest(ssn, interest)
    message= "Deletion tuple of person with ssn "+ssn+ " and interest "+interest + " has been performed."
    print(message)
    results= db.return_tuples('Customer_Interests')
    return render_template('delete_customer_interest.html', to_delete=results, msg= message)

# # # views for delete_customer_child page
@app.route('/delete_customer_child', methods=['GET'])
def delete_customer_child_get():
    results= db.return_tuples('Customers_Children')
    return render_template('delete_customer_child.html', to_delete= results)

@app.route('/delete_customer_child', methods=['POST'])
def delete_customer_child_post():
    full_str = request.form['child']
    new_dict= full_str.split('|')
    ssn= new_dict[0]
    child_num= new_dict[1]
    db.delete_customer_child(ssn, child_num)
    message= "Deletion tuple of child with parent's ssn: "+ssn+ ", and child number>= "+child_num + " has been performed."
    print(message)
    results= db.return_tuples('Customers_Children')
    return render_template('delete_customer_child.html', to_delete=results, msg= message)


# # views for delete_customer_crime page
@app.route('/delete_customer_crime', methods=['GET'])
def delete_customer_crime_get():
    results= db.return_tuples('Customer_Crimes')
    return render_template('delete_customer_crime.html', to_delete= results)

@app.route('/delete_customer_crime', methods=['POST'])
def delete_customer_crime_post():
    ssn = request.form['crime']
    db.delete_customer_crime(ssn)
    message= "Deletion of crime for person with ssn "+ssn+  " has been performed."
    print(message)
    results= db.return_tuples('Customer_Crimes')
    return render_template('delete_customer_crime.html', to_delete=results, msg= message)

# # views for delete_user page
@app.route('/delete_user', methods=['GET'])
def delete_user_get():
    results= db.return_tuples('Users')
    return render_template('delete_user.html', to_delete= results)

@app.route('/delete_user', methods=['POST'])
def delete_user_post():
    username = request.form['user']
    db.delete_user(username)
    message= "Deletion of user with username "+username+  " has been performed."
    print(message)
    results= db.return_tuples('Users')
    return render_template('delete_user.html', to_delete=results, msg= message)

# # views for delete_customer_child page
@app.route('/delete_registration_fee', methods=['GET'])
def delete_registration_fee_get():
    results= db.return_tuples('Registration_Fees')
    return render_template('delete_registration_fee.html', to_delete= results)

@app.route('/delete_registration_fee', methods=['POST'])
def delete_registration_fee_post():
    ssn = request.form['reg']
    db.delete_registration_fee(ssn)
    message= "Deletion of registration fee for person with ssn "+ssn+  " has been performed."
    print(message)
    results= db.return_tuples('Registration_Fees')
    return render_template('delete_registration_fee.html', to_delete=results, msg= message)


# def delete_match_fee(self, ssn, fee_num): # delete a match fee
# def delete_registration_fee(self, ssn): # delete a registration fee



# # views for delete_customer_child page
@app.route('/delete_match_fee', methods=['GET'])
def delete_match_fee_get():
    results= db.return_tuples('Match_Fees')
    return render_template('delete_match_fee.html', to_delete= results)

@app.route('/delete_match_fee', methods=['POST'])
def delete_match_fee_post():
    full_str = request.form['match_fee']
    print(full_str)
    split_str = full_str.split('|')
    ssn = split_str[0]
    fee_num = split_str[1] 
    db.delete_match_fee(ssn, fee_num)
    message= "Deletion of match fee for person with ssn "+ssn+ " and for fee number "+ fee_num+ " has been performed."
    print(message)
    results= db.return_tuples('Match_Fees')
    return render_template('delete_match_fee.html', to_delete=results, msg= message)

# # views for delete_match page
@app.route('/delete_match', methods=['GET'])
def delete_match_get():
    results= db.return_tuples('Matches')
    return render_template('delete_match.html', to_delete= results)

@app.route('/delete_match', methods=['POST'])
def delete_match_post():
    matchID = request.form['match']
    db.delete_match(matchID)
    message= "Deletion of match for matchID "+matchID+  " has been performed."
    print(message)
    results= db.return_tuples('Matches')
    return render_template('delete_match.html', to_delete=results, msg= message)


# # views for delete_date page
@app.route('/delete_date', methods=['GET'])
def delete_date_get():
    results= db.return_tuples('Dates')
    counter=0
    return render_template('delete_date.html', to_delete= results)

@app.route('/delete_date', methods=['POST'])
def delete_date_post():
    full_str = request.form['date']
    split_str = full_str.split('|')
    matchID = split_str[0]
    date_num = int(split_str[1])
    db.delete_date(matchID,date_num)
    message= "Deletion of date for matchID "+matchID+" and date number " +str(date_num)+ " has been performed."
    print(message)
    results= db.return_tuples('Dates')
    return render_template('delete_date.html', to_delete=results, msg= message)



# @app.route('/resources/<path:path>')
# def send_resources(path):
#     return send_from_directory('resources', path)


if __name__ == '__main__':
    app.run()




