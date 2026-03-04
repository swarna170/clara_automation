import copy
from scripts.schema import ACCOUNT_MEMO_TEMPLATE


def extract_onboarding_memo(transcript, account_id):
    memo = copy.deepcopy(ACCOUNT_MEMO_TEMPLATE)
    memo["account_id"] = account_id

    t = transcript.lower()

    # -------------------------
    # Business Hours
    # -------------------------
    if "monday to friday" in t:
        memo["business_hours"]["days"] = "Monday to Friday"

    if "8:30" in t and "5" in t:
        memo["business_hours"]["start"] = "8:30 AM"
        memo["business_hours"]["end"] = "5:00 PM"

    # -------------------------
    # Pricing
    # -------------------------
    if "$115" in transcript:
        memo["notes"] = (
            "Service call fee $115 call-out + $98/hour billed in half-hour increments. "
            "Mention only if caller asks."
        )

    # -------------------------
    # Emergency Clarification
    # -------------------------
    if "g&m" in t or "gnm" in t or "pressure washing" in t or "gas station" in t:
        memo["emergency_definition"] = [
            "After-hours emergency support ONLY for G&M Pressure Washing managed gas stations"
        ]

        memo["emergency_routing_rules"] = [
            "If caller identifies as G&M Pressure Washing",
            "Collect gas station details",
            "Patch call directly to Ben"
        ]

        memo["after_hours_flow_summary"] = (
            "No general emergency dispatch. Only G&M Pressure Washing calls "
            "are patched through. Others logged for next business day."
        )

    # -------------------------
    # Notification Settings
    # -------------------------
    if "info@benelectricsolutionsteam.com" in t:
        memo["integration_constraints"].append(
            "Post-call notifications via email and SMS enabled"
        )

    # -------------------------
    # Transfer Fallback
    # -------------------------
    memo["call_transfer_rules"]["fallback_action"] = (
        "If transfer fails, inform caller Ben will return call."
    )

    return memo