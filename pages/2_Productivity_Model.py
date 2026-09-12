import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="RIE-X Productivity & Participant Capital Model", page_icon="⚙️", layout="wide")

MAIN_RIE_MODEL = "https://ruralint-egrated-economy.streamlit.app/"

st.title("RIE-X Productivity & Participant Capital Model")
st.caption(
    "Classify projects, participants, education, skills, experience and participant-owned assets; "
    "identify bottlenecks; test interventions; and estimate value per participant."
)

a,b = st.columns([1,4])
with a:
    st.link_button("← Main RIE-X Model", MAIN_RIE_MODEL, use_container_width=True)
with b:
    st.info("Scenario tool: coefficients and intervention effects are assumptions until calibrated with field data.")

PROJECT_CLASSES = {
    "Software & Digital Services": ["Software development","Shared digital storage","Web / app development","Cloud / server services","Digital design","Data services","Cybersecurity"],
    "Mechanical & Repair Services": ["Automobile repair","Machine repair","Welding / fabrication","Electrical repair","Tool-room services","Maintenance services"],
    "Agriculture & Primary Production": ["Crop production","Dairy","Poultry","Fisheries","Livestock","Horticulture"],
    "Food Processing & Manufacturing": ["Food processing","Packaging","Textiles","Garments","Wood products","Light manufacturing"],
    "Logistics & Distribution": ["Transport","Warehousing","Cold chain","Last-mile delivery","Procurement","Distribution"],
    "Market & Sales": ["Retail","B2B sales","Urban market cell","E-commerce","Marketing","Customer support"],
    "Knowledge & Professional Services": ["Engineering","Accounting","Legal","Training","Research","Consulting"],
    "Shared Infrastructure": ["Shared workshop","Shared machinery","Shared storage","Shared energy","Shared digital infrastructure","Community facility"],
}

st.sidebar.header("Project Setup")
project_class = st.sidebar.selectbox("Project class", list(PROJECT_CLASSES))
project_type = st.sidebar.selectbox("Project type", PROJECT_CLASSES[project_class])
project_name = st.sidebar.text_input("Project name", project_type)
period = st.sidebar.selectbox("Analysis period", ["Annual","Monthly"])
period_label = "year" if period == "Annual" else "month"

st.header("1. Participants, Education and Skills")

participants = st.number_input("Number of active participants", 1, 10000, 6 if project_class=="Software & Digital Services" else 10, 1)

EDUCATION_WEIGHTS = {
    "No formal qualification / learned on job":1.00,
    "School education":1.03,
    "ITI / vocational certificate":1.12,
    "Diploma":1.16,
    "Bachelor degree":1.20,
    "Postgraduate degree":1.24,
    "Doctoral / specialist qualification":1.28,
}
SKILL_WEIGHTS = {"Beginner":0.80,"Basic":0.95,"Competent":1.10,"Advanced":1.25,"Expert":1.40}
EXPERIENCE_WEIGHTS = {"0–1 years":0.90,"1–3 years":1.00,"3–5 years":1.08,"5–10 years":1.15,"10+ years":1.22}
CERT_WEIGHTS = {"None":1.00,"Relevant basic certification":1.04,"Relevant professional certification":1.09,"Multiple / advanced certifications":1.14}
RELEVANCE_WEIGHTS = {"Low relevance":0.85,"Moderate relevance":1.00,"High relevance":1.10,"Direct specialist match":1.20}

c1,c2,c3 = st.columns(3)
with c1:
    education = st.selectbox("Typical education / qualification", list(EDUCATION_WEIGHTS))
    skill = st.selectbox("Typical skill level", list(SKILL_WEIGHTS), index=2)
with c2:
    experience = st.selectbox("Typical experience", list(EXPERIENCE_WEIGHTS), index=2)
    certification = st.selectbox("Typical certification", list(CERT_WEIGHTS))
with c3:
    relevance = st.selectbox("Capability-to-role match", list(RELEVANCE_WEIGHTS), index=2)
    productive_hours = st.number_input(
        f"Average productive hours / participant / {period_label}",
        1.0, value=1600.0 if period=="Annual" else 140.0, step=10.0
    )

