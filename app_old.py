import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)
app.secret_key = "super_secret_key_for_sessions"

# --- NEW CLOUD-PROOF FILE PATHS ---
# This tells Python to find the absolute path of wherever the app is hosted
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# We attach the base directory to your uploads folder and database
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
DATABASE = os.path.join(BASE_DIR, 'memories.db')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the uploads folder exists when the app starts
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Helper to check if a filename is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Helper function to connect to the database 
def get_db_connection():
    # UPDATED: Now it uses the cloud-proof DATABASE path!
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row 
    return conn

# --- ROUTES ---

# 1. The main homepage route
@app.route('/')
def home():
    conn = get_db_connection()
    events = conn.execute('SELECT * FROM Events').fetchall()
    letters = conn.execute('SELECT * FROM OpenWhen').fetchall()
    
    # Fetch photos to display in your gallery!
    photos = conn.execute("SELECT * FROM Memories WHERE media_type='photo' ORDER BY upload_timestamp DESC").fetchall()
    
    conn.close()
    
    # We pass 'photos' to the HTML now too
    return render_template('index.html', events=events, letters=letters, photos=photos)

# 2. Route to handle photo uploads from the form
@app.route('/add_photo', methods=['POST'])
def add_photo():
    if 'photo_file' not in request.files:
        flash('No file selected!')
        return redirect(url_for('home'))
        
    file = request.files['photo_file']
    caption = request.form.get('caption', '') 
    
    if file.filename == '':
        flash('No file selected!')
        return redirect(url_for('home'))
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save file to your computer or cloud server
        file.save(filepath)
        
        # Save reference to the database
        conn = get_db_connection()
        conn.execute('INSERT INTO Memories (media_url, media_type, caption) VALUES (?, ?, ?)',
                    (filename, 'photo', caption))
        conn.commit()
        conn.close()
        
        flash('Photo memory added successfully!')
        return redirect(url_for('home'))
    else:
        flash('Allowed file types are png, jpg, jpeg, gif!')
        return redirect(url_for('home'))

# 3. Route to serve the image so the HTML can see it
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)