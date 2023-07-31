from constants import folder_id, local_directory
import os
import io
import json
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account

# Set up Google Drive API credentials
# Make sure you have the credentials file (client_secrets.json) in the same directory as this script
credentials = service_account.Credentials.from_service_account_file('client_secrets.json')
drive_service = build('drive', 'v3', credentials=credentials)

def download_files_from_folder(folder_id, local_directory):
    # Retrieve the list of files in the folder
    results = drive_service.files().list(q=f"'{folder_id}' in parents and trashed=false",
                                         fields='files(id, name)').execute()
    files = results.get('files', [])

    # Download each file
    for file in files:
        file_id = file['id']
        file_name = file['name']
        print(f"Attempting to download file {file_name} with ID {file_id}...")  # Debugging line

        # If the file is an Excel file, convert it to JSON
        if file_name.endswith('.xlsx'):
            request = drive_service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print(f"Downloading {file_name}... {int(status.progress() * 100)}%")
            fh.seek(0)

            # Read the Excel file and convert each sheet to a separate JSON string
            xls = pd.read_excel(fh, sheet_name=None)  # sheet_name=None reads all sheets
            for sheet_name, df in xls.items():
                json_str = df.to_json(orient='records')

                # Write the JSON data to a file
                json_file_name = f"{file_name.rsplit('.', 1)[0]}_{sheet_name}.json"  # Change the file extension to .json and append the sheet name
                json_path = os.path.join(local_directory, json_file_name)
                with open(json_path, 'w') as json_file:
                    json_file.write(json_str)
        else:
            # For non-Excel files, download and save them as they are
            local_path = os.path.join(local_directory, file_name)
            request = drive_service.files().get_media(fileId=file_id)
            with open(local_path, 'wb') as f:
                downloader = MediaIoBaseDownload(f, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                    print(f"Downloading {file_name}... {int(status.progress() * 100)}%")

    print('Download complete!')


download_files_from_folder(folder_id, local_directory)
