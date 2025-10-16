from flask import Flask, request, jsonify, send_file
from datetime import datetime
import json
import os
from flask_cors import CORS

app = Flask(__name__)
# Allows the frontend on a different port to talk to the backend
CORS(app) 

DATA_FILE = 'data.json'
# ⭐️ CRITICAL FIX: Ensure this password matches the one in index (3).html
ADMIN_PASSWORD = "asdfghjkl;'"

# Helper function to read/write data
def load_match_data():
    if not os.path.exists(DATA_FILE):
        return None
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_match_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# --- API ENDPOINTS ---

@app.route('/api/matchdata', methods=['GET'])
def get_match_data():
    """Endpoint for all users to fetch current match data."""
    data = load_match_data()
    if data:
        return jsonify(data)
    return jsonify({"error": "No match data found"}), 404

@app.route('/api/matchdata', methods=['POST'])
def update_match_data():
    """Endpoint for admin to update match data."""
    # 1. Admin Authentication: Check the custom header sent from the frontend
    auth_header = request.headers.get('X-Admin-Password')
    if auth_header != ADMIN_PASSWORD:
        # This is what generates the 401 UNAUTHORIZED error if the header is missing or wrong
        return jsonify({"message": "Unauthorized access."}), 401

    # 2. Update Data
    new_data = request.json
    if not new_data:
        return jsonify({"message": "Invalid data format."}), 400

    # Optional: Basic validation to ensure all required fields are present
    required_keys = ['matchName', 'startTime', 'roomId', 'password', 'teamNames', 'mapStatuses', 'winnerPoints']
    if not all(k in new_data for k in required_keys):
        return jsonify({"message": "Missing required fields."}), 400
            
    # Preserve the maps array since it's static in your client code
    current_data = load_match_data()
    if current_data:
        new_data['maps'] = current_data.get('maps', ["Bermuda", "Purgatory", "Kalahari", "Alpine"])
            
    save_match_data(new_data)
    
    return jsonify({"message": "Match data updated successfully!", "data": new_data}), 200

# --- Serve Static HTML/Image (Optional but helpful) ---
@app.route('/')
def serve_index():
    # Assuming your main HTML file is now named index (3).html, rename it to index.html 
    # OR change the line below to: return send_file('index (3).html')
    return send_file('index.html') 

@app.route('/tpg.png')
def serve_logo():
    # If you have the image, uncomment the next line. Otherwise, it returns nothing.
    # return send_file('tpg.png') 
    return "" 


if __name__ == '__main__':
    # Initialize data.json if it doesn't exist
    if not os.path.exists(DATA_FILE):
        print(f"Initializing {DATA_FILE} with default data...")
        # Use a simplified default structure to start
        initial_data = {
            "matchName": "TPG Scrims Match 1",
            "gameName": "Free Fire",
            "startTime": datetime.now().strftime("%Y-%m-%dT%H:%M"),
            "revealTime": datetime.now().strftime("%Y-%m-%dT%H:%M"),
            "status": "UPCOMING",
            "roomId": "N/A",
            "password": "N/A",
            "teamNames": [f"Squad {i+1}" for i in range(12)],
            "maps": ["Bermuda", "Purgatory", "Kalahari", "Alpine"],
            "mapStatuses": ["UPCOMING", "UPCOMING", "UPCOMING", "UPCOMING"],
            "winnerPoints": [{"name": "", "points": 0}, {"name": "", "points": 0}, {"name": "", "points": 0}]
        }
        save_match_data(initial_data)

    app.run(debug=True, port=5000)