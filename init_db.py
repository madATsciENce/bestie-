import sqlite3
from werkzeug.security import generate_password_hash

def initialize_database():
    # Connect to (or create) the database file
    conn = sqlite3.connect('memories.db')
    cursor = conn.cursor()

    # Create Users Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(50) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        join_date DATE DEFAULT CURRENT_DATE
    )
    ''')

    # Create Memories Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Memories (
        memory_id INTEGER PRIMARY KEY AUTOINCREMENT,
        uploaded_by INTEGER,
        media_url VARCHAR(500) NOT NULL,
        media_type VARCHAR(10) CHECK (media_type IN ('photo', 'video')),
        caption TEXT,
        memory_date DATE,
        upload_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (uploaded_by) REFERENCES Users(user_id)
    )
    ''')

    # Create Events Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Events (
        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_name VARCHAR(100) NOT NULL,
        target_date DATE NOT NULL,
        event_type VARCHAR(50)
    )
    ''')

    # --- Seed Initial Data ---
    # Create two secure users: you and your best friend
    sushmita_pass = generate_password_hash("change_this_password_later")
    bestie_pass = generate_password_hash("change_this_password_too")
    
    # We use INSERT OR IGNORE so it doesn't crash if you run the script twice
    cursor.execute("INSERT OR IGNORE INTO Users (username, password_hash) VALUES ('Sushmita', ?)", (sushmita_pass,))
    cursor.execute("INSERT OR IGNORE INTO Users (username, password_hash) VALUES ('Bestie', ?)", (bestie_pass,))

    # Add a sample countdown event
    cursor.execute("INSERT OR IGNORE INTO Events (event_name, target_date, event_type) VALUES ('Bestieversary', '2026-08-15', 'anniversary')")

    # Save and close
    conn.commit()
    conn.close()
    print("Database 'memories.db' successfully created and seeded!")

if __name__ == '__main__':
    initialize_database()
    
# Create Open When Letters Table
    conn = sqlite3.connect('memories.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS OpenWhen (
        letter_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(100) NOT NULL,
        message TEXT NOT NULL,
        image_url VARCHAR(500)
    )
    ''')

    # Seed some sample letters
    cursor.execute("INSERT OR IGNORE INTO OpenWhen (title, message) VALUES ('you miss me', 'Hey bestie! Distance means nothing when someone means everything. I miss you too! 💙')")
    cursor.execute("INSERT OR IGNORE INTO OpenWhen (title, message) VALUES ('you are sad', 'Take a deep breath. You are the strongest person I know. I am always here for you.')")
    cursor.execute("INSERT OR IGNORE INTO OpenWhen (title, message) VALUES ('we fight', 'I hate fighting with you. You are my favorite person. Let us talk it out, okay?')")
    conn.close()