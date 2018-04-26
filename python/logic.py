# original author: Luca Soldaini

import pymysql
import datetime


class CursorIterator(object):
    """Iterator for the cursor object."""

    def __init__(self, cursor):
        """ Instantiate a cursor object"""
        self.__cursor = cursor

    def __iter__(self):
        elem = self.__cursor.fetchone()
        while elem:
            yield elem
            elem = self.__cursor.fetchone()
        self.__cursor.close()

class Database(object):
    """Database object"""

    def __init__(self, opts):
        """Initalize database object"""
        super(Database, self).__init__()
        self.opts = opts
        self.__connect()

    def __connect(self):
        """Connect to the database"""
        self.conn = pymysql.connect(self.opts.DB_HOST, self.opts.DB_USER,
                                    self.opts.DB_PASSWORD, self.opts.DB_NAME)

    def insert_user(self, username, password, role):
        """Search for a venue in the database"""
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = 'INSERT INTO Users (username, password, role) VALUES (%s, %s, %s)' 
        result = cur.execute(sql, (username, password, role))
        self.conn.commit()
        return result

    def insert_role(self,role):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = 'INSERT INTO Roles (role) VALUES ("{0}")'.format(role)
        print(sql)
        result = cur.execute(sql)
        self.conn.commit()
        return result


    def insert_customer(self, ssn, first_name, last_name, username, DOB, interested_in, phone,
                    gender, eye_color, hair_color, children_count, married_prev): 
        """ account_closed must be added to the database later """
        cur = self.conn.cursor(pymysql.cursors.DictCursor)

        today = datetime.datetime.now().date()
        dob = str(DOB)
        yob = dob.split('-')[0]
        thisyear = datetime.datetime.now().year
        age = int(thisyear) - int(yob)
        age= str(age)

        sql = 'INSERT INTO Customers (ssn, first_name, last_name, username, DOB, interested_in, phone, age, gender, \
                children_count, married_prev, account_opened, eye_color, hair_color ) \
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        print(sql)
        result = cur.execute(sql, (ssn, first_name, last_name, username, 
                        dob, interested_in, phone, age, gender, children_count, married_prev, today, eye_color, hair_color))
        self.conn.commit()
        return result
        
    def insert_customer_interest(self, ssn, interest):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = 'INSERT INTO Customer_Interests (ssn, interest) VALUES (%s, %s);'
        result = cur.execute(sql, (ssn, interest))
        self.conn.commit()
        return result

    def insert_match(self, ssn1, ssn2, matchID) :
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql1 = 'INSERT INTO Matches (matchID, ssn) VALUES ("{0}","{1}")'.format(matchID,ssn1)
        sql2 = 'INSERT INTO Matches (matchID, ssn) VALUES ("{0}","{1}")'.format(matchID,ssn2)
        # print('INSERT MATCH SQL1: {0}'.format(sql1))
        # print('INSERT MATCH SQL2: {0}'.format(sql2))
        try :
            result = cur.execute(sql1)
            self.conn.commit()
            result += cur.execute(sql2)
            self.conn.commit()
            return result
        except:
            print('ERROR INSERTING MATCH')
            return 0

    def insert_date(self, date_time, date_date, location, matchID) :
        cur = self.conn.cursor(pymysql.cursors.DictCursor)

        sql = 'SELECT MAX(date_number) FROM Dates WHERE matchID = "{0}"'.format(matchID)
        print(sql)
        cur.execute(sql)
        try :
            date_num = (int(cur.fetchall()[0]['MAX(date_number)']) + 1)
        except:
            print('except')
            date_num = 1

        sql = 'INSERT INTO Dates (date_number, date_time, date_date, location, matchID) \
                VALUES ("{0}", "{1}", "{2}", "{3}", "{4}")'.format(date_num,date_time,date_date,location, matchID)
        print(sql)
        result = cur.execute(sql)
        self.conn.commit()
        return result

    def insert_crime(self, crime) :
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = 'INSERT INTO Crimes (crime) VALUES ("{0}")'.format(crime)
        print(sql)
        result = cur.execute(sql)
        self.conn.commit()
        return result


