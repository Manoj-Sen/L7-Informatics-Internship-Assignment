import sqlite3

def create_tables():
    conn = sqlite3.connect('ice_cream_parlor.db')
    cursor = conn.cursor()

    # Create Seasonal Flavors table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS seasonal_flavors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL
    )
    ''')

    # Create Cart table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cart (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        flavor_id INTEGER,
        FOREIGN KEY (flavor_id) REFERENCES seasonal_flavors(id)
    )
    ''')

    conn.commit()
    conn.close()

def add_seasonal_flavor(name, description, price):
    conn = sqlite3.connect('ice_cream_parlor.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO seasonal_flavors (name, description, price)
    VALUES (?, ?, ?)
    ''', (name, description, price))
    conn.commit()
    conn.close()

def add_to_cart(flavor_id):
    try:
        flavor_id = int(flavor_id)
    except ValueError:
        print("Invalid flavor ID. Please enter a valid integer.")
        return
    
    conn = sqlite3.connect('ice_cream_parlor.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO cart (flavor_id)
    VALUES (?)
    ''', (flavor_id,))
    conn.commit()
    conn.close()

def view_cart():
    conn = sqlite3.connect('ice_cream_parlor.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT seasonal_flavors.id, seasonal_flavors.name, seasonal_flavors.price
    FROM cart
    JOIN seasonal_flavors ON cart.flavor_id = seasonal_flavors.id
    ''')
    cart = cursor.fetchall()
    
    cursor.execute('''
    SELECT SUM(seasonal_flavors.price)
    FROM cart
    JOIN seasonal_flavors ON cart.flavor_id = seasonal_flavors.id
    ''')
    total_price = cursor.fetchone()[0]
    
    conn.close()
    return cart, total_price

def search_seasonal_flavors(keyword=None):
    conn = sqlite3.connect('ice_cream_parlor.db')
    cursor = conn.cursor()
    query = "SELECT * FROM seasonal_flavors WHERE 1=1"
    params = []

    if keyword:
        query += " AND name LIKE ?"
        params.append(f"%{keyword}%")

    cursor.execute(query, params)
    flavors = cursor.fetchall()
    conn.close()
    return flavors

def view_seasonal_flavors():
    conn = sqlite3.connect('ice_cream_parlor.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM seasonal_flavors')
    flavors = cursor.fetchall()
    conn.close()
    return flavors

def populate_initial_data():
    conn = sqlite3.connect('ice_cream_parlor.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM seasonal_flavors')
    count = cursor.fetchone()[0]

    if count == 0:
        flavors = [
            ('Vanilla Delight', 'Classic vanilla ice cream', 300),
            ('Chocolate Heaven', 'Rich chocolate ice cream', 200),
            ('Strawberry Surprise', 'Fresh strawberry ice cream', 284),
            ('Minty Fresh', 'Cool mint ice cream',160),
            ('Caramel Crunch', 'Caramel ice cream with crunchy bits', 210),
            ('Cookies and Cream', 'Cookies and cream ice cream', 305),
            ('Pistachio Paradise', 'Pistachio flavored ice cream', 120),
        ]
        for flavor in flavors:
            add_seasonal_flavor(*flavor)
    
    conn.close()

def clear_cart():
    conn = sqlite3.connect('ice_cream_parlor.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM cart')
    conn.commit()
    conn.close()
