CREATE DATABASE dating_site_project;
USE dating_site_project;

CREATE TABLE Roles
	(
		role VARCHAR(40) NOT NULL,
		PRIMARY KEY (role)
	);
CREATE TABLE Users # primary key is username
	(
		username VARCHAR(40) NOT NULL,
		password VARCHAR(40) NOT NULL,
		role VARCHAR(40) NOT NULL,
		FOREIGN KEY (role) REFERENCES Roles (role) ON DELETE CASCADE,
		PRIMARY KEY (username)
	);

CREATE TABLE Customers # primary key is ssn
	(
		ssn VARCHAR(40) NOT NULL,
		username VARCHAR(40) NOT NULL,
		DOB DATE NOT NULL,
		interested_in CHAR(1) NOT NULL, # can be M or F
		phone# CHAR(10) NOT NULL, 
		age INT NOT NULL,
		gender CHAR NOT NULL,
		children_count INT NOT NULL,
		married_prev BOOLEAN NOT NULL,
		account_opened DATE NOT NULL,
		account_closed DATE NULL, # this is nullable(if it is open we dont have a val here)
		status CHAR NOT NULL,
		FOREIGN KEY (username) REFERENCES Users (username) ON DELETE CASCADE,
		PRIMARY KEY (ssn),
		check (children_count>=0)
	);

CREATE TABLE Interests # primary key is interest
	( 
		category VARCHAR(40) NOT NULL,
		interest VARCHAR(40) NOT NULL,
		PRIMARY KEY (interest)
	);
	
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

We need a trigger to charge people for certain dates… so maybe there should be another table for keeping track of each person’s number of dates with eachother/ individually?







