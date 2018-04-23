# ACTUAL DATA
#Roles --> role VARCHAR(40)
#Users --> username VARCHAR(40), password VARCHAR(40), role references role in Roles
#Customers --> ssn VARCHAR(40), username VARCHAR(40), DOB DATE, interested_in CHAR(1),
			 # phone# char(10), age INT, gender CHAR, children_count INT, 
			 # married_prev BOOLEAN, account_opened DATE, account_closed DATE (Nullable),
			 # status CHAR
#Interests --> category VARCHAR(40), interest VARCHAR(40)
#Customer_Interests --> ssn VARCHAR(40)


# FAKE DATA
# INSERT BELOW
USE dating_site_project;
INSERT INTO Interests (category, interest) VALUES ('Music', 'Jazz');
INSERT INTO Interests (category, interest) VALUES ('Music', 'Hip Hop');
INSERT INTO Interests (category, interest) VALUES ('Music', 'Pop');
INSERT INTO Interests (category, interest) VALUES ('Sports', 'Basketball');
INSERT INTO Interests (category, interest) VALUES ('Sports', 'Curling');
INSERT INTO Interests (category, interest) VALUES ('Sports', 'Biathlon');
INSERT INTO Roles (role) VALUES ('Specialist');
INSERT INTO Roles (role) VALUES ('Entry-level');
INSERT INTO Roles (role) VALUES ('Customer');
INSERT INTO Crimes (crime) VALUES ('Minor Offense');
INSERT INTO Crimes (crime) VALUES ('Repeat Minor Offense');
INSERT INTO Crimes (crime) VALUES ('Violent Offense');


INSERT INTO Users (username, password, role) VALUES ('Special1', '0123', 'Specialist');
INSERT INTO Users (username, password, role) VALUES ('Entry1', '0123', 'Entry-level');

INSERT INTO Users (username, password, role) VALUES ('jd1', '123', 'Customer');
INSERT INTO Users (username, password, role) VALUES ('jd2', '123', 'Customer');
INSERT INTO Users (username, password, role) VALUES ('jd3', '123', 'Customer');

INSERT INTO Users (username, password, role) VALUES ('jr1', '123', 'Customer');
INSERT INTO Users (username, password, role) VALUES ('jr2', '123', 'Customer');
INSERT INTO Users (username, password, role) VALUES ('jr3', '123', 'Customer');

-- INSERT INTO Users (username, password, role) VALUES ('aharp420', '420', 'Customer')
-- INSERT INTO Customers (ssn, first_name, last_name, username, DOB, interested_in, phone, age, gender, children_count, married_prev, account_opened ) 
--                 	VALUES ('69','Alex','Harp', 'aharp420', '1997-01-31', 'F','1234567891', '21', 'M', '0', 'N', '2018-04-23');

INSERT INTO Customers (ssn, first_name, last_name, username, DOB, interested_in, phone, age, gender, 
						children_count, married_prev, account_opened ) 
                	VALUES ('1','John','Doe', 'jd1', '1997-01-31', 'F','1234567891', '21', 'M', '0', 'N', '2018-04-23');
INSERT INTO Customers (ssn, first_name, last_name, username, DOB, interested_in, phone, age, gender, 
						children_count, married_prev, account_opened ) 
                	VALUES ('2','John','Doe', 'jd2', '1997-01-31', 'F','1234567891', '21', 'M', '1', 'N', '2018-04-23');
INSERT INTO Customers (ssn, first_name, last_name, username, DOB, interested_in, phone, age, gender, 
						children_count, married_prev, account_opened ) 
                	VALUES ('3','John','Doe', 'jd3', '1997-01-31', 'F','1234567891', '21', 'M', '2', 'N', '2018-04-23');

INSERT INTO Customers (ssn, first_name, last_name, username, DOB, interested_in, phone, age, gender, 
						children_count, married_prev, account_opened ) 
                	VALUES ('4','Jane','Doe', 'jr1', '1997-01-31', 'M','1234567891', '21', 'F', '0', 'N', '2018-04-23');
INSERT INTO Customers (ssn, first_name, last_name, username, DOB, interested_in, phone, age, gender, 
						children_count, married_prev, account_opened ) 
                	VALUES ('5','Jane','Doe', 'jr2', '1997-01-31', 'M','1234567891', '21', 'F', '1', 'N', '2018-04-23');
INSERT INTO Customers (ssn, first_name, last_name, username, DOB, interested_in, phone, age, gender, 
						children_count, married_prev, account_opened ) 
                	VALUES ('6','Jane','Doe', 'jr3', '1997-01-31', 'M','1234567891', '21', 'F', '2', 'N', '2018-04-23');

INSERT INTO Customer_Interests VALUES ('1', 'Jazz');
INSERT INTO Customer_Interests VALUES ('1', 'Pop');
INSERT INTO Customer_Interests VALUES ('1', 'Hip Hop');

INSERT INTO Customer_Interests VALUES ('2', 'Jazz');
INSERT INTO Customer_Interests VALUES ('2', 'Pop');
INSERT INTO Customer_Interests VALUES ('2', 'Basketball');
INSERT INTO Customer_Interests VALUES ('2', 'Curling');

INSERT INTO Customer_Interests VALUES ('3', 'Basketball');
INSERT INTO Customer_Interests VALUES ('3', 'Curling');
INSERT INTO Customer_Interests VALUES ('3', 'Biathlon');

INSERT INTO Customer_Interests VALUES ('4', 'Jazz');
INSERT INTO Customer_Interests VALUES ('4', 'Pop');
INSERT INTO Customer_Interests VALUES ('4', 'Hip Hop');

INSERT INTO Customer_Interests VALUES ('5', 'Jazz');
INSERT INTO Customer_Interests VALUES ('5', 'Pop');
INSERT INTO Customer_Interests VALUES ('5', 'Basketball');
INSERT INTO Customer_Interests VALUES ('5', 'Curling');

INSERT INTO Customer_Interests VALUES ('6', 'Basketball');
INSERT INTO Customer_Interests VALUES ('6', 'Curling');
INSERT INTO Customer_Interests VALUES ('6', 'Biathlon');

