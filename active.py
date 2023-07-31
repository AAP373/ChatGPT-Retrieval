from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route('/run_script', methods=['GET'])
def run_script():
    subprocess.call(['/folder/home/chatgpt-retrieval/venv/bin/python3', '/folder/home/chatgpt-retrieval/auto.py'])
    return jsonify(message="Script is running")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
