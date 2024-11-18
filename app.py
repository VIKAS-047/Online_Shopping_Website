# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import os
from functools import wraps

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.urandom(24)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Replace with your MySQL username
app.config['MYSQL_PASSWORD'] = 'Meghana@685'  # Replace with your MySQL password
app.config['MYSQL_DB'] = 'PROJECT'

# Initialize MySQL
mysql = MySQL(app)

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

# Modify the products route in app.py
@app.route('/products')
def products():
    try:
        selected_category = request.args.get('category')
        
        cur = mysql.connection.cursor()
        
        # Get categories
        cur.execute("SELECT * FROM Categories")
        categories = cur.fetchall()
        
        # Modified query to include image_url
        base_query = """
            SELECT 
                p.product_id,
                p.name,
                COALESCE(p.description, ''),
                COALESCE(p.price, 0.0),
                p.category_id,
                COALESCE(p.stock_quantity, 0),
                c.category_name,
                c.category_type,
                GROUP_CONCAT(
                    CONCAT(
                        ps.product_size_id, ':',
                        ps.size, ':',
                        COALESCE(ps.stock_quantity, 0)
                    ) SEPARATOR '|'
                ) as sizes,
                p.image_url
            FROM Products p
            LEFT JOIN Categories c ON p.category_id = c.category_id
            LEFT JOIN Product_Sizes ps ON p.product_id = ps.product_id
        """
        
        if selected_category:
            query = base_query + " WHERE c.category_name = %s GROUP BY p.product_id"
            cur.execute(query, (selected_category,))
        else:
            query = base_query + " GROUP BY p.product_id"
            cur.execute(query)
        
        products = cur.fetchall()
        
        # Process the products to format sizes properly
        formatted_products = []
        for product in products:
            # Convert product tuple to list for modification
            product_list = list(product)
            
            # Handle sizes
            sizes_str = product_list[8]
            formatted_sizes = []
            
            if sizes_str:  # Check if sizes exist
                size_entries = sizes_str.split('|')
                for size_entry in size_entries:
                    if size_entry:  # Make sure the entry is not empty
                        try:
                            size_id, size, stock = size_entry.split(':')
                            formatted_sizes.append({
                                'id': int(size_id),
                                'size': size,
                                'stock': int(stock)
                            })
                        except (ValueError, IndexError):
                            continue  # Skip invalid entries
            
            # Replace the sizes string with formatted sizes list
            product_list[8] = formatted_sizes
            
            # Ensure image_url is properly formatted
            if product_list[9]:  # index 9 contains the image_url
                # Convert Windows path format to URL format if needed
                product_list[9] = product_list[9].replace('\\', '/')
                # Make sure the path starts with /static/
                if not product_list[9].startswith('/static/'):
                    product_list[9] = f'/static/images/{os.path.basename(product_list[9])}'
            else:
                product_list[9] = '/static/images/placeholder.jpg'  # Default image
                
            formatted_products.append(tuple(product_list))
        
        return render_template('products.html', 
                             products=formatted_products, 
                             categories=categories,
                             selected_category=selected_category)
                             
    except Exception as e:
        flash(f'Error loading products: {str(e)}', 'error')
        return redirect(url_for('index'))
    finally:
        if 'cur' in locals():
            cur.close()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        address = request.form['address']
        mobile_no = request.form['mobile_no']
        gender = request.form['gender']
        age = request.form['age']

        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        cur = mysql.connection.cursor()
        
        try:
            cur.execute("SELECT * FROM Users WHERE email = %s", (email,))
            if cur.fetchone():
                flash('Email already exists!', 'error')
                return redirect(url_for('register'))

            cur.execute("""
                INSERT INTO Users (name, email, password, address, mobile_no, gender, age)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (name, email, hashed_password, address, mobile_no, gender, age))
            
            mysql.connection.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')
            return redirect(url_for('register'))
        finally:
            cur.close()

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        try:
            cur.execute("SELECT * FROM Users WHERE email = %s", (email,))
            user = cur.fetchone()

            if user and check_password_hash(user[3], password):
                session['user_id'] = user[0]
                session['user_name'] = user[1]
                flash('Login successful!', 'success')
                return redirect(url_for('profile'))
            else:
                flash('Invalid email or password!', 'error')
        finally:
            cur.close()

    return render_template('login.html')

@app.route('/profile')
@login_required
def profile():
    cur = mysql.connection.cursor()
    try:
        # Get user details with dictionary cursor for cleaner data handling
        cur.execute("""
            SELECT 
                name,
                email,
                address,
                mobile_no,
                gender,
                age
            FROM Users 
            WHERE user_id = %s
        """, (session['user_id'],))
        
        user = cur.fetchone()
        
        if user:
            # Create a dictionary with meaningful keys
            user_data = {
                'name': user[0],
                'email': user[1],
                'address': user[2],
                'mobile_no': user[3],
                'gender': user[4],
                'age': user[5]
            }
            return render_template('profile.html', user=user_data)
        
        flash('User profile not found!', 'error')
        return redirect(url_for('login'))
        
    except Exception as e:
        flash(f'Error loading profile: {str(e)}', 'error')
        return redirect(url_for('login'))
    finally:
        cur.close()

@app.route('/cart')
@login_required
def cart():
    cur = mysql.connection.cursor()
    try:
        # Updated query to include product image_url
        cur.execute("""
            SELECT 
                ci.cart_item_id,
                ci.user_id,
                ci.product_id,
                p.name as product_name,
                ci.quantity,
                ps.size,
                p.price,
                ps.product_size_id,
                p.image_url  # Added image_url to the selection
            FROM Cart_Items ci
            JOIN Products p ON ci.product_id = p.product_id
            JOIN Product_Sizes ps ON ci.product_size_id = ps.product_size_id
            WHERE ci.user_id = %s
        """, (session['user_id'],))
        cart_items = cur.fetchall()
        
        # Process cart items to ensure proper image URLs
        processed_cart_items = []
        for item in cart_items:
            # Convert to list to modify
            item_list = list(item)
            
            # Process image URL (index 8 contains image_url)
            if item_list[8]:
                # Ensure proper URL format
                image_url = item_list[8]
                if not image_url.startswith('/static/'):
                    image_url = f'/static/images/{os.path.basename(image_url)}'
                item_list[8] = image_url
            else:
                # Set default image if none exists
                item_list[8] = '/static/images/placeholder.jpg'
                
            processed_cart_items.append(tuple(item_list))
        
        # Calculate totals using the correct price from Products table
        subtotal = sum(float(item[4]) * float(item[6]) for item in processed_cart_items)  # quantity * product price
        shipping = 5.99 if processed_cart_items else 0.00
        total = subtotal + shipping
        
        return render_template('cart.html', 
                             cart_items=processed_cart_items,
                             subtotal=subtotal,
                             shipping=shipping,
                             total=total)
    except Exception as e:
        flash(f'Error loading cart: {str(e)}', 'error')
        return redirect(url_for('index'))
    finally:
        cur.close()

@app.route('/add_to_cart', methods=['POST'])
@login_required
def add_to_cart():
    if request.method == 'POST':
        try:
            product_id = request.form.get('product_id')
            size_id = request.form.get('size_id')
            quantity = request.form.get('quantity', 1, type=int)
            
            # Input validation
            if not all([product_id, size_id]):
                flash('Missing required fields', 'error')
                return redirect(url_for('products'))
            
            try:
                quantity = int(quantity)
                if quantity <= 0:
                    flash('Please select a valid quantity', 'error')
                    return redirect(url_for('products'))
            except ValueError:
                flash('Invalid quantity', 'error')
                return redirect(url_for('products'))
            
            cur = mysql.connection.cursor()
            
            try:
                # Check stock availability and get product price
                cur.execute("""
                    SELECT ps.stock_quantity, p.price 
                    FROM Product_Sizes ps
                    JOIN Products p ON p.product_id = ps.product_id
                    WHERE ps.product_size_id = %s AND ps.product_id = %s
                """, (size_id, product_id))
                
                result = cur.fetchone()
                if not result:
                    flash('Product not found', 'error')
                    return redirect(url_for('products'))
                
                available_stock, price = result
                
                if quantity > available_stock:
                    flash(f'Only {available_stock} items available in stock', 'error')
                    return redirect(url_for('products'))
                
                # Check if item already exists in cart
                cur.execute("""
                    SELECT cart_item_id, quantity 
                    FROM Cart_Items 
                    WHERE user_id = %s AND product_id = %s AND product_size_id = %s
                """, (session['user_id'], product_id, size_id))
                
                existing_item = cur.fetchone()
                
                if existing_item:
                    new_quantity = quantity
                    if new_quantity > available_stock:
                        flash(f'Cannot add more items. Stock limit reached.', 'error')
                        return redirect(url_for('products'))
                    
                    cur.execute("""
                        UPDATE Cart_Items 
                        SET quantity = %s 
                        WHERE cart_item_id = %s
                    """, (new_quantity, existing_item[0]))
                else:
                    # Add new cart item
                    cur.execute("""
                        INSERT INTO Cart_Items (user_id, product_id, product_size_id, quantity, price)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (session['user_id'], product_id, size_id, quantity, price))
                
                mysql.connection.commit()
                flash('Cart updated successfully', 'success')
                return redirect(url_for('cart'))
                
            except Exception as e:
                mysql.connection.rollback()
                flash(f'Error updating cart: {str(e)}', 'error')
                return redirect(url_for('products'))
            finally:
                cur.close()
                
        except Exception as e:
            flash(f'Error adding to cart: {str(e)}', 'error')
            return redirect(url_for('products'))
    
    return redirect(url_for('products'))