# BEGIN THE STATEMENTS FOR DELETION
    def delete_user(self, username): # delete a user
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = 'DELETE FROM Users WHERE username = %s'
        cur.execute(sql, (username))
        self.conn.commit()
        return 1

    def delete_customer(self, ssn):  # delete a customer 
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = 'DELETE FROM Customers WHERE ssn = %s'
        cur.execute(sql, (ssn))
        self.conn.commit()
        return 1
        
    def delete_customer_interest(self, ssn, interest): # delete a customer interest
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = 'DELETE FROM Customer_Interests WHERE ssn=%s AND interest= %s'
        cur.execute(sql, (ssn, interest))
        self.conn.commit()
        return 1

    def delete_customer_crime(self, ssn): # delete a customer crime
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = 'DELETE FROM Customer_Crimes WHERE ssn=%s'
        cur.execute(sql, (ssn))
        self.conn.commit()
        # RE OPEN THE CLIENTS ACCOUNT!!
        status='open'
        criminal= 'N'
        null = 'NULL'
        sql = 'UPDATE Customers SET account_closed= NULL WHERE ssn=%s'
        cur.execute(sql, (ssn))
        self.conn.commit()
        sql='UPDATE Customers  SET status = %s WHERE ssn=%s'
        cur.execute(sql, (ssn, status))
        self.conn.commit()
        sql='UPDATE Customers SET criminal=%s WHERE ssn=%s '
        cur.execute(sql, (ssn, criminal))
        self.conn.commit()
        return 1

    def delete_interest(self, interest): # delete an interest
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = 'DELETE FROM Interests WHERE interest= %s'
        cur.execute(sql, (interest))
        self.conn.commit()
        return 1

    def delete_match(self, matchID): # delete a match
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = 'DELETE FROM Matches WHERE matchID= %s'
        result = cur.execute(sql, (matchID))
        self.conn.commit()
        return 1
    
    def delete_date(self, matchID, date_number): # delete a date
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = 'DELETE FROM Dates WHERE date_number= ' + str(date_number)+ ' AND matchID= %s'
        cur.execute(sql, matchID)
        self.conn.commit()
        return 1

    def delete_customer_child(self, ssn, child_num): # delete a customer's child-- this will also delete all children that come after that one (aka with childID>= child_num)
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = 'DELETE FROM Customers_Children WHERE ssn= %s AND childID>= ' + str(child_num)
        print(sql)
        cur.execute(sql, (ssn))
        self.conn.commit()
        return 1
    
    def delete_match_fee(self, ssn, fee_num): # delete a match fee
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = 'DELETE FROM Match_Fees WHERE ssn = %s AND fee_number= ' +str(fee_num)
        cur.execute(sql, (ssn))
        self.conn.commit()
        return 1

    def delete_registration_fee(self, ssn): # delete a registration fee
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = 'DELETE FROM Registration_Fees WHERE ssn = %s'
        cur.execute(sql, (ssn))
        self.conn.commit()
        return 1
    # END THE STATEMENTS FOR DELETION

    # BEGIN THE STATEMENTS FOR INSERTION
    # already have some for inserting: user, customer, customer-interest, match, date + DONT NEED ONE FOR : registration + match fees b/c they're already triggered
    def insert_customer_crime(self, ssn, crime ): # insert a customer crime-- ssn, crime, date_recorded--> defaults to current_date( no need to add it in!)
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        today = datetime.datetime.now().date()
        sql = 'INSERT INTO Customer_Crimes(ssn, crime, date_recorded) VALUES ("{0}", "{1}", "{2}")'.format(ssn, crime, today)
        print(sql)
        result = cur.execute(sql)
        self.conn.commit()
        # RE OPEN THE CLIENTS ACCOUNT!!
        # status='open'
        # criminal= 'N'
        # sql = 'UPDATE Customers WHERE ssn=%s SET account_closed=NULL AND status = %s AND criminal=%s'
        # cur.execute(sql, (ssn, status, criminal))
        # self.conn.commit()
        return result

    def insert_interest(self, interest, category): # insert an interest
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = 'INSERT INTO Interests (interest, category) VALUES (%s, %s)'
        cur.execute(sql, (interest, category))
        self.conn.commit()
        return 1

    def insert_customer_child(self, ssn, child_num): # delete a customer's child-- this will also delete all children that come after that one (aka with childID>= child_num)
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = 'DELETE FROM Customers_Children WHERE ssn= %s AND childID>= %d'
        cur.execute(sql, (ssn, child_num))
        self.conn.commit()
        return 1
# END THE STATEMENTS FOR INSERTION


