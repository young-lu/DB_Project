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
INSERT INTO Interests (category, interest) VALUES ('Music', 'Jazz');
INSERT INTO Interests (category, interest) VALUES ('Music', 'Hip Hop');
INSERT INTO Interests (category, interest) VALUES ('Music', 'Pop');
INSERT INTO Interests (category, interest) VALUES ('Music', 'Funk');
INSERT INTO Interests (category, interest) VALUES ('Music', 'Country');
INSERT INTO Interests (category, interest) VALUES ('Celebrities', 'Blake Shelton');
INSERT INTO Interests (category, interest) VALUES ('Celebrities', 'The Beatles');
INSERT INTO Interests (category, interest) VALUES ('Celebrities', 'Sophia Vergara');
INSERT INTO Interests (category, interest) VALUES ('Celebrities', 'Gigi Hadid');
INSERT INTO Interests (category, interest) VALUES ('Celebrities', 'Maroon 5');
INSERT INTO Interests (category, interest) VALUES ('Celebrities', 'George Clooney');
INSERT INTO Interests (category, interest) VALUES ('Sports', 'Basketball');
INSERT INTO Interests (category, interest) VALUES ('Sports', 'Curling');
INSERT INTO Interests (category, interest) VALUES ('Sports', 'Biathlon');
INSERT INTO Interests (category, interest) VALUES ('Sports', 'Soccer');
INSERT INTO Interests (category, interest) VALUES ('Sports', 'Football');
INSERT INTO Interests (category, interest) VALUES ('Sports', 'Running');
INSERT INTO Interests (category, interest) VALUES ('Food', 'Chinese Food');
INSERT INTO Interests (category, interest) VALUES ('Food', 'Lebanese Food');
INSERT INTO Interests (category, interest) VALUES ('Food', 'Italian Food');
INSERT INTO Interests (category, interest) VALUES ('Food', 'Ethiopian Food');
INSERT INTO Interests (category, interest) VALUES ('Food', 'French Food');
INSERT INTO Interests (category, interest) VALUES ('Activity', 'Hiking');
INSERT INTO Interests (category, interest) VALUES ('Activity', 'Card Games');
INSERT INTO Interests (category, interest) VALUES ('Activity', 'Biking');
INSERT INTO Interests (category, interest) VALUES ('Activity', 'Travel');
INSERT INTO Interests (category, interest) VALUES ('Activity', 'Eating');
INSERT INTO Interests (category, interest) VALUES ('Activity', 'Uno');
INSERT INTO Interests (category, interest) VALUES ('Language', 'French Language');
INSERT INTO Interests (category, interest) VALUES ('Language', 'Spanish Language');
INSERT INTO Interests (category, interest) VALUES ('Language', 'English Language');
INSERT INTO Interests (category, interest) VALUES ('Language', 'Italian Language');
INSERT INTO Interests (category, interest) VALUES ('Language', 'Arabic Language');
INSERT INTO Interests (category, interest) VALUES ('Academia', 'Philosophy');
INSERT INTO Interests (category, interest) VALUES ('Academia', 'Linguistics');
INSERT INTO Interests (category, interest) VALUES ('Academia', 'Computer Science');
INSERT INTO Interests (category, interest) VALUES ('Academia', 'Mathematics');
INSERT INTO Interests (category, interest) VALUES ('Academia', 'Economics');
INSERT INTO Interests (category, interest) VALUES ('Academia', 'Biology');
INSERT INTO Interests (category, interest) VALUES ('Academia', 'Literature');
INSERT INTO Interests (category, interest) VALUES ('Academia', 'History');
INSERT INTO Interests (category, interest) VALUES ('Academia', 'Pyschology');


INSERT INTO Roles (role) VALUES ('Specialist');
INSERT INTO Roles (role) VALUES ('Entry-level');
INSERT INTO Roles (role) VALUES ('Customer');

INSERT INTO Crimes (crime) VALUES ('Minor Offense');
INSERT INTO Crimes (crime) VALUES ('Repeat Minor Offense');
INSERT INTO Crimes (crime) VALUES ('Violent Offense');
INSERT INTO Crimes (crime) VALUES ('Sexual Assault');
INSERT INTO Crimes (crime) VALUES ('Murder');
INSERT INTO Crimes (crime) VALUES ('Other Offense (Not Listed Here)');



