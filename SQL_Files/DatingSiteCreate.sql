
DROP DATABASE IF EXISTS `dating_site_project`;
CREATE DATABASE dating_site_project;
USE dating_site_project;

DROP TABLE IF EXISTS `Roles`;
CREATE TABLE Roles
	(
		role VARCHAR(40) NOT NULL,
		PRIMARY KEY (role)
	);


DROP TABLE IF EXISTS `Users`;
CREATE TABLE Users # primary key is username
	(
		username VARCHAR(40) NOT NULL,
		password VARCHAR(40) NOT NULL,
		role VARCHAR(40) NOT NULL,
		FOREIGN KEY (role) REFERENCES Roles (role) ON DELETE CASCADE,
		PRIMARY KEY (username)
	);


DROP TABLE IF EXISTS `Customers`;
CREATE TABLE Customers 
	(
		ssn VARCHAR(40) NOT NULL,
		username VARCHAR(40) NOT NULL,
		first_name VARCHAR(40) NOT NULL,
		last_name VARCHAR(40) NOT NULL,
		DOB DATE NOT NULL,
		interested_in CHAR(1) NOT NULL, # can be M or F
		phone CHAR(10) NOT NULL, 
		age INT NOT NULL,
		gender CHAR NOT NULL,
		children_count INT NOT NULL,
		married_prev BOOLEAN NOT NULL,
		criminal BOOLEAN NOT NULL,
		account_opened DATE NOT NULL,
		account_closed DATE NULL, # this is nullable (if it is open we dont have a val here)
		status CHAR NOT NULL DEFAULT 'open',
		FOREIGN KEY (username) REFERENCES Users (username) ON DELETE CASCADE,
		PRIMARY KEY (ssn),
		check (children_count>=0)
	);


DROP TABLE IF EXISTS `Interests`;
CREATE TABLE Interests # primary key is interest
	( 
		category VARCHAR(40) NOT NULL,
		interest VARCHAR(40) NOT NULL,
		PRIMARY KEY (interest)
	);


DROP TABLE IF EXISTS `Customer_Interests`;	
CREATE TABLE Customer_Interests # primary key is the combination of ssn and interest
	(
		ssn VARCHAR(40) NOT NULL,
		interest VARCHAR(40) NOT NULL,
		FOREIGN KEY (ssn) REFERENCES Customers (ssn) ON DELETE CASCADE,
		FOREIGN KEY (interest) REFERENCES Interests (interest) ON DELETE CASCADE,
		PRIMARY KEY (ssn, interest)
	);


DROP TABLE IF EXISTS `Matches`;
CREATE TABLE Matches # primary key is matchID
	(
		matchID CHAR(10) NOT NULL,
		ssn1 VARCHAR(40) NOT NULL, # put the ssn's in in whatever order (does not matter! so long as we dont re add them in the opposite order)
		ssn2 VARCHAR(40) NOT NULL,
		FOREIGN KEY (ssn1) REFERENCES Customers (ssn) ON DELETE CASCADE,
		FOREIGN KEY (ssn2) REFERENCES Customers (ssn) ON DELETE CASCADE,
		PRIMARY KEY (matchID)
	);


DROP TABLE IF EXISTS `Dates`;
CREATE TABLE Dates # primary key is the combination of date_number and matchID
	(
		date_number INT NOT NULL,
		date_time TIME NOT NULL,
		date_date DATE NOT NULL,
		both_still_interested BOOLEAN NOT NULL,
		happened BOOLEAN NOT NULL,
		location VARCHAR(40) NOT NULL,
		matchID CHAR(10) NOT NULL,
		FOREIGN KEY (matchID) REFERENCES Matches (matchID) ON DELETE CASCADE,
		PRIMARY KEY (date_number, matchID)
	);


DROP TABLE IF EXISTS `Crimes`;
CREATE TABLE Crimes # primary key is crime
	(
		crime VARCHAR(40) NOT NULL,
		PRIMARY KEY (crime)
	);



