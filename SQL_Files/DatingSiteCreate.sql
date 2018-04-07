
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
		DOB DATE NOT NULL,
		interested_in CHAR(1) NOT NULL, # can be M or F
		phone CHAR(10) NOT NULL, 
		age INT NOT NULL,
		gender CHAR NOT NULL,
		children_count INT NOT NULL,
		married_prev BOOLEAN NOT NULL,
		account_opened DATE NOT NULL,
		account_closed DATE NULL, # this is nullable (if it is open we dont have a val here)
		status CHAR NOT NULL,
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
CREATE TABLE Matches
	(
		matchID CHAR(10) NOT NULL,
		ssn1 VARCHAR(40) NOT NULL,
		ssn2 VARCHAR(40) NOT NULL,
		FOREIGN KEY (ssn1) REFERENCES Customers (ssn) ON DELETE CASCADE,
		FOREIGN KEY (ssn2) REFERENCES Customers (ssn) ON DELETE CASCADE,
		PRIMARY KEY (matchID)
	);


DROP TABLE IF EXISTS `Dates`;
CREATE TABLE Dates # primary key is the combination of date_number and mathID
	(
		date_number INT NOT NULL,
		date_time TIME NOT NULL, # IS THIS RIGHT??
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


DROP TABLE IF EXISTS `Charges`;
CREATE TABLE Charges(
	amount DECIMAL(5,2) NOT NULL,
	ssn VARCHAR(40) NOT NULL,
	charge_count INT NOT NULL,
	FOREIGN KEY (ssn) REFERENCES Customers (ssn) ON DELETE CASCADE,
	PRIMARY KEY (ssn, charge_count)
);

-- We need a trigger to charge people for certain dates… so maybe there should be another table for keeping track of each person’s number of dates with eachother/ individually?







