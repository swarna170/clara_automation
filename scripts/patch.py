import copy


def patch_memo(old_memo, new_memo):
    updated = copy.deepcopy(old_memo)
    changelog = []

    for key, value in new_memo.items():

        # Nested dictionaries (business_hours, call_transfer_rules)
        if isinstance(value, dict):
            for subkey, subvalue in value.items():
                if subvalue and updated[key].get(subkey) != subvalue:
                    changelog.append({
                        "field": f"{key}.{subkey}",
                        "old": updated[key].get(subkey),
                        "new": subvalue,
                        "reason": "Updated from onboarding"
                    })
                    updated[key][subkey] = subvalue

        # Lists
        elif isinstance(value, list):
            if value and updated[key] != value:
                changelog.append({
                    "field": key,
                    "old": updated[key],
                    "new": value,
                    "reason": "Updated from onboarding"
                })
                updated[key] = value

        # Simple fields
        else:
            if value and updated.get(key) != value:
                changelog.append({
                    "field": key,
                    "old": updated.get(key),
                    "new": value,
                    "reason": "Updated from onboarding"
                })
                updated[key] = value

    return updated, changelog