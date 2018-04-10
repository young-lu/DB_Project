# original author: Luca Soldaini

import pymysql



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

    def insert_new_user(self, username, password, role ):
        """Search for a venue in the database"""
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = 'INSERT INTO Users (username, password, role) VALUES (%s, %s, %s)'
        result = cur.execute(sql, (username, password, role))
        self.conn.commit()
        return result

    def insert_new_customer(self, ssn, username, DOB, interested_in, phone, age, gender, 
                                children_count, married_prev, account_opened, status): 
        """ account_closed must be added to the database later """
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = 'INSERT INTO Customers (ssn, username, DOB, interested_in, phone, age, gender, \
                children_count, married_prev, account_opened, account_closed, status) \
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,)'
        result = cur.execute(sql, ( ssn, username, DOB, interested_in, phone, age, gender, 
                                children_count, married_prev, account_opened, account_closed, status))
        self.conn.commit()
        return result

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
        # """don't know how to do this yet """


    # def get_match(self):
    #     # """Fetch a veuw from the database"""
    #     # cur = self.conn.cursor(pymysql.cursors.DictCursor)

    #     # cur.execute('SELECT first_name, last_name FROM People ORDER BY time_added;')

    #     # return CursorIterator(cur)

    def get_interests(self):
        """Get comments for a venue"""
        cur = self.conn.cursor(pymysql.cursors.DictCursor)

        cur.execute('SELECT interest, category FROM Interests ORDER BY category;')

        return CursorIterator(cur)

    # def get_user_by_id(self, user_id):
    #     # TODO: implement this in DB
    #     if str(user_id) == '1':
    #         return {'user_id': 1, 'username': 'sean'}
    #     else:
    #         return None

    # def get_user_by_credentials(self, username, password):
    #     # TODO: implement this in DB
    #     if username == 'sean' and password == 'test':
    #         return {'user_id': 1, 'username': 'sean'}
    #     else:
    #         return None
