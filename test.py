import requests
import json

repo_url = "https://github.com/vercel/ai-chatbot"

# url = f'http://127.0.0.1:5000/embed-repo'  # URL format

# data = {
#     "repo_url": repo_url  # Replace with the actual repo URL
# }

# # Send a POST request with JSON data
# response = requests.post(url, json=data)

# print(response.text)
# print(str(response))

url = f'http://127.0.0.1:5000/query'  # URL format

data = {
    "query": """

    I don't want to have the same type of authentication in my own project as this one. How do I remove that authentication because I don't want end users having to log in or anything like that. This will be a open chatbot for anyone to use.

    """,  # Replace with the actual repo URL
    "repo_url": repo_url
}

# Send a POST request with JSON data
response = requests.get(url, json=data)

# print(json.dumps(response.json()))
# print(str(response))

if response.status_code == 200:
    try:
        # Parse and pretty-print the JSON response
        print("Response JSON:")
        json_msg = response.json().get('response')
        print(json_msg)
    except json.JSONDecodeError as e:
        print("Failed to parse JSON:", e)
        print("Raw Response Text:", response.text)
else:
    print(f"Request failed with status code {response.status_code}")
    print("Response text:", response.text)