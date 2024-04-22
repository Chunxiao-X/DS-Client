from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login_service():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # Placeholder validation - in production, integrate with a database or other authentication mechanism
    if username == "admin" and password == "admin":
        response = {"success": True, "message": "Login successful"}
    else:
        response = {"success": False, "message": "Invalid username or password"}

    return jsonify(response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5004)
