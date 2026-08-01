import base64
from email.mime.text import MIMEText

import httpx

GMAIL_SEND_URL = "https://gmail.googleapis.com/gmail/v1/users/me/messages/send"


async def send_notification_email(access_token: str, to_addresses: str, subject: str, body_html: str) -> None:
    message = MIMEText(body_html, "html")
    message["To"] = to_addresses
    message["Subject"] = subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            GMAIL_SEND_URL,
            json={"raw": raw},
            headers={"Authorization": f"Bearer {access_token}"},
        )
        response.raise_for_status()
