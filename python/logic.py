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

    def insert_new_user(self, username, password, role):
        """Search for a venue in the database"""
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = 'INSERT INTO Users (username, password, role) VALUES (%s, %s, %s)'
        result = cur.execute(sql, (username, password, role))
        self.conn.commit()
        return result

    def insert_new_customer(self, ssn, first_name, last_name, username, DOB, interested_in, phone, gender, 
                                children_count, married_prev): 
        """ account_closed must be added to the database later """
        cur = self.conn.cursor(pymysql.cursors.DictCursor)

        today = datetime.datetime.now().date()
        dob = str(DOB)
        yob = dob.split('-')[0]
        thisyear = datetime.datetime.now().year
        age = int(thisyear) - int(yob)
        age= str(age)
        thisyear

        sql = 'INSERT INTO Customers (ssn, first_name, last_name, username, DOB, interested_in, phone, age, gender, \
                children_count, married_prev, account_opened ) \
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        result = cur.execute(sql, (ssn, first_name, last_name, username, 
                        dob, interested_in, phone, age, gender, children_count, married_prev, today))
        self.conn.commit()
        return result

    def insert_customer_interest(self, ssn, interest):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = 'INSERT INTO Customer_Interests (ssn, interest) VALUES (%s, %s);'
        result = cur.execute(sql, (ssn, interest))
        self.conn.commit()
        return result

    def insert_customer_interests(self, ssn, interest_list):
        for intrst in (interest_list):
            self.insert_customer_interest(ssn, intrst)

    """ update functions --->  what page format should we use? this will affect how we write the function"""
        # def update_user(self, username, password, role): 
        #      cur = self.conn.cursor(pymysql.cursors.DictCursor)
        #     sql = 'UPDATE Users (username, password, role) \
        #             SET (%s, %s, %s, NOW())'
        #     result = cur.execute(sql, (username, password, role))
        #     self.conn.commit()
        #     return result

    def get_people(self):
        """fetch all people from the database"""
        cur = self.conn.cursor(pymysql.cursors.DictCursor)

        cur.execute('SELECT * FROM Users')

        return CursorIterator(cur)
        
    # def update_customer():
        """ show ALL data of customer with option to edit"""
        """ pass every piece of data in update_customer() """


    def find_matches(self,ssn, interested_in, married_prev,max_kids,min_age,max_age,interests):
        """Fetch a view from the database"""
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        interests = ", ".join('"' + interest + '"' for interest in interests)
        # sql = 'SELECT DISTINCT(c.ssn) FROM Customers c, Customer_Interests ci WHERE '
        sql = 'SELECT DISTINCT(ssn) FROM Customers NATURAL JOIN Customer_Interests WHERE '
        if not married_prev :
            print("MARRIED PREV: {0}".format(married_prev))
            sql += " (married_prev = 'N' ) AND "
        sql +=  "(gender = '{0}'') AND ".format(interested_in)
        sql += " (children_count <= {0}) AND ".format(max_kids)
        sql += " (age >= {0} AND age <= {1}) AND ".format(min_age,max_age)
        sql += " (interest IN ({0}))".format(interests)

        cur.execute(sql)
        ssn_list = cur.fetchall()

        if not ssn_list:
            return 0
        print("MATCHES: {0}".format(ssn_list))
        return ssn_list

    def find_exact_matches(self, ssn, interested_in, married_prev,max_kids,min_age,max_age,interests) :
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        interest_string = ", ".join('"' + interest + '"' for interest in interests)
        sql = 'SELECT DISTINCT(ssn) FROM Customers NATURAL JOIN Customer_Interests WHERE '
        if not married_prev :
            sql += " (married_prev = 'N' ) AND "
        sql +=  "(gender = '{0}') AND ".format(interested_in)
        sql += " (children_count <= {0}) AND ".format(max_kids)
        sql += " (age >= {0} AND age <= {1}) AND".format(min_age,max_age)
        sql += " (interest IN ({0})) GROUP BY ssn HAVING COUNT(*) = {1}".format(interest_string,len(interests))
        # print(sql)
        cur.execute(sql)
        ssn_list = cur.fetchall()
        if not ssn_list:
            return 0
        print(sql)
        return ssn_list


    def get_interests(self):
        """Get comments for a venue"""
        cur = self.conn.cursor(pymysql.cursors.DictCursor)

        cur.execute('SELECT interest, category FROM Interests ORDER BY category;')

        return CursorIterator(cur)

    def get_customer_by_ssn(self, ssn) :
        try:
            cur = self.conn.cursor(pymysql.cursors.DictCursor)
            cur.execute('SELECT * FROM Customers WHERE (ssn = "{0}")'.format(ssn))
            result=cur.fetchall()
            return result[0]
        except:
            return 0

    def get_user_by_name(self, username):
        # TODO: implement this in DB
        try:
            cur = self.conn.cursor(pymysql.cursors.DictCursor)
            cur.execute('SELECT * FROM Customers WHERE (username = %s)', username)
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

            

        # if username == 'sean' and password == 'test':
        #     return {'user_id': 1, 'username': 'sean'}
        # else:
        #     return None

    def getquery1(self, num, what_option):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute('SELECT c.* FROM Customers c, Dates d, Matches m WHERE m.matchID= d.matchID'+
                        ' AND c.ssn= m.ssn'+
                        ' GROUP BY m.ssn'+
                        ' HAVING count(*) %s %n', what_option, num)
        result=cur.fetchall()
        return result[0]

    def getquery2(self):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute('SELECT count(*) FROM Customers WHERE married_prev = True')
        result=cur.fetchall()
        return result[0]

    def getquery3(self):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute('SELECT count(*) AS "count", gender FROM Customers GROUP BY gender')
        result=cur.fetchall()

        counter=0
        for count, gender in result:
            if(gender== "M"):
                gender_str= "males"
            else:
                gender_str= "females"
            result_str[counter]= "For " +gender + ", there are "+ count +" people registered. "
            counter+=1

        return result_str

    def getquery4(self):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute('SELECT avg(*) AS "average" , gender FROM Customers c, Dates d, Matches m ' +
                    'WHERE d.matchID = m.matchID AND m.ssn= c.ssn GROUP BY c.gender')
        result=cur.fetchall()

        counter=0
        for average, gender in result:
            if(gender== "M"):
                gender_str= "males"
            else:
                gender_str= "females"
            result_str[counter]= "For " +gender + ", there are an average of "+ average +" date events. "
            counter+=1

        return result_str
        # for each gender, av number of dates

    def getquery5(self):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute('SELECT crime FROM Crimes')
        result=cur.fetchall()
        return result[0]
        

    def getquery6(self):
        # TO DO!!!!: CONNOR HELP HERE PLZ
        return 0

    def getquery7(self):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute('SELECT avg(age) FROM Customers_Children')
        result=cur.fetchall()
        return result[0]

    def getquery8a(self):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute('SELECT avg(count(m.matchID)) FROM Matches m, Customers c WHERE m.ssn= c.ssn '+
                    'AND c.children_count >0 GROUP BY m.ssn')
        result=cur.fetchall()
        return result[0]
    
    def getquery8b(self):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute('SELECT count(*) FROM Dates')
        result=cur.fetchall()
        return result[0]

    def getquery8c(self):
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute('SELECT married_prev FROM Customers WHERE gender="M" '+
                    'GROUP BY married_prev ORDER BY count(*) DESC LIMIT 1')
        result=cur.fetchall()
        return result[0]
