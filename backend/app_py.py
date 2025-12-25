from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import subprocess
import os
import sys
import sqlite3
from datetime import datetime
from contextlib import contextmanager

# Import chatbot module
try:
    from chatbot import initialize_chatbot, get_response
    CHATBOT_AVAILABLE = True
except ImportError:
    print("Warning: chatbot module not found. Chat feature will be disabled.")
    CHATBOT_AVAILABLE = False

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
CORS(app)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Detect OS and set executable name
if os.name == 'nt':  # Windows
    CPP_EXE_NAME = "ds.exe"
else:  # Linux/Unix
    CPP_EXE_NAME = "ds"
CPP_EXE = os.path.join(SCRIPT_DIR, CPP_EXE_NAME)
DB_FILE = os.path.join(SCRIPT_DIR, "hospital_queue.db")

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

def call_cpp(*args):
    try:
        result = subprocess.run([CPP_EXE, *args],
                                capture_output=True,
                                text=True,
                                check=True,
                                cwd=SCRIPT_DIR,
                                timeout=10)
        return {"success": True, "output": result.stdout.strip()}
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "C++ executable timed out"}
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else str(e)
        return {"success": False, "error": error_msg, "output": e.stdout.strip() if e.stdout else ""}
    except FileNotFoundError:
        return {"success": False, "error": f"Executable not found: {CPP_EXE}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

# Queue management functions
def read_queue():
    patients = []
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name, age, priority FROM patients WHERE status = 'queued' "
                "ORDER BY priority ASC, age DESC, id ASC"
            )
            rows = cursor.fetchall()
            patients = [{"id": row[0], "name": row[1], "age": row[2], "priority": row[3]} for row in rows]
    except Exception as e:
        print(f"Error reading queue from database: {e}")
    return patients

def read_served():
    patients = []
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name, age, priority FROM patients WHERE status = 'served' "
                "ORDER BY served_at DESC"
            )
            rows = cursor.fetchall()
            patients = [{"id": row[0], "name": row[1], "age": row[2], "priority": row[3]} for row in rows]
    except Exception as e:
        print(f"Error reading served from database: {e}")
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
    
    if not name:
        return jsonify({"success": False, "error": "Name is required"}), 400
    if not age or not priority:
        return jsonify({"success": False, "error": "Age and priority are required"}), 400
    
    try:
        age = int(age)
        priority = int(priority)
        if age < 1 or age > 150:
            return jsonify({"success": False, "error": "Age must be between 1 and 150"}), 400
        if priority not in [1, 2, 3]:
            return jsonify({"success": False, "error": "Priority must be 1, 2, or 3"}), 400
    except (ValueError, TypeError):
        return jsonify({"success": False, "error": "Age and priority must be valid numbers"}), 400
    
    result = call_cpp('add', name, str(age), str(priority))
    if result["success"]:
        return jsonify({**result, "queue": read_queue()})
    else:
        return jsonify(result), 500

@app.route('/api/serve', methods=['POST'])
def serve_patient():
    result = call_cpp('serve')
    if result["success"]:
        return jsonify({**result, "queue": read_queue(), "served": read_served()})
    else:
        return jsonify(result), 500

@app.route('/api/sort', methods=['POST'])
def sort_queue():
    result = call_cpp('sort')
    if result["success"]:
        return jsonify({**result, "queue": read_queue()})
    else:
        return jsonify(result), 500

@app.route('/api/clear', methods=['POST'])
def clear_queue():
    result = call_cpp('clear')
    if result["success"]:
        return jsonify({**result, "queue": read_queue(), "served": read_served()})
    else:
        return jsonify(result), 500

