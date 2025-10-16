# ... (Imports and SECRET_PASSWORD definition) ...

@app.route('/api/matchdata', methods=['POST'])
def update_data():
    try:
        data = request.get_json()
        
        # 🛑 TEMPORARY LOGGING LINE 1: Password received from the browser
        # This will show you exactly what 'data.get('password')' returns.
        print(f"Password received from browser: '{data.get('password')}'") 

        # 🛑 TEMPORARY LOGGING LINE 2: Password the server is checking against
        # This will show you exactly what 'SECRET_PASSWORD' (from os.environ.get) holds.
        print(f"Server secret password is:      '{SECRET_PASSWORD}'")
        
        # The password check logic
        if data.get('password') != SECRET_PASSWORD:
            return jsonify({"error": "Unauthorized"}), 401 
        
        # ... (rest of your save logic) ...

    except Exception as e:
        # ... (error handling) ...
        return jsonify({"error": f"Internal Server Error: {e}"}), 500
