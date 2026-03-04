import os
from scripts.pipeline_demo import run_demo_pipeline
from scripts.pipeline_onboarding import run_onboarding_pipeline


def run_all():
    demo_folder = "dataset/demo_calls"
    onboarding_folder = "dataset/onboarding_calls"

    # Process demo calls
    for filename in os.listdir(demo_folder):
        if filename.endswith(".txt"):
            account_id = filename.split("_")[1]
            transcript_path = os.path.join(demo_folder, filename)
            run_demo_pipeline(transcript_path, account_id)

    # Process onboarding calls
    for filename in os.listdir(onboarding_folder):
        if filename.endswith(".txt"):
            account_id = filename.split("_")[1]
            transcript_path = os.path.join(onboarding_folder, filename)
            run_onboarding_pipeline(transcript_path, account_id)


if __name__ == "__main__":
    run_all()