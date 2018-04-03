# ACTUAL DATA
#Roles --> role VARCHAR(40)
#Users --> username VARCHAR(40), password VARCHAR(40), role references role in Roles
#Customers --> ssn VARCHAR(40), username VARCHAR(40), DOB DATE, interested_in CHAR(1),
			 # phone# char(10), age INT, gender CHAR, children_count INT, 
			 # married_prev BOOLEAN, account_opened DATE, account_closed DATE (Nullable),
			 # status CHAR
#Interests --> category VARCHAR(40), interest VARCHAR(40)
#Customer_Interests --> ssn VARCHAR(40)

CREATE TABLE Customer_Interests # primary key is the combination of ssn and interest
	(
		ssn VARCHAR(40) NOT NULL,
		interest VARCHAR(40) NOT NULL,
		FOREIGN KEY (ssn) REFERENCES Customer (ssn) ON DELETE CASCADE,
		PRIMARY KEY (ssn, interest)
	);


CREATE TABLE Matches
	(
		matchID CHAR(10) NOT NULL,
		ssn1 VARCHAR(40) NOT NULL,
		ssn2 VARCHAR(40) NOT NULL,
		FOREIGN KEY (ssn1) REFERENCES Customer (ssn) ON DELETE CASCADE,
		FOREIGN KEY (ssn2) REFERENCES Customer (ssn) ON DELETE CASCADE,
		PRIMARY KEY (matchID)
	);

CREATE TABLE Dates # primary key is the combination of date_number and ssn1 and ssn2
	(
		date_number INT NOT NULL,
		time TIME NOT NULL, # IS THIS RIGHT??
		date DATE NOT NULL,
		both_still_interested BOOLEAN NOT NULL,
		happened BOOLEAN NOT NULL,
		location VARCHAR(40) NOT NULL,
		matchID CHAR(10) NOT NULL,
		FOREIGN KEY (matchID) REFERENCES Matches (matchID) ON DELETE CASCADE,
		PRIMARY KEY (date_number, match)
	);
CREATE TABLE Crimes # primary key is crime
	(
		crime VARCHAR(40) NOT NULL,
		PRIMARY KEY (crime)
	);
CREATE TABLE Customer_Crimes #primary key is ssn
	(
		ssn VARCHAR(40) NOT NULL,
		crime VARCHAR(40) NOT NULL,
		date_recoreded DATE NOT NULL,
		FOREIGN KEY (ssn) REFERENCES Customer (ssn) ON DELETE CASCADE,
		PRIMARY KEY (ssn)
	);
CREATE TABLE Charges(
	total_charges DECIMAL(5,2) NOT NULL,
	ssn VARCHAR(40) NOT NULL,
	FOREIGN KEY (ssn) REFERENCES Customer (ssn) ON DELETE CASCADE,
	PRIMARY KEY (ssn)
);

# FAKE DATA
# INSERT BELOW