# BEGIN THE STATEMENTS FOR UPDATE
    # basically these will be passed parameters by kwargs
    # example: update_user ( "snf34", username= "sara") would just update the username of the previous username "sara"
    def update_user(self, username, **kwargs): # update a user
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql_base = 'UPDATE Users WHERE username = %s '
        if kwargs['password']:
            sql= sql_base+ ' SET password= %s'
            cur.execute(sql, (username, kwargs['password']))
            self.conn.commit()
        if kwargs['role']:
            sql= sql_base+ ' SET role= %s'
            cur.execute(sql, (username, kwargs['role']))
            self.conn.commit()
        return 1

    def show_tables(self):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute('Show tables;')
        result = cur.fetchall()
        results = []
        for each in range(len(result)) :
            results.append(result[each]['Tables_in_dating_site_project'])
        return results


    def add_child(self, ssn, age, at_home, childid) :
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = 'UPDATE Customers SET children_count = "{1}" WHERE ssn = "{0}"'.format(ssn, childid)
        cur.execute(sql)
        self.conn.commit()
        print('id:')
        print(childid)

        sql = 'INSERT INTO Customers_Children (ssn, childID, age, lives_with_them) VALUES ("{0}", "{1}", "{2}", "{3}")'.format(ssn, childid, age, at_home)
        result = cur.execute(sql)
        self.conn.commit()
        return result

    def get_children_count(self, ssn):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute('SELECT count(*) from Customers_Children where ssn="{0}"'.format(ssn))
        result =cur.fetchall()[0]['count(*)']
        print(result)
        return result


    def update_customer(self, ssn, **kwargs):  # update a customer 
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql_base = 'UPDATE Customers '
        basept2= '  WHERE ssn = %s'
        if 'username' in kwargs.keys():
            # get old username 
            sql="SELECT username FROM Customers WHERE ssn = %s"
            cur.execute(sql, ssn)
            result= cur.fetchall()
            username= result[0]['username']
            # and change the users table with that username too
            sql1= 'UPDATE Users SET username = %s WHERE username = %s'
            cur.execute(sql1, (kwargs['username'], username))
            self.conn.commit()
        if 'first_name' in kwargs.keys():
            sql= sql_base+ ' SET first_name= %s'+basept2
            cur.execute(sql, ( kwargs['first_name'], ssn))
            self.conn.commit()
        if 'last_name' in kwargs.keys():
            sql= sql_base+ ' SET last_name= %s'+basept2
            cur.execute(sql, (kwargs['last_name'], ssn))
            self.conn.commit()
        if 'DOB' in kwargs.keys():
            sql=sql_base+ ' SET DOB= %s'+basept2
            cur.execute(sql, (kwargs['DOB'], ssn))
            self.conn.commit()
        if 'interested_in' in kwargs.keys():
            sql= sql_base+ ' SET interested_in= %s'+basept2
            cur.execute(sql, (kwargs['interested_in'], ssn))
            self.conn.commit()
        if 'phone' in kwargs.keys():
            sql= sql_base+ ' SET phone= %s'+basept2
            cur.execute(sql, ( kwargs['phone'], ssn))
            self.conn.commit()
        if 'age' in kwargs.keys():
            sql= sql_base+ ' SET age= '+str(kwargs['age'])+basept2
            cur.execute(sql, (ssn))
            self.conn.commit()
        if 'gender' in kwargs.keys():
            sql= sql_base+ ' SET gender= %s'+basept2
            cur.execute(sql, (kwargs['gender'], ssn))
            self.conn.commit()
        if 'children_count' in kwargs.keys():
            sql= sql_base+ ' SET children_count= '+str(kwargs['children_count'])+basept2
            cur.execute(sql, (ssn))
            self.conn.commit()
        if 'married_prev' in kwargs.keys():
            sql= sql_base+ ' SET married_prev= %s'+basept2
            cur.execute(sql, (kwargs['married_prev'], ssn))
            self.conn.commit()
        if 'criminal' in kwargs.keys():
            sql= sql_base+ ' SET criminal= %s'+basept2
            cur.execute(sql, (kwargs['criminal'], ssn))
            self.conn.commit()
        if 'account_opened' in kwargs.keys():
            sql= sql_base+ ' SET account_opened= %s'+basept2
            cur.execute(sql, (kwargs['account_opened'], ssn))
            self.conn.commit()
        if 'account_closed' in kwargs.keys():
            sql= sql_base+ ' SET account_closed= %s'+basept2
            cur.execute(sql, (kwargs['account_closed'], ssn))
            self.conn.commit()
        if 'status' in kwargs.keys():
            sql= sql_base+ ' SET status= %s'+basept2
            cur.execute(sql, (kwargs['status'], ssn))
            self.conn.commit()
        if 'eye_color' in kwargs.keys():
            sql= sql_base+ ' SET status= %s'+basept2
            cur.execute(sql,  (kwargs['eye_color'], ssn))
            self.conn.commit()
        if 'hair_color' in kwargs.keys():
            sql= sql_base+ ' SET status= %s'+basept2
            cur.execute(sql, (kwargs['hair_color'], ssn))
            self.conn.commit()
        return 1

    # def update_customer_interest(self, ssn, interest, new_interest): # update a customer interest
    #     cur = self.conn.cursor(pymysql.cursors.DictCursor)
    #     sql = 'UPDATE Customer_Interests WHERE ssn=%s AND interest= %s SET interest=%s'
    #     cur.execute(sql, (ssn, interest, new_interest))
    #     self.conn.commit()
    #     return 1

    def update_customer_crime(self, ssn, **kwargs): # update a customer crime
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql_base = 'UPDATE Customer_Crimes '
        sql_pt2 =' WHERE ssn = %s'
        if 'crime' in kwargs.keys():
            sql= sql_base+ ' SET crime= %s ' +sql_pt2
            cur.execute(sql, (kwargs['crime'], ssn))
            self.conn.commit()
        if 'date_recorded' in kwargs.keys():
            sql= sql_base+ ' SET date_recorded= %s' +sql_pt2
            cur.execute(sql, (kwargs['date_recorded'], ssn))
            self.conn.commit()
        return 1

    def update_customer_children(self, ssn, childID, **kwargs): # update a customer's child
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql_base = 'UPDATE Customers_Children '
        sql_pt2 =' WHERE ssn = %s AND childID= ' +childID
        if 'age' in kwargs.keys():
            sql= sql_base+ ' SET age= ' +str(kwargs['age']) +sql_pt2
            cur.execute(sql, ssn)
            self.conn.commit()
        if 'lives_with_them' in kwargs.keys():
            sql= sql_base+ ' SET lives_with_them= %s ' +sql_pt2
            cur.execute(sql, (kwargs['lives_with_them'], ssn))
            self.conn.commit()
        
        return 1

    def update_date(self, matchID, date_number, **kwargs): # update a date
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql_base = 'UPDATE Dates '
        sql_pt2= ' WHERE matchID= %s AND date_number= ' + str(date_number)
        
        if 'date_date' in kwargs.keys():
            sql= sql_base + ' SET date_date= %s'+ sql_pt2
            cur.execute(sql, (kwargs['date_date'], matchID))
            self.conn.commit()

        if 'happened' in kwargs.keys():
            sql= sql_base + ' SET happened= %s'+ sql_pt2
            cur.execute(sql, (kwargs['happened'], matchID))
            self.conn.commit()

        if 'location' in kwargs.keys():
            sql= sql_base + ' SET location= %s' + sql_pt2
            cur.execute(sql, (kwargs['location'], matchID))
            self.conn.commit()
        return 1

    def update_match_fee(self, ssn, fee_num, **kwargs): # update a match fee
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql_base = 'UPDATE Match_Fees '
        sql_pt2= ' WHERE ssn = %s AND fee_number= ' + str(fee_num)
        if 'amount' in kwargs.keys():
            sql= sql_base + ' SET amount= %s' +sql_pt2
            cur.execute(sql, (kwargs['amount'], ssn)) 
            self.conn.commit()
        if 'date_charged' in kwargs.keys():
            sql= sql_base + ' SET date_charged= %s' +sql_pt2
            cur.execute(sql, (kwargs['date_charged'], ssn))
            self.conn.commit()
        if 'paid' in kwargs.keys():
            sql= sql_base + ' SET paid= %s' +sql_pt2
            cur.execute(sql, (kwargs['paid'], ssn))
            self.conn.commit()
        if 'date_paid' in kwargs.keys():
            sql= sql_base + ' SET date_paid= %s' +sql_pt2
            cur.execute(sql, (kwargs['date_paid'], ssn))
            self.conn.commit()    
        return 1

    def update_registration_fee(self, ssn, **kwargs): # update a registration fee
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql_base = 'UPDATE Registration_Fees '
        sql_pt2 = ' WHERE ssn = %s '
        if 'amount' in kwargs.keys():
            sql= sql_base + ' SET amount= %s' +sql_pt2
            cur.execute(sql, (kwargs['amount'], ssn))
            self.conn.commit()
        if 'date_charged' in kwargs.keys():
            sql= sql_base + ' SET date_charged= %s' +sql_pt2
            cur.execute(sql, (kwargs['date_charged'], ssn))
            self.conn.commit()
        if 'paid' in kwargs.keys():
            sql= sql_base + ' SET paid= %s' +sql_pt2
            cur.execute(sql, (kwargs['paid'], ssn))
            self.conn.commit()
        if 'date_paid' in kwargs.keys():
            sql= sql_base + ' SET date_paid= %s' +sql_pt2
            cur.execute(sql, (kwargs['date_paid'], ssn))
            self.conn.commit()    
        return 1

