from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import subprocess
import os
import sys
import sqlite3
from datetime import datetime

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
CORS(app)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CPP_EXE = os.path.join(SCRIPT_DIR, "ds.exe")
DB_FILE = os.path.join(SCRIPT_DIR, "hospital_queue.db")

def call_cpp(*args):
    """Call the C++ executable with arguments"""
    try:
        result = subprocess.run([CPP_EXE, *args],
                              capture_output=True,
                              text=True,
                              check=True,
                              cwd=SCRIPT_DIR)
        return {"success": True, "output": result.stdout}
    except subprocess.CalledProcessError as e:
        return {"success": False, "error": str(e), "output": e.stdout}
    except Exception as e:
        return {"success": False, "error": str(e)}

def read_queue():
    """Read current queue from database"""
    patients = []
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, age, priority FROM patients WHERE status = 'queued' ORDER BY priority ASC, age DESC, created_at ASC")
        rows = cursor.fetchall()
        for row in rows:
            patients.append({"id": row[0], "name": row[1], "age": row[2], "priority": row[3]})
        conn.close()
    except Exception as e:
        print(f"Error reading queue from database: {e}")

    return patients

def read_served():
    """Read served patients from database"""
    patients = []
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, age, priority FROM patients WHERE status = 'served' ORDER BY served_at DESC")
        rows = cursor.fetchall()
        for row in rows:
            patients.append({"id": row[0], "name": row[1], "age": row[2], "priority": row[3]})
        conn.close()
    except Exception as e:
        print(f"Error reading served from database: {e}")

    return patients



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/queue', methods=['GET'])
def get_queue():
    return jsonify({"queue": read_queue(), "served": read_served()})

@app.route('/api/add', methods=['POST'])
def add_patient():
    data = request.json
    name = data.get('name', '').strip()
    age = data.get('age')
    priority = data.get('priority')
    
    if not name or not age or not priority:
        return jsonify({"success": False, "error": "Missing required fields"}), 400
    
    try:
        age = int(age)
        priority = int(priority)
        if priority not in [1, 2, 3]:
            return jsonify({"success": False, "error": "Priority must be 1, 2, or 3"}), 400
    except ValueError:
        return jsonify({"success": False, "error": "Age and priority must be numbers"}), 400
    
    result = call_cpp('add', name, str(age), str(priority))
    return jsonify({**result, "queue": read_queue()})

@app.route('/api/serve', methods=['POST'])
def serve_patient():
    result = call_cpp('serve')
    return jsonify({**result, "queue": read_queue(), "served": read_served()})

@app.route('/api/sort', methods=['POST'])
def sort_queue():
    result = call_cpp('sort')
    return jsonify({**result, "queue": read_queue()})

@app.route('/api/clear', methods=['POST'])
def clear_queue():
    result = call_cpp('clear')
    return jsonify({**result, "queue": read_queue(), "served": read_served()})

@app.route('/api/export', methods=['GET'])
def export_data():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, age, priority, status, created_at, served_at FROM patients ORDER BY created_at ASC")
        rows = cursor.fetchall()
        
        patients_data = []
        for row in rows:
            patients_data.append({
                "id": row[0],
                "name": row[1],
                "age": row[2],
                "priority": row[3],
                "status": row[4],
                "created_at": row[5],
                "served_at": row[6]
            })

        conn.close()

        return jsonify({
            "patients": patients_data,
            "timestamp": datetime.now().isoformat(),
            "total_patients": len(patients_data),
            "queued_count": len([p for p in patients_data if p["status"] == "queued"]),
            "served_count": len([p for p in patients_data if p["status"] == "served"])
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/display', methods=['GET'])
def display_queue():
    result = call_cpp('display')
    return jsonify(result)

@app.route('/api/remove_served', methods=['POST'])
def remove_served():
    data = request.json
    patient_id = data.get('id')

    if not patient_id:
        return jsonify({"success": False, "error": "Missing patient ID"}), 400

    result = call_cpp('remove_served', str(patient_id))
    return jsonify({**result, "served": read_served()})

if __name__ == '__main__':
    # Check for required files
    print("=" * 60)
    print("🏥 PATIENT QUEUE SYSTEM - SERVER STARTING")
    print("=" * 60)
    
    # Check ds.exe
    if not os.path.exists(CPP_EXE):
        print(f"❌ ERROR: ds.exe not found at: {CPP_EXE}")
        print(f"   Please compile ds.cpp first:")
        print(f"   g++ ds.cpp -o ds.exe")
        sys.exit(1)
    else:
        print(f"✅ Found ds.exe: {CPP_EXE}")
    
    # Initialize database if it doesn't exist
    if not os.path.exists(DB_FILE):
        print(f"📊 Initializing database: {DB_FILE}")
        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()

            # Read and execute schema
            schema_path = os.path.join(SCRIPT_DIR, "init_db.sql")
            if os.path.exists(schema_path):
                with open(schema_path, 'r') as f:
                    schema_sql = f.read()
                cursor.executescript(schema_sql)
                print("✅ Database schema created")
            else:
                print("❌ init_db.sql not found")

            conn.commit()
            conn.close()
            print(f"✅ Database initialized: {DB_FILE}")
        except Exception as e:
            print(f"❌ Error initializing database: {e}")
            sys.exit(1)
    else:
        print(f"✅ Found database: {DB_FILE}")
    
    print("=" * 60)
    print("🌐 SERVER RUNNING AT: http://localhost:5000")
    print("=" * 60)
    print("📝 Press CTRL+C to stop the server")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
