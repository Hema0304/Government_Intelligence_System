import pandas as pd
def compare_policies(policies, names):
    selected = [p for p in policies if p["name"] in names]

    comparison = []

    for p in selected:
        comparison.append({
            "Name": p["name"],
            "Category": p["category"],
            "Benefits": p["benefits"],
            "Income Limit": p["eligibility"]["income_max"]
        })

    df = pd.DataFrame(comparison)
    return df