# END THE STATEMENTS FOR UPDATE


# BEGIN THE STATEMENTS FOR CHECKING DATA!! -- THESE WILL RETURN "no error" or the error message
    # check a date:
    def check_date(self, date_check):
        year= int(date_check[0:3])
        dash1= date_check[4]
        month= int(date_check[5:6])
        dash2= date_check[7]
        day= int(date_check[8:9])
        if 1900<=year<=2018 and dash1== "-" and dash2== "-" and  0<month<=12 and  0<day<=31:
            error_msg= "no error"
        else:
            error_msg= "The date " + str(date_check) + " is not a valid date for entry."
        return error_msg

    # check a number:
    def check_number(self, num_check):
        if(num_check >= 0):
            error_msg= "no error"
        else:
            error_msg= "The number " + str(num_check) + " is not a valid number for entry."
        return error_msg

    # check an ssn to make sure it doesn't already exist
    def check_ssn(self, ssn_check):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql= 'SELECT ssn FROM Customers'
        cur.execute(sql)
        for ssn in results:
            if(ssn_check == ssn):
                error_msg = "The ssn " + ssn_check + " is already in the database."
        self.conn.commit()
        return error_msg


# END THE STATEMENTS FOR CHECKING DATA!!

    def get_users(self):
        """fetch all people from the database"""
        cur = self.conn.cursor(pymysql.cursors.DictCursor)

        cur.execute('SELECT * FROM Users')

        result = CursorIterator(cur)
        print(result)
        return result
        
    def get_all_matches(self) :
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute('select distinct(d.matchid) as id, m.ssn as ssn1, n.ssn as ssn2 from dates d, matches m, matches n where d.matchId = m.matchid and d.matchid = n.matchid and m.ssn != n.ssn')
        # cur.execute('select * from dates d, matches m, matches n where d.matchId = m.matchid and d.matchid = n.matchid and m.ssn != n.ssn')
        result = cur.fetchall()
        result = result[1::2]
        return result

    def get_all_date_pairs(self) :
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute('select d.happened as happened, d.date_number as DateNumber, d.matchid as MatchID, d.location as location, d.date_date as date_date, d.date_time as time, m.ssn as ssn1, n.ssn as ssn2 from Dates d, matches m, matches n where d.matchid = m.matchid and d.matchid = n.matchid and m.ssn != n.ssn order by matchid, date_number')
        result = cur.fetchall()
        result=result[1::2]
        return result

    # def update_customer():
        """ show ALL data of customer with option to edit"""
        """ pass every piece of data in update_customer() """

    def find_matches(self,ssn, interested_in, married_prev,max_kids,min_age,max_age,interests, eye_color, hair_color):
        """Fetch a view from the database"""
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        interests = ", ".join('"' + interest + '"' for interest in interests)
        # sql = 'SELECT DISTINCT(c.ssn) FROM Customers c, Customer_Interests ci WHERE '
        sql = 'SELECT DISTINCT(ssn) FROM Customers NATURAL JOIN Customer_Interests WHERE status = "Open" AND ssn != "{0}" AND'.format(ssn)
        if not married_prev :
            sql += " (married_prev = 'N' ) AND "
        if eye_color != 'any':
            sql += " (eye_color = '{0}' ) AND ".format(eye_color)
        if hair_color != 'any':
            sql += " (hair_color = '{0}' ) AND ".format(hair_color)

        sql += " (gender = '{0}') AND ".format(interested_in)
        sql += " (children_count <= {0}) AND ".format(max_kids)
        sql += " (age >= {0} AND age <= {1}) AND ".format(min_age,max_age)
        sql += " (interest IN ({0}))".format(interests)
        print(sql)
        cur.execute(sql)
        ssn_list = cur.fetchall()

        if not ssn_list:
            return 0
        return ssn_list

