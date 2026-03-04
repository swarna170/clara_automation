import os
import json
from scripts.extract import extract_account_memo
from scripts.prompt_generator import generate_agent_spec


def run_demo_pipeline(transcript_path, account_id):
    print(f"[INFO] Processing demo for account {account_id}")

    # -----------------------------
    # Load transcript
    # -----------------------------
    with open(transcript_path, "r", encoding="utf-8") as f:
        transcript = f.read()

    # -----------------------------
    # Extract structured memo (v1)
    # -----------------------------
    account_memo = extract_account_memo(transcript, account_id)

    # -----------------------------
    # Generate Retell Draft Spec (v1)
    # -----------------------------
    agent_spec = generate_agent_spec(account_memo, version="v1")

    # -----------------------------
    # Create output directory
    # -----------------------------
    output_dir = f"outputs/accounts/account_{account_id}/v1"
    os.makedirs(output_dir, exist_ok=True)

    # -----------------------------
    # Save Account Memo
    # -----------------------------
    memo_path = os.path.join(output_dir, "account_memo.json")
    with open(memo_path, "w", encoding="utf-8") as f:
        json.dump(account_memo, f, indent=4)

    # -----------------------------
    # Save Retell Agent Draft Spec
    # -----------------------------
    agent_spec_path = os.path.join(output_dir, "agent_spec.json")
    with open(agent_spec_path, "w", encoding="utf-8") as f:
        json.dump(agent_spec, f, indent=4)

    print("[INFO] v1 demo agent generated successfully.")