import streamlit as st
import pandas as pd
import numpy as np

# ============================================================
# RIE-X DYNAMIC ECONOMIC MODEL
# Structural Counterfactual Simulation
# Monetary calibration: rupees internally; crore/lakh for display
# ============================================================

st.set_page_config(
    page_title="RIE-X Dynamic Economic Model",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Unit helpers
# -----------------------------
RUPEES_PER_LAKH = 100_000.0
RUPEES_PER_CRORE = 10_000_000.0


def to_lakh(x):
    return x / RUPEES_PER_LAKH


def to_crore(x):
    return x / RUPEES_PER_CRORE


# ============================================================
# PAGE HEADER
# ============================================================

st.title("RIE-X Dynamic Economic Model")
st.markdown(
    """
### Structural Counterfactual Model for Rural Economic Transformation

This model compares two economic trajectories:

**1. Traditional / Business-as-Usual Economy**  
**2. Rural Integrated Economy (RIE-X)**

The simulation explicitly models labour, productive capital, productivity,
value-chain leakage, reinvestment, depreciation, contributor income and
local economic circulation.

**Unit convention:** all financial calculations are performed internally in
**Indian rupees (₹)**. Charts and tables display aggregate monetary values in
**₹ crore** and income per worker in **₹ lakh per year**.
"""
)

st.info(
    """
All values are simulation parameters. The model does not claim that the
assumed coefficients are empirically verified. They may be replaced with
field estimates, published studies or pilot observations. The base case is
calibrated so that one 100-member cell produces approximately ₹8 crore of
Year-1 gross output.
"""
)

# ============================================================
# SIDEBAR PARAMETERS
# ============================================================

st.sidebar.title("Model Parameters")

# ------------------------------------------------------------
# 1. TIME
# ------------------------------------------------------------
st.sidebar.header("1. Simulation Horizon")
years = st.sidebar.slider("Years", min_value=5, max_value=30, value=5, step=1)

# ------------------------------------------------------------
# 2. LABOUR
# ------------------------------------------------------------
st.sidebar.header("2. Labour")
cells = st.sidebar.slider("Number of RIE-X Cells", 1, 2000, 1)
workers_per_cell = st.sidebar.slider("Workers per Cell", 10, 2000, 100)
initial_labour = float(cells * workers_per_cell)

labour_growth = st.sidebar.slider(
    "Annual Labour Growth gL (%)", -5.0, 10.0, 0.0, 0.1
) / 100.0

# ------------------------------------------------------------
# 3. CAPITAL
# ------------------------------------------------------------
st.sidebar.header("3. Capital")
initial_capital_per_worker = st.sidebar.number_input(
    "Initial Productive Capital per Worker (₹)",
    min_value=0.0,
    value=100000.0,
    step=10000.0,
)
initial_capital = initial_labour * initial_capital_per_worker

# Traditional capital formation is now adjustable rather than hard-coded.
traditional_savings_rate = st.sidebar.slider(
    "Traditional Savings / Reinvestment (%)", 0.0, 40.0, 5.0, 0.5
) / 100.0

depreciation = st.sidebar.slider(
    "Capital Depreciation δ (%)", 0.0, 25.0, 5.0, 0.5
) / 100.0

# ------------------------------------------------------------
# 4. PRODUCTION FUNCTION
# ------------------------------------------------------------
st.sidebar.header("4. Production Function")
capital_elasticity = st.sidebar.slider(
    "Capital Elasticity α", 0.10, 0.70, 0.35, 0.01
)
labour_elasticity = 1.0 - capital_elasticity

# Replace dimensionally ambiguous A0 input with an explicit rupee target.
target_turnover_per_cell_crore = st.sidebar.number_input(
    "Target Year-1 Gross Output per Cell (₹ crore)",
    min_value=0.10,
    value=8.00,
    step=0.25,
    format="%.2f",
)
target_year1_output = target_turnover_per_cell_crore * RUPEES_PER_CRORE * cells

# A0 is calibrated so Cobb-Douglas output equals the Year-1 monetary target.
production_base = (
    max(initial_capital, 1.0) ** capital_elasticity
    * max(initial_labour, 1.0) ** labour_elasticity
)
initial_tfp = target_year1_output / max(production_base, 1e-12)

st.sidebar.caption(f"Calibrated initial TFP A₀: {initial_tfp:,.4f}")

traditional_tfp_growth = st.sidebar.slider(
    "Traditional TFP Growth (%)", -2.0, 10.0, 1.0, 0.1
) / 100.0

riex_tfp_growth = st.sidebar.slider(
    "RIE-X TFP Growth (%)", -2.0, 15.0, 5.0, 0.1
) / 100.0

# ------------------------------------------------------------
# 5. TRADITIONAL VALUE LEAKAGE
# ------------------------------------------------------------
st.sidebar.header("5. Traditional Value Leakage")
middleman = st.sidebar.slider("Middleman Margin (%)", 0.0, 30.0, 10.0, 0.5) / 100.0
logistics = st.sidebar.slider("Logistics Inefficiency (%)", 0.0, 20.0, 6.0, 0.5) / 100.0
spoilage = st.sidebar.slider("Spoilage Loss (%)", 0.0, 20.0, 7.0, 0.5) / 100.0
finance_cost = st.sidebar.slider("Finance Cost (%)", 0.0, 20.0, 4.0, 0.5) / 100.0
distribution = st.sidebar.slider("Distribution Leakage (%)", 0.0, 20.0, 5.0, 0.5) / 100.0

traditional_leakage = middleman + logistics + spoilage + finance_cost + distribution
st.sidebar.caption(f"Total traditional leakage: {traditional_leakage * 100:.1f}%")

# ------------------------------------------------------------
# 6. RIE-X COST STRUCTURE
# ------------------------------------------------------------
st.sidebar.header("6. RIE-X Cost Structure")
riex_residual_leakage = st.sidebar.slider(
    "Residual External Leakage (%)", 0.0, 30.0, 8.0, 0.5
) / 100.0
administration_cost = st.sidebar.slider(
    "Administration Cost (%)", 0.0, 15.0, 3.0, 0.25
) / 100.0
reserve_rate = st.sidebar.slider(
    "Community Reserve (%)", 0.0, 20.0, 5.0, 0.5
) / 100.0
reinvestment_rate = st.sidebar.slider(
    "Surplus Reinvestment s (%)", 0.0, 60.0, 30.0, 1.0
) / 100.0

# ------------------------------------------------------------
# 7. LOCAL ECONOMIC MULTIPLIER
# ------------------------------------------------------------
st.sidebar.header("7. Local Circulation")
traditional_multiplier = st.sidebar.slider(
    "Traditional Local Multiplier", 1.0, 3.0, 1.3, 0.1
)
riex_multiplier = st.sidebar.slider(
    "RIE-X Local Multiplier", 1.0, 4.0, 2.1, 0.1
)

# ------------------------------------------------------------
# 8. ECONOMIC SHOCKS
# ------------------------------------------------------------
st.sidebar.header("8. Economic Shocks")
demand_shock_year = st.sidebar.slider("Demand Shock Year", 0, years, 0)
demand_shock = st.sidebar.slider("Demand Shock (%)", -50.0, 50.0, 0.0, 1.0) / 100.0

# ============================================================
# MATHEMATICAL MODEL
# ============================================================
# Y_t = A_t K_t^α L_t^(1-α)
# V_T,t = Y_T,t (1 - λ_T)
# Π_R,t = Y_R,t (1 - λ_R - c_a)
# Q_t = r Π_R,t
# I_t = s (Π_R,t - Q_t)
# D_t = (1-s)(Π_R,t - Q_t)
# K_(t+1) = (1-δ)K_t + I_t
# L_(t+1) = L_t(1+g_L)
# A_(t+1) = A_t(1+g_A)
# ============================================================

periods = np.arange(1, years + 1)
traditional_rows = []
riex_rows = []

K_T = initial_capital
K_R = initial_capital
L_T = initial_labour
L_R = initial_labour
A_T = initial_tfp
A_R = initial_tfp

cumulative_recovered_value = 0.0
cumulative_reinvestment = 0.0

for t in periods:
    # Gross output in rupees.
    Y_T = A_T * (max(K_T, 1.0) ** capital_elasticity) * (max(L_T, 1.0) ** labour_elasticity)
    Y_R = A_R * (max(K_R, 1.0) ** capital_elasticity) * (max(L_R, 1.0) ** labour_elasticity)

    shock_factor = 1.0
    if demand_shock_year > 0 and t >= demand_shock_year:
        shock_factor += demand_shock
    Y_T *= shock_factor
    Y_R *= shock_factor

    # Traditional economy
    traditional_net_value = Y_T * (1.0 - traditional_leakage)
    traditional_loss = Y_T * traditional_leakage
    traditional_income_per_worker = traditional_net_value / max(L_T, 1.0)
    traditional_local_activity = traditional_net_value * traditional_multiplier
    traditional_investment = traditional_net_value * traditional_savings_rate

    # RIE-X economy
    riex_operating_surplus = Y_R * (1.0 - riex_residual_leakage - administration_cost)
    community_reserve = riex_operating_surplus * reserve_rate
    allocatable_surplus = riex_operating_surplus - community_reserve
    reinvestment = allocatable_surplus * reinvestment_rate
    contributor_income = allocatable_surplus - reinvestment
    riex_income_per_worker = contributor_income / max(L_R, 1.0)
    riex_local_activity = contributor_income * riex_multiplier

    comparable_traditional_loss = Y_R * traditional_leakage
    riex_system_cost = Y_R * (riex_residual_leakage + administration_cost)
    recovered_value = max(0.0, comparable_traditional_loss - riex_system_cost)

    cumulative_recovered_value += recovered_value
    cumulative_reinvestment += reinvestment

    traditional_rows.append({
        "Year": t,
        "Capital Stock": K_T,
        "Labour": L_T,
        "TFP": A_T,
        "Output": Y_T,
        "Net Producer Value": traditional_net_value,
        "Value Leakage": traditional_loss,
        "Income per Worker": traditional_income_per_worker,
        "Investment": traditional_investment,
        "Local Economic Activity": traditional_local_activity,
    })

    riex_rows.append({
        "Year": t,
        "Capital Stock": K_R,
        "Labour": L_R,
        "TFP": A_R,
        "Output": Y_R,
        "Operating Surplus": riex_operating_surplus,
        "Community Reserve": community_reserve,
        "Reinvestment": reinvestment,
        "Contributor Income": contributor_income,
        "Income per Worker": riex_income_per_worker,
        "Recovered Structural Value": recovered_value,
        "Cumulative Recovered Value": cumulative_recovered_value,
        "Cumulative Reinvestment": cumulative_reinvestment,
        "Local Economic Activity": riex_local_activity,
    })

    # Update state for the next year only after current-year values are stored.
    K_T = (1.0 - depreciation) * K_T + traditional_investment
    K_R = (1.0 - depreciation) * K_R + reinvestment
    L_T = L_T * (1.0 + labour_growth)
    L_R = L_R * (1.0 + labour_growth)
    A_T = A_T * (1.0 + traditional_tfp_growth)
    A_R = A_R * (1.0 + riex_tfp_growth)

# ============================================================
# DATAFRAMES
# ============================================================
traditional_df = pd.DataFrame(traditional_rows)
riex_df = pd.DataFrame(riex_rows)

comparison_df = pd.DataFrame({
    "Year": periods,
    "Traditional Output": traditional_df["Output"],
    "RIE-X Output": riex_df["Output"],
    "Traditional Capital": traditional_df["Capital Stock"],
    "RIE-X Capital": riex_df["Capital Stock"],
    "Traditional Income per Worker": traditional_df["Income per Worker"],
    "RIE-X Income per Worker": riex_df["Income per Worker"],
})

final_T = traditional_df.iloc[-1]
final_R = riex_df.iloc[-1]

output_difference = final_R["Output"] - final_T["Output"]
output_gain_pct = output_difference / max(final_T["Output"], 1.0) * 100.0
income_difference = final_R["Income per Worker"] - final_T["Income per Worker"]
income_gain_pct = income_difference / max(final_T["Income per Worker"], 1.0) * 100.0
capital_difference = final_R["Capital Stock"] - final_T["Capital Stock"]

# ============================================================
# DASHBOARD
# ============================================================
st.markdown("---")
st.header("Model Results")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Initial Labour Force", f"{initial_labour:,.0f}")
c2.metric(f"Output Difference — Year {years}", f"{output_gain_pct:+.1f}%")
c3.metric("Income / Worker Difference", f"{income_gain_pct:+.1f}%")
c4.metric("Additional RIE-X Capital", f"₹{to_crore(capital_difference):,.2f} cr")

# Base calibration check
b1, b2, b3 = st.columns(3)
b1.metric("Year-1 Gross Output / Cell", f"₹{to_crore(riex_df.iloc[0]['Output']) / cells:,.2f} cr")
b2.metric("Initial Capital Stock", f"₹{to_crore(initial_capital):,.2f} cr")
b3.metric("Initial Capital / Worker", f"₹{to_lakh(initial_capital_per_worker):,.2f} lakh")

# ============================================================
# 1. OUTPUT TRAJECTORY — ₹ CRORE
# ============================================================
st.subheader("1. Output Trajectory (₹ crore)")
output_chart = pd.DataFrame({
    "Year": periods,
    "Traditional Output (₹ cr)": traditional_df["Output"].apply(to_crore),
    "RIE-X Output (₹ cr)": riex_df["Output"].apply(to_crore),
}).set_index("Year")
st.line_chart(output_chart)

# ============================================================
# 2. CAPITAL ACCUMULATION — ₹ CRORE
# ============================================================
st.subheader("2. Productive Capital Accumulation (₹ crore)")
capital_chart = pd.DataFrame({
    "Year": periods,
    "Traditional Capital (₹ cr)": traditional_df["Capital Stock"].apply(to_crore),
    "RIE-X Capital (₹ cr)": riex_df["Capital Stock"].apply(to_crore),
}).set_index("Year")
st.line_chart(capital_chart)

# ============================================================
# 3. INCOME PER WORKER — ₹ LAKH / YEAR
# ============================================================
st.subheader("3. Income per Worker (₹ lakh/year)")
income_chart = pd.DataFrame({
    "Year": periods,
    "Traditional Income / Worker (₹ lakh)": traditional_df["Income per Worker"].apply(to_lakh),
    "RIE-X Income / Worker (₹ lakh)": riex_df["Income per Worker"].apply(to_lakh),
}).set_index("Year")
st.line_chart(income_chart)

# ============================================================
# 4. VALUE-CHAIN RECOVERY — ₹ CRORE
# ============================================================
st.subheader("4. Value-Chain Recovery (₹ crore)")
recovery_chart = pd.DataFrame({
    "Year": periods,
    "Cumulative Recovered Value (₹ cr)": riex_df["Cumulative Recovered Value"].apply(to_crore),
}).set_index("Year")
st.line_chart(recovery_chart)
st.metric(
    "Cumulative Structural Value Recovered",
    f"₹{to_crore(riex_df.iloc[-1]['Cumulative Recovered Value']):,.2f} cr",
)

# ============================================================
# 5. REINVESTMENT — ₹ CRORE
# ============================================================
st.subheader("5. Closed-Loop Reinvestment (₹ crore)")
reinvestment_chart = pd.DataFrame({
    "Year": periods,
    "Reinvestment (₹ cr)": riex_df["Reinvestment"].apply(to_crore),
    "Cumulative Reinvestment (₹ cr)": riex_df["Cumulative Reinvestment"].apply(to_crore),
}).set_index("Year")
st.line_chart(reinvestment_chart)

# ============================================================
# 6. LOCAL ECONOMIC ACTIVITY — ₹ CRORE
# ============================================================
st.subheader("6. Local Economic Circulation (₹ crore)")
local_df = pd.DataFrame({
    "Year": periods,
    "Traditional Local Activity (₹ cr)": traditional_df["Local Economic Activity"].apply(to_crore),
    "RIE-X Local Activity (₹ cr)": riex_df["Local Economic Activity"].apply(to_crore),
}).set_index("Year")
st.line_chart(local_df)

# ============================================================
# FINAL COMPARISON TABLE
# ============================================================
st.markdown("---")
st.header(f"Year {years} Comparative Outcome")

# Keep unlike quantities in their proper units instead of mixing them in one
# unitless numeric table.
final_comparison = pd.DataFrame({
    "Indicator": [
        "Output (₹ crore)",
        "Productive Capital Stock (₹ crore)",
        "Labour Force (persons)",
        "Total Factor Productivity (index)",
        "Income per Worker (₹ lakh/year)",
        "Local Economic Activity (₹ crore)",
    ],
    "Traditional": [
        to_crore(final_T["Output"]),
        to_crore(final_T["Capital Stock"]),
        final_T["Labour"],
        final_T["TFP"],
        to_lakh(final_T["Income per Worker"]),
        to_crore(final_T["Local Economic Activity"]),
    ],
    "RIE-X": [
        to_crore(final_R["Output"]),
        to_crore(final_R["Capital Stock"]),
        final_R["Labour"],
        final_R["TFP"],
        to_lakh(final_R["Income per Worker"]),
        to_crore(final_R["Local Economic Activity"]),
    ],
})

final_comparison["Difference"] = final_comparison["RIE-X"] - final_comparison["Traditional"]
final_comparison["Difference %"] = (
    final_comparison["Difference"]
    / final_comparison["Traditional"].replace(0, np.nan)
    * 100.0
)

st.dataframe(
    final_comparison.style.format({
        "Traditional": "{:,.4f}",
        "RIE-X": "{:,.4f}",
        "Difference": "{:,.4f}",
        "Difference %": "{:,.2f}",
    }),
    use_container_width=True,
    hide_index=True,
)

# ============================================================
# FIVE-YEAR RIE-X TURNOVER TABLE
# ============================================================
st.subheader("RIE-X Annual and Cumulative Gross Output")
riex_projection = pd.DataFrame({
    "Year": periods,
    "Annual Gross Output (₹ crore)": riex_df["Output"].apply(to_crore),
})
riex_projection["Cumulative Gross Output (₹ crore)"] = riex_projection[
    "Annual Gross Output (₹ crore)"
].cumsum()
st.dataframe(
    riex_projection.style.format({
        "Annual Gross Output (₹ crore)": "{:,.2f}",
        "Cumulative Gross Output (₹ crore)": "{:,.2f}",
    }),
    use_container_width=True,
    hide_index=True,
)

# ============================================================
# ECONOMIC EQUATIONS
# ============================================================
st.markdown("---")
st.header("Mathematical Specification")
st.latex(r"Y_t = A_t K_t^{\alpha} L_t^{1-\alpha}")
st.markdown("Gross production is denominated in rupees after monetary calibration of $A_0$.")
st.latex(r"A_0 = \frac{Y_1^{target}}{K_1^{\alpha}L_1^{1-\alpha}}")
st.markdown("The initial TFP coefficient is calibrated to the selected Year-1 gross-output target.")
st.latex(r"V^{T}_t = Y^{T}_t(1-\lambda_T)")
st.markdown("Traditional net producer value equals gross output minus structural leakage.")
st.latex(r"\Pi^{R}_t=Y^{R}_t(1-\lambda_R-c_a)")
st.markdown("RIE-X operating surplus equals output after residual leakage and administration cost.")
st.latex(r"Q_t = r\Pi^{R}_t")
st.markdown("A proportion $r$ is allocated to the community reserve.")
st.latex(r"I_t=s(\Pi^{R}_t-Q_t)")
st.markdown("A proportion $s$ of allocatable surplus becomes productive reinvestment.")
st.latex(r"K_{t+1}=(1-\delta)K_t+I_t")
st.markdown("Capital evolves through reinvestment net of depreciation; both terms are in rupees.")
st.latex(r"L_{t+1}=L_t(1+g_L)")
st.latex(r"A_{t+1}=A_t(1+g_A)")

# ============================================================
# LEAKAGE DECOMPOSITION
# ============================================================
st.header("Value-Chain Leakage Decomposition")
leakage_table = pd.DataFrame({
    "Component": [
        "Middleman / Aggregator",
        "Logistics",
        "Spoilage",
        "Finance",
        "Distribution",
        "Total",
    ],
    "Percent": [
        middleman * 100,
        logistics * 100,
        spoilage * 100,
        finance_cost * 100,
        distribution * 100,
        traditional_leakage * 100,
    ],
})
st.dataframe(leakage_table, use_container_width=True, hide_index=True)

# ============================================================
# MODEL INTERPRETATION
# ============================================================
st.markdown("---")
st.header("Economic Interpretation")
st.markdown(
    """
The model tests whether structural value-chain integration can create a
different medium-run trajectory from the traditional rural economy.

**Lower Value Leakage**  
↓  
**Higher Captured Surplus**  
↓  
**Contributor Income + Community Reserves**  
↓  
**Productive Reinvestment**  
↓  
**Larger Capital Stock**  
↓  
**Higher Future Productive Capacity**  
↓  
**Higher Local Value Creation**

The traditional and RIE-X counterfactuals therefore diverge through
differences in leakage, capital retention and assumed productivity growth.
"""
)

# ============================================================
# DOWNLOAD
# ============================================================
st.markdown("---")
st.header("Export Model Results")
export_df = pd.DataFrame({
    "Year": periods,
    "Traditional Output Rupees": traditional_df["Output"],
    "RIE-X Output Rupees": riex_df["Output"],
    "Traditional Output Crore": traditional_df["Output"].apply(to_crore),
    "RIE-X Output Crore": riex_df["Output"].apply(to_crore),
    "Traditional Capital Rupees": traditional_df["Capital Stock"],
    "RIE-X Capital Rupees": riex_df["Capital Stock"],
    "Traditional Income Per Worker Rupees": traditional_df["Income per Worker"],
    "RIE-X Income Per Worker Rupees": riex_df["Income per Worker"],
    "Traditional Income Per Worker Lakh": traditional_df["Income per Worker"].apply(to_lakh),
    "RIE-X Income Per Worker Lakh": riex_df["Income per Worker"].apply(to_lakh),
    "RIE-X Reinvestment Rupees": riex_df["Reinvestment"],
    "RIE-X Reinvestment Crore": riex_df["Reinvestment"].apply(to_crore),
    "RIE-X Recovered Value Rupees": riex_df["Recovered Structural Value"],
    "RIE-X Cumulative Recovered Value Rupees": riex_df["Cumulative Recovered Value"],
})

csv = export_df.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download Simulation CSV",
    csv,
    "riex_dynamic_economic_model.csv",
    "text/csv",
)

# ============================================================
# MODEL NOTES
# ============================================================
with st.expander("Model Assumptions and Limitations"):
    st.markdown(
        """
1. Financial variables are calculated internally in rupees; aggregate charts
   use ₹ crore and income-per-worker charts use ₹ lakh/year.
2. Year 1 is calibrated to the selected gross-output target. The default is
   ₹8 crore per cell for a 100-worker cell.
3. Cobb-Douglas is an analytical structure, not evidence that RIE-X must obey
   this exact production function.
4. Leakage coefficients are user-defined scenario assumptions.
5. Local multipliers are shown separately from productive output to avoid
   double-counting induced activity.
6. Productivity growth rates are assumptions and should ultimately be
   calibrated with pilot or longitudinal data.
7. Depreciation is explicitly included.
8. The same labour-growth rate is currently applied to both counterfactuals.
9. Prices, inflation, interest rates and exchange rates are not explicitly modelled.
10. Risk and uncertainty are deterministic except for the user-defined demand shock.
11. Future extensions can add Monte Carlo simulation, confidence intervals and sensitivity analysis.
"""
    )
