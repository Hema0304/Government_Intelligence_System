def evaluate_system(policies):
    test_cases = [
        {"age": 25, "income": 500000},
        {"age": 40, "income": 1200000},
    ]

    results = []

    for test in test_cases:
        matched = []

        for p in policies:
            if test["income"] <= p["eligibility"]["income_max"]:
                matched.append(p["name"])

        results.append({
            "input": test,
            "expected_matches": matched
        })

    return results