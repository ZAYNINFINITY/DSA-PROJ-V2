# Flask Static Serving Code Snippet
# Add this code to your Flask app (e.g., backend/app_py.py) to serve the frontend folder and static assets
# Note: Your app already serves templates and static via template_folder and static_folder, but this adds additional routes if needed

from flask import send_from_directory

# Add these routes to your Flask app for serving the entire frontend folder
@app.route('/frontend/<path:filename>')
def serve_frontend(filename):
    """Serve files from the frontend directory"""
    return send_from_directory('../frontend', filename)

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files from the frontend/static directory"""
    return send_from_directory('../frontend/static', filename)

# If you want to serve the index.html directly from /frontend
@app.route('/app')
def app_page():
    """Serve the main app page"""
    return send_from_directory('../frontend', 'index.html')
