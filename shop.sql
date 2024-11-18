CREATE DATABASE PROJECT;
USE PROJECT;

CREATE TABLE Users (
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  address TEXT,
  mobile_no VARCHAR(15) UNIQUE,
  gender CHAR(1) NOT NULL,
  age INT,
  role VARCHAR(20) DEFAULT 'user',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Categories (
  category_id INT PRIMARY KEY AUTO_INCREMENT,
  category_name VARCHAR(255) UNIQUE NOT NULL,
  category_type ENUM('men', 'women', 'kids', 'accessories','electronics') NOT NULL
);

CREATE TABLE Products (
  product_id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  price FLOAT NOT NULL,
  category_id INT NOT NULL,
  stock_quantity INT NOT NULL,
  image_url VARCHAR(255),
  FOREIGN KEY (category_id) REFERENCES Categories(category_id)
    ON DELETE CASCADE
);

CREATE TABLE Product_Sizes (
  product_size_id INT PRIMARY KEY AUTO_INCREMENT,
  product_id INT NOT NULL,
  size VARCHAR(10) NOT NULL,
  stock_quantity INT NOT NULL,
  FOREIGN KEY (product_id) REFERENCES Products(product_id)
    ON DELETE CASCADE
);


CREATE TABLE Cart_Items (
  cart_item_id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL,
  product_id INT NOT NULL,
  product_size_id INT NOT NULL,
  quantity INT NOT NULL,
  price FLOAT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES Users(user_id)
    ON DELETE CASCADE,
  FOREIGN KEY (product_id) REFERENCES Products(product_id)
    ON DELETE CASCADE,
  FOREIGN KEY (product_size_id) REFERENCES Product_Sizes(product_size_id)
    ON DELETE CASCADE
);

CREATE TABLE Orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount FLOAT NOT NULL,
    shipping_address TEXT NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    order_status VARCHAR(20) DEFAULT 'pending',
    shipping_fee FLOAT NOT NULL,
    tax_amount FLOAT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE Order_Items (
    order_item_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    product_size_id INT NOT NULL,
    quantity INT NOT NULL,
    price_per_unit FLOAT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE CASCADE,
    FOREIGN KEY (product_size_id) REFERENCES Product_Sizes(product_size_id) ON DELETE CASCADE
);



-- Categories
INSERT INTO Categories (category_name, category_type) VALUES
  ('Men', 'men'),
  ('Women', 'women'), 
  ('Kids', 'kids'),
  ('Accessories', 'accessories'),
  ('Electronics', 'electronics');
  
INSERT INTO Products 
(name, description, price, category_id, stock_quantity, image_url) 
VALUES 
('Black T-Shirt', 'Cotton T-Shirt', 799.00, 1, 40, '/static/images/MTshirt1.jpg'),
('White T-Shirt', 'Cotton T-Shirt', 599.00, 1, 40, '/static/images/MTshirt2.jpg'),
('Sweat Shirt'  , 'Cotton SweatShirt', 999.00, 1, 40, '/static/images/MSweatShirt.jpg'),
('Black Hoodie'  , 'Hoodie For Men', 1099.00, 1, 40, '/static/images/MHoodie1.jpg'),
('Green Hoodie'  , 'Hoodie For Men', 1199.00, 1, 40, '/static/images/MHoodie2.jpg'),
('Navy Blue Shirt', 'Cotton Shirt', 999.00, 1, 40, '/static/images/MTshirt1.jpg'),
('Black Shirt', 'Cotton Shirt', 899.00, 1, 40, '/static/images/MShirt2.jpg'),
('Grey Denim Jeans for Men', '100% Pure Denim', 1299.00, 1, 40, '/static/images/MJeans1.jpg'),
('Black Denim Jeans for Men', '100% Pure Denim', 1499.00, 1, 40, '/static/images/MJeans2.jpg'),
('Sneakers'  , 'Sneakers For Men', 4999.00, 1, 40, '/static/images/MSneakers1.jpg'),
('Sneakers'  , 'Sneakers For Men', 4499.00, 1, 40, '/static/images/MSneakers2.jpg'),
('Belt','Belt for Men' , 599.00, 1, 20, '/static/images/MBelt.jpg'),
('Wallet','Pure Leather' , 899.00, 1, 20, '/static/images/Wallet.jpg'),
('Blue Kurta Set ', 'Pure Cotton', 1299.00, 2, 40, '/static/images/WKurtaSet1.jpg'),
('White Kurta Set ', 'Pure Cotton', 1299.00, 2, 40, '/static/images/WKurtaSet2.jpg'),
('Brown Hoodie'  , 'Hoodie For Women', 1099.00, 2, 40, '/static/images/WHoodie1.jpg'),
('Pink Hoodie'  , 'Hoodie For Women', 1199.00, 2, 40, '/static/images/WHoodie2.jpg'),
('Black Denim Jeans for Men', '100% Pure Denim', 1299.00, 2, 40, '/static/images/WJeans.jpg'),
('Sneakers'  , 'Sneakers For Women', 4999.00, 2, 40, '/static/images/WSneakers1.jpg'),
('Sneakers'  , 'Sneakers For Women', 4499.00, 2, 40, '/static/images/WSneakers2.jpg'),
('Brown Handbag'  , 'Pure Leather', 1499, 2, 20, '/static/images/WHandBag1.jpg'),
('Black Handbag'  , 'Pure Leather', 1499, 2, 20, '/static/images/WHandBag2.jpg'),
('Printed T-Shirt', 'Cotton T-Shirt', 599.00, 3, 40, '/static/images/BTshirt1.jpg'),
('Printed T-Shirt', 'Cotton T-Shirt', 599.00, 3, 40, '/static/images/BTshirt2.jpg'),
('Top for Girls', 'Pure Cotton', 999.00, 3, 40, '/static/images/GTop.jpg'),
('Baseball Cap', 'Black' , 699.00, 4, 20, '/static/images/Cap1.jpg'),
('Beanie', 'Black' , 699.00, 4, 20, '/static/images/Cap2.jpg'),
('Black Shades', 'Black' , 1299.00, 4, 20, '/static/images/Specs1.jpg'),
('Blue Shades', 'Blue' , 1299.00, 4, 20, '/static/images/Specs2.jpg'),
('IPhone 16 Pro Max', 'Desert Titanium', 144900.00,5,20,'/static/images/IPhone.jpg'),
('Airpods pro', 'White', 23999.00, 5 , 20,'/static/images/Airpods.jpg'),
('Macbook', 'Midnight Blue', 87999.00, 5 , 20,'/static/images/Macbook.jpg'),
('Airpods Max', 'Midnight Blue', 49999.00, 5 , 20,'/static/images/Headset.jpg'),
('Apple Watch', 'Black', 33999.00, 5 , 20,'/static/images/AppleWatch.jpg');


INSERT INTO Product_Sizes (product_id, size, stock_quantity) VALUES
  (1, 'S', 10),
  (1, 'M', 10),
  (1, 'L', 10),
  (1, 'XL', 10),
  (2, 'S', 10),
  (2, 'M', 10),
  (2, 'L', 10),
  (2, 'XL', 10),  
  (3, 'S', 10),
  (3, 'M', 10),
  (3, 'L', 10),
  (3, 'XL', 10),  
  (4, 'S', 10),
  (4, 'M', 10),
  (4, 'L', 10),
  (4, 'XL', 10),
  (5, 'S', 10),
  (5, 'M', 10),
  (5, 'L', 10),
  (5, 'XL', 10),
  (6, 'S', 10),
  (6, 'M', 10),
  (6, 'L', 10),
  (6, 'XL', 10),  
  (7, 'S', 10),
  (7, 'M', 10),
  (7, 'L', 10),
  (7, 'XL', 10),
  (8, '30', 10),
  (8, '32', 10),
  (8, '34', 10),
  (8, '36', 10),
  (9, '30', 10),
  (9, '32', 10),
  (9, '34', 10),
  (9, '36', 10),
  (10, '8', 10),
  (10, '9', 10),
  (10, '10', 10),
  (10, '11', 10),
  (11, '8', 10),
  (11, '9', 10),
  (11, '10', 10),
  (11, '11', 10),
  (12, 'OneSize',20),
  (13, 'OneSize',20),
  (14, 'XS', 10),
  (14, 'S', 10),
  (14, 'M', 10),
  (14, 'L', 10),  
  (15, 'XS', 10),
  (15, 'S', 10),
  (15, 'M', 10),
  (15, 'L', 10),
  (16, 'XS', 10),
  (16, 'S', 10),
  (16, 'M', 10),
  (16, 'L', 10),  
  (17, 'XS', 10),
  (17, 'S', 10),
  (17, 'M', 10),
  (17, 'L', 10),  
  (18, '26', 10),
  (18, '28', 10),
  (18, '30', 10),
  (18, '32', 10),  
  (19, '5', 10),
  (19, '6', 10),
  (19, '7', 10),
  (19, '8', 10),
  (20, '5', 10),
  (20, '6', 10),
  (20, '7', 10),
  (20, '8', 10),
  (21, 'OneSize',20),  
  (22, 'OneSize',20),
  (23, '1Y-3Y',10),
  (23, '4Y-6Y',10),  
  (23, '7Y-9Y',10),
  (23, '10Y-12Y',10),  
  (24, '1Y-3Y',10),
  (24, '4Y-6Y',10),  
  (24, '7Y-9Y',10),
  (24, '10Y-12Y',10),
  (25, '1Y-3Y',10),
  (25, '4Y-6Y',10),  
  (25, '7Y-9Y',10),
  (25, '10Y-12Y',10),
  (26, 'OneSize',20),  
  (27, 'OneSize',20), 
  (28, 'OneSize',20),   
  (29, 'OneSize',20),
  (30, '256GB',10),
  (30, '512GB',5),  
  (30, '1TB',5), 
  (31, 'OneSize',20),  
  (32, 'OneSize',20), 
  (33, 'OneSize',20),   
  (34, 'OneSize',20);  

DELIMITER //

-- Trigger 1: Update product stock when order is placed
CREATE TRIGGER after_order_item_insert
AFTER INSERT ON Order_Items
FOR EACH ROW
BEGIN
    UPDATE Products 
    SET stock_quantity = stock_quantity - NEW.quantity
    WHERE product_id = NEW.product_id;
    
    UPDATE Product_Sizes
    SET stock_quantity = stock_quantity - NEW.quantity
    WHERE product_size_id = NEW.product_size_id;
END//

-- Trigger 2: Validate age before user insert
CREATE TRIGGER before_user_insert
BEFORE INSERT ON Users
FOR EACH ROW
BEGIN
    IF NEW.age < 18 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'User must be at least 18 years old';
    END IF;
END//

-- Trigger 3: Prevent negative stock in Product_Sizes
CREATE TRIGGER before_product_size_update
BEFORE UPDATE ON Product_Sizes
FOR EACH ROW
BEGIN
    IF NEW.stock_quantity < 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cannot set negative stock quantity';
    END IF;
END//