DROP TABLE IF EXISTS `Customer_Crimes`;
CREATE TABLE Customer_Crimes #primary key is ssn
	(
		ssn VARCHAR(40) NOT NULL,
		crime VARCHAR(40) NOT NULL,
		date_recoreded DATE NOT NULL,
		FOREIGN KEY (ssn) REFERENCES Customers (ssn) ON DELETE CASCADE,
		PRIMARY KEY (ssn)
	);


DROP TABLE IF EXISTS `Match_Fees`;
CREATE TABLE Match_Fees( # the match fee occurs after user goes for a 3rd different date
	amount DECIMAL(5,2) NOT NULL,
	date_charged DATE NOT NULL,
	date_paid DATE NULL, 
	paid BOOLEAN NOT NULL DEFAULT FALSE,
	ssn VARCHAR(40) NOT NULL,
	FOREIGN KEY (ssn) REFERENCES Customers (ssn) ON DELETE CASCADE,
	PRIMARY KEY (ssn)
);

DROP TABLE IF EXISTS `Registration_Fees`;
CREATE TABLE Registration_Fees( # the registratuon fee occurs after user goes for a 3rd different date
	amount DECIMAL(5,2) NOT NULL,
	date_charged DATE NOT NULL,
	date_paid DATE NULL, 
	paid BOOLEAN NOT NULL DEFAULT FALSE,
	ssn VARCHAR(40) NOT NULL,
	FOREIGN KEY (ssn) REFERENCES Customers (ssn) ON DELETE CASCADE,
	PRIMARY KEY (ssn)
);

DROP TABLE IF EXISTS `DateSuccess`;
CREATE TABLE DateSuccess(
	matchID char(10) NOT NULL,
	ssn VARCHAR(40) NOT NULL,
	review VARCHAR(40) NOT NULL,
	PRIMARY KEY (matchID,ssn),
	FOREIGN KEY (ssn) REFERENCES Customers (ssn) ON DELETE CASCADE,
	FOREIGN KEY (matchID) REFERENCES Matches (matchID) ON DELETE CASCADE
);
-- We need a trigger to charge people for certain dates… so maybe there should be another table for keeping track of each person’s number of dates with eachother/ individually?


-- triggers are written below. we have three:
	-- one trigger works to add the charges when necessary if there are 3 dates
	-- the other adds necessary triggers if there are 7 dates
	-- the other automatically closes the profile of one who has a criminal record
----------- TRIGGERS -------------


-- If a client's criminal status is criminal then 
	-- we have to close the account 
	-- but still keep it for our records
DELIMITER //

CREATE TRIGGER update_criminal_status
AFTER INSERT ON Customer_Crimes FOR EACH ROW
BEGIN
	UPDATE Customer
	SET account_closed= GETDATE ()
	WHERE NEW.criminal= True
	AND NEW.ssn= ssn;
END; //

DELIMITER ;

-- If a client goes for a 3rd DIFFERENT!! date, 
	-- then a message should be shown on the screen to show that the person 
	-- has to be charged the match fee
		-- also update the database to reflect the balance due for that person.

DELIMITER //

CREATE TRIGGER update_match_fee
AFTER INSERT ON Dates FOR EACH ROW nnn...n .;nnBEGIN
	UPDATE Match_Fees
	SET date_charged= GETDATE()
	SET ssn= NEW.matchID
	SET amount= 100
	WHERE NEW.ssn1 IN (SELECT ssn1 FROM Matches
		)
	OR NEW.ssn1 IN (SELECT ssn FROM Dates # select all of the ssn1's that appear 3 times in the dates section with a unique matchID
		);
			
	UPDATE Match_Fees 
	SET date_charged = GETDATE()
	SET ssn= NEW.ssn2
	SET amount= 100;
	WHERE NEW.ssn2 = (SELECT ssn2 FROM );
END; //
DELIMITER ;


-- If a client goes for a 7th DIFFERENT!! date, 
	-- then a message shown on the screen to show 
	-- that the person has to be charged the registration fee; 
	-- also update the database to reflect the balance due for that person

DELIMITER //

CREATE TRIGGER update_registration_fee
AFTER INSERT ON Matches FOR EACH ROW
BEGIN
	UPDATE Registration_Fees
	SET activity_count= activity_count + 1
	WHERE band_name= NEW.band_name;
END; //

DELIMITER ;



