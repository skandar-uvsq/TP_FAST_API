import requests
import json

# Define the URL of your FastAPI app (adjust the port as necessary)
url = "http://localhost:8000/extract-data/"

# Define the payload, replacing "Your text here" with the actual text you want to send
payload = {
    "text": "John Doe is looking to purchase a charming two-story house with a garden, located at 123 Rue de la Liberte, 75001 Paris, France, Apt N° 1401. This lovely property, with a surface area of 150m², is situated in a peaceful residential neighborhood and is in good condition. John is seeking a loan of 200000$ to finance this purchase. He can be contacted via email at john.doe@email.com or by phone at +33 123 456 789."
}

# Send a POST request to the endpoint
response = requests.post(
    url, data=json.dumps(payload), headers={"Content-Type": "application/json"}
)
data = response.json()

# Print the response
print("Status Code:", response.status_code)
print("Response JSON:", response.json())


url = "http://localhost:8000/evaluate-property/"
payload = {"data": data}

response = requests.post(
    url, data=json.dumps(payload), headers={"Content-Type": "application/json"}
)

print("Status Code:", response.status_code)
print("Response JSON:", response.json())


url = "http://localhost:8000/check-solvency/"
payload = {"data": data, "estimated_value": response.json()}

response = requests.post(
    url, data=json.dumps(payload), headers={"Content-Type": "application/json"}
)

print("Status Code:", response.status_code)
print("Response JSON:", response.json())


url = "http://localhost:8000/make-decision/"
payload = {"client_solvable": response.json()}

response = requests.post(
    url, data=json.dumps(payload), headers={"Content-Type": "application/json"}
)

print("Status Code:", response.status_code)
print("Response JSON:", response.json())
