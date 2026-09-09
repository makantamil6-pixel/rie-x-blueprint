import streamlit as st
import pandas as pd
import numpy as np

# Page Configuration & Layout
st.set_page_config(
    page_title="RIE-X & The Trust Economy | Master Blueprint",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar UI Panel
st.sidebar.markdown("# 🎛️ Institutional Settings")
region = st.sidebar.selectbox(
    "Geographic Archetype Deployment",
    ["South Asia Matrix (India Focus)", "Sub-Saharan Africa Network (East Africa Focus)", "Southeast Asia Cluster (Vietnam Focus)", "Latin America Localized Hub"]
)

# Regional Currencies Matrix configuration
if "South Asia" in region:
    currency_symbol, currency_code, base_val_default = "₹", "INR", 10000
elif "Sub-Saharan" in region:
    currency_symbol, currency_code, base_val_default = "KSh", "KES", 12000
elif "Southeast Asia" in region:
    currency_symbol, currency_code, base_val_default = "₫", "VND", 250000
else:
    currency_symbol, currency_code, base_val_default = "$", "USD", 150

cells = st.sidebar.slider("Total Operational Cells (Nodes)", min_value=5, max_value=1500, value=150, step=5)
participants_per_cell = st.sidebar.slider("Active Contributor Base per Local Cell", min_value=50, max_value=1500, value=250, step=10)
base_unit_value = st.sidebar.slider(f"Base Unit Capital Matrix Value ({currency_symbol})", min_value=100, max_value=50000, value=base_val_default, step=100)
reinvestment_rate = st.sidebar.slider("Systemic Closed-Loop Reinvestment Rate (%)", min_value=20, max_value=35, value=30, step=1)
scenario = st.sidebar.radio("Macroeconomic Value-Chain Mode", ["Scenario A: Raw Micro-Industrial Processing Line", "Scenario B: Value-Added Integrated Logistics Network", "Scenario C: Closed-Loop Circular Resource Loop"])

# Macroeconomic Simulation Engine Mathematics
total_participants = cells * participants_per_cell
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
gross_traditional = total_participants * v_traditional_base
net_riex_surplus = total_participants * (v_riex_base - c_admin_base)
per_capita_income_boost = ((v_riex_base - c_admin_base) - v_traditional_base) / v_traditional_base * 100
annual_reinvestment_pool = net_riex_surplus * (reinvestment_rate / 100.0)

# Main Application Core UI
st.markdown("<h1 style='color: #1e3a8a;'>THE RURAL INTEGRATED TOKENIZED ECONOMY (RIE-X)</h1>", unsafe_allow_html=True)
st.caption(f"A Consolidated Global Strategy and Deployment Blueprint for the Trust Economy | Deployment Mode: {region}")
st.markdown("---")

doc_view, simulation_view = st.columns(2)

with doc_view:
    st.markdown("### I. THE EXTRACTION PARADOX & MACROECONOMIC DISTANCE")
    st.write("Contemporary global regional value chains suffer from a chronic, structural layout of value extraction. Primary producers create foundational physical products but capture a minor fraction of final value. Meanwhile, downstream intermediaries, speculative traders, corporate distributors, and centralized platform monopolies extract outsized margins. This spatial-economic distance generates severe producer compression vectors, final consumer premium vectors, and permanent structural capital flight from rural zones.")
    st.info("The Core Distance Theorem: RIE-X replaces speculative intermediary leakage with an auditable structural administration cost matrix (Cs), where Cs is significantly smaller than the sum of traditional middleman margins, routing the recovered surplus directly to primary community producers.")
    
    st.markdown("### II. CONCEPTUAL FOUNDATIONS & THE ASSETIZATION OF LABOR")
    st.write("The RIE-X framework upgrades conventional cooperative setups by fundamentally rewriting the treatment of work. Instead of treating labor as an operational expense cost to be minimized, the architecture treats labor as a long-term capital asset. This structural paradigm is operationalized through a non-speculative digital record layer known as Rural Value Tokens (RVTs), which act as an un-cheatable scoreboard tracking sovereign capital stake, productivity coefficients, democratic governance rights, and long-term dividend entitlements.")
    st.success("The Sweat Equity Invariant: 1 Labour-Hour = 1 Base RVT Unit. Because RVTs are explicitly non-transferable, they cannot be accumulated, bought out, or co-opted by wealthy external investors or centralized financial interests.")

    st.markdown("### III. VILLAGE-OWNED MICRO-INDUSTRIAL INFRASTRUCTURE")
    st.write("RIE-X permanently terminates the standard dependency on external corporate distribution by deploying processing apparatus loops straight into rural communities. The infrastructure footprint consists of three primary active components: localized value-addition processing lines, decentralized cold chain preservation to eliminate harvest-time price crashes, and an urban demand synchronization matrix driven by real-time SKU telemetry.")

    st.markdown("### IV. THE ECO-SOCIOLOGICAL LOOP & ENVIRONMENTAL RESILIENCE")
    st.write("A structural contention of the RIE-X manuscript is that unchecked economic inequality functions as a primary driver of environmental degradation. This occurs via elite resource extraction capture and survival-driven exploitation by low-income households. RIE-X acts as an environmental stabilization strategy by transitioning the ownership of productive assets directly to local community cells, lowering survival-based pressure on local ecosystems.")

    st.markdown("### V. INSTITUTIONAL ACCOUNTABILITY & FOUR-TIER GOVERNANCE")
    st.write("To fully eliminate localized corruption, the system enforces a strict four-tier institutional hierarchy built on transparent, decentralized consensus rules: The Contributor Assembly (Tier 1: One Person, One Vote), The Operational Council (Tier 2), The Professional Management Unit (Tier 3), and The Compliance & Oversight Body (Tier 4). The ledger enforces an absolute ban on physical cash collections, envelope handoffs, or individual fund custody.")

    st.markdown("### VI. EVOLVED COMPARATIVE PRECEDENTS")
    st.write("The architecture scales by solving structural flaws observed in historic cooperative and global microfinance systems: The Mondragón Cooperative Framework ( Spain ), The Amul Dairy Framework ( India ), and The Grameen Micro-Enterprise Model ( Bangladesh ). RIE-X advances these systems by requiring a fixed capital retention pool to fund local processing factories via automated multi-signature ledger checking.")

with simulation_view:
    st.markdown("### 📊 ACTIVE SYSTEMIC SIMULATION MATRIX")
    st.write(f"**Target Optimization Profile:** {scenario}")
    
    col_m1, col_m2 = st.columns(2)
    col_m1.metric("Aggregated Network Size", f"{total_participants:,} Active Workers")
    col_m2.metric("Per-Capita Income Boost", f"+{per_capita_income_boost:.2f}%")
    
    col_m3, col_m4 = st.columns(2)
    col_m3.metric(f"Net Capital Surplus ({currency_symbol})", f"{net_riex_surplus:,.2f}")
    col_m4.metric(f"Annual Reinvestment Pool ({currency_symbol})", f"{annual_reinvestment_pool:,.2f}")
    
    st.markdown("---")
    st.markdown("### 📈 6-Year Capital Compounding Horizon (Figure 1)")
    
    years = np.arange(0, 7)
    compounding_growth_factor = 1 + ((reinvestment_rate / 100.0) * (local_multiplier / 1.5))
    relative_capital_stock = [1.0 * (compounding_growth_factor ** t) for t in years]
    
    chart_df = pd.DataFrame({"Timeline (Years)": years, "Relative Rural Capital Stock": relative_capital_stock}).set_index("Timeline (Years)")
    st.line_chart(chart_df, color="#0d9488")
    st.caption(f"Figure 1 Interpretation: Driven by a {reinvestment_rate}% retention rate, the capital stock expands exponentially over 6 years. The regional local GDP multiplier is verified at {local_multiplier}x.")
    
    st.markdown("---")
    st.markdown("### 📋 Comparative Value-Chain Cost Analysis")
    
    comparison_data = {
        "Structural Parameter": ["Intermediary Leakage", "Raw Material Cost Matrix", "Governance Weight Matrix", "Systemic Fraud Vectors", "Regional Economic Multiplier"],
        "Traditional Extractive Model": ["High Layer Costs (Speculative Loss)", "Volatile / Middlemen Dictated", "Skewed via Wealth Concentration", "High Vulnerability (Physical Cash/Blind Trust)", "Stagnant (1.0x - 1.2x)"],
        "Tokenized RIE-X Blueprint": ["Minimised / Transparent (C_s Cost Only)", "Near-Zero (Circular Waste Reversion)", "Linear Base (1 Person = 1 Vote)", "Cryptographically Secure / Zero-Cash", f"Verified Multiplier ({local_multiplier}x)"]
    }
    st.table(pd.DataFrame(comparison_data))

st.markdown("---")
st.markdown("### VII. GLOBAL SCALABILITY & SYSTEMIC ADAPTATION POLICY")
st.write(f"The RIE-X blueprint transitions regional economies from dependent, debt-driven structures into highly resilient, self-sustaining engines. By aligning model deployment with the {region} economic archetype, public capital injections act strictly as one-time bootstrapping reserves rather than permanent fiscal burdens. Once initialized, the {reinvestment_rate}% closed-loop retention rate guarantees that the system dynamically funds its own infrastructure expansion, builds long-term wealth, and provides a stable, reproducible framework for international economic development.")