education_factor = EDUCATION_WEIGHTS[education]
skill_factor = SKILL_WEIGHTS[skill]
experience_factor = EXPERIENCE_WEIGHTS[experience]
cert_factor = CERT_WEIGHTS[certification]
relevance_factor = RELEVANCE_WEIGHTS[relevance]

human_capital_index = (education_factor*skill_factor*experience_factor*cert_factor*relevance_factor)**(1/5)
effective_labour = participants * human_capital_index

m1,m2,m3 = st.columns(3)
m1.metric("Headcount labour", f"{participants}")
m2.metric("Human-capital index", f"{human_capital_index:.2f}")
m3.metric("Effective labour units", f"{effective_labour:.2f}")

st.caption(
    "Human-capital index combines education, skill, experience, certification and role relevance. "
    "Default weights are illustrative and should later be calibrated by project category."
)

st.subheader("Role Mix")
ROLES = ["General labour","Skilled production","Technical / engineering","Management / coordination",
         "Sales / market access","Logistics","Knowledge / IP","Capital / equipment",
         "Digital infrastructure","Quality / compliance"]
rcols = st.columns(2)
for i,role in enumerate(ROLES):
    with rcols[i%2]:
        st.number_input(f"{role} participants", 0, int(participants), 0, 1, key=f"role_{i}")

st.header("2. Participant-Owned Productive Capital")
st.write(
    "Participant-owned assets remain privately owned. Only the portion committed to productive project use "
    "is recognized as productive capital."
)

ASSET_PRESETS = {
    "Software & Digital Services":[("Laptop / workstation",60000,.60),("Desktop / workstation",50000,.60),("NAS / shared storage",80000,.75),("Networking equipment",25000,.75),("Software licence",30000,.80)],
    "Mechanical & Repair Services":[("Hand tool set",25000,.70),("Diagnostic meter / scanner",40000,.70),("Welding machine",60000,.65),("Air compressor",55000,.65),("Power tools",30000,.70)],
    "Agriculture & Primary Production":[("Pump / irrigation equipment",40000,.65),("Power tiller",150000,.55),("Sprayer",18000,.60),("Tractor access",700000,.20),("Storage equipment",50000,.60)],
    "Food Processing & Manufacturing":[("Processing machine",150000,.65),("Packaging equipment",70000,.60),("Sewing / production machine",35000,.70),("Cutting equipment",45000,.65),("Quality testing tools",30000,.50)],
    "Logistics & Distribution":[("Two-wheeler",90000,.55),("Delivery van",700000,.40),("Storage racks",60000,.70),("Cold-storage equipment",250000,.60),("Tracking / communication device",25000,.70)],
    "Market & Sales":[("Laptop / POS device",45000,.55),("Display / retail equipment",60000,.60),("Two-wheeler",90000,.45),("Communication equipment",20000,.70),("Marketing equipment",25000,.50)],
    "Knowledge & Professional Services":[("Laptop / workstation",65000,.60),("Professional software",50000,.75),("Testing / measurement equipment",75000,.55),("Training equipment",40000,.55),("Reference / digital resources",20000,.70)],
    "Shared Infrastructure":[("Shared workstation",60000,.80),("Shared server / storage",120000,.85),("Workshop equipment",200000,.75),("Energy system",250000,.80),("Shared vehicle / logistics asset",600000,.55)]
}

asset_rows=[]
for i,(name,default_value,default_util) in enumerate(ASSET_PRESETS[project_class]):
    with st.expander(name, expanded=(i<2)):
        x1,x2,x3,x4 = st.columns(4)
        with x1:
            qty = st.number_input("Quantity",0,1000,1 if i==0 else 0,1,key=f"qty_{i}")
        with x2:
            fair = st.number_input("Fair value / asset (₹)",0.0,value=float(default_value),step=5000.0,key=f"fair_{i}")
        with x3:
            util = st.slider("Project utilisation %",0,100,int(default_util*100),5,key=f"util_{i}")/100
        with x4:
            condition = st.slider("Condition %",40,100,90,5,key=f"cond_{i}")/100
        recognized = qty*fair*util*condition
        asset_rows.append({"Asset":name,"Qty":qty,"Fair value":fair,"Utilisation":util,"Condition":condition,"Recognized participant capital":recognized})