# TEST THIS 
    def find_exact_matches(self, ssn, interested_in, married_prev,max_kids,min_age,max_age,interests,eye_color, hair_color) :
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        interest_string = ", ".join('"' + interest + '"' for interest in interests)
        sql = 'SELECT DISTINCT(ssn) FROM Customers NATURAL JOIN Customer_Interests WHERE status = "Open" AND ssn != "{0}" AND'.format(ssn)
        if not married_prev :
            sql += " (married_prev = 'N' ) AND "
        if eye_color != 'any':
            sql += " (eye_color = '{0}' ) AND ".format(eye_color)
        if hair_color != 'any':
            sql += " (hair_color = '{0}' ) AND ".format(hair_color)

        sql += " (gender = '{0}') AND ".format(interested_in)
        sql += " (children_count <= {0}) AND ".format(max_kids)
        sql += " (age >= {0} AND age <= {1}) AND".format(min_age,max_age)
        sql += " (interest IN ({0})) GROUP BY ssn HAVING COUNT(*) = {1}".format(interest_string,len(interests))
        # print(sql)
        cur.execute(sql)
        ssn_list = cur.fetchall()
        if not ssn_list:
            return 0
        # print("EXACT MATCHES: {0}".format(sql))
        return ssn_list


    def get_interests(self):
        """Get comments for a venue"""
        cur = self.conn.cursor(pymysql.cursors.DictCursor)

        cur.execute('SELECT interest, category FROM Interests ORDER BY category;')

        result=cur.fetchall()
        return result

    def get_customer_by_ssn(self, ssn) :
        try:
            cur = self.conn.cursor(pymysql.cursors.DictCursor)
            cur.execute('SELECT * FROM Customers WHERE (ssn = "{0}")'.format(ssn))
            result=cur.fetchall()
            return result[0]
        except:
            return 0


    def get_matches_by_ssn(self, ssn) :
        """ return ssn's of matches of ssn """
        try :
            cur = self.conn.cursor(pymysql.cursors.DictCursor)
            # sql = 'SELECT distinct(matchID) FROM Matches WHERE ssn= "{0}"'.format(ssn)
            sql = 'select * from matches m, customers c WHERE m.ssn = c.ssn and m.matchid in (Select matchID from matches where ssn = "{0}") and m.ssn != "{0}"'.format(ssn)
            cur.execute(sql)
            result = cur.fetchall()
            return result
        except:
            print('ERROR: get_matches_by_ssn()')
            return 0

    def get_dates(self, ssn) :
        try :
            cur = self.conn.cursor(pymysql.cursors.DictCursor)
            sql = 'SELECT * FROM  matches m, customers c, dates d WHERE m.matchid = d.matchid AND \
                    m.matchid IN (SELECT matchid FROM Matches WHERE ssn = "{0}") AND c.ssn = m.ssn AND m.ssn != "{0}" ORDER BY d.date_date'.format( ssn)
            cur.execute(sql)
            result = cur.fetchall()
            # print(result)
            return result
        except :
            print('ERROR: get_dates_by_ssn()')
            return 0



    def get_all_customers(self) :
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = 'SELECT * FROM Customers'
        cur.execute(sql)
        result = cur.fetchall()
        return result

    def get_all_crimes(self) :
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = 'SELECT * FROM Crimes'
        cur.execute(sql)
        results = cur.fetchall()
        result=[]
        for each in results:
            result.append(each['crime'])
        # print (result)
        return result


    def get_customers_by_match_id(self, matchID) :
        
        try :
            cur = self.conn.cursor(pymysql.cursors.DictCursor)
            sql = 'SELECT DISTINCT(ssn) FROM Matches WHERE matchID= "{0}"'.format(matchID)
            cur.execute(sql)
            result = cur.fetchall()
            return result
        except :
            print('ERROR get_customers_by_id()')
            return 0


    def get_match_id(self, ssn1, ssn2) :
        """ return match_ID for match between ssn1 and ssn2 """
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = 'select m.ssn, n.ssn from matches m, matches n where m.ssn = "{0}" and n.ssn = "{1}" and m.matchid = n.matchid'.format(ssn1,ssn2)
        cur.execute(sql)
        result = cur.fetchall()[0]
        return result

    def get_customer_by_name(self, username):
        # TODO: implement this in DB
        try:
            cur = self.conn.cursor(pymysql.cursors.DictCursor)
            cur.execute('SELECT * FROM Customers natural join Users WHERE (username = %s)', username)
            result=cur.fetchall()
            return result[0]
        except:
            return 0

    def get_user_by_name(self, username):
        # TODO: implement this in DB
        try:
            cur = self.conn.cursor(pymysql.cursors.DictCursor)
            cur.execute('SELECT * FROM Users WHERE (username = "{0}")'.format(username))
            result=cur.fetchall()
            return result[0]
        except:
            return 0

    def get_user_by_credentials(self, username, password,role):
        # TODO: implement this in DB
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql1 = 'SELECT * FROM users WHERE (username = %s and password= %s and role= %s)'
        cur.execute(sql1, (username, password, role))
        result = cur.fetchall()

        try:
            username = (result[0]['username'])
            password = result[0]['password']
            role = result[0]['role']
            return 1
        except: 
            return 0

    def get_user_role(self, username):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql1 = 'SELECT role FROM Users WHERE (username = %s)'
        cur.execute(sql1, (username))
        result = cur.fetchall()
        invalid="This username was not in the DB."

        try:
            role = result[0]['role']
            return role
        except: 
            return invalid

    def get_largest_matchID(self) :
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = 'SELECT MAX(matchID) FROM Matches'
        try:
            cur.execute(sql)
            result = cur.fetchall()
            result = result[0]['MAX(matchID)']
        except:
            print('error getting largest matchID')
            result = 0

        if not result :
            return 0
        else:
            return result

    def submit_date(self, ssn, success, matchid, date_num) :
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        try :
            sql = 'INSERT INTO DateSuccess (matchid,ssn, success, date_number) VALUES("{0}", "{1}", "{2}", "{3}")'.format(matchid,ssn, success,date_num)
            cur.execute(sql)
            self.conn.commit()
            sql = 'UPDATE Dates SET happened="Y" WHERE matchID= "{0}" AND date_number= "{1}"'.format(matchid,date_num)
            result = cur.execute(sql)
            self.conn.commit()
            return result
        except:
            print('ERROR: submit_date()')
            return 0

    def insert_new_match(self, ssn1, ssn2, matchID) :
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql1 = 'INSERT INTO Matches (matchID, ssn) VALUES ("{0}","{1}")'.format(matchID,ssn1)
        sql2 = 'INSERT INTO Matches (matchID, ssn) VALUES ("{0}","{1}")'.format(matchID,ssn2)
        print('INSERT MATCH SQL1: {0}'.format(sql1))
        print('INSERT MATCH SQL2: {0}'.format(sql2))

        try :
            result = cur.execute(sql1)
            result += cur.execute(sql2)
            self.conn.commit()
            return result
        except:
            print('ERROR INSERTING MATCH')
            return 0

    def insert_new_date(self, date_time, date_date, location, matchID) :
        cur = self.conn.cursor(pymysql.cursors.DictCursor)

        sql = 'SELECT MAX(date_number) FROM Dates WHERE matchID = "{0}"'.format(matchID)
        cur.execute(sql)
        # print(cur.fetchall()[0]['MAX(date_number)'])
        try :
            date_num = int(cur.fetchall()[0]['MAX(date_number)']) + 1
        except:
            date_num = 1

        sql = 'INSERT INTO Dates (date_number, date_time, date_date, location, matchID) \
                VALUES ("{0}", "{1}", "{2}", "{3}", "{4}")'.format(date_num,date_time,date_date,location, matchID)
        # print(sql)
        result = cur.execute(sql)
        self.conn.commit()
        return result

