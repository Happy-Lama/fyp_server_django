import requests

def send_data_to_api(devEUI, hex_payload):
    url = "http://localhost:8000/api/data/gsm/"
    payload = {
        "devEUI": devEUI,
        "payload": hex_payload
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        # if response.status_code == 200:
        #     print("Data sent successfully.")
        # else:
        #     print(f"Failed to send data. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error occurred: {str(e)}")

# Example usage
devEUI = "1"
hex_payload = "4148000041480000414800004148000041480000414800004148000041480000414800004148000041480000414800004148000041480000000000000000000000000000000000004148000001"

send_data_to_api(devEUI, hex_payload)
