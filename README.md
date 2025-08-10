# RentTracker

A simple web application to manage tenants, track rent collection, and view payment history.  
Built with **Python Flask** and **SQLite**, with a minimal HTML frontend.
Features
- Tenant Management
  - Add new tenants
  - View list of tenants
  - Deactivate tenants
- Rent Tracking
  - Record rent payments
  - View payment history
- Lightweight Backend
  - REST API with JSON responses
  - SQLite database (no external DB setup required)
  - Easy to deploy and extend

Requirements
- Python 3.8+
- pip (Python package installer)
Installation
python -m venv venv
# Activate:
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
pip install -r requirements.txt

 Clone the repository
   ```bash
   git clone https://github.com/yourusername/rentracker.git
   cd rentracker
python -m venv venv

source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
pip install -r requirements.txt
```
File structure:
rentracker/
│
├── app.py                 # Main Flask application with routes & API
├── init_db.py              # Script to create SQLite database & tables
├── requirements.txt        # Python dependencies
├── renttracker.db          # SQLite database file (created after init_db.py)
│
├── templates/              # HTML templates (Jinja2)
│   ├── base.html           # Common layout (navbar, footer)
│   ├── home.html           # Home/dashboard page
│   ├── tenants.html        # List + add tenants page
│   └── payments.html       # List + add payments page
│
├── static/                 # CSS, JS, images
│   ├── styles.css          # Basic styling
│   └── script.js           # (Optional) Frontend JavaScript
│
└── README.md               # Project documentation

