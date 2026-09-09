import streamlit as st
import pandas as pd
import numpy as np

# 1. Page Configuration & Semantic Layout Design
st.set_page_config(
    page_title="RIE-X & The Trust Economy | Comprehensive Master Blueprint",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Institutional CSS styling for clean, academic scannability
st.markdown("""
<style>
    .reportview-container { background: #f8fafc; }
    .main-header { color: #1e3a8a; font-weight: 800; font-size: 2.6rem; margin-bottom: 2px; }
    .academic-cite { color: #475569; font-style: italic; font-size: 0.95rem; margin-bottom: 25px; line-height: 1.5; }
    .section-header { color: #0f172a; font-weight: 700; font-size: 1.7rem; border-bottom: 3px solid #0d9488; padding-bottom: 8px; margin-top: 35px; margin-bottom: 15px; }
    .highlight-box { background-color: #f0fdf4; padding: 22px; border-left: 6px solid #16a34a; border-radius: 6px; margin: 20px 0; line-height: 1.6; font-size: 1.05rem; }
    .matrix-box { background-color: #f8fafc; padding: 22px; border: 1px solid #cbd5e1; border-radius: 6px; margin: 20px 0; line-height: 1.6; }
    p, li { font-size: 1.05rem; line-height: 1.7; color: #334155; }
</style>
""", unsafe_allow_html=True)

# 2. Sidebar Administration Panel
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

# 3. Macroeconomic Simulation Mathematics
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

# Aggregated Output Equations
gross_traditional = total_participants * v_traditional_base
net_riex_surplus = total_participants * (v_riex_base - c_admin_base)
system_surplus_created = net_riex_surplus - gross_traditional
per_capita_income_boost = ((v_riex_base - c_admin_base) - v_traditional_base) / v_traditional_base * 100
annual_reinvestment_pool = net_riex_surplus * (reinvestment_rate / 100.0)

# 4. Interface Rendering Pipeline
st.markdown("<h1 class='main-header'>THE RURAL INTEGRATED TOKENIZED ECONOMY (RIE-X)</h1>", unsafe_allow_html=True)
st.markdown("<div class='academic-cite'>A Comprehensive Institutional Strategy and Deployment Blueprint. Synthesizing the Principles of Distributed Trust Networks, Tokenized Labour-Capital Paradigms, and Closed-Loop Environmental Resilience Ecosystems. Cross-Referenced JEL Classification Codes: O13, Q56, D63, H41, P46.</div>", unsafe_allow_html=True)
st.markdown("---")

# Split Framework (50% Comprehensive Text Document / 50% Simulation Graphics)
doc_view, simulation_view = st.columns(2)

with doc_view:
    st.markdown("<div class='section-header'>I. THE EXTRACTION PARADOX & MACROECONOMIC DISTANCE</div>", unsafe_allow_html=True)
    text_sec1 = (
        "Contemporary global regional value chains suffer from a chronic, structural layout of value extraction. "
        "Primary producers create foundational physical products but capture a minor fraction of final value. "
        "Meanwhile, downstream intermediaries, speculative traders, corporate distributors, and centralized platform monopolies "
        "extract outsized margins. This spatial-economic distance generates several severe imbalances:\n\n"
        "* **The Producer Compression Vector:** Local villages and primary producers face irregular employment, seasonal income volatility, and severely undervalued labor returns. Because they lack direct access to distribution channels, processing equipment, and pricing information, they are routinely forced to sell raw commodities at near-loss baseline margins.\n"
        "* **The Consumer Premium Vector:** Urban consumers pay high final market premiums for basic agricultural and processed goods. This cost elevation is driven entirely by layered intermediary markups, inefficient storage hand-offs, and speculative logistics networks, rather than genuine improvements in product quality.\n"
        "* **The Structural Capital Flight:** Regional savings and local capital are continuously pulled out of rural environments and redirected to centralized financial hubs. This starves regional networks of the development reserves required to build processing factories, install cold-storage networks, or fund localized entrepreneurship."
    )
    st.markdown(text_sec1)
    
    matrix_sec1 = (
        "<strong>The Core Distance Theorem:</strong> In traditional networks, Final Price satisfies: <em>P_c = V_v + &Sigma; I_k</em>, "
        "where <em>&Sigma; I_k</em> represents the sum of costs and margins extracted by k layers of non-value-adding traditional intermediaries. "
        "RIE-X replaces this with an auditable structural administration cost matrix <em>C_s</em>, where <em>C_s &ll; &Sigma; I_k</em>. "
        "This bypasses speculative extraction and maps the recovered surplus directly to primary contributors as shared participant value."
    )
    st.markdown(f"<div class='matrix-box'>{matrix_sec1}</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-header'>II. CONCEPTUAL FOUNDATIONS & THE ASSETIZATION OF LABOR</div>", unsafe_allow_html=True)
    text_sec2 = (
        "The Rural Integrated Economy (RIE-X) blueprint upgrades conventional cooperative networks by fundamentally rewriting the treatment of work. "
        "Instead of treating labor as an operational expense cost to be minimized, the architecture treats labor as a **long-term capital asset**.\n\n"
        "This structural paradigm is operationalized through a non-speculative digital record layer known as **Rural Value Tokens (RVTs)**. "
        "RVTs are non-transferable, cryptographically checked accounting markers that represent four core institutional attributes:\n\n"
        "1. **Sovereign Capital Stake:** Proportional to a worker's lifetime labor contribution, raw material provisioning, or local processing deployment.\n"
        "2. **Productivity Multiplier:** Adjusted dynamically by an automated quality coefficient based on output accuracy, grading standards, and processing consistency.\n"
        "3. **Democratic Governance Rights:** Secure linear baseline distribution ensuring that community governance weight is fully decoupled from wealth concentration.\n"
        "4. **Surplus Entitlements:** Permanent access to recurring dividends and capital distribution generated from value-added processing and urban retail operations."
    )
    st.markdown(text_sec2)
    
    highlight_sec2 = (
        "<strong>The Sweat Equity Invariant:</strong> 1 Labour-Hour = 1 Base RVT Unit. Because RVTs are explicitly non-transferable, "
        "they cannot be accumulated, bought out, or co-opted by wealthy external investors or centralized financial interests. "
        "This ensures that power, control, and capital accumulation remain permanently anchored inside the local community that drives production."
    )
    st.markdown(f"<div class='highlight-box'>{highlight_sec2}</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-header'>III. VILLAGE-OWNED MICRO-INDUSTRIAL INFRASTRUCTURE</div>", unsafe_allow_html=True)
    text_sec3 = (
        "RIE-X permanently terminates the standard dependency on external corporate distribution by deploying processing apparatus loops straight into rural communities. "
        "These micro-industrial clusters allow raw products to undergo primary value addition locally, increasing income buffers and generating local technical fields.\n\n"
        "The infrastructure footprint consists of three primary active components:\n"
        "* **Value-Addition Processing Lines:** In-village setups for sorting, cleaning, grading, packaging, and transforming raw inputs into standardized higher-value goods (SKUs).\n"
        "* **Decentralized Cold Chain Preservation:** Modular cold-storage facilities that preserve crop lifespans, eliminating desperation-driven harvest selling during market drops and stabilizing year-round supply channels.\n"
