-- Exercise 6-1

SELECT a.first_name, a.last_name
FROM actor a
WHERE a.last_name LIKE 'L%'
UNION
(SELECT a.first_name, a.last_name
 FROM actor a
 WHERE a.last_name LIKE 'L%'
 UNION ALL
 SELECT c.first_name, c.last_name
 FROM customer c
 WHERE c.last_name LIKE 'L%'
);

-- same can be achived in easier way:
 
SELECT first_name, last_name
FROM actor
WHERE last_name LIKE 'L%'

UNION

SELECT first_name, last_name
FROM customer
WHERE last_name LIKE 'L%';



-- Exercise 6-3
SELECT first_name AS fname, last_name AS lname
FROM actor
WHERE last_name LIKE 'L%'

UNION

SELECT first_name, last_name
FROM customer
WHERE last_name LIKE 'L%'
ORDER BY lname;
