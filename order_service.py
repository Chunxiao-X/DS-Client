from flask import Flask, request, jsonify
app = Flask(__name__)

orders = []

@app.route('/order', methods=['POST'])
def manage_order():
    data = request.get_json()
    order = {
        "id": len(orders) + 1,
        "status": "placed",
        "details": data['details']
    }
    orders.append(order)
    return jsonify({"message": "Order placed successfully", "order": order})

@app.route('/order/status', methods=['GET'])
def order_status():
    order_id = request.args.get('id')
    order = next((order for order in orders if order["id"] == int(order_id)), None)
    if order:
        return jsonify(order)
    else:
        return jsonify({"error": "Order not found"}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002)
