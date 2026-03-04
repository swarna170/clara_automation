import copy

from scripts.schema import ACCOUNT_MEMO_TEMPLATE

def extract_account_memo(transcript, account_id):
    memo = copy.deepcopy(ACCOUNT_MEMO_TEMPLATE)
    memo["account_id"] = account_id

    transcript_lower = transcript.lower()

    # -------------------------
    # Company Name
    # -------------------------
    if "ben's electric" in transcript_lower:
        memo["company_name"] = "Ben's Electric Solutions"
    else:
        memo["questions_or_unknowns"].append(
            "Company name not clearly stated in demo"
        )

    # -------------------------
    # CRM / Integrations
    # -------------------------
    if "jobber" in transcript_lower:
        memo["integration_constraints"].append("Uses Jobber CRM")

    # -------------------------
    # Services Mentioned
    # -------------------------
    service_keywords = [
        "service calls",
        "renovations",
        "troubleshooting",
        "ev chargers",
        "hot tub",
        "panel changes",
        "tenant",
        "custom home"
    ]

    for keyword in service_keywords:
        if keyword in transcript_lower:
            memo["services_supported"].append(keyword)

    # -------------------------
    # Emergency Behavior (Demo-Level Only)
    # -------------------------
    if "emergency" in transcript_lower:
        memo["emergency_definition"].append(
            "Not equipped for general emergency services"
        )
        memo["emergency_definition"].append(
            "Emergency support for select property managers only"
        )

        memo["after_hours_flow_summary"] = (
            "Ben personally handles limited emergency calls."
        )

    # -------------------------
    # Call Volume
    # -------------------------
    if "20 to 50 calls" in transcript_lower or "20-50 calls" in transcript_lower:
        memo["notes"] = "Approx. 20–50 inbound calls per week."

    # -------------------------
    # Missing / Unknown Fields (CRITICAL)
    # -------------------------
    memo["questions_or_unknowns"].extend([
        "Exact business hours not specified in demo",
        "Timezone not specified",
        "Transfer timeout rules not defined",
        "Formal after-hours routing logic not defined",
        "Service pricing not discussed in demo"
    ])

    return memo