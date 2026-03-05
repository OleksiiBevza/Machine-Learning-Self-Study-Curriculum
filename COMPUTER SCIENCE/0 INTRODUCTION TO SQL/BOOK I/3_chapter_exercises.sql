-- EXERCISE 1
SELECT actor_id, first_name, last_name 
FROM actor 
ORDER BY last_name, first_name;




-- EXERCISE 2
SELECT actor_id, first_name, last_name 
FROM actor
WHERE last_name = 'WILLIAMS' OR last_name = 'DAVIS'




-- EXERCISE 3
SELECT DISTINCT customer_id
FROM rental
WHERE DATE(rental_date) = '2005/07/05';




-- EXERCISE 4
--question
mysql> SELECT c.email, r.rental_date
    -> FROM customer AS c
    ->   INNER JOIN rental AS <_fill_>
    ->   ON c.customer_id = <_fill_>
    -> WHERE date(r.rental_date) = '2005-06-14'
    -> ORDER BY <_fill_> <_fill_>;


--answer
SELECT c.email, r.return_date
FROM customer AS c
  INNER JOIN rental AS r
  ON c.customer_id = r.customer_id
WHERE DATE(r.rental_date) = '2005-06-14'
ORDER BY r.return_date DESC;












