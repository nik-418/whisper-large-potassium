import requests

url = "http://localhost:8000"  # Replace with your actual URL

# Set the file path of the MP3 file
mp3_file_path = "hello_world.wav"  # Replace with the actual file path

# Set the additional variables
data = {
    "path": mp3_file_path,
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
