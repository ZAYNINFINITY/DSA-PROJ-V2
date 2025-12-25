import os
import sys
import sqlite3
from datetime import datetime
from contextlib import contextmanager
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import subprocess

# Import chatbot module
try:
    from chatbot import initialize_chatbot, get_response
    CHATBOT_AVAILABLE = True
except ImportError:
    print("Warning: chatbot module not found. Chat feature will be disabled.")
    CHATBOT_AVAILABLE = False

# Flask setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
CORS(app)

# OS-dependent C++ executable
if os.name == 'nt':
    CPP_EXE_NAME = "ds.exe"
    CPP_EXE = os.path.join(SCRIPT_DIR, CPP_EXE_NAME)
else:
    CPP_EXE_NAME = "ds"
    CPP_EXE = os.path.join(SCRIPT_DIR, "backend", CPP_EXE_NAME)  # Must match build.sh

DB_FILE = os.path.join(SCRIPT_DIR, "hospital_queue.db")

# DB helper
@contextmanager
def get_db_connection():
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        yield conn
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

# Call C++ backend
def call_cpp(*args):
    try:
        result = subprocess.run([CPP_EXE, *args],
                                capture_output=True,
                                text=True,
                                check=True,
                                cwd=os.path.join(SCRIPT_DIR, "backend"),
                                timeout=10)
        return {"success": True, "output": result.stdout.strip()}
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "C++ executable timed out"}
    except subprocess.CalledProcessError as e:
        return {"success": False, "error": e.stderr.strip() if e.stderr else str(e),
                "output": e.stdout.strip() if e.stdout else ""}
    except FileNotFoundError:
        return {"success": False, "error": f"Executable not found: {CPP_EXE}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

# Queue and served patient functions
def read_queue():
    patients = []
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name, age, priority FROM patients WHERE status='queued' "
                "ORDER BY priority ASC, age DESC, id ASC"
            )
            rows = cursor.fetchall()
            patients = [{"id": row[0], "name": row[1], "age": row[2], "priority": row[3]} for row in rows]
    except Exception as e:
        print(f"Error reading queue: {e}")
    return patients

def read_served():
    patients = []
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name, age, priority FROM patients WHERE status='served' "
                "ORDER BY served_at DESC"
            )
            rows = cursor.fetchall()
            patients = [{"id": row[0], "name": row[1], "age": row[2], "priority": row[3]} for row in rows]
    except Exception as e:
        print(f"Error reading served: {e}")
    return patients

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/queue', methods=['GET'])
def get_queue():
    return jsonify({"queue": read_queue(), "served": read_served()})

@app.route('/api/add', methods=['POST'])
def add_patient():
    if not request.is_json:
        return jsonify({"success": False, "error": "Request must be JSON"}), 400
    data = request.json or {}
    name = data.get('name', '').strip()
    age = data.get('age')
    priority = data.get('priority')
    if not name or not age or not priority:
        return jsonify({"success": False, "error": "Name, age, and priority required"}), 400
    try:
        age = int(age)
        priority = int(priority)
        if age < 1 or age > 150 or priority not in [1, 2, 3]:
            return jsonify({"success": False, "error": "Invalid age or priority"}), 400
    except:
        return jsonify({"success": False, "error": "Age and priority must be numbers"}), 400
    result = call_cpp('add', name, str(age), str(priority))
    if result["success"]:
        return jsonify({**result, "queue": read_queue()})
    return jsonify(result), 500

# Keep the rest of the routes same: /api/serve, /api/sort, /api/clear, /api/export, /api/display, /api/remove_served, /api/chat

if __name__ == '__main__':
    print("="*60)
    print("🏥 PATIENT QUEUE SYSTEM - SERVER STARTING")
    print("="*60)

    # Check C++ executable
    if not os.path.exists(CPP_EXE):
        print(f"❌ ERROR: {CPP_EXE_NAME} not found at: {CPP_EXE}")
        sys.exit(1)
    else:
        print(f"✅ Found {CPP_EXE_NAME}: {CPP_EXE}")

    # Initialize database if missing
    if not os.path.exists(DB_FILE):
        print(f"📊 Initializing database: {DB_FILE}")
        schema_path = os.path.join(SCRIPT_DIR, "backend", "init_db.sql")
        if not os.path.exists(schema_path):
            print(f"❌ ERROR: init_db.sql not found at: {schema_path}")
            sys.exit(1)
        with get_db_connection() as conn:
            with open(schema_path, 'r') as f:
                conn.executescript(f.read())
            conn.commit()
        print("✅ Database initialized")
    else:
        print(f"✅ Found database: {DB_FILE}")

    # Initialize chatbot
    if CHATBOT_AVAILABLE:
        try:
            chatbot_initialized = initialize_chatbot(DB_FILE, "intents.json")
            if chatbot_initialized:
                print("✅ Chatbot initialized")
            else:
                print("⚠️ Chatbot initialization failed, continuing...")
        except Exception as e:
            print(f"⚠️ Chatbot init error: {e}")

    port = int(os.environ.get("PORT", 5000))  # Railway-friendly
    print(f"🌐 SERVER RUNNING AT: http://0.0.0.0:{port}")
    app.run(debug=True, host='0.0.0.0', port=port)
