from flask import Flask
import subprocess
import threading

app = Flask(__name__)

@app.route('/run-script', methods=['POST'])
def run_script():
    def start_script():
        subprocess.call(['/folder/home/chatgpt-retrieval/venv/bin/python', '/folder/home/chatgpt-retrieval/auto.py'])
    thread = threading.Thread(target=start_script)
    thread.start()
    return 'Script started'

if __name__ == "__main__":
    app.run(port=5004)
