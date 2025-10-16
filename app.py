import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- FIX 1: DEPLOYMENT FIX (NameError) ---
# This line MUST be here so Gunicorn (Render's server) can find the app instance.import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- FIX 1: DEPLOYMENT FIX (NameError) ---
# This line MUST be here so Gunicorn (Render's server) can find the app instance.
app = Flask(__name__) 

CORS(app) # Enable CORS for all routes

# --- SECURE PASSWORD RETRIEVAL ---
# This reads the password from your Render Environment Variable (SECRET_PASSWORD)
# Your Render screenshot uses SECRET_PASSWORD as the key, so we use it here.
SECRET_PASSWORD = os.environ.get('SECRET_PASSWORD')
# You must set SECRET_PASSWORD = Tanmayts@123 on your Render dashboard.

# --- DATA FILE FUNCTIONS ---
def load_data():
    """Loads match data from the JSON file."""
    try:
        # Assuming your data file is named data.json
        with open('data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"error": "Data file not found"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format in file"}

def save_data(data):
    """Saves match data to the JSON file."""
    try:
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False

# --- ROUTES ---

@app.route('/api/matchdata', methods=['GET'])
def get_data():
    """Handles GET requests to retrieve the current match data."""
    data = load_data()
    if "error" in data:
        return jsonify(data), 500
    return jsonify(data), 200

@app.route('/api/matchdata', methods=['POST'])
def update_data():
    """Handles POST requests to update the match data, checking the password."""
    try:
        data = request.get_json()
        
        # 🛑 TEMPORARY LOGGING LINE 1: Password received from the browser
        # Look for this value in the Render logs.
        print(f"Password received from browser: '{data.get('password')}'") 

        # 🛑 TEMPORARY LOGGING LINE 2: Password the server is checking against
        # Look for this value in the Render logs. (Should be 'Tanmayts@123')
        print(f"Server secret password is:      '{SECRET_PASSWORD}'")
        
        # The password check logic
        # It checks if the password field exists and matches the secret
        if data.get('password') != SECRET_PASSWORD:
            # This is the 401 UNAUTHORIZED error you've been seeing
            return jsonify({"error": "Unauthorized"}), 401 
        
        # Remove the password field before saving the data
        if 'password' in data:
            del data['password']

        # Save the updated data
        if save_data(data):
            return jsonify({"message": "Data updated successfully"}), 200
        else:
            return jsonify({"error": "Failed to write data to file"}), 500

    except Exception as e:
        # Catch any other errors during the request handling
        print(f"Request error: {e}")
        return jsonify({"error": f"Internal Server Error: {e}"}), 500

# --- RUNNING THE APP (for local testing) ---
# Render/Gunicorn ignores this block.
if __name__ == '__main__':
    # You must set the environment variable locally to test this block!
    # e.g., in Windows PowerShell: $env:SECRET_PASSWORD="Tanmayts@123"
    app.run(debug=True, port=5000)
app = Flask(__name__) 

CORS(app) # Enable CORS for all routes

# --- SECURE PASSWORD RETRIEVAL ---
# This reads the password from your Render Environment Variable (API_PASSWORD)
SECRET_PASSWORD = os.environ.get('API_PASSWORD')
# You must set API_PASSWORD = Tanmayts@123 on your Render dashboard.

# --- DATA FILE FUNCTIONS ---
def load_data():
    """Loads match data from the JSON file."""
    try:
        with open('data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"error": "Data file not found"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format in file"}

def save_data(data):
    """Saves match data to the JSON file."""
    try:
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False

# --- ROUTES ---

@app.route('/api/matchdata', methods=['GET'])
def get_data():
    """Handles GET requests to retrieve the current match data."""
    data = load_data()
    if "error" in data:
        return jsonify(data), 500
    return jsonify(data), 200

@app.route('/api/matchdata', methods=['POST'])
def update_data():
    """Handles POST requests to update the match data, checking the password."""
    try:
        data = request.get_json()
        
        # 🛑 TEMPORARY LOGGING LINE 1: Password received from the browser
        # Look for this value in the Render logs.
        print(f"Password received from browser: '{data.get('password')}'") 

        # 🛑 TEMPORARY LOGGING LINE 2: Password the server is checking against
        # Look for this value in the Render logs. (Should be 'Tanmayts@123')
        print(f"Server secret password is:      '{SECRET_PASSWORD}'")
        
        # The password check logic
        # It checks if the password field exists and matches the secret
        if data.get('password') != SECRET_PASSWORD:
            return jsonify({"error": "Unauthorized"}), 401 
        
        # Remove the password field before saving the data
        if 'password' in data:
            del data['password']

        # Save the updated data
        if save_data(data):
            return jsonify({"message": "Data updated successfully"}), 200
        else:
            return jsonify({"error": "Failed to write data to file"}), 500

    except Exception as e:
        # Catch any other errors during the request handling
        print(f"Request error: {e}")
        return jsonify({"error": f"Internal Server Error: {e}"}), 500

# --- RUNNING THE APP (for local testing) ---
# Render/Gunicorn ignores this block, but it's useful for local testing.
if __name__ == '__main__':
    # You must set the environment variable locally to test this block!
    # e.g., in Windows PowerShell: $env:API_PASSWORD="Tanmayts@123"
    app.run(debug=True)

