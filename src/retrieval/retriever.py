def prepare_policy_texts(policies):
    texts = []

    for p in policies:
        text = f"""
        Scheme: {p['name']}
        Category: {p['category']}
        Benefits: {p['benefits']}
        Eligibility: Income <= {p['eligibility']['income_max']}, Age >= {p['eligibility']['age_min']}
        Target: {p['target']}
        """
        texts.append(text)

    return texts