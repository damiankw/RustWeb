# RustDesk Web Console

This project provides a web-based console for managing RustDesk Server OSS devices. It allows you to see all devices that are connected to your private network as well as add a device name, password and additional notes to the connection.

The application integrates directly into RustDesk database itself and provides real-time up to date client information.

## Features
- View and manage RustDesk devices.
- Log connections and device updates.
- Search and filter devices dynamically.

## Prerequisites
- Python 3.8 or higher
- SQLite3
- RustDesk database (`/opt/rustdesk/db_v2.sqlite3`)

## Installation

1. **Clone the Repository**
   Although it doesn't need to run in the /opt, it is recommended to be put into /opt/RustWeb so it conforms with how RustDesk natively works.
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

5. **Run the Application**
   Start the application with Python
   ```bash
   python app.py
   ```
   The web console will be accessible at `http://localhost:9000`.

## File Structure
- `app.py`: Python application for integrating with databases.
- `templates/`: HTML templates for the frontend.
- `requirements.txt`: Python dependencies.

## Notes
- The RustDesk database (`db_v2.sqlite3`) must be present at `/opt/rustdesk/`.
- This project uses Flask as the web server which throws a warning about it being a development server. This is not an issue due to the weight of the application.

## Troubleshooting
- **Database Errors**: Ensure the RustDesk database path is correct and accessible.
- **Missing Dependencies**: Reinstall the required packages using `pip install -r requirements.txt`.
- **Port Conflicts**: Change the port in `app.run()` in `app.py` if `9000` is in use.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

For further assistance, please contact the repository owner.