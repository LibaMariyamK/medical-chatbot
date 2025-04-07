import sqlite3

def init_db():
    conn = sqlite3.connect('health_data.db')
    c = conn.cursor()
    # Users table for authentication
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password TEXT
    )''')
    # Health data table linked to users
    c.execute('''CREATE TABLE IF NOT EXISTS health_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT,
        age INTEGER,
        height REAL,
        weight REAL,
        bmi REAL,
        blood_group TEXT,
        symptoms TEXT,
        timestamp TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )''')
    conn.commit()
    conn.close()

def save_user(email, hashed_password):
    conn = sqlite3.connect('health_data.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, hashed_password))
    conn.commit()
    conn.close()

def authenticate_user(email):
    conn = sqlite3.connect('health_data.db')
    c = conn.cursor()
    c.execute('SELECT id, password FROM users WHERE email = ?', (email,))
    user = c.fetchone()
    conn.close()
    if user:
        return {'id': user[0], 'password': user[1]}
    return None

def save_health_data(data):
    conn = sqlite3.connect('health_data.db')
    c = conn.cursor()
    c.execute('''INSERT INTO health_data (user_id, name, age, height, weight, bmi, blood_group, symptoms, timestamp)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (data['user_id'], data['name'], data['age'], data['height'], data['weight'], data['bmi'],
               data['blood_group'], data['symptoms'], data['timestamp']))
    conn.commit()
    conn.close()

def get_health_data(user_id):
    conn = sqlite3.connect('health_data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM health_data WHERE user_id = ? ORDER BY timestamp DESC LIMIT 1', (user_id,))
    data = c.fetchone()
    conn.close()
    if data:
        return dict(zip(['id', 'user_id', 'name', 'age', 'height', 'weight', 'bmi', 'blood_group', 'symptoms', 'timestamp'], data))
    return "No data found."