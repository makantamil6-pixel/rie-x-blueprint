import streamlit as st
import pandas as pd
import numpy as np

# ============================================================
# RIE-X DYNAMIC ECONOMIC MODEL
# Structural Counterfactual Simulation
# ============================================================

st.set_page_config(
    page_title="RIE-X Dynamic Economic Model",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

The simulation explicitly models labour, capital accumulation,
productivity, value-chain leakage, reinvestment, depreciation,
surplus distribution and local economic circulation.
"""
)

st.info(
    """
All values are simulation parameters. The model does not claim that
the assumed coefficients are empirically verified. They may be replaced
with estimates from field data, published studies or pilot observations.
"""
)

# ============================================================
# SIDEBAR PARAMETERS
# ============================================================

st.sidebar.title("Model Parameters")

# ------------------------------------------------------------
# TIME
# ------------------------------------------------------------

st.sidebar.header("1. Simulation Horizon")

years = st.sidebar.slider(
    "Years",
    min_value=5,
    max_value=30,
    value=25,
    step=1
)

# ------------------------------------------------------------
# POPULATION / LABOUR
# ------------------------------------------------------------

st.sidebar.header("2. Labour")

cells = st.sidebar.slider(
    "Number of RIE-X Cells",
    1, 2000, 150
)

workers_per_cell = st.sidebar.slider(
    "Workers per Cell",
    10, 2000, 250
)

initial_labour = cells * workers_per_cell

labour_growth = st.sidebar.slider(
    "Annual Labour Growth gL (%)",
    -5.0, 10.0, 1.0, 0.1
) / 100

# ------------------------------------------------------------
# CAPITAL
# ------------------------------------------------------------

st.sidebar.header("3. Capital")

initial_capital_per_worker = st.sidebar.number_input(
    "Initial Productive Capital per Worker",
    min_value=0.0,
    value=100000.0,
    step=10000.0
)

initial_capital = (
    initial_labour * initial_capital_per_worker
)

depreciation = st.sidebar.slider(
    "Capital Depreciation δ (%)",
    0.0, 25.0, 5.0, 0.5
) / 100

# ------------------------------------------------------------
# PRODUCTION FUNCTION
# ------------------------------------------------------------

st.sidebar.header("4. Production Function")

capital_elasticity = st.sidebar.slider(
    "Capital Elasticity α",
    0.10, 0.70, 0.35, 0.01
)

labour_elasticity = 1 - capital_elasticity

initial_tfp = st.sidebar.number_input(
    "Initial Total Factor Productivity A₀",
    min_value=0.0001,
    value=1.0,
    step=0.05,
    format="%.4f"
)

traditional_tfp_growth = st.sidebar.slider(
    "Traditional TFP Growth (%)",
    -2.0, 10.0, 1.0, 0.1
) / 100

riex_tfp_growth = st.sidebar.slider(
    "RIE-X TFP Growth (%)",
    -2.0, 15.0, 3.0, 0.1
) / 100

# ------------------------------------------------------------
# VALUE-CHAIN LEAKAGE
# ------------------------------------------------------------

st.sidebar.header("5. Traditional Value Leakage")

middleman = st.sidebar.slider(
    "Middleman Margin (%)",
    0.0, 30.0, 10.0, 0.5
) / 100

logistics = st.sidebar.slider(
    "Logistics Inefficiency (%)",
    0.0, 20.0, 6.0, 0.5
) / 100

spoilage = st.sidebar.slider(
    "Spoilage Loss (%)",
    0.0, 20.0, 7.0, 0.5
) / 100

finance_cost = st.sidebar.slider(
    "Finance Cost (%)",
    0.0, 20.0, 4.0, 0.5
) / 100

distribution = st.sidebar.slider(
    "Distribution Leakage (%)",
    0.0, 20.0, 5.0, 0.5
) / 100

traditional_leakage = (
    middleman
    + logistics
    + spoilage
    + finance_cost
    + distribution
)

st.sidebar.caption(
    f"Total traditional leakage: "
    f"{traditional_leakage * 100:.1f}%"
)

# ------------------------------------------------------------
# RIE-X COST STRUCTURE
# ------------------------------------------------------------

st.sidebar.header("6. RIE-X Cost Structure")

riex_residual_leakage = st.sidebar.slider(
    "Residual External Leakage (%)",
    0.0, 30.0, 8.0, 0.5
) / 100

administration_cost = st.sidebar.slider(
    "Administration Cost (%)",
    0.0, 15.0, 3.0, 0.25
) / 100

reserve_rate = st.sidebar.slider(
    "Community Reserve (%)",
    0.0, 20.0, 5.0, 0.5
) / 100

reinvestment_rate = st.sidebar.slider(
    "Surplus Reinvestment s (%)",
    0.0, 60.0, 30.0, 1.0
) / 100

# ------------------------------------------------------------
# LOCAL ECONOMIC MULTIPLIER
# ------------------------------------------------------------

st.sidebar.header("7. Local Circulation")

traditional_multiplier = st.sidebar.slider(
    "Traditional Local Multiplier",
    1.0, 3.0, 1.3, 0.1
)

riex_multiplier = st.sidebar.slider(
    "RIE-X Local Multiplier",
    1.0, 4.0, 2.1, 0.1
)

# ------------------------------------------------------------
# SHOCKS
# ------------------------------------------------------------

st.sidebar.header("8. Economic Shocks")

demand_shock_year = st.sidebar.slider(
    "Demand Shock Year",
    0, years, 0
)

demand_shock = st.sidebar.slider(
    "Demand Shock (%)",
    -50.0, 50.0, 0.0, 1.0
) / 100

# ============================================================
# MATHEMATICAL MODEL
# ============================================================

# Cobb-Douglas:
#
# Y_t = A_t K_t^α L_t^(1-α)
#
# Traditional disposable value:
#
# V_T,t = Y_T,t (1 - λ_T)
#
# RIE-X operating surplus:
#
# Π_R,t = Y_R,t (1 - λ_R - c_a)
#
# Community reserve:
#
# Q_t = r Π_R,t
#
# Reinvestment:
#
# I_t = s (Π_R,t - Q_t)
#
# Contributor income:
#
# D_t = (1-s)(Π_R,t - Q_t)
#
# Capital accumulation:
#
# K_(t+1) = (1-δ)K_t + I_t
#
# Labour:
#
# L_(t+1) = L_t(1+g_L)
#
# Productivity:
#
# A_(t+1) = A_t(1+g_A)

# ============================================================
# INITIALISE ARRAYS
# ============================================================

periods = np.arange(0, years + 1)

traditional_rows = []
riex_rows = []

K_T = initial_capital
K_R = initial_capital

L_T = float(initial_labour)
L_R = float(initial_labour)

A_T = initial_tfp
A_R = initial_tfp

cumulative_recovered_value = 0.0
cumulative_reinvestment = 0.0

# ============================================================
# SIMULATION LOOP
# ============================================================

for t in periods:

    # --------------------------------------------------------
    # OUTPUT
    # --------------------------------------------------------

    Y_T = (
        A_T
        * (max(K_T, 1) ** capital_elasticity)
        * (max(L_T, 1) ** labour_elasticity)
    )

    Y_R = (
        A_R
        * (max(K_R, 1) ** capital_elasticity)
        * (max(L_R, 1) ** labour_elasticity)
    )

    # Demand shock applies in selected year onward
    shock_factor = 1.0

    if demand_shock_year > 0 and t >= demand_shock_year:
        shock_factor += demand_shock

    Y_T *= shock_factor
    Y_R *= shock_factor

    # --------------------------------------------------------
    # TRADITIONAL ECONOMY
    # --------------------------------------------------------

    traditional_net_value = (
        Y_T * (1 - traditional_leakage)
    )

    traditional_loss = (
        Y_T * traditional_leakage
    )

    traditional_income_per_worker = (
        traditional_net_value / max(L_T, 1)
    )

    traditional_local_activity = (
        traditional_net_value
        * traditional_multiplier
    )

    # Assume traditional capital formation is limited
    traditional_savings_rate = 0.05

    traditional_investment = (
        traditional_net_value
        * traditional_savings_rate
    )

    # --------------------------------------------------------
    # RIE-X ECONOMY
    # --------------------------------------------------------

    riex_operating_surplus = (
        Y_R
        * (
            1
            - riex_residual_leakage
            - administration_cost
        )
    )

    community_reserve = (
        riex_operating_surplus
        * reserve_rate
    )

    allocatable_surplus = (
        riex_operating_surplus
        - community_reserve
    )

    reinvestment = (
        allocatable_surplus
        * reinvestment_rate
    )

    contributor_income = (
        allocatable_surplus
        - reinvestment
    )

    riex_income_per_worker = (
        contributor_income / max(L_R, 1)
    )

    riex_local_activity = (
        contributor_income
        * riex_multiplier
    )

    # --------------------------------------------------------
    # STRUCTURAL VALUE RECOVERY
    # --------------------------------------------------------

    comparable_traditional_loss = (
        Y_R * traditional_leakage
    )

    riex_system_cost = (
        Y_R
        * (
            riex_residual_leakage
            + administration_cost
        )
    )

    recovered_value = max(
        0,
        comparable_traditional_loss
        - riex_system_cost
    )

    cumulative_recovered_value += recovered_value
    cumulative_reinvestment += reinvestment

    # --------------------------------------------------------
    # STORE RESULTS
    # --------------------------------------------------------

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
        "Local Economic Activity": traditional_local_activity
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
        "Local Economic Activity": riex_local_activity
    })

    # --------------------------------------------------------
    # DYNAMIC UPDATE
    # --------------------------------------------------------

    K_T = (
        (1 - depreciation) * K_T
        + traditional_investment
    )

    K_R = (
        (1 - depreciation) * K_R
        + reinvestment
    )

    L_T = L_T * (1 + labour_growth)
    L_R = L_R * (1 + labour_growth)

    A_T = A_T * (1 + traditional_tfp_growth)
    A_R = A_R * (1 + riex_tfp_growth)

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
    "Traditional Income per Worker":
        traditional_df["Income per Worker"],
    "RIE-X Income per Worker":
        riex_df["Income per Worker"]
})

# ============================================================
# SUMMARY METRICS
# ============================================================

final_T = traditional_df.iloc[-1]
final_R = riex_df.iloc[-1]

output_difference = (
    final_R["Output"]
    - final_T["Output"]
)

output_gain_pct = (
    output_difference
    / max(final_T["Output"], 1)
    * 100
)

income_difference = (
    final_R["Income per Worker"]
    - final_T["Income per Worker"]
)

income_gain_pct = (
    income_difference
    / max(final_T["Income per Worker"], 1)
    * 100
)

capital_difference = (
    final_R["Capital Stock"]
    - final_T["Capital Stock"]
)

# ============================================================
# DASHBOARD
# ============================================================

st.markdown("---")
st.header("Model Results")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Initial Labour Force",
    f"{initial_labour:,.0f}"
)

c2.metric(
    f"Output Difference — Year {years}",
    f"{output_gain_pct:+.1f}%"
)

c3.metric(
    f"Income / Worker Difference",
    f"{income_gain_pct:+.1f}%"
)

c4.metric(
    "Additional RIE-X Capital",
    f"{capital_difference:,.2f}"
)

# ============================================================
# OUTPUT TRAJECTORY
# ============================================================

st.subheader("1. Output Trajectory")

output_chart = comparison_df[
    [
        "Year",
        "Traditional Output",
        "RIE-X Output"
    ]
].set_index("Year")

st.line_chart(output_chart)

# ============================================================
# CAPITAL ACCUMULATION
# ============================================================

st.subheader("2. Productive Capital Accumulation")

capital_chart = comparison_df[
    [
        "Year",
        "Traditional Capital",
        "RIE-X Capital"
    ]
].set_index("Year")

st.line_chart(capital_chart)

# ============================================================
# INCOME PER WORKER
# ============================================================

st.subheader("3. Income per Worker")

income_chart = comparison_df[
    [
        "Year",
        "Traditional Income per Worker",
        "RIE-X Income per Worker"
    ]
].set_index("Year")

st.line_chart(income_chart)

# ============================================================
# STRUCTURAL VALUE RECOVERY
# ============================================================

st.subheader("4. Value-Chain Recovery")

recovery_chart = riex_df[
    [
        "Year",
        "Cumulative Recovered Value"
    ]
].set_index("Year")

st.line_chart(recovery_chart)

st.metric(
    "Cumulative Structural Value Recovered",
    f"{riex_df.iloc[-1]['Cumulative Recovered Value']:,.2f}"
)

# ============================================================
# REINVESTMENT
# ============================================================

st.subheader("5. Closed-Loop Reinvestment")

reinvestment_chart = riex_df[
    [
        "Year",
        "Reinvestment",
        "Cumulative Reinvestment"
    ]
].set_index("Year")

st.line_chart(reinvestment_chart)

# ============================================================
# LOCAL ECONOMIC ACTIVITY
# ============================================================

st.subheader("6. Local Economic Circulation")

local_df = pd.DataFrame({
    "Year": periods,
    "Traditional Local Activity":
        traditional_df["Local Economic Activity"],
    "RIE-X Local Activity":
        riex_df["Local Economic Activity"]
}).set_index("Year")

st.line_chart(local_df)

# ============================================================
# FINAL COMPARISON TABLE
# ============================================================

st.markdown("---")
st.header(f"Year {years} Comparative Outcome")

final_comparison = pd.DataFrame({
    "Indicator": [
        "Output",
        "Productive Capital Stock",
        "Labour Force",
        "Total Factor Productivity",
        "Income per Worker",
        "Local Economic Activity"
    ],
    "Traditional": [
        final_T["Output"],
        final_T["Capital Stock"],
        final_T["Labour"],
        final_T["TFP"],
        final_T["Income per Worker"],
        final_T["Local Economic Activity"]
    ],
    "RIE-X": [
        final_R["Output"],
        final_R["Capital Stock"],
        final_R["Labour"],
        final_R["TFP"],
        final_R["Income per Worker"],
        final_R["Local Economic Activity"]
    ]
})

final_comparison["Difference"] = (
    final_comparison["RIE-X"]
    - final_comparison["Traditional"]
)

final_comparison["Difference %"] = (
    final_comparison["Difference"]
    / final_comparison["Traditional"]
        .replace(0, np.nan)
    * 100
)

st.dataframe(
    final_comparison,
    use_container_width=True,
    hide_index=True
)

# ============================================================
# ECONOMIC EQUATIONS
# ============================================================

st.markdown("---")
st.header("Mathematical Specification")

st.latex(
    r"Y_t = A_t K_t^{\alpha} L_t^{1-\alpha}"
)

st.markdown(
    "Production follows a constant-returns Cobb-Douglas specification."
)

st.latex(
    r"V^{T}_t = Y^{T}_t(1-\lambda_T)"
)

st.markdown(
    "Traditional net producer value equals output minus structural leakage."
)

st.latex(
    r"\Pi^{R}_t="
    r"Y^{R}_t(1-\lambda_R-c_a)"
)

st.markdown(
    "RIE-X operating surplus equals output after residual leakage "
    "and administrative cost."
)

st.latex(
    r"Q_t = r\Pi^{R}_t"
)

st.markdown(
    "A proportion r is allocated to the community reserve."
)

st.latex(
    r"I_t=s(\Pi^{R}_t-Q_t)"
)

st.markdown(
    "A proportion s of allocatable surplus becomes productive reinvestment."
)

st.latex(
    r"K_{t+1}=(1-\delta)K_t+I_t"
)

st.markdown(
    "Capital evolves through reinvestment net of depreciation."
)

st.latex(
    r"L_{t+1}=L_t(1+g_L)"
)

st.latex(
    r"A_{t+1}=A_t(1+g_A)"
)

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
        "Total"
    ],
    "Coefficient": [
        middleman,
        logistics,
        spoilage,
        finance_cost,
        distribution,
        traditional_leakage
    ]
})

leakage_table["Percent"] = (
    leakage_table["Coefficient"] * 100
)

st.dataframe(
    leakage_table[
        ["Component", "Percent"]
    ],
    use_container_width=True,
    hide_index=True
)

# ============================================================
# MODEL INTERPRETATION
# ============================================================

st.markdown("---")
st.header("Economic Interpretation")

st.markdown(
    """
The model tests whether structural value-chain integration can create
a different long-run equilibrium from the traditional rural economy.

The key mechanism is not simply a higher multiplier.

The proposed transmission mechanism is:

**Lower Value Leakage**

↓  

**Higher Captured Surplus**

↓  

**Higher Contributor Income + Community Reserves**

↓  

**Higher Productive Reinvestment**

↓  

**Larger Capital Stock**

↓  

**Higher Future Productive Capacity**

↓  

**Higher Local Value Creation**

The traditional model and RIE-X model therefore diverge dynamically
through differences in leakage, capital retention and productivity.
"""
)

# ============================================================
# DOWNLOAD
# ============================================================

st.markdown("---")
st.header("Export Model Results")

export_df = comparison_df.copy()

export_df["RIE-X Reinvestment"] = (
    riex_df["Reinvestment"]
)

export_df["RIE-X Recovered Value"] = (
    riex_df["Recovered Structural Value"]
)

export_df["RIE-X Cumulative Recovered Value"] = (
    riex_df["Cumulative Recovered Value"]
)

csv = export_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    "Download Simulation CSV",
    csv,
    "riex_dynamic_economic_model.csv",
    "text/csv"
)

# ============================================================
# MODEL NOTES
# ============================================================

with st.expander("Model Assumptions and Limitations"):

    st.markdown(
        """
1. The model is deterministic unless a demand shock is introduced.

2. Cobb-Douglas production is used as a transparent analytical
   structure, not as proof that RIE-X necessarily follows that
   production function.

3. The leakage coefficients are user-defined parameters.

4. The local multiplier is displayed separately from productive
   output to avoid double-counting induced economic activity.

5. Productivity growth rates are assumptions and should ultimately
   be calibrated using pilot or longitudinal data.

6. Capital depreciation is explicitly included.

7. The model currently assumes the same labour growth rate in both
   counterfactuals.

8. Prices, inflation, interest rates and exchange rates are not yet
   explicitly modelled.

9. Risk and uncertainty are not yet stochastic.

10. The next econometric extension can introduce Monte Carlo
    simulation, confidence intervals and sensitivity analysis.
"""
)
