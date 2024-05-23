-- Create the Visits table
CREATE TABLE Visits (
    visit_id INT PRIMARY KEY,
    customer_id INT
);
-- Insert data into Visits table
INSERT INTO Visits (visit_id, customer_id) VALUES
(1, 23),
(2, 9),
(4, 30),
(5, 54),
(6, 96),
(7, 54),
(8, 54);


-- Create the Transactions table
CREATE TABLE Transactions (
    transaction_id INT PRIMARY KEY,
    visit_id INT,
    amount INT,
    FOREIGN KEY (visit_id) REFERENCES Visits(visit_id)
);
-- Insert data into Transactions table
INSERT INTO Transactions (transaction_id, visit_id, amount) VALUES
(2, 5, 310),
(3, 5, 300),
(9, 5, 200),
(12, 1, 910),
(13, 2, 970);


-- Create Sales table
CREATE TABLE Sales (
    sales_id INT PRIMARY KEY,
    name VARCHAR(50),
    salary DECIMAL(10, 2),
    commission_rate DECIMAL(5, 2),
    hire_date DATE
);
-- Insert data into Sales table
INSERT INTO Sales (
        sales_id,
        name,
        salary,
        commission_rate,
        hire_date
    )
VALUES (1, 'John', 100000, 6, '2006-04-01'),
    (2, 'Amy', 12000, 5, '2010-05-01'),
    (3, 'Mark', 65000, 12, '2008-12-25'),
    (4, 'Pam', 25000, 25, '2005-01-01'),
    (5, 'Alex', 5000, 10, '2007-02-03');

-- Create Company table
CREATE TABLE Company (
    com_id INT PRIMARY KEY,
    name VARCHAR(50),
    city VARCHAR(50)
);
-- Insert data into Company table
INSERT INTO Company (com_id, name, city)
VALUES (1, 'RED', 'Boston'),
    (2, 'ORANGE', 'New York'),
    (3, 'YELLOW', 'Boston'),
    (4, 'GREEN', 'Austin');

-- Create Orders table
CREATE TABLE Orders (
    order_id INT PRIMARY KEY,
    order_date DATE,
    com_id INT,
    sales_id INT,
    amount DECIMAL(10, 2),
    FOREIGN KEY (com_id) REFERENCES Company(com_id),
    FOREIGN KEY (sales_id) REFERENCES Sales(sales_id)
);
-- Insert data into Orders table
INSERT INTO Orders (order_id, order_date, com_id, sales_id, amount)
VALUES (1, '2014-01-01', 3, 4, 10000),
    (2, '2014-02-01', 4, 5, 5000),
    (3, '2014-03-01', 1, 1, 50000),
    (4, '2014-04-01', 1, 4, 25000);