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

        # ssn = self.ssn
        # first_name= self.first_name
        # last_name= self.last_name
        # username= self.username
        # dob= self.DOB
        # interested_in= self.interested_in
        # phone= self.phone
        # gender= self.gender
        # children_count= self.children_count
        # married_prev= self.married_prev

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
        """Fetch a veuw from the database"""
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        interests = ", ".join('"' + interest + '"' for interest in interests)
        sql = 'SELECT DISTINCT(c.ssn) FROM Customers c, Customer_Interests ci WHERE '
        print("MARRIED PREV".format(married_prev))
        if not married_prev :
            sql += " (c.married_prev = 'N' ) AND "
        sql +=  "c.gender = %s AND "
        sql += " (c.children_count <= %s) AND "
        sql += " c.age >= %s AND c.age <= %s AND "
        sql += " ci.interest IN (%s)"

        cur.execute(sql,(interested_in ,max_kids, min_age,max_age, interests))
        ssn_list = cur.fetchall()
        if not ssn_list:
            return 0

        sql = "SELECT * FROM Customers WHERE "

        i=0
        for ssn in ssn_list:
            sql.append(" ssn= {0} ".format(ssn))
            if(i<len(ssn_list - 1)):
                sql.append(" OR ")
            i+=1
        cur.execute(sql)
        result = cur.fetchall()
        return result

    def get_interests(self):
        """Get comments for a venue"""
        cur = self.conn.cursor(pymysql.cursors.DictCursor)

        cur.execute('SELECT interest, category FROM Interests ORDER BY category;')

        return CursorIterator(cur)

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