assets_df = pd.DataFrame(asset_rows)
participant_owned_value = (assets_df["Qty"]*assets_df["Fair value"]).sum()
participant_capital = assets_df["Recognized participant capital"].sum()

st.dataframe(assets_df,use_container_width=True,hide_index=True)

shared_capital = st.number_input("Project-owned / shared productive assets (₹)",0.0,value=0.0,step=10000.0)
cash_capital = st.number_input("Cash-funded productive capital (₹)",0.0,value=0.0,step=10000.0)
total_capital = participant_capital + shared_capital + cash_capital

k1,k2,k3 = st.columns(3)
k1.metric("Participant assets owned",f"₹{participant_owned_value:,.0f}")
k2.metric("Participant capital recognized",f"₹{participant_capital:,.0f}")
k3.metric("Total productive capital",f"₹{total_capital:,.0f}")

st.header("3. Output, Productivity and Value per Participant")

o1,o2,o3,o4 = st.columns(4)
with o1:
    gross_output = st.number_input(f"Gross project output / {period_label} (₹)",0.0,value=3000000.0 if period=="Annual" else 250000.0,step=50000.0)
with o2:
    intermediate_cost = st.number_input(f"Materials / outside services / {period_label} (₹)",0.0,value=900000.0 if period=="Annual" else 75000.0,step=25000.0)
with o3:
    leakage_rate = st.slider("Waste / leakage %",0.0,40.0,10.0,1.0)/100
with o4:
    admin_rate = st.slider("Administration cost %",0.0,20.0,3.0,.5)/100

value_added = max(0.0,gross_output-intermediate_cost)
retained_value = max(0.0,value_added-gross_output*leakage_rate-gross_output*admin_rate)

output_per_person = gross_output/participants
output_per_effective_labour = gross_output/effective_labour if effective_labour else 0
value_added_per_person = value_added/participants
retained_per_person = retained_value/participants
capital_productivity = gross_output/total_capital if total_capital else 0

p1,p2,p3,p4,p5 = st.columns(5)
p1.metric("Output / participant",f"₹{output_per_person:,.0f}")
p2.metric("Output / effective labour unit",f"₹{output_per_effective_labour:,.0f}")
p3.metric("Value added / participant",f"₹{value_added_per_person:,.0f}")
p4.metric("Retained value / participant",f"₹{retained_per_person:,.0f}")
p5.metric("Output / ₹ capital",f"{capital_productivity:.2f}×" if total_capital else "—")

st.header("4. Human-Capital Development Opportunity")

skill_keys=list(SKILL_WEIGHTS)
rel_keys=list(RELEVANCE_WEIGHTS)
target_skill = st.selectbox("Target skill level after training / recruitment",skill_keys,index=min(skill_keys.index(skill)+1,len(skill_keys)-1))
target_relevance = st.selectbox("Target role match after redeployment / recruitment",rel_keys,index=min(rel_keys.index(relevance)+1,len(rel_keys)-1))

target_hci = (education_factor*SKILL_WEIGHTS[target_skill]*experience_factor*cert_factor*RELEVANCE_WEIGHTS[target_relevance])**(1/5)
hci_improvement = max(0.0,target_hci/human_capital_index-1)
st.metric("Potential human-capital index",f"{target_hci:.2f}",f"{hci_improvement*100:.1f}%")

st.header("5. Productivity Bottleneck Diagnosis")

BOTTLENECKS=["Skill / training","Education / technical knowledge","Tools / machinery","Digital technology",
             "Working capital","Energy / power","Raw material supply","Logistics","Market access",
             "Quality / standards","Management / coordination","Storage / infrastructure","Information / data"]

