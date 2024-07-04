
import requests

response = requests.get("http://127.0.0.1:5000/")
print(response.text)

response = requests.get("http://127.0.0.1:5000/website")
print(response.text)

response = requests.post("http://127.0.0.1:5000/post_request", json={"text": "Exciting content for processing."})
print(response.text)

response = requests.get("http://127.0.0.1:5000/params?my_parameter=test")
print(response.text)

response = requests.get("http://127.0.0.1:5000/dynamic/example")
print(response.text)
