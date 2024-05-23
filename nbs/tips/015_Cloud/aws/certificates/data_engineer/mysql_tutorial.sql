
--------------- SCHEMA AND TABLE CREATION ----------------

CREATE SCHEMA `new_schema` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE `new_schema`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT 'This is the primary index',
  `name` VARCHAR(45) NOT NULL DEFAULT 'N/A',
  PRIMARY KEY (`id`)
);

ALTER TABLE `new_schema`.`users`
ADD COLUMN `age` INT NULL AFTER `name`;

ALTER TABLE `new_schema`.`users`
CHANGE COLUMN `id` `id` INT(11) NOT NULL AUTO_INCREMENT,
CHANGE COLUMN `name` `user_name` VARCHAR(45) NOT NULL DEFAULT 'No Name';

SHOW FULL COLUMNS FROM `new_schema`.`users`;

-------------------- WHERE CLAUSE ------------------------

SELECT * FROM `new_schema`.`users` WHERE height IS NULL; -- this is sometimes relevant to include as null values can be excluded from query, 
-- for example !=2 will exclude not only what is equals to 2 but also null values, i.e. null != 2 is True.

SELECT * FROM `new_schema`.`users` WHERE height IS NOT NULL;

SELECT * FROM `new_schema`.`users` WHERE age < 40 AND height > 160;

SELECT * FROM `new_schema`.`users` WHERE age < 40 OR height > 160;

SELECT * FROM `new_schema`.`users` WHERE id < 4 AND (age > 30 OR height > 175);

SELECT * FROM `new_schema`.`users` WHERE `id` IN (1, 3);

SELECT * FROM `new_schema`.`users` WHERE id NOT IN (1, 4);

SELECT * FROM `new_schema`.`users` WHERE height BETWEEN 160 AND 190;

-- Note: The percent sign (%) will match zero, one, or multiple characters. To match exactly one character we could use an underscore (_).
SELECT * FROM `new_schema`.`users` WHERE name LIKE '%a%';

SELECT * FROM `new_schema`.`users` WHERE name LIKE 'J%';

----------------------- JSON ----------------------------

ALTER TABLE `new_schema`.`users` 
ADD COLUMN `contact` JSON NULL AFTER `id`;  -- NULL means it can be null

INSERT INTO `new_schema`.`users` (`id`, `name`, `contact`) VALUES 
  (1, 'John', JSON_OBJECT('phone', '123-456', 'address', 'New York')),
  (2, 'May', JSON_OBJECT('phone', '888-99', 'address', 'LA')),
  (3, 'Tim', NULL),
  (4, 'Jay', JSON_OBJECT('phone', '321-6', 'address', 'Boston'));

SELECT `id`, JSON_UNQUOTE(JSON_EXTRACT(contact, '$.phone')) AS phone
FROM `new_schema`.`users`;

----- DELETE FROM ----------------

DELETE FROM US.users WHERE id = 1;

---------- UPDATE -----------------------
UPDATE `new_schema`.`users` SET `contact` = JSON_SET(contact, '$.phone', '6666', '$.phone_2', '888') WHERE `id` = 2;

UPDATE Salary SET sex = CASE WHEN sex = 'f' THEN 'm' WHEN sex = 'm' THEN 'f' END;

---------- DISTINCT, LIMIT, OFFSET, GROUP BY --

SELECT DISTINCT age FROM `new_schema`.`users`;

SELECT * FROM `new_schema`.`users` LIMIT 3 OFFSET 1;

SELECT * FROM `new_schema`.`users` ORDER BY age DESC, height DESC;

SELECT `age` FROM `new_schema`.`users` GROUP BY age;


select Email
from Person
group by Email
having count(Email) > 1;  -- WHERE is applied before data is grouped, making it more efficient for initial data filtration. HAVING, on the other hand, is applied after, making it less efficient for initial filtering.


select
    actor_id,
    director_id
from ActorDirector
group by
    actor_id,
    director_id
having 
    count(*) >= 3;




------- COUNT, SUM, AVG, MIN, MAX, CONCAT ----------------

SELECT COUNT(*) AS `user_count` FROM `new_schema`.`users` WHERE id > 1;
SELECT SUM(`age`) AS `sum_of_user_ages` FROM `new_schema`.`users`;
SELECT AVG(`height`) AS `avg_user_height` FROM `new_schema`.`users`;
SELECT MIN(`height`) AS `user_min` FROM `new_schema`.`users`;
SELECT MAX(`height`) AS `user_max` FROM `new_schema`.`users`;
SELECT CONCAT(`id`, '-', `name`) AS `identification`, `age` FROM `new_schema`.`users`;

SELECT 
    date_id, 
    make_name, 
    COUNT(DISTINCT lead_id) AS unique_leads, 
    COUNT(DISTINCT partner_id) AS unique_partners
FROM DailySales
GROUP BY date_id, make_name
ORDER BY date_id, make_name;

select (COUNT(CASE WHEN Survived = 1 THEN 1 END) * 1.0 / count(*)) as overall_rate FROM titanic;

select 
    player_id,
    MIN(event_date) as first_login
from 
    Activity
group by
    player_id;


SELECT date_id, make_name, COUNT(DISTINCT CONCAT(lead_id, '-', partner_id)) AS num_leads
FROM CarLeads

----------- CTE ----------------

-- Common Table Expression (CTE) in SQL is a temporary result set that you can reference within a SELECT, INSERT, UPDATE, or DELETE statement.

WITH FirstLogins AS (
    SELECT 
        player_id,
        MIN(event_date) AS first_login
    FROM 
        Activity
    GROUP BY 
        player_id
)
SELECT 
    player_id, 
    first_login
FROM 
    FirstLogins
ORDER BY 
    player_id;

-------- JOIN ------------

-- 1-to-1, 1-to-many, many-to-many (requires intermediate table) --

-- Careful! LEFT/RIGHT JOIN in combination with WHERE becomes in fact INNER JOIN!!

SELECT * FROM `new_schema`.`users`
LEFT JOIN `new_schema`.`orders` ON `users`.`id` = `orders`.`user_id`;

select 
    customer_id, 
    count(*) as count_no_trans 
from 
    Visits v
left join 
    Transactions t on v.visit_id = t.visit_id
where 
    t.transaction_id is NULL
GROUP BY 
    v.customer_id


select p.firstName, p.lastName, a.city, a.state
from Person p
left join Address a on a.personId = p.personId

------ SUBQUERY ----------------

SELECT * FROM `new_schema`.`orders`
WHERE user_id IN (
  SELECT id FROM `new_schema`.`users`
  WHERE name LIKE '%j%'
);


select 
    name 
from 
    SalesPerson
where sales_id not in (
        select 
            distinct sales_id 
        from 
            Orders 
        left join 
            Company on Orders.com_id = Company.com_id 
        where
            Company.name = "RED"
)
