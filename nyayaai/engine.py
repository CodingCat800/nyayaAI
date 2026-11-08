
import os
import json
import logging
import requests

from .legal import LEGAL_SOURCES, GUIDANCE


# --------------------------------------------------
# Logging configuration
# --------------------------------------------------

logger = logging.getLogger("nyayaai")

if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
    )
    logger.addHandler(handler)

logger.setLevel(logging.INFO)
logger.propagate = False


SYSTEM = """You are a cautious Indian consumer-refund assistant.
Scope: online purchase/service refund not received.
Use only user-provided facts.
Never invent dates, amounts, order IDs, legal sections,
case law, or outcomes.
Do not make definitive legal findings.
Ask for missing facts.
Return JSON keys: summary, missing_facts (array),
timeline (array), evidence (array), next_steps (array).
If outside scope, say so and recommend appropriate
professional help."""


# --------------------------------------------------
# LLM connection and request
# --------------------------------------------------

def _llm(narrative, facts):

    base, key, model = (
        os.getenv(k, "").strip()
        for k in (
            "NYAYAI_LLM_BASE_URL",
            "NYAYAI_LLM_API_KEY",
            "NYAYAI_LLM_MODEL"
        )
    )

    # Check configuration
    missing = []

    if not base:
        missing.append("NYAYAI_LLM_BASE_URL")

    if not key:
        missing.append("NYAYAI_LLM_API_KEY")

    if not model:
        missing.append("NYAYAI_LLM_MODEL")

    if missing:
        reason = f"Missing environment variables: {', '.join(missing)}"
        logger.error(reason)

        return None, f"Offline fallback: {reason}"

    endpoint = base.rstrip("/") + "/chat/completions"

    logger.info("Attempting LLM connection")
    logger.info("Endpoint: %s", endpoint)
    logger.info("Model: %s", model)

    try:

        response = requests.post(
            endpoint,
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json"
            },
            json={
                "model": model,
                "temperature": 0.1,
                "response_format": {"type": "json_object"},
                "messages": [
                    {
                        "role": "system",
                        "content": SYSTEM
                    },
                    {
                        "role": "user",
                        "content": json.dumps({
                            "narrative": narrative,
                            "facts": facts
                        })
                    }
                ]
            },
            timeout=45
        )

        # Log unsuccessful HTTP responses
        if not response.ok:

            logger.error(
                "LLM API returned HTTP %s",
                response.status_code
            )

            logger.error(
                "API error response: %s",
                response.text[:3000]
            )

            response.raise_for_status()

        # Parse API response
        data = response.json()

        content = data["choices"][0]["message"]["content"]

        result = json.loads(content)

        if not isinstance(result, dict):
            raise ValueError("LLM response is not a JSON object")

        required_keys = [
            "summary",
            "missing_facts",
            "timeline",
            "evidence",
            "next_steps"
        ]

        missing_keys = [
            k for k in required_keys if k not in result
        ]

        if missing_keys:
            raise ValueError(
                f"LLM response missing required keys: {missing_keys}"
            )

        logger.info("LLM request successful")

        return result, f"LLM used: {model}"

    except requests.exceptions.Timeout:

        logger.exception("LLM API request timed out")

        return None, "LLM connection failed: Request timed out."

    except requests.exceptions.ConnectionError:

        logger.exception(
            "Could not connect to the LLM API. "
            "Check internet access, endpoint URL and network settings."
        )

        return None, "LLM connection failed: Could not reach API endpoint."

    except requests.exceptions.HTTPError as exc:

        status_code = (
            exc.response.status_code
            if exc.response is not None
            else "Unknown"
        )

        logger.exception("LLM HTTP error")

        if status_code == 401:
            reason = "Authentication failed. Check your API key."

        elif status_code == 403:
            reason = "Access forbidden. Check API permissions."

        elif status_code == 404:
            reason = "Endpoint or model not found. Check URL and model name."

        elif status_code == 429:
            reason = "Rate limit or quota exceeded."

        elif status_code >= 500:
            reason = "LLM provider server error."

        else:
            reason = f"HTTP error {status_code}."

        return None, f"LLM API failed: {reason}"

    except (KeyError, IndexError, TypeError, ValueError):

        logger.exception(
            "Invalid or unexpected response from LLM API"
        )

        return None, (
            "LLM response failed validation. "
            "Check model response format and JSON compatibility."
        )

    except Exception:

        logger.exception("Unexpected LLM integration error")

        return None, "LLM unavailable due to an unexpected error."


