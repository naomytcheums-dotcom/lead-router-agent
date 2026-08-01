import json
import re

from app.config import settings
from app.services.llm_client import get_client

SYSTEM_PROMPT = (
    "You process new sales/inquiry leads for a company. Given the company's products & "
    "services, its team directory (who's responsible for what), and a lead's notes, you "
    "must:\n\n"
    "1. Decide whether the inquiry is actually related to something the company offers. "
    "Job applications, spam, and requests totally unrelated to the company's products or "
    "services are INVALID.\n"
    "2. If valid, pick the team member(s) from the directory whose responsibility best "
    "matches the inquiry. If none match well, pick the closest one — never leave it "
    "empty for a valid lead.\n"
    "3. Draft a short, professional internal notification email — addressed to the team "
    "member(s), NOT to the customer — summarizing who's asking, what they want, and "
    "asking the recipient to follow up promptly. This is a system notification, not a "
    "reply from the customer.\n\n"
    "Respond with ONLY valid JSON, no markdown fences, no extra text, in exactly this "
    "shape:\n"
    '{"is_valid": true or false, "invalid_reason": "why, if invalid, else empty string", '
    '"recipient_emails": "comma-separated emails, empty if invalid", '
    '"email_subject": "short subject, empty if invalid", '
    '"email_body": "the notification email body in plain text with line breaks, empty if invalid"}'
)


def _strip_code_fence(text: str) -> str:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else text


def analyze_lead(
    company_name: str,
    products_and_services: str,
    team_directory: list[dict],
    lead_name: str,
    lead_company: str,
    notes: str,
    city: str,
    country: str,
    mobile: str,
) -> dict:
    client = get_client()

    directory_text = "\n".join(f"- {m['name']} <{m['email']}>: {m['responsibility']}" for m in team_directory)

    user_message = (
        f"Company: {company_name}\n"
        f"Products & services: {products_and_services}\n\n"
        f"Team directory:\n{directory_text or '(no team members configured)'}\n\n"
        f"Lead:\n"
        f"Name: {lead_name}\n"
        f"Company: {lead_company}\n"
        f"Notes: {notes}\n"
        f"City: {city}\n"
        f"Country: {country}\n"
        f"Mobile: {mobile}"
    )

    response = client.chat.completions.create(
        model=settings.llm_model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.3,
        max_tokens=1024,
    )
    raw = response.choices[0].message.content.strip()

    try:
        parsed = json.loads(_strip_code_fence(raw))
        return {
            "is_valid": bool(parsed.get("is_valid", False)),
            "invalid_reason": parsed.get("invalid_reason", ""),
            "recipient_emails": parsed.get("recipient_emails", ""),
            "email_subject": parsed.get("email_subject", ""),
            "email_body": parsed.get("email_body", ""),
        }
    except (json.JSONDecodeError, AttributeError):
        return {
            "is_valid": False,
            "invalid_reason": f"Could not parse AI response: {raw[:200]}",
            "recipient_emails": "",
            "email_subject": "",
            "email_body": "",
        }
