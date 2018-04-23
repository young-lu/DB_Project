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
		married_prev CHAR NOT NULL DEFAULT 'N',
		criminal INT(1),
		account_opened DATE NOT NULL,
		account_closed DATE NULL, # this is nullable (if it is open we dont have a val here)
		status VARCHAR(16) NOT NULL DEFAULT 'Open',
		FOREIGN KEY (username) REFERENCES Users (username) ON DELETE CASCADE,
		PRIMARY KEY (ssn),
		check (children_count>=0),
		check (gender = "M" or 	gender = "F"),
		check (criminal = 0 or criminal = 1),
		check (married_prev = 'Y' OR married_prev = 'N')
	);

CREATE TABLE Customers_Children
	(
		ssn VARCHAR(40) NOT NULL,
		which_child INT NOT NULL,
		age INT NOT NULL,
		PRIMARY KEY (ssn, which_child)
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
CREATE TABLE Matches # primary key is matchID, ssn (each match has two tuples)
	(
		matchID CHAR(10) NOT NULL,
		ssn VARCHAR(40) NOT NULL, # put the ssn's in in whatever order (does not matter! so long as we dont re add them in the opposite order)
		FOREIGN KEY (ssn) REFERENCES Customers (ssn) ON DELETE CASCADE,
		PRIMARY KEY (matchID, ssn)
	);


DROP TABLE IF EXISTS `Dates`;
CREATE TABLE Dates # primary key is the combination of date_number and matchID
	(
		date_number INT NOT NULL,
		date_time TIME NOT NULL,
		date_date DATE NOT NULL,
		-- both_still_interested BOOLEAN NOT NULL,
		happened CHAR(1) NOT NULL DEFAULT 'N',
		location VARCHAR(40) NOT NULL,
		matchID CHAR(10) NOT NULL,
		FOREIGN KEY (matchID) REFERENCES Matches (matchID) ON DELETE CASCADE,
		PRIMARY KEY (date_number, matchID),
		check (happened = 'Y' or happened = 'N')
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

DELIMITER //

CREATE TRIGGER update_criminal_status AFTER INSERT ON Customer_Crimes FOR EACH ROW
BEGIN
	UPDATE Customers
	SET account_closed= NOW() AND status = 'Criminal_losed'
	WHERE ssn= new.ssn;
END; //

DELIMITER ;










-- If a client goes for a 3rd DIFFERENT!! date, 
	-- then a message should be shown on the screen to show that the person 
	-- has to be charged the match fee
		-- also update the database to reflect the balance due for that person.

-- DELIMITER //

-- CREATE TRIGGER update_match_fee
-- AFTER INSERT ON Dates FOR EACH ROW
-- BEGIN
-- 	ssn1= ( SELECT ssn
-- 			FROM Matches
-- 			LIMIT=1);
-- 	ssn2= (SELECT ssn 
-- 			FROM Matches
-- 			WHERE matchID = NEW.matchID
-- 			AND ssn != ssn1);
-- 	IF ssn1 IN (SELECT m.ssn
-- 			FROM Matches m, Dates d 
-- 			WHERE d.matchID=m.matchID
-- 			AND d.ssn=m.ssn
-- 			GROUP BY m.ssn
-- 			HAVING count(DISTINCT(d.matchID))=3)
-- 	THEN 
-- 		INSERT INTO Match_Fees (100, GETDATE(), NULL, 'False', ssn1)
-- 	END IF;

-- 	IF ssn2 IN (SELECT d.ssn
-- 			FROM Matches m, Dates d 
-- 			WHERE d.matchID=m.matchID
-- 			AND d.ssn=m.ssn
-- 			GROUP BY m.ssn
-- 			HAVING count(DISTINCT(d.matchID))=3)
-- 	THEN
-- 		INSERT INTO Match_Fees (100, GETDATE(), NULL, 'False', ssn2)
-- 	END IF;
-- END; //
-- DELIMITER ;










-- If a client goes for a 7th DIFFERENT!! date, 
	-- then a message shown on the screen to show 
	-- that the person has to be charged the registration fee; 
	-- also update the database to reflect the balance due for that person

-- DELIMITER //

-- CREATE TRIGGER update_registration_fee
-- AFTER INSERT ON Dates FOR EACH ROW
-- BEGIN
-- 	ssn1= (SELECT ssn
-- 			FROM Matches
-- 			LIMIT=1);
-- 	ssn2= (SELECT ssn 
-- 			FROM Matches
-- 			WHERE matchID = NEW.matchID
-- 			AND ssn != ssn1);
-- 	IF ssn1 IN (SELECT m.ssn
-- 			FROM Matches m, Dates d 
-- 			WHERE d.matchID=m.matchID
-- 			AND d.ssn=m.ssn
-- 			GROUP BY m.ssn
-- 			HAVING count(DISTINCT(d.matchID))=3)
-- 	THEN 
-- 		INSERT INTO Registration_Fees (100, GETDATE(), NULL, 'False', ssn1) ;
-- 	END IF;

-- 	IF ssn2 IN (SELECT d.ssn
-- 			FROM Matches m, Dates d 
-- 			WHERE d.matchID=m.matchID
-- 			AND d.ssn=m.ssn
-- 			GROUP BY m.ssn
-- 			HAVING count(DISTINCT(d.matchID))=3)
-- 	THEN
-- 		INSERT INTO Registration_Fees (100, GETDATE(), NULL, 'False', ssn2) ;
-- 	END IF ;
-- END; //
-- DELIMITER ;











-- If a crime is inserted into Customer_Crimes, we need to add it to the list of crimes 
	-- IF its not already there
DELIMITER //

CREATE TRIGGER addCrime
AFTER INSERT ON Customer_Crimes FOR EACH ROW
BEGIN
	IF NEW.crime NOT IN (SELECT crime FROM Crimes) THEN
		INSERT INTO Crimes (crime) VALUES (NEW.crime) ;
	END IF;

END; //

DELIMITER ;
