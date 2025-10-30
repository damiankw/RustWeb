# RustDesk Web Console

This project provides a web-based console for managing RustDesk devices. It includes a Flask backend and a dynamic frontend for seamless device management.

## Features
- View and manage RustDesk devices.
- Log connections and device updates.
- Search and filter devices dynamically.
- Edit device details and connect to devices directly.

## Prerequisites
- Python 3.8 or higher
- SQLite3
- RustDesk database (`db_v2.sqlite3`)
- Flask and required Python packages (see `requirements.txt`)

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/damiankw/RustWeb.git
   cd RustWeb
   ```

2. **Set Up the Python Environment**
   Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. **Prepare the Database**
   Ensure the RustDesk database (`db_v2.sqlite3`) is located at `/opt/rustdesk/`.
   Initialize the web console database:
   ```bash
   python -c 'from app import init_db; init_db()'
   ```

5. **Run the Application**
   Start the Flask development server:
   ```bash
   python app.py
   ```
   The web console will be accessible at `http://localhost:5000`.

## File Structure
- `app.py`: Main Flask application.
- `templates/`: HTML templates for the frontend.
- `static/`: Static files (CSS, JavaScript, images).
- `requirements.txt`: Python dependencies.

## Notes
- The RustDesk database (`db_v2.sqlite3`) must be present at `/opt/rustdesk/`.
- The Flask app runs in debug mode by default. For production, use a WSGI server like Gunicorn.

## Troubleshooting
- **Database Errors**: Ensure the RustDesk database path is correct and accessible.
- **Missing Dependencies**: Reinstall the required packages using `pip install -r requirements.txt`.
- **Port Conflicts**: Change the port in `app.run()` in `app.py` if `5000` is in use.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

For further assistance, please contact the repository owner.