from constants import port_no
from flask import Flask, request, jsonify
from chatgpt import generate_response  # Import the generate_response function from chatgpt.py

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    message = data['queryResult']['queryText']
    # Call the generate_response function from chatgpt.py
    response = generate_response(message)

    reply = {
        "fulfillmentText": response,
    }

    return jsonify(reply)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port= port_no)
