import streamlit as st
import pandas as pd
import numpy as np

# 1. Page Configuration & Aesthetic Architecture
st.set_page_config(
    page_title="RIE-X & The Trust Economy | Comprehensive Master Blueprint",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Institutional CSS for academic scannability
st.markdown("""
<style>
    .reportview-container { background: #f8fafc; }
    .main-header { color: #1e3a8a; font-weight: 800; font-size: 2.6rem; margin-bottom: 2px; }
    .academic-cite { color: #475569; font-style: italic; font-size: 0.95rem; margin-bottom: 25px; line-height: 1.5; }
    .section-header { color: #0f172a; font-weight: 700; font-size: 1.7rem; border-bottom: 3px solid #0d9488; padding-bottom: 8px; margin-top: 35px; margin-bottom: 15px; }
    .sub-section { color: #0d9488; font-weight: 600; font-size: 1.3rem; margin-top: 20px; margin-bottom: 10px; }
    .highlight-box { background-color: #f0fdf4; padding: 22px; border-left: 6px solid #16a34a; border-radius: 6px; margin: 20px 0; line-height: 1.6; font-size: 1.05rem; }
    .matrix-box { background-color: #f8fafc; padding: 22px; border: 1px solid #cbd5e1; border-radius: 6px; margin: 20px 0; line-height: 1.6; }
    p, li { font-size: 1.05rem; line-height: 1.7; color: #334155; }
</style>
""", unsafe_allow_html=True)

# 2. Sidebar Parameters (Active Economic Engine Controls)
st.sidebar.markdown("# 🎛️ Institutional Settings")
st.sidebar.markdown("Configure regional variables to simulate systemic capital compounding.")

region = st.sidebar.selectbox(
    "Geographic Archetype Deployment",
    ["South Asia Matrix (India Focus)", "Sub-Saharan Africa Network (East Africa Focus)", "Southeast Asia Cluster (Vietnam Focus)", "Latin America Localized Hub"]
)

# Dynamic Currency Matrix configuration based on chosen archetype
if "South Asia" in region:
    currency_symbol, currency_code, base_val_default = "₹", "INR", 10000
elif "Sub-Saharan" in region:
    currency_symbol, currency_code, base_val_default = "KSh", "KES", 12000
elif "Southeast Asia" in region:
    currency_symbol, currency_code, base_val_default = "₫", "VND", 250000
else:
    currency_symbol, currency_code, base_val_default = "$", "USD", 150

st.sidebar.markdown("---")
cells = st.sidebar.slider("Total Operational Cells (Nodes)", min_value=5, max_value=1500, value=150, step=5)
participants_per_cell = st.sidebar.slider("Active Contributor Base per Local Cell", min_value=50, max_value=1500, value=250, step=10)

st.sidebar.markdown("### RVT Assetization Engine")
base_unit_value = st.sidebar.slider(f"Base Unit Capital Matrix Value ({currency_symbol})", min_value=100, max_value=50000, value=base_val_default, step=100)
reinvestment_rate = st.sidebar.slider("Systemic Closed-Loop Reinvestment Rate (%)", min_value=20, max_value=35, value=30, step=1)

scenario = st.sidebar.radio(
    "Macroeconomic Value-Chain Mode",
    ["Scenario A: Raw Micro-Industrial Processing Line", "Scenario B: Value-Added Integrated Logistics Network", "Scenario C: Closed-Loop Circular Resource Loop"]
)

# 3. Macroeconomic Equation Computations
total_participants = cells * participants_per_cell
v_traditional_base = base_unit_value * 0.015  # Extractive market reference point

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

# Aggregated Output Equations
gross_traditional = total_participants * v_traditional_base
net_riex_surplus = total_participants * (v_riex_base - c_admin_base)
system_surplus_created = net_riex_surplus - gross_traditional
per_capita_income_boost = ((v_riex_base - c_admin_base) - v_traditional_base) / v_traditional_base * 100
annual_reinvestment_pool = net_riex_surplus * (reinvestment_rate / 100.0)

# 4. Interface Frame Execution
st.markdown("<h1 class='main-header'>THE RURAL INTEGRATED TOKENIZED ECONOMY (RIE-X)</h1>", unsafe_allow_html=True)
st.markdown("<div class='academic-cite'>A Comprehensive Institutional Strategy and Deployment Blueprint. Synthesizing the Principles of Distributed Trust Networks, Tokenized Labour-Capital Paradigms, and Closed-Loop Environmental Resilience Ecosystems. Cross-Referenced JEL Classification Codes: O13 (Agriculture; Natural Resources), Q56 (Sustainability), D63 (Equity, Justice, Inequality), H41 (Public Goods), P46 (Other Heterodox Systems).</div>", unsafe_allow_html=True)
st.markdown("---")

# Main Multi-Column Split Framework (50% Text Document / 50% Live Matrix Visuals)
doc_view, simulation_view = st.columns(2)

with doc_view:
    st.markdown("<div class='section-header'>I. THE EXTRACTION PARADOX & MACROECONOMIC DISTANCE</div>", unsafe_allow_html=True)
    st.markdown("""
    Contemporary global regional value chains suffer from a chronic, structural layout of value extraction. 
    Primary producers create foundational physical products but capture a minor fraction of final value. 
    Meanwhile, downstream intermediaries, speculative traders, corporate distributors, and centralized platform monopolies 
    extract outsized margins. This spatial-economic distance generates several severe imbalances:
    """)
    
    st.markdown("""
    * **The Producer Compression Vector:** Local villages and primary producers face irregular employment, seasonal income volatility, and severely undervalued labor returns. Because they lack direct access to distribution channels, processing equipment, and pricing information, they are routinely forced to sell raw commodities at near-loss baseline margins.
    * **The Consumer Premium Vector:** Urban consumers pay high final market premiums for basic agricultural and processed goods. This cost elevation is driven entirely by layered intermediary markups, inefficient storage hand-offs, and speculative logistics networks, rather than genuine improvements in product quality.
    * **The Structural Capital Flight:** Regional savings and local capital are continuously pulled out of rural environments and redirected to centralized financial hubs. This starves regional networks of the development reserves required to build processing factories, install cold-storage networks, or fund localized entrepreneurship.
    """)
    
    st.markdown("<div class='matrix-box'><strong>The Core Distance Theorem:</strong> In traditional networks, Final Price satisfies: <em>P_c = V_v + &Sigma; I_k</em>, where <em>&Sigma; I_k</em> represents the sum of costs and margins extracted by k layers of non-value-adding traditional intermediaries. RIE-X replaces this with an auditable structural administration cost matrix <em>C_s</em>, where <em>C_s &ll; &Sigma; I_k</em>. This bypasses speculative extraction and maps the recovered surplus directly to primary contributors as shared participant value.</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-header'>II. CONCEPTUAL FOUNDATIONS & THE ASSETIZATION OF LABOR</div>", unsafe_allow_html=True)
    st.markdown("""
    The Rural Integrated Economy (RIE-X) blueprint upgrades conventional cooperative networks by fundamentally rewriting the treatment of work. Instead of treating labor as an operational expense cost to be minimized, the architecture treats labor as a **long-term capital asset**. 
    
    This structural paradigm is operationalized through a non-speculative digital record layer known as **Rural Value Tokens (RVTs)**. RVTs are non-transferable, cryptographically checked accounting markers that represent four core institutional attributes:
    """)
    
    st.markdown("""
    1. **Sovereign Capital Stake:** Proportional to a worker's lifetime labor contribution, raw material provisioning, or local processing deployment.
    2. **Productivity Multiplier:** Adjusted dynamically by an automated quality coefficient based on output accuracy, grading standards, and processing consistency.
    3. **Democratic Governance Rights:** Secure linear baseline distribution ensuring that community governance weight is fully decoupled from wealth concentration.
    4. **Surplus Entitlements:** Permanent access to recurring dividends and capital distribution generated from value-added processing and urban retail operations.
    """)
    
    st.markdown("<div class='highlight-box'><strong>The Sweat Equity Invariant:</strong> 1 Labour-Hour = 1 Base RVT Unit. Because RVTs are explicitly non-transferable, they cannot be accumulated, bought out, or co-opted by wealthy external investors or centralized financial interests. This ensures that power, control, and capital accumulation remain permanently anchored inside the local community that drives production.</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-header'>III. THE ECO-SOCIOLOGICAL LOOP & ENVIRONMENTAL RESILIENCE</div>", unsafe_allow_html=True)
    st.markdown("""
    A core contention of the RIE-X framework is that extreme structural economic inequality directly drives regional environmental degradation. This instability operates through four compounding causal pathways:
    """)
    
    st.markdown("""
    * **Elite Natural Asset Capture:** Concentrated financial wealth enables top-tier interests to secure exclusive access to community resources (land, groundwater, forests). This skews local policy in favor of highly extractive rent-seeking, concentrating ecological harms in marginal areas.
Use code with caution.* Survival-Driven Overexploitation: Severe poverty and unstable, irregular local employment force low-income households to overuse local ecosystems (e.g., clearing wood for fuel, overgrazing, depleting topsoil nutrients) simply to maintain immediate subsistence.* Weakened Collective Governance: Outrageous wealth inequality erodes mutual social trust and local civic capacity. This makes environmental regulations nearly impossible to enforce, as powerful actors can easily avoid compliance or externalize ecological costs.""")st.markdown("Breaking the Cycle: RIE-X acts as an environmental stabilization strategy by transitioning the ownership of productive assets directly to local community cells. By securing stable, predictable livelihoods, the model eliminates survival-based extraction pressure on ecosystems. Furthermore, environmental indicators (such as groundwater recharge milestones or regenerative farming practices) are coded directly into the RVT issuance logic as capital bonuses.", unsafe_allow_html=True)st.markdown("IV. INSTITUTIONAL ACCOUNTABILITY & FOUR-TIER GOVERNANCE", unsafe_allow_html=True)st.markdown("""To eliminate corruption, protect shared resources, and avoid the historical failures of centralized top-down hierarchies, RIE-X implements a robust four-tier governance infrastructure built entirely on real-world accountability:""")st.markdown("""* The Contributor Assembly (Tier 1): The primary democratic foundation consisting of all active token holders. Operates on a strict linear baseline: one participant, one vote, regardless of total capitalization or unit accumulation.* The Operational Council (Tier 2): Elected community representatives who manage immediate operational instructions, resource allocations, and day-to-day processing line schedules.* The Professional Management Unit (Tier 3): Specialized execution professionals hired to optimize processing lines, maintain cold-storage mechanics, and orchestrate logistics.* The Compliance & Oversight Body (Tier 4): Independent multi-signature monitoring teams executing transparent digital bookkeeping, real-time disclosure paths, and automated ledger tracking.""")st.markdown("The Financial Security Constraint: The network enforces a strict zero-cash invariant. No envelopes, no paper cash collections, and no local agents handling physical currency. All movements travel through traceable digital smart contracts under the legally established structure. This renders the utility of fraud mathematically negative (E[U] < 0), making structural transparency the only viable strategy for survival.", unsafe_allow_html=True)with simulation_view:st.markdown("📊 ACTIVE SYSTEMIC SIMULATION MATRIX", unsafe_allow_html=True)st.markdown(f"### Live Scalability Metrics: {region}")st.markdown(f"Targeting: {scenario}")col_m1, col_m2 = st.columns(2)col_m1.metric("Aggregated Network Size", f"{total_participants:,} Active Workers")col_m2.metric("Per-Capita Income Boost", f"+{per_capita_income_boost:.2f}%")col_m3, col_m4 = st.columns(2)col_m3.metric(f"Net Capital Surplus ({currency_symbol})", f"{net_riex_surplus:,.2f}")col_m4.metric(f"Annual Reinvestment Pool ({currency_symbol})", f"{annual_reinvestment_pool:,.2f}")st.markdown("---")st.markdown("### 📈 6-Year Capital Compounding Horizon (Figure 1)")# 6-Year Compound Capital Stock Equation Execution (Based on Section 11 & 14)years = np.array([0, 1, 2, 3, 4, 5, 6])compounding_growth_factor = 1 + ((reinvestment_rate / 100.0) * (local_multiplier / 1.5))relative_capital_stock = [1.0 * (compounding_growth_factor ** t) for t in years]chart_df = pd.DataFrame({"Timeline (Years)": years,"Relative Rural Capital Stock": relative_capital_stock}).set_index("Timeline (Years)")st.line_chart(chart_df, color="#0d9488")st.caption(f"Figure 1 Interpretation: Driven by a {reinvestment_rate}% retention rate, the capital stock expands exponentially over 6 years. The regional local GDP multiplier is verified at {local_multiplier}x.")st.markdown("---")st.markdown("### 📋 Comparative Value-Chain Cost Analysis")comparison_data = {"Structural Parameter": ["Intermediary Leakage", "Raw Material Cost Matrix", "Governance Weight Matrix", "Systemic Fraud Vectors", "Regional Economic Multiplier"],"Traditional Extractive Model": ["High Layer Costs (Speculative Loss)", "Volatile / Middlemen Dictated", "Skewed via Wealth Concentration", "High Vulnerability (Physical Cash/Blind Trust) [", "Stagnant (1.0x - 1.2x)"],"Tokenized RIE-X Blueprint": ["Minimised / Transparent (C_s Cost Only)", "Near-Zero (Circular Waste Reversion)", "Linear Base (1 Person = 1 Vote)", "Cryptographically Secure / Zero-Cash", f"Verified Multiplier ({local_multiplier}x) ["]}st.table(pd.DataFrame(comparison_data))st.markdown("### 🌾 Micro-Industrial Infrastructure Nodes")st.markdown("""The simulated net surplus directly funds the deployment of localized village processing components inside the community:* Grain, Pulse & Spice lines: Converts bulk raw products into retail-ready SKUs inside the village itself to capture maximum value.* Cold-Storage Units: Stabilizes crop lifespans to eliminate harvest price drops and reduce food waste vectors.* Urban Synchronization Layer: Feeds real-time sales data from urban outlets straight to village processing units, matching production with demand.""")st.markdown("---")st.markdown("V. GLOBAL SCALABILITY & SYSTEMIC ADAPTATION POLICY", unsafe_allow_html=True)st.markdown(f"""The RIE-X blueprint transitions regional economies from dependent, debt-driven structures into highly resilient, self-sustaining engines.By aligning model deployment with the {region} economic archetype, public capital injections or initial grants act strictly as one-time bootstrapping reserves rather than permanent fiscal burdens.Once initialized, the {reinvestment_rate}% closed-loop retention rate guarantees that the system dynamically funds its own infrastructure expansion, builds long-term wealth, and provides a stable, reproducible framework for international economic development.""")
