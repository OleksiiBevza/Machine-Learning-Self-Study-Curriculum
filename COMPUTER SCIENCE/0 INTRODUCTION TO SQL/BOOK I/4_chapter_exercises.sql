
-- EXERCISE 3
SELECT * FROM payments 
WHERE amount IN (1.98, 7.98, 9.98);


-- EXERCISE 4

SELECT c.last_name, c.customer_id
FROM customer AS c   
INNER JOIN payment AS p
  ON c.customer_id = p.customer_id
WHERE c.last_name LIKE '_A%W%';

