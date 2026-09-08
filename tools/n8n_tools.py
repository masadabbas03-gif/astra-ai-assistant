import requests

N8N_WEBHOOK = "http://localhost:5678/webhook/astra"


def send_email_n8n(to, subject, message):
    payload = {
        "to": to,
        "subject": subject,
        "message": message
    }

    response = requests.post(
        N8N_WEBHOOK,
        json=payload,
        timeout=30
    )

    return response.json()