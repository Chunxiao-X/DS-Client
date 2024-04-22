from flask import Flask, request, jsonify
import psycopg2
import psycopg2.extras
import logging


app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def connect_db():
    conn = psycopg2.connect(
        dbname='Product',  
        user='postgres',
        password='1234',
        host='localhost',
        port='5435'
    )
    return conn


@app.route('/product', methods=['POST'])
def manage_product():
    data = request.get_json()
    logging.debug(f"Received data: {data}")
    valid, message = validate_product_data(data)
    if not valid:
        logging.error(f"Validation failed: {message}")
        return jsonify({"error": message}), 400
    
    conn = connect_db()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        if data['action'] == 'add':
            cursor.execute('INSERT INTO product (name, price, quantity, supplierid, regionid) VALUES (%s, %s, %s, %s, %s)',
                           (data['name'], data['price'], data['quantity'], data['supplierid'], data['regionid']))
            conn.commit()
            return jsonify({"message": "Product added successfully"}), 201
        elif data['action'] == 'update':
            cursor.execute('UPDATE product SET name = %s, price = %s, quantity = %s, supplierid = %s, regionid = %s WHERE id = %s',
                           (data['name'], data['price'], data['quantity'], data['supplierid'], data['regionid'], data['id']))
            conn.commit()
            return jsonify({"message": "Product updated successfully"})
        elif data['action'] == 'delete':
            cursor.execute('DELETE FROM product WHERE id = %s', (data['id'],))
            conn.commit()
            return jsonify({"message": "Product deleted successfully"})
    except psycopg2.DatabaseError as e:
        logging.exception("Database error occurred")
        conn.rollback()
        return jsonify({"error": "Database operation failed", "details": str(e)}), 500
    except Exception as e:
        logging.exception("An unexpected error occurred")
        return jsonify({"error": "An error occurred", "details": str(e)}), 500
    finally:
        conn.close()
        logging.info("Database connection closed")

# @app.route('/product', methods=['POST'])
# def manage_product():
#     data = request.get_json()
#     conn = connect_db()
#     cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#     try:
#         if data['action'] == 'add':
#             cursor.execute('INSERT INTO product (name, price, quantity, supplierid, regionid) VALUES (%s, %s, %s, %s, %s)',
#                            (data['name'], data['price'], data['quantity'], data['supplierid'], data['regionid']))
#             conn.commit()
#             return jsonify({"message": "Product added successfully"}), 201
#         elif data['action'] == 'update':
#             cursor.execute('UPDATE product SET name = %s, price = %s, quantity = %s, supplierid = %s, regionid = %s WHERE id = %s',
#                            (data['name'], data['price'], data['quantity'], data['supplierid'], data['regionid'], data['id']))
#             conn.commit()
#             return jsonify({"message": "Product updated successfully"})
#         elif data['action'] == 'delete':
#             cursor.execute('DELETE FROM product WHERE id = %s', (data['id'],))
#             conn.commit()
#             return jsonify({"message": "Product deleted successfully"})
#         else:
#             return jsonify({"error": "Invalid action"}), 400
#     except Exception as e:
#         conn.rollback()
#         return jsonify({"error": str(e)}), 500
#     finally:
#         conn.close()


@app.route('/products/search', methods=['GET'])
def search_products():
    conn = connect_db()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query_params = request.args
    query = "SELECT * FROM product WHERE 1=1"
    params = []

    if 'name' in query_params:
        query += " AND name ILIKE %s"
        params.append('%' + query_params['name'] + '%')
    if 'price_from' in query_params and 'price_to' in query_params:
        query += " AND price BETWEEN %s AND %s"
        params.append(float(query_params['price_from']))
        params.append(float(query_params['price_to']))

    cursor.execute(query, tuple(params))
    products = cursor.fetchall()
    conn.close()
    return jsonify([dict(product) for product in products])

@app.route('/alerts', methods=['GET'])
def get_alerts():
    conn = connect_db()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT * FROM product WHERE quantity < 10')
    low_inventory_products = cursor.fetchall()
    alerts = [{"product_id": product['id'], "message": f"Low inventory alert for {product['name']}! Only {product['quantity']} left."} for product in low_inventory_products]
    conn.close()
    return jsonify(alerts)

def view_alerts():
    alert_data = {
        "service": "product",
        "action": "view_alerts"
    }
    try:
        response = requests.get(f"{base_url}/service", json=alert_data)
        response.raise_for_status()  # Checks HTTP status codes for errors
        alerts = response.json()  # Attempts to decode JSON
        print("Alerts:")
        if alerts:
            for alert in alerts:
                print(alert)
        else:
            print("No alerts found.")
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err} - {response.text}")
    except requests.exceptions.JSONDecodeError:
        print("Failed to decode JSON, possibly due to empty response: ", response.text)
    except Exception as err:
        print("An error occurred: ", err)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, threaded=True)
