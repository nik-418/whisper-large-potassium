import requests
import json

url = "http://localhost:8000"  # Replace with your actual URL

# Set the file path of the MP3 file
mp3_file_path = "test.wav"  # Replace with the actual file path

# Create a dictionary to hold the file data
files = {
    "file": open(mp3_file_path, "rb")
}

# Set the additional variables
data = {
    "path": "test.wav",
    "variable2": "value2"
}

headers = {
    "Content-Type": "application/json"
}

# Send the POST request
response = requests.post(url, json=data, headers=headers)

# Check the response status code
if response.status_code == 200:
    print("POST request successful!", response.text)
else:
    print("POST request failed with status code:", response.status_code, response.text)
