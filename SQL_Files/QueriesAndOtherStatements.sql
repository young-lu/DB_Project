
-- this file contains the insert statements and queries that we will
-- use as our statements in other pages (this is just a place to store them)


-- query for "Who are those who had [at least, at most, exactly] X number of date events?"
SELECT c.*
FROM Customers c, Dates d, Matches m
WHERE m.matchID= d.matchID
AND c.ssn= m.ssn
GROUP BY m.ssn
HAVING count(*) -- (INSERT =, <=, or >= here) (insert number here)
;

-- query for "How many people who were earlier married are the clients?"
SELECT count(*)
FROM Customers
WHERE married_prev = True;

-- query for "How many male and female are registered?"
SELECT count(*), gender
FROM Customers
GROUP BY gender;

-- query for "For each gender what is the average number of dates?"
SELECT avg(*), gender
FROM Customers c, Dates d, Matches m
WHERE d.matchID = m.matchID
AND m.ssn= c.ssn
GROUP BY c.gender;

-- query for "What type of crime was recorded in database for the “criminal_closed” cases?"
SELECT crime FROM Crimes;

-- query for "Query the database based on any one or the combination of the characteristics 
	-- to find potential list of match.  For each potential match, 
	-- the information of that match should be shown." 
-----------
	-- ******* USE WHAT CONNOR DID ?? ******
-----------

-- query for "What is the average age of the children of the clients?"
SELECT avg(age) FROM Customers_Children;

-- this query below is dumb  (idk why i thought someone would need the average age of one person's kids)
--	SELECT avg(cc.age), c.* FROM Customers_Children cc, Customers c WHERE cc.ssn = c.ssn GROUP BY cc.ssn;

-- query for "What is the average number of matches that the clients with 
	-- >=1 child have?"
SELECT avg(count(m.matchID)) FROM Matches m, Customers c WHERE m.ssn= c.ssn 
AND c.children_count >0 GROUP BY m.ssn;

-- query for "What is the total number of dates that have occured?"
SELECT count(*)
FROM Dates;

-- query for "What is the most common previous marital status amongst the men 
	-- in the database?"
SELECT married_prev
FROM Customers
WHERE gender="M"
GROUP BY married_prev
ORDER BY count(*) DESC
LIMIT 1;
