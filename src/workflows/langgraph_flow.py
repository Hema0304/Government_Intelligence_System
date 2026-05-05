from langgraph.graph import StateGraph

# ---------------- STATE ---------------- #
class GraphState(dict):
    pass


# ---------------- NODES ---------------- #

def validate_input(state):
    # Ensure required keys exist
    if "user" not in state:
        state["error"] = "Missing user data"
    if "policies" not in state:
        state["error"] = "Missing policies"

    return state


def run_eligibility(state):
    from src.eligibility.scorer import recommend_schemes

    user = state.get("user", {})
    policies = state.get("policies", [])

    if not user or not policies:
        state["results"] = []
        return state

    results = recommend_schemes(user, policies)
    state["results"] = results

    return state


def generate_explanations(state):
    from src.workflows.decision_mode import generate_explanation

    user = state.get("user", {})
    policies = state.get("policies", [])
    results = state.get("results", [])

    final_output = []

    for r, p in zip(results, policies):
        explanation = generate_explanation(
            user, p, r.get("eligible", False), r.get("reasons", [])
        )

        final_output.append({
            "name": r.get("name"),
            "eligible": r.get("eligible"),
            "explanation": explanation,
            "benefits": r.get("benefits")
        })

    state["final"] = final_output
    return state


# ---------------- GRAPH ---------------- #

def build_graph():
    graph = StateGraph(dict)

    graph.add_node("validate", validate_input)
    graph.add_node("eligibility", run_eligibility)
    graph.add_node("explain", generate_explanations)

    graph.set_entry_point("validate")

    graph.add_edge("validate", "eligibility")
    graph.add_edge("eligibility", "explain")

    graph.set_finish_point("explain")

    compiled = graph.compile()

    return compiled