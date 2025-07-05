# ShopEase E-Commerce Platform

ShopEase is a full-featured e-commerce web application built with Python's Flask framework and MySQL. It provides a seamless online shopping experience for users, allowing them to browse products, manage their cart, and place orders.

## Features

  * **User Authentication:** Secure user registration and login functionality.
  * **Product Catalog:** Browse products by category with details like name, description, price, and available sizes.
  * **Shopping Cart:** Add products to the cart, update quantities, and see a summary of the order.
  * **Checkout Process:** A smooth checkout process with shipping details and multiple payment options.
  * **Order History:** Users can view their past orders and their statuses.
  * **User Profile:** A dedicated profile page for users to view their information.

## Technologies Used

  * **Backend:** Python (Flask)
  * **Database:** MySQL
  * **Frontend:** HTML, CSS, JavaScript

## Project Structure

```
.
├── app.py              # Main Flask application file
├── static
│   ├── images
│   ├── Cstyles.css
│   ├── Istyles.css
│   ├── Lstyles.css
│   ├── Ostyles.css
│   ├── PRstyles.css
│   └── Rstyles.css
├── templates
│   ├── cart.html
│   ├── checkoutpage.html
│   ├── index.html
│   ├── login.html
│   ├── orders.html
│   ├── products.html
│   ├── profile.html
│   └── register.html
└── README.md
```

## Setup and Installation

### Prerequisites

  * Python 3.x
  * MySQL Server
  * Flask and other required Python packages

### 1\. Clone the Repository

```bash
git clone <https://github.com/Sudheendra18/Online-Shopping-Website>
cd <Online-Shopping-Website>
```

### 2\. Create a Virtual Environment

It's recommended to use a virtual environment to manage project dependencies.

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3\. Install Dependencies

Install the required Python packages using pip:

```bash
pip install Flask Flask-MySQLdb Werkzeug
```

### 4\. Database Setup

1.  Make sure your MySQL server is running.

2.  Open the `app.py` file and update the MySQL configuration with your database credentials:

    ```python
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'your_mysql_username'
    app.config['MYSQL_PASSWORD'] = 'your_mysql_password'
    app.config['MYSQL_DB'] = 'PROJECT'
    ```

3.  Create a database named `PROJECT`.

4.  You will need to create the necessary tables in your `PROJECT` database. Here are the SQL statements to create the required tables. You can execute these in your MySQL client.

    **Users Table**

    ```sql
    CREATE TABLE Users (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        address VARCHAR(200),
        mobile_no VARCHAR(15),
        gender CHAR(1),
        age INT
    );
    ```

    **Categories Table**

    ```sql
    CREATE TABLE Categories (
        category_id INT AUTO_INCREMENT PRIMARY KEY,
        category_name VARCHAR(100) NOT NULL,
        category_type VARCHAR(50)
    );
    ```

    **Products Table**

    ```sql
    CREATE TABLE Products (
        product_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        description TEXT,
        price DECIMAL(10, 2),
        category_id INT,
        stock_quantity INT,
        image_url VARCHAR(255),
        FOREIGN KEY (category_id) REFERENCES Categories(category_id)
    );
    ```

    **Product\_Sizes Table**

    ```sql
    CREATE TABLE Product_Sizes (
        product_size_id INT AUTO_INCREMENT PRIMARY KEY,
        product_id INT,
        size VARCHAR(50),
        stock_quantity INT,
        FOREIGN KEY (product_id) REFERENCES Products(product_id)
    );
    ```

    **Cart\_Items Table**

    ```sql
    CREATE TABLE Cart_Items (
        cart_item_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        product_id INT,
        product_size_id INT,
        quantity INT,
        price DECIMAL(10, 2),
        FOREIGN KEY (user_id) REFERENCES Users(user_id),
        FOREIGN KEY (product_id) REFERENCES Products(product_id),
        FOREIGN KEY (product_size_id) REFERENCES Product_Sizes(product_size_id)
    );
    ```

    **Orders Table**

    ```sql
    CREATE TABLE Orders (
        order_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        total_amount DECIMAL(10, 2),
        shipping_address VARCHAR(255),
        payment_method VARCHAR(50),
        order_status VARCHAR(50),
        shipping_fee DECIMAL(10, 2),
        tax_amount DECIMAL(10, 2),
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
    );
    ```

    **Order\_Items Table**

    ```sql
    CREATE TABLE Order_Items (
        order_item_id INT AUTO_INCREMENT PRIMARY KEY,
        order_id INT,
        product_id INT,
        product_size_id INT,
        quantity INT,
        price_per_unit DECIMAL(10, 2),
        FOREIGN KEY (order_id) REFERENCES Orders(order_id),
        FOREIGN KEY (product_id) REFERENCES Products(product_id),
        FOREIGN KEY (product_size_id) REFERENCES Product_Sizes(product_size_id)
    );
    ```

### 5\. Run the Application

Once the setup is complete, you can run the Flask application:

```bash
python app.py
```

The application will be accessible at `http://127.0.0.1:5000`.

## How to Use

1.  **Register:** Create a new account by providing your details.
2.  **Login:** Log in with your registered email and password.
3.  **Browse Products:** Navigate to the "Products" page to see the available items. You can filter them by category.
4.  **Add to Cart:** Select a product, choose the size and quantity, and add it to your shopping cart.
5.  **View Cart:** Go to your cart to review the items, update quantities, or remove items.
6.  **Checkout:** Proceed to checkout, fill in your shipping information, and select a payment method to place your order.
7.  **My Orders:** You can check the "My Orders" page to see your order history and the status of each order.
8.  **Profile:** Your user profile displays your registered information.
