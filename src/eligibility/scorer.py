from src.eligibility.rules_engine import check_eligibility

def score_policy(user, policy):
    score = 0

    # Income match
    if user["income"] <= policy["eligibility"]["income_max"]:
        score += 1

    # Age match
    if user["age"] >= policy["eligibility"]["age_min"]:
        score += 1

    return score


def recommend_schemes(user, policies):
    results = []

    for policy in policies:
        eligible, reasons = check_eligibility(user, policy)
        score = score_policy(user, policy)

        results.append({
            "name": policy["name"],
            "eligible": eligible,
            "reasons": reasons,
            "benefits": policy["benefits"],
            "score": score
        })

    # Sort by score (highest first)
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return results