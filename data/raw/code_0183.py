import sqlite3

def manage_database():
    conn = sqlite3.connect('local_server.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL,
            category TEXT
        )
    ''')
    
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_category ON products(category)')

    cursor.execute('INSERT INTO products (name, price, category) VALUES (?, ?, ?)', ('Laptop', 1200.0, 'Electronics'))
    conn.commit()

    cursor.execute('SELECT * FROM products WHERE category = ?', ('Electronics',))
    rows = cursor.fetchall()

    cursor.execute('UPDATE products SET price = ? WHERE name = ?', (1100.0, 'Laptop'))
    cursor.execute('DELETE FROM products WHERE id = ?', (1,))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    manage_database()