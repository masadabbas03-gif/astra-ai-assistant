import requests

url = "http://localhost:5678/webhook-test/astra"

payload = {
    "to": "muhammadassadabbas50@gmail.com",
    "subject": "Dynamic Email Test",
    "message": "Hello! This email was sent dynamically from Astra through n8n."
}

response = requests.post(url, json=payload)

print(response.status_code)
print(response.text)