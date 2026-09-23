import os
import psycopg2
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv

load_dotenv()  # reads your .env file

DATABASE_URL = os.environ.get('DATABASE_URL')

def initialize_database():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    # Create Users Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        user_id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        join_date DATE DEFAULT CURRENT_DATE
    )
    ''')

    # Create Memories Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Memories (
        memory_id SERIAL PRIMARY KEY,
        uploaded_by INTEGER,
        media_url VARCHAR(500) NOT NULL,
        media_type VARCHAR(10) CHECK (media_type IN ('photo', 'video')),
        caption TEXT,
        memory_date DATE,
        upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (uploaded_by) REFERENCES Users(user_id)
    )
    ''')

    # Create Events Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Events (
        event_id SERIAL PRIMARY KEY,
        event_name VARCHAR(100) UNIQUE NOT NULL,
        target_date DATE NOT NULL,
        event_type VARCHAR(50)
    )
    ''')

    # Create Open When Letters Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS OpenWhen (
        letter_id SERIAL PRIMARY KEY,
        title VARCHAR(100) UNIQUE NOT NULL,
        message TEXT NOT NULL,
        image_url VARCHAR(500)
    )
    ''')

    # --- Seed Initial Data ---
    sushmita_pass = generate_password_hash("change_this_password_later")
    bestie_pass = generate_password_hash("change_this_password_too")

    cursor.execute(
        "INSERT INTO Users (username, password_hash) VALUES (%s, %s) ON CONFLICT (username) DO NOTHING",
        ('Sushmita', sushmita_pass)
    )
    cursor.execute(
        "INSERT INTO Users (username, password_hash) VALUES (%s, %s) ON CONFLICT (username) DO NOTHING",
        ('Bestie', bestie_pass)
    )

    cursor.execute(
        "INSERT INTO Events (event_name, target_date, event_type) VALUES (%s, %s, %s) ON CONFLICT (event_name) DO NOTHING",
        ('Bestieversary', '2026-08-15', 'anniversary')
    )

    cursor.execute(
        "INSERT INTO OpenWhen (title, message) VALUES (%s, %s) ON CONFLICT (title) DO NOTHING",
        ('you miss me', 'Hey bestie! Distance means nothing when someone means everything. I miss you too! 💙')
    )
    cursor.execute(
        "INSERT INTO OpenWhen (title, message) VALUES (%s, %s) ON CONFLICT (title) DO NOTHING",
        ('you are sad', 'Take a deep breath. You are the strongest person I know. I am always here for you.')
    )
    cursor.execute(
        "INSERT INTO OpenWhen (title, message) VALUES (%s, %s) ON CONFLICT (title) DO NOTHING",
        ('we fight', 'I hate fighting with you. You are my favorite person. Let us talk it out, okay?')
    )

    conn.commit()
    cursor.close()
    conn.close()
    print("Postgres database successfully set up and seeded!")

if __name__ == '__main__':
    initialize_database()