# 多线程
from flask import Flask, request, jsonify
import requests
import threading
import socket

app = Flask(__name__)

print("Setting up routes...")  # Debug print

@app.route('/service', methods=['POST'])
def gateway():
    print("Handling a request...")  # Debug print
    data = request.get_json()
    service_type = data['service']
    port_mapping = {
        'product': 5001,
        'order': 5002,
        'notification': 5003,
        'login': 5004
    }
    
    print(f"Received service type: {service_type}")  # Debug print
    
    if service_type in port_mapping:
        service_url = f"http://localhost:{port_mapping[service_type]}"
        response = requests.post(service_url, json=data)
        return jsonify(response.json())
    else:
        return jsonify({"error": "Service type not supported"}), 400
    
def handle_client(connection, address):
    print(f"Connected by {address}")  # Debug print
    try:
        while True:
            data = connection.recv(1024)
            if not data:
                break
            connection.sendall(data)
    finally:
        connection.close()

def tcp_server():
    host = '127.0.0.1'
    port = 9000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print("TCP server running and listening...")  # Debug print
    
    try:
        while True:
            client_socket, addr = server_socket.accept()
            threading.Thread(target=handle_client, args=(client_socket, addr)).start()
    finally:
        server_socket.close()

if __name__ == "__main__":
    print("Starting Flask app and TCP server...")  # Debug print
    # Start the TCP server in a separate thread
    threading.Thread(target=tcp_server).start()
    # Start the Flask app with multi-threading enabled
    app.run(host='0.0.0.0', port=1234, threaded=True)
