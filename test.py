import requests
import json

repo_url = "https://github.com/CoderAgent/SecureAgent"

url = f'http://127.0.0.1:5000/embed-repo'  # URL format

data = {
    "repo_url": repo_url  # Replace with the actual repo URL
}

# Send a POST request with JSON data
response = requests.post(url, json=data)

print(response.text)
print(str(response))

# url = f'http://127.0.0.1:5000/query'  # URL format

# data = {
#     "query": "Yes, can you delve into how the implementation for the python parser would work!",  # Replace with the actual repo URL
#     "repo_url": repo_url
# }

# # Send a POST request with JSON data
# response = requests.get(url, json=data)

# # print(json.dumps(response.json()))
# # print(str(response))

# if response.status_code == 200:
#     try:
#         # Parse and pretty-print the JSON response
#         print("Response JSON:")
#         json_msg = response.json().get('response')
#         print(json_msg)
#     except json.JSONDecodeError as e:
#         print("Failed to parse JSON:", e)
#         print("Raw Response Text:", response.text)
# else:
#     print(f"Request failed with status code {response.status_code}")
#     print("Response text:", response.text)