@app.route('/update_cart', methods=['POST'])
@login_required
def update_cart():
    cart_item_id = request.form.get('cart_item_id')
    quantity = request.form.get('quantity')
    
    if not cart_item_id or not quantity:
        flash('Invalid update request', 'error')
        return redirect(url_for('cart'))
    
    try:
        quantity = int(quantity)
    except ValueError:
        flash('Invalid quantity value', 'error')
        return redirect(url_for('cart'))
    
    cur = mysql.connection.cursor()
    try:
        if quantity > 0:
            # First check if we have enough stock
            cur.execute("""
                SELECT ps.stock_quantity
                FROM Cart_Items ci
                JOIN Product_Sizes ps ON ci.product_size_id = ps.product_size_id
                WHERE ci.cart_item_id = %s AND ci.user_id = %s
            """, (cart_item_id, session['user_id']))
            
            result = cur.fetchone()
            if not result:
                flash('Cart item not found', 'error')
                return redirect(url_for('cart'))
                
            available_stock = result[0]
            
            if quantity > available_stock:
                flash(f'Only {available_stock} items available in stock', 'error')
                return redirect(url_for('cart'))
            
            # Update quantity if stock is available
            cur.execute("""
                UPDATE Cart_Items 
                SET quantity = %s 
                WHERE cart_item_id = %s AND user_id = %s
            """, (quantity, cart_item_id, session['user_id']))
        else:
            # Remove item if quantity is 0 or negative
            cur.execute("""
                DELETE FROM Cart_Items 
                WHERE cart_item_id = %s AND user_id = %s
            """, (cart_item_id, session['user_id']))
        
        mysql.connection.commit()
        flash('Cart updated successfully', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error updating cart: {str(e)}', 'error')
    finally:
        cur.close()
    
    return redirect(url_for('cart'))

@app.route('/checkout')
@login_required
def checkout():
    cur = mysql.connection.cursor()
    try:
        # Get cart items with specific field selection
        cur.execute("""
            SELECT 
                ci.cart_item_id,
                ci.user_id,
                ci.product_id,
                ci.product_size_id,
                ci.quantity,
                ci.price as unit_price,
                p.name as product_name,
                ps.size
            FROM Cart_Items ci 
            JOIN Products p ON ci.product_id = p.product_id
            JOIN Product_Sizes ps ON ci.product_size_id = ps.product_size_id
            WHERE ci.user_id = %s
        """, (session['user_id'],))
        cart_items = cur.fetchall()
        
        if not cart_items:
            flash('Your cart is empty!', 'error')
            return redirect(url_for('cart'))
        
        # Get user info for pre-filling
        cur.execute("SELECT * FROM Users WHERE user_id = %s", (session['user_id'],))
        user = cur.fetchone()
        
        # Calculate totals using the correct indices
        # cart_items[4] is quantity and cart_items[5] is unit_price
        subtotal = sum(item[4] * item[5] for item in cart_items)
        shipping = 10.00  # Fixed shipping fee
        tax = subtotal * 0.025  # 2.5% tax
        total = subtotal + shipping + tax
        
        return render_template('checkoutpage.html',
                             cart_items=cart_items,
                             user=user,
                             subtotal=subtotal,
                             shipping=shipping,
                             tax=tax,
                             total=total)
    except Exception as e:
        flash(f'Error loading checkout: {str(e)}', 'error')
        return redirect(url_for('cart'))
    finally:
        cur.close()

@app.route('/orders')
@login_required
def orders():
    cur = mysql.connection.cursor()
    try:
        
        cur.execute("""
            SELECT 
                o.order_id,
                o.order_date,
                o.total_amount,
                o.shipping_address,
                o.payment_method,
                o.order_status,
                o.shipping_fee,
                o.tax_amount
            FROM Orders o
            WHERE o.user_id = %s
            ORDER BY o.order_date DESC
        """, (session['user_id'],))
        
        orders_data = cur.fetchall()
        orders = []
        
        for order in orders_data:
            
            cur.execute("""
                SELECT 
                    oi.order_item_id,
                    p.name as product_name,
                    ps.size,
                    oi.quantity,
                    oi.price_per_unit,
                    p.image_url  -- Added image_url
                FROM Order_Items oi
                JOIN Products p ON oi.product_id = p.product_id
                JOIN Product_Sizes ps ON oi.product_size_id = ps.product_size_id
                WHERE oi.order_id = %s
            """, (order[0],))
            
            items = cur.fetchall()
            
            
            order_dict = {
                'order_id': order[0],
                'order_date': order[1],
                'total_amount': float(order[2]),
                'shipping_address': order[3],
                'payment_method': order[4],
                'order_status': order[5],
                'shipping_fee': float(order[6]),
                'tax_amount': float(order[7]),
                'items': [
                    {
                        'order_item_id': item[0],
                        'product_name': item[1],
                        'size': item[2],
                        'quantity': item[3],
                        'price_per_unit': float(item[4]),
                        'image_url': item[5] if item[5] else '/static/images/placeholder.jpg' 
                        
                    } for item in items
                ]
            }
            orders.append(order_dict)
        
        return render_template('orders.html', orders=orders)
    except Exception as e:
        flash(f'Error loading orders: {str(e)}', 'error')
        return redirect(url_for('index'))
    finally:
        cur.close()

@app.route('/place_order', methods=['POST'])
@login_required
def place_order():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        try:
            # Debug: Print form data
            print("Form Data:", request.form)
            print("Raw Address:", request.form.get('address'))
            
            # Get cart items and verify they exist
            cur.execute("""
                SELECT 
                    ci.cart_item_id,
                    ci.product_id,
                    ci.product_size_id,
                    ci.quantity,
                    ci.price,
                    ps.stock_quantity
                FROM Cart_Items ci
                JOIN Product_Sizes ps ON ci.product_size_id = ps.product_size_id
                WHERE ci.user_id = %s
            """, (session['user_id'],))
            
            cart_items = cur.fetchall()
            if not cart_items:
                flash('Your cart is empty!', 'error')
                return redirect(url_for('cart'))
            
            # Verify stock availability
            for item in cart_items:
                if item[3] > item[5]:
                    flash(f'Some items are no longer in stock in the requested quantity.', 'error')
                    return redirect(url_for('cart'))
            
            # Calculate totals
            subtotal = sum(item[3] * item[4] for item in cart_items)
            shipping_fee = 10.00
            tax_amount = subtotal * 0.08
            total_amount = subtotal + shipping_fee + tax_amount
            
            # Get shipping address directly from form
            shipping_address = request.form.get('address')
            # Debug: Print address before storage
            print("Address before storage:", shipping_address)
            
            payment_method = request.form.get('payment_method')
            
            # Validate required fields
            if not shipping_address:
                flash('Please provide a shipping address', 'error')
                return redirect(url_for('checkout'))
            
            if not payment_method:
                flash('Please select a payment method', 'error')
                return redirect(url_for('checkout'))
            
            # Debug: Print values before database insertion
            print("Values for insertion:")
            print(f"User ID: {session['user_id']}")
            print(f"Total Amount: {total_amount}")
            print(f"Shipping Address: {shipping_address}")
            print(f"Payment Method: {payment_method}")
            
            # Insert order with explicit column names
            cur.execute("""
                INSERT INTO Orders 
                (user_id, total_amount, shipping_address, payment_method, shipping_fee, tax_amount, order_status)
                VALUES 
                (%s, %s, %s, %s, %s, %s, 'processing')
            """, (
                session['user_id'],
                total_amount,
                shipping_address,  # Raw address, no transformation
                payment_method,
                shipping_fee,
                tax_amount
            ))
            
            order_id = cur.connection.insert_id()
            
            # After insertion, verify the stored address
            cur.execute("SELECT shipping_address FROM Orders WHERE order_id = %s", (order_id,))
            stored_address = cur.fetchone()[0]
            print("Stored address:", stored_address)
            
            # Process order items
            for item in cart_items:
                cur.execute("""
                    INSERT INTO Order_Items 
                    (order_id, product_id, product_size_id, quantity, price_per_unit)
                    VALUES (%s, %s, %s, %s, %s)
                """, (order_id, item[1], item[2], item[3], item[4]))
                
                cur.execute("""
                    UPDATE Product_Sizes 
                    SET stock_quantity = stock_quantity - %s
                    WHERE product_size_id = %s
                """, (item[3], item[2]))
            
            # Clear cart
            cur.execute("DELETE FROM Cart_Items WHERE user_id = %s", (session['user_id'],))
            
            mysql.connection.commit()
            flash('Order placed successfully! You can track your order in the Orders section.', 'success')
            return redirect(url_for('orders'))
            
        except Exception as e:
            mysql.connection.rollback()
            print("Error occurred:", str(e))  # Debug: Print any errors
            flash(f'Error placing order: {str(e)}', 'error')
            return redirect(url_for('checkout'))
        finally:
            cur.close()
    
    return redirect(url_for('checkout'))

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)