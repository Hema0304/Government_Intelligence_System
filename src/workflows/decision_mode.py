from src.llm.generator import generate_response

def generate_explanation(user, policy, eligible, reasons):
    prompt = f"""
    User Profile:
    Age: {user['age']}
    Income: {user['income']}

    Policy: {policy['name']}
    Benefits: {policy['benefits']}

    Eligibility Result: {"Eligible" if eligible else "Not Eligible"}
    Reasons: {reasons}

    Explain clearly in 3-4 lines in simple English.
    """

    return generate_response(prompt)