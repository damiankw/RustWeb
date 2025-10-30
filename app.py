from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
import sqlite3
import os
import hashlib

app = Flask(__name__)

# Database setup
def init_db():
    # Check if the database file exists
    # If not, create it and the necessary tables
    if not os.path.exists('rustweb.db'):
        create_rustweb_db()

    # Update the RustWeb database with running information
    

def create_rustweb_db():
    # Create the logs table
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT,
                created_at datetime not null default(current_timestamp)
            )
        ''')

    write_db_log('Initialised RustWeb database')
    write_db_log('Created Logs table')

    # Create the devices table
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE devices (
                id VARCHAR(100) PRIMARY KEY,
                name TEXT,
                password TEXT,
                notes TEXT
            )
        ''')

    write_db_log('Created Devices table')

    # Add initial devices to the devices table
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO devices (id)
        SELECT id
        FROM rustdesk.peer;
        ''')

    write_db_log('Imported RustDesk devices')

    # Create the settings table
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT,
                value TEXT
            )
        ''')

    write_db_log('Created Settings table')

    with get_db_connection() as conn:
        cursor = conn.cursor()
        hashed_password = hashlib.sha256("admin".encode()).hexdigest()
        cursor.execute("INSERT INTO settings (key, value) VALUES ('username', 'admin')")
        cursor.execute("INSERT INTO settings (key, value) VALUES ('password', ?)", (hashed_password,))
        cursor.execute("INSERT INTO settings (key, value) VALUES ('created_at', CURRENT_TIMESTAMP)")

    write_db_log('Updated initialisation settings')

# Helper function to manage database connections
def get_db_connection():
    conn = sqlite3.connect('rustweb.db')
    conn.row_factory = sqlite3.Row  # Enable named column access

    cursor = conn.cursor()

    cursor.execute(f"ATTACH DATABASE '/opt/rustdesk/db_v2.sqlite3' AS rustdesk")
    return conn

def get_db_devices():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT peer.id, peer.created_at, devices.name, devices.password, devices.notes, peer.status FROM peer, devices WHERE (peer.id = devices.id)")
        devices = cursor.fetchall()
    return devices

def get_db_logs():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM logs ORDER BY created_at DESC LIMIT 20")
        logs = cursor.fetchall()
    return logs

def write_db_log(action):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO logs (action) VALUES (?)", (action,))  # Fixed tuple issue
        conn.commit()

@app.route('/')
def index():
    # get devices from the database
    devices = get_db_devices()

    # get logs from the database
    logs = get_db_logs()
    return render_template('index.html', devices=devices, logs=logs)


@app.route('/add', methods=['POST'])
def add_device():
    name = request.form['name']
    status = request.form['status']
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO devices (name, status) VALUES (?, ?)', (name, status))
        conn.commit()
    return redirect(url_for('index'))

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(os.path.join(app.root_path, 'templates/images'), filename)

@app.route('/update_device', methods=['POST'])
def update_device():
    data = request.get_json()
    device_id = data.get('id')
    name = data.get('name')
    password = data.get('password')
    notes = data.get('notes')

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE devices
            SET name = ?, password = ?, notes = ?
            WHERE id = ?
        ''', (name, password, notes, device_id))
        conn.commit()

    write_db_log(f'Updated device {device_id} (name: {name}, password: {password}, notes: {notes})')

    return {'status': 'success', 'message': 'Device updated successfully'}

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=9000, debug=True)