# --------------------------------------------------
# Main analysis
# --------------------------------------------------

def analyze(narrative, facts):

    result, status = _llm(narrative, facts)

    if result is None:

        logger.warning(
            "Using deterministic fallback. Reason: %s",
            status
        )

        required = {
            "seller": "Seller/platform",
            "order_id": "Order/booking ID",
            "purchase_date": "Purchase date",
            "refund_requested_date": "Refund request date",
            "amount": "Amount paid/refund due",
            "refund_reason": "Reason for refund"
        }

        result = {
            "summary": (
                "The user reports an online purchase/service "
                "refund that has not been received. This is a "
                "preliminary summary, not a legal conclusion."
            ),

            "missing_facts": [
                label
                for key, label in required.items()
                if not facts.get(key)
            ],

            "timeline": [
                f"{label}: {facts.get(key) or 'Not provided'}"
                for key, label in [
                    ("purchase_date", "Purchase date"),
                    ("refund_requested_date", "Refund requested"),
                    ("seller", "Seller/platform"),
                    ("amount", "Amount"),
                    ("order_id", "Order ID")
                ]
            ],

            "evidence": [
                "Order confirmation/invoice",
                "Payment receipt or UPI/card/bank transaction reference",
                "Cancellation/return confirmation",
                "Refund request acknowledgement and promised timeline",
                "Emails, chats, tickets and seller responses",
                "Bank statement showing whether refund was credited"
            ],

            "next_steps": [
                "Contact the seller/platform in writing and ask for status, reason for delay, and expected credit date.",
                "Preserve order, payment, return and support records.",
                "If unresolved, consider registering a grievance with the National Consumer Helpline.",
                "If still unresolved, seek advice on the appropriate Consumer Commission."
            ]
        }

    safety_terms = [
        "threat",
        "come to my house",
        "harm me",
        "kill me",
        "attack me",
        "violence",
        "blackmail"
    ]

    safety_flag = any(
        term in narrative.lower()
        for term in safety_terms
    )

    if safety_flag:

        result["summary"] = (
            "The narrative includes a possible personal-safety "
            "concern in addition to the refund issue. "
            "The refund workflow cannot assess or resolve threats."
        )

        result["next_steps"] = [
            "If you believe there is an immediate threat, move to a safe place and contact local emergency services or police. Do not rely on this refund assistant for urgent safety support."
        ] + result.get("next_steps", [])

    result.update({
        "safety_flag": safety_flag,
        "model_status": status,
        "official_guidance": GUIDANCE,
        "legal_sources": LEGAL_SOURCES,
        "disclaimer": (
            "General information and document assistance only; "
            "not legal advice or representation. Documents and "
            "seller records have not been verified. For urgent, "
            "complex, high-value, limitation-sensitive, or disputed "
            "matters, consult a qualified advocate."
        )
    })

    return result


# --------------------------------------------------
# Complaint draft
# --------------------------------------------------

def complaint_draft(name, address, facts, issue, requested):

    def v(x):
        return (
            x.strip()
            if isinstance(x, str) and x.strip()
            else "[Please fill in]"
        )

    return f"""To,
The Grievance Officer / Customer Support Team
{v(facts.get('seller', ''))}

Subject: Request for resolution of pending refund — Order {v(facts.get('order_id', ''))}

Dear Sir/Madam,

I am {v(name)}, residing at {v(address)}. I placed an online order/booking with your platform.

Order/booking ID: {v(facts.get('order_id', ''))}
Date of purchase: {v(facts.get('purchase_date', ''))}
Amount paid: {v(facts.get('amount', ''))}
Date refund was requested: {v(facts.get('refund_requested_date', ''))}

Issue:
{v(issue)}

I request that you: {v(requested)}

Please provide a written update explaining the status, reason for any delay, and expected date of resolution. I request a response within 7 days of receiving this message. This is a proposed communication timeline, not a statutory deadline.

I have retained relevant order, payment, and communication records.

Regards,
{v(name)}
{v(address)}
"""