######### GET TUPLES FUNCTION ####### 
# will take argument of table name
    def return_tuples(self, table_name):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql= 'SELECT * FROM '+ table_name
        cur.execute(sql)
        results = cur.fetchall()
        return results

    def getquery1(self, username, num, what_option):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute('SELECT c.* FROM Customers c, Dates d, Matches m WHERE m.matchID= d.matchID'+
                        ' AND c.ssn= m.ssn'+
                        ' GROUP BY m.ssn'+
                        ' HAVING count(*) %s %n', what_option, num)
        result= cur.fetchall()
        counter=0
        if get_user_role(username) == 'Entry-level':
            counter=0
            for (ssn, username, first_name, last_name, DOB, interested_in, phone, age, gender, 
            children_count, married_prev, criminal) in result:
                result_str[counter] = (first_name +" " +last_name + " whose birthday is " + DOB + " is interested in " +interested_in+
                ", is " + age + " years old " + ", and is of gender " + gender +".")
            counter+= 1
        else:
            counter=0
            for (ssn, username, first_name, last_name, DOB, interested_in, phone, age, gender, 
            children_count, married_prev, criminal) in result:
                result_str[counter] = (first_name +" " +last_name + " whose birthday is " + DOB + " is interested in " +interested_in+
                ", is " + age + " years old " + ", and is of gender " + gender +". Their ssn is " +ssn + " and their phone # is " + phone)
                counter+= 1

        result=cur.fetchall()
        return result_str

    def getquery2(self, username):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute('SELECT count(*) AS ct FROM Customers WHERE married_prev = %s', 'Y')
        result=cur.fetchall()
        result_str= ("The total number of customers that were previously married that are in the DB is " + 
                    str(result[0]['ct']) + " people.")
        return result_str

    def getquery3(self, username):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute('SELECT gender, count(*) AS ct FROM Customers GROUP BY gender')
        result=cur.fetchall()
        result_str=""
        print(result)
        counter=0
        for gender in result:
            gender= result[counter]['gender']
            if str(gender)== "M":
                gender_str= "males"
            elif str(gender) =="F":
                gender_str= "females"
            result_str+= "For " + gender_str + ", there are "+ str(result[counter]['ct']) +" people registered. "
            counter+=1

        return result_str

    def getquery4(self, username):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute('SELECT  temp.gender AS gender, avg(temp.counter) AS average FROM (SELECT COUNT(*) AS counter, c.gender AS gender FROM Customers c, Dates d, Matches m WHERE d.matchID = m.matchID AND m.ssn= c.ssn GROUP BY c.gender)  as temp GROUP BY temp.gender')
        result=cur.fetchall()

        counter=0
        result_str="None"
        for gender in result:
            gender= result[counter]['gender']
            if str(gender)== "M":
                gender_str= "males"
            elif str(gender) =="F":
                gender_str= "females"
            average= result[counter]['average']
            result_str+= "For " + gender_str + ", there are an average of "+ str(average) +" date events. \n"

            counter+=1

        return result_str
        # for each gender, avg number of dates

        # 
        # 
        # 
        # 
        # Do we need the username as an argument on ANY of these???
        # 
        # 
        # 
        # 

    def getquery5(self, username):
        count=0
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute('SELECT DISTINCT(crime) FROM Customer_Crimes')
        result=cur.fetchall()
        result_str=""
        for crime in result:
            if count==0:
                result_str= str(result[count]['crime'])
            else:
                result_str+= ", " + str(result[count]['crime'])
            count+=1
        result_return = "These are the crimes in the DB that have been recorded for customers: "+ result_str
        return result_return

    def getquery6(self, sql):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)

        cur.execute(sql)

        result = cur.fetchall()
        
        return result

    def getquery7(self, username):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute('SELECT avg(age) AS average FROM Customers_Children')
        result=cur.fetchall()
        answer= result[0]['average']
        ans=answer
        if str(answer)=='None':
            ans='NA (no children in DB at the moment)'

        result_str= "The average age of the customers' children in the DB is "+ str(ans) +"."
        return result_str

    def getquery8a(self, username):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute('SELECT avg(ct) AS average FROM (SELECT COUNT(m.matchID) AS ct FROM Matches m, Customers c WHERE m.ssn= c.ssn '+
                    'AND c.children_count >0 GROUP BY m.ssn) AS Derived_tab')
        result=cur.fetchall()

        result_str= "There are on average " + str(result[0]['average']) + " match(es) for users who have one or more children."
        return result_str
    
    def getquery8b(self, username):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute('SELECT count(*) AS count FROM Dates')
        result=cur.fetchall()

        result_str= "There have been "+str(result[0]['count'])+ " total dates for this dating site."
        return result_str

    def getquery8c(self, username):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)

        cur.execute('SELECT married_prev FROM Customers WHERE gender="M" '+
                    'GROUP BY married_prev ORDER BY count(*) DESC LIMIT 1')

        result=cur.fetchall()
        if(result[0]['married_prev']== "Y"):
            mar_status= " previously married."
        else:
            mar_status= " not previously married."
        result_str = "The most common marital status amongst men is " +mar_status

        return result_str

    def getquery8d(self):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)

        cur.execute('SELECT married_prev FROM Customers WHERE gender="F" '+
                    'GROUP BY married_prev ORDER BY count(*) DESC LIMIT 1')

        result=cur.fetchall()
        if(result[0]['married_prev']== "Y"):
            mar_status= " previously married."
        else:
            mar_status= " not previously married."
        result_str = "The most common marital status amongst women is " +mar_status

        return result_str
 
    def getquery8e(self): # least common interest in DB
        cur = self.conn.cursor(pymysql.cursors.DictCursor)

        cur.execute('SELECT interest FROM Customer_Interests GROUP BY interest ORDER BY count(*) ASC LIMIT 1')
        result=cur.fetchall()
        least_common= result[0]['interest']
        sql= 'SELECT interest FROM Customer_Interests GROUP BY interest HAVING count(*)= (SELECT count(*) AS ct FROM Customer_Interests WHERE interest= %s)'
        cur.execute(sql, least_common)
        result=cur.fetchall()
        counter=0
        least_common_list=""
        for thing in result:
            if counter!=0:
                least_common_list+= ", "+ str(result[counter]['interest'])
            else:
                least_common_list+= str(result[counter]['interest'])
            counter+=1
        result_str = "The most common interest(s) amongst interests chosen by the users is: " +least_common_list +"."

        return result_str

    def getquery8f(self): # most common interest in DB
        cur = self.conn.cursor(pymysql.cursors.DictCursor)

        cur.execute('SELECT interest FROM Customer_Interests GROUP BY interest ORDER BY count(*) DESC LIMIT 1')
        result=cur.fetchall()
        most_common= result[0]['interest']
        sql= 'SELECT interest FROM Customer_Interests GROUP BY interest HAVING count(*)= (SELECT count(*) AS ct FROM Customer_Interests WHERE interest= %s)'
        cur.execute(sql, most_common)
        result=cur.fetchall()
        counter=0
        most_common_list=""
        for thing in result:
            if counter!=0:
                most_common_list+= ", "+ str(result[counter]['interest'])
            else:
                most_common_list+= str(result[counter]['interest'])
            counter+=1
        result_str = "The most common interest(s) amongst interests chosen by the users is: " +most_common_list +"."
        return result_str

    """ update functions --->  what page format should we use? this will affect how we write the function"""
        # def update_user(self, username, password, role): 
        #      cur = self.conn.cursor(pymysql.cursors.DictCursor)
        #     sql = 'UPDATE Users (username, password, role) \
        #             SET (%s, %s, %s, NOW())'
        #     result = cur.execute(sql, (username, password, role))
        #     self.conn.commit()
        #     return result

    # def getquery9(self, username):
    #    cur = self.conn.cursor(pymysql.cursors.DictCursor)
    #    cur.execute('SELECT count(*) FROM Dates')
    #    result=cur.fetchall()
    #    result_str= "There have been "+result[0]+ " total dates for this dating site."
    #    return result_str