@app.route('/api/export', methods=['GET'])
def export_data():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name, age, priority, status, created_at, served_at "
                "FROM patients ORDER BY created_at ASC"
            )
            rows = cursor.fetchall()
            
            patients_data = [{
                "id": row[0],
                "name": row[1],
                "age": row[2],
                "priority": row[3],
                "status": row[4],
                "created_at": row[5],
                "served_at": row[6]
            } for row in rows]

            queued_count = sum(1 for p in patients_data if p["status"] == "queued")
            served_count = sum(1 for p in patients_data if p["status"] == "served")

            return jsonify({
                "success": True,
                "patients": patients_data,
                "timestamp": datetime.now().isoformat(),
                "total_patients": len(patients_data),
                "queued_count": queued_count,
                "served_count": served_count
            })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/display', methods=['GET'])
def display_queue():
    result = call_cpp('display')
    return jsonify(result)

@app.route('/api/remove_served', methods=['POST'])
def remove_served():
    if not request.is_json:
        return jsonify({"success": False, "error": "Request must be JSON"}), 400
    
    data = request.json or {}
    patient_id = data.get('id')

    if not patient_id:
        return jsonify({"success": False, "error": "Missing patient ID"}), 400
    
    try:
        patient_id = int(patient_id)
    except (ValueError, TypeError):
        return jsonify({"success": False, "error": "Patient ID must be a valid number"}), 400

    result = call_cpp('remove_served', str(patient_id))
    if result["success"]:
        return jsonify({**result, "served": read_served()})
    else:
        return jsonify(result), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    if not CHATBOT_AVAILABLE:
        return jsonify({"success": False, "error": "Chatbot module not available"}), 503
    
    if not request.is_json:
        return jsonify({"success": False, "error": "Request must be JSON"}), 400
    
    data = request.json or {}
    message = data.get('message', '').strip()
    
    if not message:
        return jsonify({"success": False, "error": "Message is required"}), 400
    
    try:
        response = get_response(message)
        return jsonify({"success": True, "response": response})
    except Exception as e:
        print(f"Error in chatbot: {e}")
        return jsonify({
            "success": False,
            "error": "An error occurred while processing your message",
            "response": "I'm sorry, I encountered an error. Please try again."
        }), 500

if __name__ == '__main__':
    print("=" * 60)
    print("🏥 PATIENT QUEUE SYSTEM - SERVER STARTING")
    print("=" * 60)

    # Check C++ executable
    if not os.path.exists(CPP_EXE):
        print(f"❌ ERROR: {CPP_EXE_NAME} not found at: {CPP_EXE}")
        sys.exit(1)
    else:
        print(f"✅ Found {CPP_EXE_NAME}: {CPP_EXE}")

    # Initialize database if it doesn't exist
    if not os.path.exists(DB_FILE):
        print(f"📊 Initializing database: {DB_FILE}")
        try:
            schema_path = os.path.join(SCRIPT_DIR, "init_db.sql")
            if not os.path.exists(schema_path):
                print(f"❌ ERROR: init_db.sql not found at: {schema_path}")
                sys.exit(1)

            with get_db_connection() as conn:
                cursor = conn.cursor()
                with open(schema_path, 'r') as f:
                    cursor.executescript(f.read())
                conn.commit()
            print("✅ Database initialized")
        except Exception as e:
            print(f"❌ Error initializing database: {e}")
            sys.exit(1)
    else:
        print(f"✅ Found database: {DB_FILE}")

    # Initialize chatbot
    if CHATBOT_AVAILABLE:
        try:
            chatbot_initialized = initialize_chatbot(DB_FILE, "intents.json")
            if chatbot_initialized:
                print("✅ Chatbot initialized successfully")
            else:
                print("⚠️ Chatbot initialization failed, continuing...")
        except Exception as e:
            print(f"⚠️ Error initializing chatbot: {e}")
            print("   Chat feature may not work properly")
    else:
        print("⚠️ Chatbot module not available - chat feature disabled")

    print("=" * 60)
    port = int(os.environ.get("PORT", 5000))  # Railway-friendly port
    print(f"🌐 SERVER RUNNING AT: http://0.0.0.0:{port}")
    app.run(debug=True, host='0.0.0.0', port=port)
