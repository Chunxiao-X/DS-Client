from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/notify', methods=['POST'])
def notify():
    data = request.get_json()
    if data['type'] == 'notify_low_inventory':
        # Placeholder: Logic to notify about low inventory
        response = {"message": "Low inventory notification sent"}
    else:
        response = {"message": "Notification type not supported"}
    return jsonify(response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5003)
