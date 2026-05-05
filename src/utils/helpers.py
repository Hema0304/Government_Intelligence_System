import json

def load_policies():
    with open("data/processed/policies.json", "r") as f:
        return json.load(f)