INSERT INTO Users (username, password, role) VALUES ('Special1', '0123', 'Specialist');
INSERT INTO Users (username, password, role) VALUES ('Entry1', '0123', 'Entry-level');

INSERT INTO Users (username, password, role) VALUES ('jd1', '123', 'Customer');
INSERT INTO Users (username, password, role) VALUES ('jd2', '123', 'Customer');
INSERT INTO Users (username, password, role) VALUES ('jd3', '123', 'Customer');

INSERT INTO Users (username, password, role) VALUES ('jr1', '123', 'Customer');
INSERT INTO Users (username, password, role) VALUES ('jr2', '123', 'Customer');
INSERT INTO Users (username, password, role) VALUES ('jr3', '123', 'Customer');

INSERT INTO Users (username, password, role) VALUES ('sf1', '123', 'Customer');
INSERT INTO Users (username, password, role) VALUES ('sf2', '123', 'Customer');
INSERT INTO Users (username, password, role) VALUES ('sf3', '123', 'Customer');
INSERT INTO Users (username, password, role) VALUES ('sf4', '123', 'Customer');

INSERT INTO Users (username, password, role) VALUES ('md1', '123', 'Customer');
INSERT INTO Users (username, password, role) VALUES ('md2', '123', 'Customer');

INSERT INTO Users (username, password, role) VALUES ('crim1', '123', 'Customer');
INSERT INTO Users (username, password, role) VALUES ('crim2', '123', 'Customer');


-- CUSTOMERS W/ OUT KIDS 
-- INSERT INTO Users (username, password, role) VALUES ('aharp420', '420', 'Customer')
-- INSERT INTO Customers (ssn, first_name, last_name, username, DOB, interested_in, phone, age, gender, children_count, married_prev, account_opened ) 
--                 	VALUES ('69','Alex','Harp', 'aharp420', '1997-01-31', 'F','1234567891', '21', 'M', '0', 'N', '2018-04-23');

INSERT INTO Customers (ssn, first_name, last_name, username, DOB, interested_in, phone, age, gender, 
						children_count, married_prev, account_opened ) 
                	VALUES ('1','John1','Doe', 'jd1', '1997-01-31', 'F','1234567891', '21', 'M', '0', 'N', '2018-04-23');
INSERT INTO Customers (ssn, first_name, last_name, username, DOB, interested_in, phone, age, gender, 
						children_count, married_prev, account_opened ) 

                	VALUES ('2','James','Doe', 'jd2', '1997-01-31', 'F','1234567891', '21', 'M', '0', 'N', '2018-04-23');
INSERT INTO Customers (ssn, first_name, last_name, username, DOB, interested_in, phone, age, gender, 
						children_count, married_prev, account_opened ) 
                	VALUES ('3','Jonathan','Doe', 'jd3', '1997-01-31', 'F','1234567891', '21', 'M', '0', 'N', '2018-04-23');



INSERT INTO Customers (ssn, first_name, last_name, username, DOB, interested_in, phone, age, gender, 
						children_count, married_prev, account_opened ) 
                	VALUES ('4','Jane1','Doe', 'jr1', '1997-01-31', 'M','1234567891', '21', 'F', '0', 'N', '2018-04-23');
INSERT INTO Customers (ssn, first_name, last_name, username, DOB, interested_in, phone, age, gender, 
						children_count, married_prev, account_opened ) 

                	VALUES ('5','Jackie','Doe', 'jr2', '1997-01-31', 'M','1234567891', '21', 'F', '0', 'N', '2018-04-23');
INSERT INTO Customers (ssn, first_name, last_name, username, DOB, interested_in, phone, age, gender, 
						children_count, married_prev, account_opened ) 
                	VALUES ('6','Janie','Doe', 'jr3', '1997-01-31', 'M','1234567891', '21', 'F', '0', 'N', '2018-04-23');

---- CUSTOMERS WITH KIDS!!!!

INSERT INTO Customers (ssn, first_name, last_name, username, DOB, interested_in, phone, age, gender, 
						children_count, married_prev, account_opened ) 
                	VALUES ('7','Sam','Fares', 'sf1', '1997-01-31', 'F','1234567891', '21', 'M', '0', 'N', '2018-04-23');
