-- EXERCISE 1

SELECT c.first_name, c.last_name, a.address, ct.city
FROM customer c
INNER JOIN address AS a
ON c.address_id = a.address_id
INNER JOIN city ct
ON a.city_id = ct.city_id
WHERE a.district = 'California';





-- EXERCISE 2
SELECT f.title
FROM film AS f
INNER JOIN film_actor AS fa
  ON f.film_id = fa.film_id
INNER JOIN actor AS a
  ON fa.actor_id = a.actor_id
WHERE a.first_name = 'JOHN';





   





