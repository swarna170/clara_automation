import os
import json
from scripts.extract_onboarding import extract_onboarding_memo
from scripts.patch import patch_memo
from scripts.prompt_generator import generate_agent_spec


def run_onboarding_pipeline(transcript_path, account_id):
    print(f"[INFO] Processing onboarding for account {account_id}")

    # -----------------------------------
    # Load onboarding transcript
    # -----------------------------------
    with open(transcript_path, "r", encoding="utf-8") as f:
        transcript = f.read()

    # -----------------------------------
    # Load existing v1 memo
    # -----------------------------------
    v1_path = f"outputs/accounts/account_{account_id}/v1/account_memo.json"

    if not os.path.exists(v1_path):
        print("[ERROR] v1 not found. Run demo pipeline first.")
        return

    with open(v1_path, "r", encoding="utf-8") as f:
        old_memo = json.load(f)

    # -----------------------------------
    # Extract onboarding updates
    # -----------------------------------
    new_memo = extract_onboarding_memo(transcript, account_id)

    # -----------------------------------
    # Apply safe patch (field-level override)
    # -----------------------------------
    updated_memo, changelog = patch_memo(old_memo, new_memo)

    # -----------------------------------
    # Remove resolved unknowns
    # -----------------------------------
    resolved_unknowns = [
        "Exact business hours not specified in demo",
        "Service pricing not discussed in demo",
        "Formal after-hours routing logic not defined"
    ]

    updated_memo["questions_or_unknowns"] = [
        q for q in updated_memo.get("questions_or_unknowns", [])
        if q not in resolved_unknowns
    ]

    # -----------------------------------
    # Generate updated Retell Agent Draft Spec (v2)
    # -----------------------------------
    agent_spec = generate_agent_spec(updated_memo, version="v2")

    # -----------------------------------
    # Prepare v2 output directory
    # -----------------------------------
    output_dir = f"outputs/accounts/account_{account_id}/v2"

    if os.path.exists(output_dir):
        print("[INFO] v2 already exists. Overwriting safely.")

    os.makedirs(output_dir, exist_ok=True)

    # -----------------------------------
    # Save updated account memo
    # -----------------------------------
    memo_path = os.path.join(output_dir, "account_memo.json")
    with open(memo_path, "w", encoding="utf-8") as f:
        json.dump(updated_memo, f, indent=4)

    # -----------------------------------
    # Save updated agent spec
    # -----------------------------------
    agent_spec_path = os.path.join(output_dir, "agent_spec.json")
    with open(agent_spec_path, "w", encoding="utf-8") as f:
        json.dump(agent_spec, f, indent=4)

    # -----------------------------------
    # Save changelog
    # -----------------------------------
    changelog_path = os.path.join(output_dir, "changelog.json")
    with open(changelog_path, "w", encoding="utf-8") as f:
        json.dump(changelog, f, indent=4)

    print("[INFO] v2 onboarding agent generated successfully.")