INSERT INTO Customers (ssn, first_name, last_name, username, DOB, interested_in, phone, age, gender, 
						children_count, married_prev, account_opened ) 
                	VALUES ('8','Stanley','Fares', 'sf2', '1997-01-31', 'F','1234567891', '21', 'M', '1', 'N', '2018-04-23');
INSERT INTO Customers (ssn, first_name, last_name, username, DOB, interested_in, phone, age, gender, 
						children_count, married_prev, account_opened ) 
                	VALUES ('9','Sara','Fares', 'sf3', '1997-01-31', 'M','1234567891', '21', 'F', '1', 'N', '2018-04-23');
INSERT INTO Customers (ssn, first_name, last_name, username, DOB, interested_in, phone, age, gender, 
						children_count, married_prev, account_opened ) 
                	VALUES ('10','Sonya','Fares', 'sf4', '1997-01-31', 'M','1234567891', '21', 'F', '2', 'N', '2018-04-23');


--- CUSTOMERS THAT WERE PREV. MARRIED
INSERT INTO Customers (ssn, first_name, last_name, username, DOB, interested_in, phone, age, gender, 
						children_count, married_prev, account_opened )
                	VALUES ('11','Mark','Divorce', 'md1', '1997-01-31', 'M','1234567891', '21', 'M', '0', 'Y', '2018-04-23');
INSERT INTO Customers (ssn, first_name, last_name, username, DOB, interested_in, phone, age, gender, 
						children_count, married_prev, account_opened ) 
                	VALUES ('12','Monnica','Divorce', 'md2', '1997-01-31', 'M','1234567891', '21', 'F', '0', 'Y', '2018-04-23');

--- CUSTOMERS THAT ARE CRIMINALS!!! (YIKES!) 

INSERT INTO Customers (ssn, first_name, last_name, username, DOB, interested_in, phone, age, gender, 
						children_count, married_prev, account_opened, criminal) 
                	VALUES ('13','Mark','Divorce', 'crim1', '1997-01-31', 'M','1234567891', '21', 'M', '0', 'Y', '2018-04-23', 'Y');
INSERT INTO Customers (ssn, first_name, last_name, username, DOB, interested_in, phone, age, gender, 
						children_count, married_prev, account_opened, criminal) 
                	VALUES ('14','Monnica','Divorce', 'crim2', '1997-01-31', 'M','1234567891', '21', 'F', '0', 'Y', '2018-04-23', 'Y');


--- INSERT CRIMES IN FOR THE CRIMINALS 
INSERT INTO Customer_Crimes (ssn, crime, date_recorded) VALUES ('13', 'Minor Offense', '2018-04-23');
INSERT INTO Customer_Crimes (ssn, crime, date_recorded) VALUES ('14', 'Minor Offense', '2018-04-23');


---- CUSTOMER INTERESTS
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


INSERT INTO Customer_Interests VALUES ('7', 'Jazz');
INSERT INTO Customer_Interests VALUES ('7', 'Pop');
INSERT INTO Customer_Interests VALUES ('7', 'Hip Hop');

INSERT INTO Customer_Interests VALUES ('8', 'Jazz');
INSERT INTO Customer_Interests VALUES ('8', 'Pop');

INSERT INTO Customer_Interests VALUES ('9', 'Basketball');
INSERT INTO Customer_Interests VALUES ('9', 'Curling');

INSERT INTO Customer_Interests VALUES ('10', 'Basketball');

INSERT INTO Customer_Interests VALUES ('11', 'French Food');
INSERT INTO Customer_Interests VALUES ('11', 'Biathlon');


INSERT INTO Customer_Interests VALUES ('12', 'Jazz');
INSERT INTO Customer_Interests VALUES ('12', 'Pop');
INSERT INTO Customer_Interests VALUES ('12', 'Hip Hop');

INSERT INTO Customer_Interests VALUES ('13', 'French Food');
INSERT INTO Customer_Interests VALUES ('13', 'Pop');
INSERT INTO Customer_Interests VALUES ('13', 'Basketball');
INSERT INTO Customer_Interests VALUES ('13', 'Curling');

INSERT INTO Customer_Interests VALUES ('14', 'George Clooney');
INSERT INTO Customer_Interests VALUES ('14', 'Curling');
INSERT INTO Customer_Interests VALUES ('14', 'Biathlon');
