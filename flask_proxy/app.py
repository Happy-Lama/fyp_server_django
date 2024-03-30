from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Define the endpoint where the decoded data will be forwarded
FORWARD_ENDPOINT = "https://fyp-server-django.onrender.com/api/data/gsm/"

@app.route('/receive', methods=['POST'])
def receive_data():
    try:
        # Get the JSON data from the POST request
        data = request.get_json()
        if data:
            # Print the received data
            print("Received Data:", data)

            # Forward the decoded data to the specified endpoint
            response = requests.post(FORWARD_ENDPOINT, json=data)
            print("Forwarding Response:", response.status_code)
            
            # Return a response indicating success
            return jsonify({"message": "Data received and forwarded successfully"}), 200
        else:
            return jsonify({"error": "No JSON data received"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
