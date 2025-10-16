# app.py (inside update_data function)

@app.route('/api/matchdata', methods=['POST'])
def update_data():
    try:
        data = request.get_json()
        
        # 🛑 REMOVE THESE TWO LINES FOR SECURITY 🛑
        # print(f"Password received from browser: '{data.get('password')}'") 
        # print(f"Server secret password is:      '{SECRET_PASSWORD}'")
        
        # The password check logic
        if data.get('password') != SECRET_PASSWORD:
            return jsonify({"error": "Unauthorized"}), 401 
        
        # ... (rest of your save logic) ...
