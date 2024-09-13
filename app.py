# app.py
# flask run  --host=127.0.0.1 --port=5000
# flask run

import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from PIL import Image
import pytesseract
from werkzeug.utils import secure_filename
import sqlite3
from functools import wraps
import subprocess
import exifread
#from jinja2.environment import Environment


app = Flask(__name__)
app.secret_key = os.urandom(24)

UPLOAD_FOLDER = 'temp'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_db():
    db = sqlite3.connect('ocr_data.db')
    db.row_factory = sqlite3.Row
    return db


def init_db():
    db = get_db()
    db.execute('CREATE TABLE IF NOT EXISTS ocr_results (id INTEGER PRIMARY KEY, text TEXT, filename TEXT, width INTEGER, height INTEGER, format TEXT, exif_data TEXT)')
    db.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)')
    db.commit()

init_db()


def create_admin_user(username, password):
    db = get_db()
    try:
        db.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        db.commit()
        print(f"Usuario administrador '{username}' creado con éxito.")
    except sqlite3.IntegrityError:
        print(f"El usuario '{username}' ya existe.")
    finally:
        db.close()

create_admin_user('admin', 'password123')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_json(value):
  try:
    import json
    json.loads(value)
    return True
  except (ValueError, TypeError):
    return False

# Register custom filter with the Jinja2 environment (optional)
app.jinja_env.filters['is_json'] = is_json  # uncomment this line if using custom filter

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        try:
            # Open image for OCR processing
            with Image.open(filepath) as img:
                text = pytesseract.image_to_string(img)
                width, height = img.size
                format = img.format

            # Extract EXIF data using ExifTool
            exif_process = subprocess.Popen(['exiftool', filepath], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            exif_output, _ = exif_process.communicate()
            exif_data = exif_output.decode('utf-8')  # Decode byte output

            # Parse EXIF data (optional)
            # You can use libraries like 'exifread' to parse the raw data into a structured format (dictionary)
            # exif_data_dict = exifread.process_file(open(filepath, 'rb'))
            # with open(filepath, 'rb') as f:
            #     tags = exifread.process_file(f)
            #     exif_data_dict = dict(tags)


            db = get_db()

            try:
                db.execute('INSERT INTO ocr_results (text, filename, width, height, format, exif_data) VALUES (?, ?, ?, ?, ?, ?)',
                           (text, filename, width, height, format, exif_data))
                           #(text, filename, width, height, format, json.dumps(exif_data_dict)))
                db.commit()
            finally:
                db.close()

            os.remove(filepath)  # Remove the temporary file
            # Return data as JSON
            return jsonify({'text': text, 'exif_data': exif_data})  # or exif_data_dict if parsed
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'File type not allowed'}), 400

@app.route('/admin')
@login_required
def admin():
    db = get_db()
    try:
        results = db.execute('SELECT * FROM ocr_results ORDER BY id DESC').fetchall()
    finally:
        db.close()
    return render_template('admin.html', results=results)

@app.route('/admin/delete/<int:id>', methods=['POST'])
@login_required
def delete_result(id):
    db = get_db()
    try:
        db.execute('DELETE FROM ocr_results WHERE id = ?', (id,))
        db.commit()
    finally:
        db.close()
    return redirect(url_for('admin'))

@app.route('/admin/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_result(id):
    db = get_db()
    if request.method == 'POST':
        text = request.form['text']
        try:
            db.execute('UPDATE ocr_results SET text = ? WHERE id = ?', (text, id))
            db.commit()
        finally:
            db.close()
        return redirect(url_for('admin'))
    try:
        result = db.execute('SELECT * FROM ocr_results WHERE id = ?', (id,)).fetchone()
    finally:
        db.close()
    return render_template('edit.html', result=result)

@app.route('/admin/details/<int:id>', methods=['GET'])
@login_required
def view_details(id):
    db = get_db()

    try:
        result = db.execute('SELECT * FROM ocr_results WHERE id = ?', (id,)).fetchone()
    finally:
        db.close()

    if result:
        return render_template('details.html', result=result)
    else:
        return render_template('error.html', message='Record not found')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        try:
            user = db.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        finally:
            db.close()
        if user:
            session['username'] = username
            return redirect(url_for('admin'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    init_db()

    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    # app.run(debug=True)
    app.run(debug=True, ssl_context='adhoc')
