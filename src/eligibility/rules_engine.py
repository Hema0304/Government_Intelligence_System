def check_eligibility(user, policy):
    reasons = []
    eligible = True

    if user["income"] > policy["eligibility"]["income_max"]:
        eligible = False
        reasons.append("Income exceeds limit")

    if user["age"] < policy["eligibility"]["age_min"]:
        eligible = False
        reasons.append("Age below minimum requirement")

    return eligible, reasons