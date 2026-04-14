import sqlite3

DB_NAME = "driveshare.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    db = get_db()
    cur = db.cursor()

    # USERS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password TEXT,
        q1 TEXT,
        q2 TEXT,
        q3 TEXT
    )
    """)

    # CARS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner_id INTEGER,
        model TEXT,
        year INTEGER,
        mileage INTEGER,
        location TEXT,
        price REAL,
        available TEXT
    )
    """)
    # BOOKINGS 
    cur.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        car_id INTEGER,
        user_id INTEGER,
        start_date TEXT,
        end_date TEXT,
        price REAL
    )
    """)

    # NOTIFACTIONS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        message TEXT,
        type TEXT
    )
    """)

    # WATCHES
    cur.execute("""
    CREATE TABLE IF NOT EXISTS watches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        car_id INTEGER,
        max_price REAL
    )
    """)

    db.commit()
    db.close()