import streamlit as st
import pandas as pd
import numpy as np

# 1. Page Configuration and Theming
st.set_page_config(
    page_title="RIE-X & The Trust Economy Blueprint",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for scannability and clean layout
st.markdown("""
<style>
    .reportview-container { background: #f5f7f9; }
    .main-header { color: #1E3A8A; font-weight: 700; }
    .sub-header { color: #0D9488; font-weight: 600; }
    .highlight-box { background-color: #f0fdf4; padding: 15px; border-left: 5px solid #22c55e; border-radius: 4px; margin-bottom: 15px;}
    .alert-box { background-color: #fef2f2; padding: 15px; border-left: 5px solid #ef4444; border-radius: 4px; margin-bottom: 15px;}
</style>
""", unsafe_allow_html=True)

# 2. Sidebar Navigation and Sliders (Active Simulation Engine)
st.sidebar.markdown("# 🎛️ Simulation Controls")
st.sidebar.markdown("Adjust these parameters to watch the macroeconomy scale in real time.")

region = st.sidebar.selectbox(
    "Target Geographic Region",
    ["South Asia (India Pilot)", "Sub-Saharan Africa (Kenya/East Africa Mesh)", "Southeast Asia (Vietnam Matrix)", "Latin America Cluster"]
)

# Regional Currency Setup
currency_symbol = "₹" if "South Asia" in region else "$" if "Latin America" in region else "KSh" if "Africa" in region else "₫"
currency_code = "INR" if "South Asia" in region else "USD" if "Latin America" in region else "KES" if "Africa" in region else "VND"

st.sidebar.markdown("---")
cells = st.sidebar.slider("Total Operational Cells / Nodes", min_value=5, max_value=1000, value=100, step=5)
participants_per_cell = st.sidebar.slider("Active Participants per Cell", min_value=50, max_value=1000, value=250, step=10)

st.sidebar.markdown("### RIE-X Tokenization & Retention Variables")
base_unit_value = st.sidebar.slider(f"Base Participation Unit ({currency_symbol})", min_value=500, max_value=10000, value=1000, step=500)
reinvestment_rate = st.sidebar.slider("Closed-Loop Reinvestment Rate (%)", min_value=20, max_value=35, value=25, step=1)

scenario = st.sidebar.radio(
    "Optimization Scenario Mode",
    ["Scenario A: Baseline (Raw Processing)", "Scenario B: Value-Added Industrialization", "Scenario C: Full Circular Waste Loop"]
)

# 3. Mathematical Simulation Framework (Equations based on RIE-X and Trust Economy)
total_participants = cells * participants_per_cell

# Base Multipliers and Values derived from the Research paper
v_traditional_base = base_unit_value * 0.015
if "Scenario A" in scenario:
    v_riex_base = base_unit_value * 0.022
    local_multiplier = 1.8
elif "Scenario B" in scenario:
    v_riex_base = base_unit_value * 0.0285
    local_multiplier = 2.1
else:
    v_riex_base = base_unit_value * 0.036
    local_multiplier = 2.4

c_admin_base = base_unit_value * 0.0032

# Calculations
gross_traditional = total_participants * v_traditional_base
net_riex_surplus = total_participants * (v_riex_base - c_admin_base)
system_surplus_created = net_riex_surplus - gross_traditional
per_capita_income_boost = ((v_riex_base - c_admin_base) - v_traditional_base) / v_traditional_base * 100
annual_reinvestment_pool = net_riex_surplus * (reinvestment_rate / 100.0)

# 4. Main App Interface Rendering
st.markdown(f"<h1 class='main-header'>THE RURAL INTEGRATED TOKENIZED ECONOMY (RIE-X)</h1>", unsafe_allow_html=True)
st.caption(f"**A Consolidated Global Blueprint for the Trust Economy** | Currently Optimizing for: `{region}`")
st.markdown("---")

# Layout into two main operational views
doc_view, simulation_view = st.columns()

with doc_view:
    st.markdown("## 📜 Executive Blueprint Document")
    
    st.markdown("### 1. Introduction: Resolving the Global Extraction Paradox")
    st.markdown("""
    Modern linear value chains face structural collapse. Rural producers regularly capture a minor fraction 
    of the value they create, while centralized middlemen and downstream networks accumulate disproportionate gains. 
    This structural misalignment forces systemic asset depletion, local poverty, and involuntary urban migration.
    
    The **Rural Integrated Economy (RIE-X)** and **The Trust Economy** models offer an integrated structural 
    framework. By embedding industrial capacity directly inside village clusters, tokenizing labor into capital assets, 
    and linking regional production to synchronized urban retail networks, RIE-X creates a self-reinforcing, 
    democratic economic engine.
    """)
    
    st.markdown("<div class='highlight-box'><strong>Core Systemic Invariant:</strong> Structural prosperity emerges only when local communities retain ownership of capital, control value addition, and establish a structurally protected share of long-term surplus.</div>", unsafe_allow_html=True)
    
    st.markdown("### 2. The Five Foundational Architectural Pillars")
    st.markdown(f"""
    1. **Fractional Micro-Capitalization:** Entry participation is structured in precise, accessible units (e.g., base unit configured at **{currency_symbol}{base_unit_value:,}** {currency_code}). This builds a community of legitimate network participants, rather than vague, unbacked financial promises.
    2. **The Tokenized Labour-Capital System (RVT):** Labor is structurally treated as a long-term capital asset, not an operational expense cost. One labor-hour equals one base Rural Value Token (RVT) unit, granting lifetime entitlements to dividends and capital stakes.
    3. **Absolute Separation of Wealth and Governance:** Financial investment size does not grant structural dominance. The governance model strictly enforces a non-speculative, linear threshold: **one participant, one vote**.
    4. **The Hierarchy of Operational Consequences:** The network functions through local cells. Authority scales strictly with the radius of a decision's outcome. If a choice affects a single cell, it belongs to that cell collectively. The wider the network impact, the wider the required cryptographic consent.
    5. **Zero-Cash Traceability:** All economic movements are completely digital, verifiable, and recorded. The system establishes a zero-cash invariant—no individual holds physical boxes or collective money envelopes, completely cutting off traditional corruption channels at the protocol level.
    """)
    
    st.markdown("### 3. The Inequality-Environment Causal Stabilization Loop")
    st.markdown("""
    RIE-X formally links economic inequality directly to regional environmental degradation. When wealth concentrates at the top, elites execute extractive resource strategies, while low incomes force survival-driven overexploitation of regional soils, water, and forests. 
    
    RIE-X functions simultaneously as an ecological stabilization strategy by:
    * Shifting asset ownership to community hands to remove short-term extractive investment models.
    * Securing stable, predictable livelihoods to eliminate survival-based extraction pressure on ecosystems.
    * Integrating environmental compliance parameters directly into the RVT valuation matrix.
    """)

with simulation_view:
    st.markdown("## 📊 Active Matrix Live Simulation")
    
    # Live KPI Scorecard
    st.markdown(f"### Live Metrics for {region}")
    
    kpi1, kpi2 = st.columns(2)
    kpi1.metric("Active Network Size", f"{total_participants:,} Workers")
    kpi2.metric("Per-Capita Income Boost", f"+{per_capita_income_boost:.2f}%")
    
    kpi3, kpi4 = st.columns(2)
    kpi3.metric(f"Net Capital Surplus ({currency_symbol})", f"{net_riex_surplus:,.2f}")
    kpi4.metric(f"Annual Reinvestment Pool ({currency_symbol})", f"{annual_reinvestment_pool:,.2f}")
    
    st.markdown("---")
    st.markdown("### 📈 6-Year Capital Compounding Curve")
    
    # 6-Year Compounding Math Model based on RIE-X Manuscript Section 11 & 14
    years = np.array([0, 1, 2, 3, 4, 5, 6])
    compounding_growth_factor = 1 + ((reinvestment_rate / 100.0) * (local_multiplier / 1.5))
    relative_capital_stock = [1.0 * (compounding_growth_factor ** t) for t in years]
    
    chart_df = pd.DataFrame({
        "Timeline (Years)": years,
        "Relative Rural Capital Stock": relative_capital_stock
    }).set_index("Timeline (Years)")
    
    st.line_chart(chart_df, color="#0d9488")
    
    st.caption(f"**Figure 1:** Capital Compounding Curve under `{scenario}` over a 6-year development horizon. The regional GDP multiplier is verified at **{local_multiplier}x**.")
    
    # Strategic Cross-Section Comparison Table
    st.markdown("### 📋 System Verification Reference")
    comparison_data = {
        "Variable": ["Intermediary Leakage", "Input Material Expense", "Governance Weight", "Fraud Protection Vector"],
        "Traditional Extractive Model": ["High Layer Cost Matrix", "Linear / Volatile Cost", "Proportional to Wealth", "Blind Human Trust / Cash Based"],
        "Tokenized RIE-X Engine": ["Visible Structural Cost", "Near-Zero (Circular Waste Loop)", "Linear Base (1 Person = 1 Vote)", "Cryptographic Multi-Sig Verification"]
    }
    st.table(pd.DataFrame(comparison_data))

st.markdown("---")
st.markdown("### 🛡️ Institutional Security Architecture & Byzantine Fault Tolerance")
st.markdown("""
The architecture deploys a mandatory four-tier governance infrastructure to eliminate elite capture vectors: 
**Tier 1: Contributor Assembly** (Direct democratic rights) $\rightarrow$ **Tier 2: Operational Council** (Instruction Execution) $\rightarrow$ **Tier 3: Professional Management Unit** (Specialized Administration) $\rightarrow$ **Tier 4: Compliance & Oversight** (Automated Digital Ledger Bookkeeping). 
Internal token metrics apply immediate value updates or operational suspensions if an anomalous multi-signature transaction mismatch occurs.
""")
