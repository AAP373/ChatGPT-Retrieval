#!/folder/home/chatgpt-retrieval/venv/bin/python3
import subprocess
import os
import time
from threading import Thread
from constants import port_no

# Commands to be run
start_drive_command = '/folder/home/chatgpt-retrieval/venv/bin/python3 drive.py'
start_sync_command = '/folder/home/chatgpt-retrieval/venv/bin/python3 sync.py'
start_app_command = '/folder/home/chatgpt-retrieval/venv/bin/python3 app.py'
start_ngrok_command = f'ngrok http {port_no}'


# Change working directory
os.chdir('/folder/home/chatgpt-retrieval')

# Function to run a command
def run_command(command):
    subprocess.call(['bash', '-c', command])

# Create threads
thread_drive = Thread(target=run_command, args=(start_drive_command,))
thread_sync = Thread(target=run_command, args=(start_sync_command,))
thread_app = Thread(target=run_command, args=(start_app_command,))
thread_ngrok = Thread(target=run_command, args=(start_ngrok_command,))

# Start threads
thread_drive.start()
thread_drive.join()  # Wait for drive.py to finish

thread_sync.start()
thread_sync.join()  # Wait for sync.py to finish

time.sleep(5)  # Optional delay
thread_app.start()

time.sleep(2)  # Optional delay before starting ngrok
thread_ngrok.start()

# Wait for threads to finish
thread_app.join()
thread_ngrok.join()
