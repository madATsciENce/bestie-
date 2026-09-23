import os
from flask import Flask, render_template, request, redirect, url_for, flash
import cloudinary
import cloudinary.uploader
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()  # reads your .env file

app = Flask(__name__)
app.secret_key = "super_secret_key_for_sessions"

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# --- Cloudinary config (reads from .env) ---
cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key=os.environ.get('CLOUDINARY_API_KEY'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET')
)

# --- Postgres connection (reads from .env) ---
DATABASE_URL = os.environ.get('DATABASE_URL')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=psycopg2.extras.RealDictCursor)
    return conn

# --- ROUTES ---

@app.route('/')
def home():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Events')
    events = cur.fetchall()
    cur.execute('SELECT * FROM OpenWhen')
    letters = cur.fetchall()
    cur.execute("SELECT * FROM Memories WHERE media_type='photo' ORDER BY upload_timestamp DESC")
    photos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', events=events, letters=letters, photos=photos)

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
        # Upload directly to Cloudinary — no local saving at all
        upload_result = cloudinary.uploader.upload(file)
        image_url = upload_result['secure_url']  # this is the permanent photo link

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO Memories (media_url, media_type, caption) VALUES (%s, %s, %s)',
            (image_url, 'photo', caption)
        )
        conn.commit()
        cur.close()
        conn.close()

        flash('Photo memory added successfully!')
        return redirect(url_for('home'))
    else:
        flash('Allowed file types are png, jpg, jpeg, gif!')
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)