scores={}
b1,b2=st.columns(2)
for i,item in enumerate(BOTTLENECKS):
    with (b1 if i%2==0 else b2):
        scores[item]=st.slider(item,0,10,3,1,key=f"bn_{i}")

ranked=sorted(scores.items(),key=lambda x:x[1],reverse=True)
st.dataframe(pd.DataFrame(ranked,columns=["Bottleneck","Severity"]),use_container_width=True,hide_index=True)

st.header("6. Intervention Simulator")
top_constraint=ranked[0][0]
st.info(f"Highest rated constraint: **{top_constraint}**")

i1,i2,i3,i4=st.columns(4)
with i1:
    technical_gain=st.slider("Technology / process productivity gain %",0.0,100.0,10.0,1.0)/100
with i2:
    human_realisation=st.slider("Share of human-capital potential realised %",0.0,100.0,60.0,5.0)/100
with i3:
    leakage_reduction=st.slider("Leakage reduction percentage points",0.0,30.0,3.0,1.0)/100
with i4:
    intervention_cost=st.number_input("Intervention investment (₹)",0.0,value=100000.0,step=10000.0)

human_gain=hci_improvement*human_realisation
combined_gain=(1+technical_gain)*(1+human_gain)-1

new_output=gross_output*(1+combined_gain)
new_value_added=max(0.0,new_output-intermediate_cost)
new_leakage=max(0.0,leakage_rate-leakage_reduction)
new_retained=max(0.0,new_value_added-new_output*new_leakage-new_output*admin_rate)
new_retained_per_person=new_retained/participants
delta_retained=new_retained-retained_value
simple_payback=intervention_cost/delta_retained if delta_retained>0 else np.nan

q1,q2,q3,q4=st.columns(4)
q1.metric("Combined productivity gain",f"{combined_gain*100:.1f}%")
q2.metric("New output / participant",f"₹{new_output/participants:,.0f}",f"₹{new_output/participants-output_per_person:,.0f}")
q3.metric("New retained value / participant",f"₹{new_retained_per_person:,.0f}",f"₹{new_retained_per_person-retained_per_person:,.0f}")
q4.metric("Simple payback",f"{simple_payback:.2f} periods" if np.isfinite(simple_payback) else "—")

st.header("7. Contribution Accounting")

contrib=pd.DataFrame({
    "Contribution class":["Labour","Skill / human capital","Participant-owned capital service","Project/shared capital","Knowledge / IP","Market / logistics"],
    "Possible basis":["Verified productive hours × role rate","Verified capability × productive application","Audited asset service value × utilisation","Cash or project-owned productive assets","Documented design/process/IP contribution","Measured sales/distribution contribution"]
})
st.dataframe(contrib,use_container_width=True,hide_index=True)
st.warning("Economic contribution claims and governance voting rights should be recorded separately.")

st.header("8. Project Diagnostic Summary")

summary=pd.DataFrame({
    "Metric":["Project","Participants","Human-capital index","Effective labour units","Recognized participant capital",
              "Total productive capital","Current output","Current retained value / participant",
              "Highest bottleneck","Simulated productivity gain","Simulated retained value / participant"],
    "Value":[project_name,str(participants),f"{human_capital_index:.2f}",f"{effective_labour:.2f}",
             f"₹{participant_capital:,.0f}",f"₹{total_capital:,.0f}",f"₹{gross_output:,.0f}",
             f"₹{retained_per_person:,.0f}",top_constraint,f"{combined_gain*100:.1f}%",f"₹{new_retained_per_person:,.0f}"]
})
st.dataframe(summary,use_container_width=True,hide_index=True)

st.download_button(
    "Download Project Diagnostic CSV",
    summary.to_csv(index=False).encode("utf-8"),
    file_name="riex_project_productivity_diagnostic.csv",
    mime="text/csv"
)

st.divider()
st.markdown(
    "**Core principle:** participant value should rise through measurable increases in productive capability, "
    "output, value added and retained surplus—not merely through issuing more tokens."
)
st.link_button("Return to Main RIE-X Economic Model",MAIN_RIE_MODEL)

