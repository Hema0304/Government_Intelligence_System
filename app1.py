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


st.markdown("""
<style>
.stButton>button {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border-radius: 8px;
    border: none;
    padding: 10px 20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

/* App background */
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}

/* Text input */
input {
    background-color: #1e293b !important;
    color: white !important;
    border-radius: 8px !important;
}

/* Buttons */
.stButton>button {
    background-color: #3b82f6;
    color: white;
    border-radius: 8px;
    padding: 10px 20px;
    border: none;
}

.stButton>button:hover {
    background-color: #2563eb;
}

/* Cards */
.custom-card {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 15px;
    border: 1px solid #334155;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.4);
}



/* Headings */
h1, h2, h3, h4 {
    color: #f1f5f9;
}

/* Subtext */
.sub-text {
    color: #94a3b8;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; padding:30px 0;">
    <h1 style="font-size:48px;">Policy Intelligence System</h1>
    <p style="color:gray; font-size:18px;">
        Find, Compare & Check Eligibility for Government Schemes
    </p>
</div>
""", unsafe_allow_html=True)

policies = load_policies()
graph = build_graph()

tab1, tab2 = st.tabs([" Explore Policies", " Check Eligibility"])

with tab1:
    st.markdown("##  Explore Policies")

    query = st.text_input("Ask your question")

    if st.button("Search"):
        if query.strip() == "":
            st.warning("Enter a query")
        else:
            with st.spinner("Analyzing..."):
                response = run_info_mode(query, policies)

            st.markdown("### Answer")
            st.markdown(f"""
            <div style="
                padding:20px;
                border-radius:12px;
                background:#262730;
                margin-bottom:15px;
            ">
                {response}
            </div>
            """, unsafe_allow_html=True)

    # -------- POLICIES GRID --------
    st.markdown("##  Available Policies")

    cols = st.columns(3)

    for i, p in enumerate(policies):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="
                padding:15px;
                border-radius:12px;
                background: linear-gradient(135deg, #141E30, #243B55);
                color: white;
                margin-bottom:15px;
                box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
            ">
                <b>{p['name']}</b><br><br>
                 {p['category']}<br>
                 {p['benefits']}
            </div>
            """, unsafe_allow_html=True)
    st.markdown("##  Compare Policies")

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
            
            
with tab2:
    st.markdown("##  Check Eligibility")

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", 18, 100, 25)

    with col2:
        income = st.number_input("Income", 0, 10000000, 500000)

    if st.button("Check Eligibility"):
        user = {"age": age, "income": income}
        state = {"user": user, "policies": policies}

        with st.spinner("Evaluating..."):
            result = graph.invoke(state)

        if result and "final" in result:

            st.markdown("##  Results")

            for item in result["final"]:
                badge = " Eligible" if item["eligible"] else " Not Eligible"
                color = "#0f5132" if item["eligible"] else "#842029"

                st.markdown(f"""
                <div style="
                    padding:20px;
                    border-radius:12px;
                    background:{color};
                    margin-bottom:15px;
                    box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
                ">
                    <h4>{item['name']}</h4>
                    <b>{badge}</b><br><br>
                    {item['explanation']}<br><br>
                    {item['benefits']}
                </div>
                """, unsafe_allow_html=True)

            # -------- SUMMARY --------
            eligible_count = sum(1 for i in result["final"] if i["eligible"])

            st.markdown(f"""
            ###  Summary
            - Eligible Schemes: {eligible_count}  
            - Total Evaluated: {len(result["final"])}
            """)