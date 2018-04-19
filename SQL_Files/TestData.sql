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
INSERT INTO Users (username, password, role) VALUES ('Customer1', '0123', 'Customer');
INSERT INTO Users (username, password, role) VALUES ('Special1', '0123', 'Specialist');
INSERT INTO Users (username, password, role) VALUES ('Entry1', '0123', 'Entry-level');
