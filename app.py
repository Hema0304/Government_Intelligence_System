import streamlit as st

# Core imports
from src.utils.helpers import load_policies

# Workflows
from src.workflows.info_mode import run_info_mode
from src.workflows.comparison import compare_policies
from src.workflows.langgraph_flow import build_graph


# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Policy Intelligence System",
    layout="wide",
)

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)






st.markdown("""
<style>
.main-title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    margin-bottom: 10px;
}

.sub-text {
    text-align: center;
    color: gray;
    margin-bottom: 30px;
}

.card {
    padding: 18px;
    border-radius: 12px;
    background-color: #1e1e1e;
    margin-bottom: 15px;
    border: 1px solid #333;
}
</style>
""", unsafe_allow_html=True)

# ------------------ HEADER ------------------
st.markdown('<div class="main-title">Policy Decision Intelligence System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">Understand • Evaluate • Decide Government Schemes</div>', unsafe_allow_html=True)


# ------------------ LOAD DATA ------------------
policies = load_policies()
graph = build_graph()

# ------------------ SIDEBAR ------------------
st.sidebar.title("Navigation")

mode = st.sidebar.radio(
    "Choose Mode",
    ["Explore Policies", "Check Eligibility"]
)

st.sidebar.markdown("---")
st.sidebar.info("AI-powered decision system")

# =========================================================
# 🔹 MODE 1: EXPLORE POLICIES
# =========================================================
if mode == "Explore Policies":
    st.markdown("## Explore Policies")

    query = st.text_input("Ask about government schemes")

    if st.button("Search"):
        if query.strip() == "":
            st.warning("Enter a query")
        else:
            with st.spinner("Searching..."):
                try:
                    response = run_info_mode(query, policies)
                    st.markdown("### AI Response")
                    st.markdown(f'<div class="card">{response}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error: {e}")

    # -------- Available Policies --------
    st.markdown("## Available Policies")

    cols = st.columns(3)

    for i, p in enumerate(policies):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="card">
                <b>{p['name']}</b><br><br>
                Category: {p['category']}<br>
                Benefit: {p['benefits']}
            </div>
            """, unsafe_allow_html=True)

    # -------- Comparison --------
    st.markdown("## Compare Policies")

    selected = st.multiselect(
        "Select policies",
        [p["name"] for p in policies]
    )

    if st.button("Compare"):
        if len(selected) < 2:
            st.warning("Select at least 2 policies")
        else:
            comparison = compare_policies(policies, selected)
            st.table(comparison)

# =========================================================
# 🔹 MODE 2: CHECK ELIGIBILITY (LANGGRAPH SAFE)
# =========================================================
elif mode == "Check Eligibility":
    st.markdown("## Check Eligibility")

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", min_value=18, max_value=100, value=25)

    with col2:
        income = st.number_input("Annual Income (₹)", min_value=0, value=500000)

    if st.button("Check Eligibility"):
        user = {"age": age, "income": income}

        state = {
            "user": user,
            "policies": policies
        }

        with st.spinner("Analyzing..."):
            try:
                result = graph.invoke(state)
            except Exception as e:
                st.error(f"Graph crashed: {e}")
                st.stop()

        # -------- SAFETY CHECKS --------
        if result is None:
            st.error("Graph returned None. Check workflow.")
            st.stop()

        if "final" not in result:
            st.error("No results generated.")
            st.write("DEBUG:", result)
            st.stop()

        # -------- DISPLAY --------
        st.markdown("##  Results")

        for item in result["final"]:
            status = " Eligible" if item["eligible"] else " Not Eligible"

            st.markdown(f"""
            <div class="card">
                <h4>{item['name']}</h4>
                <b>{status}</b><br><br>
                {item['explanation']}<br><br>
                <i>💡 {item['benefits']}</i>
            </div>
            """, unsafe_allow_html=True)

# ------------------ FOOTER ------------------
st.markdown("---")
st.caption("Built using LangGraph + RAG + Rule-based AI")