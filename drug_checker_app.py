"""
drug_checker_app.py — Nigerian Drug Interaction Checker
Mobile-optimised for Android phones.
Rule-based, free, offline, no API key needed.
"""

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="💊 Nigeria Drug Checker",
    page_icon="💊",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Mobile CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Mobile-first styling */
html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}
.main .block-container {
    padding: 1rem 1rem 2rem 1rem;
    max-width: 480px;
    margin: 0 auto;
}
/* Large tap targets */
.stButton > button {
    width: 100%;
    padding: 0.75rem 1rem;
    font-size: 1rem;
    border-radius: 12px;
    font-weight: 600;
    min-height: 52px;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #008751, #00A86B);
    color: white;
    border: none;
    font-size: 1.1rem;
}
/* Input fields */
.stTextInput > div > div > input {
    font-size: 1rem;
    padding: 0.6rem 0.8rem;
    border-radius: 10px;
    min-height: 48px;
}
.stSelectbox > div > div {
    font-size: 1rem;
    border-radius: 10px;
    min-height: 48px;
}
/* Cards */
.drug-card {
    background: white;
    border-radius: 16px;
    padding: 1rem;
    margin: 0.5rem 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    border-left: 5px solid #008751;
}
.severity-severe { border-left-color: #D32F2F !important; }
.severity-moderate { border-left-color: #F57C00 !important; }
.severity-mild { border-left-color: #F9A825 !important; }
.severity-safe { border-left-color: #388E3C !important; }

/* Section headers */
.section-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #1a1a1a;
    margin: 1rem 0 0.5rem 0;
}
/* Nigerian flag header */
.app-header {
    background: linear-gradient(135deg, #008751 0%, #008751 33%, #ffffff 33%, #ffffff 66%, #008751 66%);
    border-radius: 16px;
    padding: 1rem;
    text-align: center;
    margin-bottom: 1rem;
    color: white;
}
/* Quick buttons */
.quick-btn {
    background: #F0F7F4;
    border: 1px solid #008751;
    border-radius: 10px;
    padding: 0.5rem;
    margin: 0.2rem 0;
    font-size: 0.85rem;
}
/* Expander */
.streamlit-expanderHeader {
    font-size: 0.95rem;
    border-radius: 10px;
}
/* Hide sidebar toggle on mobile */
section[data-testid="stSidebar"] { display: none; }
/* Bottom nav spacing */
.bottom-space { height: 80px; }
</style>
""", unsafe_allow_html=True)

# ── Interaction Database ───────────────────────────────────────────────────────
INTERACTIONS = [
    ("artemether-lumefantrine", "efavirenz", "MODERATE",
     "Efavirenz reduces lumefantrine blood levels by ~40%",
     "Reduced malaria treatment efficacy",
     "Monitor treatment response. Repeat RDT at day 3.",
     "🇳🇬 Common in Nigeria — HIV/malaria co-infection. Monitor closely."),

    ("artemether-lumefantrine", "rifampicin", "SEVERE",
     "Rifampicin reduces lumefantrine by 68%",
     "Likely malaria treatment failure",
     "AVOID. Use artesunate + amodiaquine instead.",
     "🇳🇬 Never combine — TB/malaria co-infection common in North Nigeria."),

    ("artemether-lumefantrine", "nevirapine", "MODERATE",
     "Nevirapine reduces lumefantrine exposure",
     "Reduced malaria treatment efficacy",
     "Monitor closely. Consider artesunate + amodiaquine.",
     "🇳🇬 Report treatment failure to SMOH."),

    ("efavirenz", "rifampicin", "MODERATE",
     "Rifampicin reduces efavirenz levels by 26%",
     "Risk of HIV virological failure",
     "Increase efavirenz to 800mg/day if >60kg. Monitor viral load.",
     "🇳🇬 Nigeria ART Guidelines 2021: standard HIV/TB co-treatment recommendation."),

    ("nevirapine", "rifampicin", "SEVERE",
     "Rifampicin reduces nevirapine by 37-58%",
     "High risk of HIV treatment failure",
     "AVOID. Switch to efavirenz-based regimen.",
     "🇳🇬 Contraindicated per Nigeria ART Guidelines."),

    ("cotrimoxazole", "methotrexate", "SEVERE",
     "Additive folate antagonism",
     "Severe bone marrow suppression",
     "AVOID combination. Monitor FBC weekly if unavoidable.",
     "🇳🇬 Cotrimoxazole used widely for HIV prophylaxis."),

    ("fluconazole", "rifampicin", "MODERATE",
     "Rifampicin reduces fluconazole levels by 23%",
     "Risk of antifungal treatment failure",
     "Double fluconazole dose to 800mg/day.",
     "🇳🇬 Cryptococcal meningitis + TB co-infection in HIV patients."),

    ("metformin", "hydrochlorothiazide", "MILD",
     "Thiazides cause hyperglycaemia",
     "Reduced blood sugar control",
     "Monitor glucose more frequently.",
     "🇳🇬 Common combination for diabetes + hypertension."),

    ("amlodipine", "rifampicin", "SEVERE",
     "Rifampicin markedly reduces amlodipine levels",
     "Loss of blood pressure control",
     "Avoid if possible. Monitor BP daily if combined.",
     "🇳🇬 TB patients on rifampicin with hypertension — monitor BP."),

    ("ciprofloxacin", "antacids", "MODERATE",
     "Antacids reduce ciprofloxacin absorption by 90%",
     "Reduced antibiotic efficacy",
     "Take ciprofloxacin 2 hours before antacids.",
     "🇳🇬 Antacid use very common in Nigeria — counsel patients."),

    ("ciprofloxacin", "metronidazole", "MILD",
     "Additive QT prolongation risk",
     "Cardiac arrhythmia risk in susceptible patients",
     "Use with caution in cardiac patients.",
     "🇳🇬 Common combination for typhoid/abdominal infections."),

    ("warfarin", "cotrimoxazole", "SEVERE",
     "Cotrimoxazole inhibits warfarin metabolism",
     "Elevated INR — serious bleeding risk",
     "Avoid. If necessary, reduce warfarin 50% and monitor INR every 2-3 days.",
     "🇳🇬 Important in cardiac patients at teaching hospitals."),

    ("warfarin", "rifampicin", "SEVERE",
     "Rifampicin powerfully induces warfarin metabolism",
     "Markedly reduced anticoagulation — thrombosis risk",
     "Increase warfarin 2-5x and monitor INR every 2-3 days.",
     "🇳🇬 Specialist management required for TB patients on warfarin."),

    ("metronidazole", "alcohol", "SEVERE",
     "Metronidazole inhibits alcohol metabolism",
     "Flushing, vomiting, hypotension (disulfiram reaction)",
     "No alcohol during treatment and 48 hours after.",
     "🇳🇬 Counsel patients explicitly about alcohol avoidance."),

    ("primaquine", "any", "SEVERE",
     "Oxidative stress on G6PD-deficient red cells",
     "Life-threatening haemolytic anaemia",
     "ALWAYS screen for G6PD before prescribing primaquine.",
     "🇳🇬 G6PD deficiency affects ~20% of Nigerian males."),

    ("dapsone", "any", "SEVERE",
     "Haemolysis in G6PD-deficient patients",
     "Haemolytic anaemia and methaemoglobinaemia",
     "Contraindicated in G6PD deficiency. Screen first.",
     "🇳🇬 Used for leprosy and PCP prophylaxis — critical G6PD check."),

    ("nitrofurantoin", "any", "MODERATE",
     "Oxidative haemolysis in G6PD deficiency",
     "Haemolytic anaemia",
     "Avoid in known G6PD deficiency.",
     "🇳🇬 High G6PD prevalence in Nigeria — check before prescribing."),

    ("tenofovir", "ibuprofen", "MODERATE",
     "Both nephrotoxic — additive kidney damage",
     "Acute kidney injury",
     "Avoid chronic NSAID use with tenofovir. Monitor creatinine quarterly.",
     "🇳🇬 Tenofovir is first-line ART backbone. Avoid diclofenac/ibuprofen."),

    ("phenytoin", "cotrimoxazole", "MODERATE",
     "Cotrimoxazole inhibits phenytoin metabolism",
     "Phenytoin toxicity — ataxia, confusion",
     "Monitor phenytoin levels. Reduce dose if toxicity appears.",
     "🇳🇬 Common in Nigerian epilepsy management."),

    ("hydroxyurea", "didanosine", "SEVERE",
     "Additive pancreatitis and neuropathy risk",
     "Severe, potentially fatal pancreatitis",
     "CONTRAINDICATED. Never combine.",
     "🇳🇬 Sickle cell patients with HIV — critical interaction."),

    ("doxycycline", "antacids", "MODERATE",
     "Chelation reduces doxycycline absorption",
     "Reduced antibiotic efficacy",
     "Take doxycycline 2 hours before antacids.",
     "🇳🇬 Used for malaria prophylaxis in Nigeria."),

    ("lisinopril", "potassium", "MODERATE",
     "ACE inhibitors reduce potassium excretion",
     "Hyperkalaemia — cardiac arrhythmia risk",
     "Avoid potassium supplements. Monitor serum K monthly.",
     "🇳🇬 Avoid with spironolactone in hypertension."),

    ("artesunate", "amodiaquine", "MILD",
     "Additive QT prolongation and hepatotoxicity",
     "Mild QT prolongation; rare hepatotoxicity",
     "Generally safe. Monitor LFTs in prolonged use.",
     "🇳🇬 FMOH-recommended first-line malaria combination."),

    ("quinine", "antacids", "MILD",
     "Antacids may reduce quinine absorption",
     "Slightly reduced quinine levels",
     "Separate by 2 hours.",
     "🇳🇬 Quinine used for severe malaria in Nigerian hospitals."),

    ("artemether-lumefantrine", "grapefruit", "MILD",
     "Grapefruit inhibits CYP3A4",
     "Possible QT prolongation",
     "Avoid grapefruit juice. Take with full-fat milk.",
     "🇳🇬 Take with food to improve lumefantrine absorption."),
]

G6PD_HIGH = ["primaquine", "dapsone", "nitrofurantoin", "rasburicase"]
G6PD_MOD  = ["chloroquine", "ciprofloxacin", "cotrimoxazole", "sulphamethoxazole", "norfloxacin"]
SEV_EMOJI = {"CONTRAINDICATED": "⛔", "SEVERE": "🔴", "MODERATE": "🟠", "MILD": "🟡", "SAFE": "🟢"}
SEV_ORDER = {"CONTRAINDICATED": 0, "SEVERE": 1, "MODERATE": 2, "MILD": 3, "SAFE": 4}
SEV_CLASS = {"SEVERE": "severity-severe", "CONTRAINDICATED": "severity-severe",
             "MODERATE": "severity-moderate", "MILD": "severity-mild"}

COMBOS = [
    ("Artemether-Lumefantrine", "Cotrimoxazole", "HIV/malaria"),
    ("Efavirenz", "Rifampicin", "HIV/TB"),
    ("Artemether-Lumefantrine", "Efavirenz", "HIV/malaria"),
    ("Metformin", "Hydrochlorothiazide", "DM + HTN"),
    ("Ciprofloxacin", "Metronidazole", "Typhoid"),
    ("Amlodipine", "Lisinopril", "Hypertension"),
]


def check(drugs):
    dl = [d.lower().strip() for d in drugs]
    found = []
    seen = set()
    for a, b, sev, mech, effect, mgmt, note in INTERACTIONS:
        ma = next((d for d in dl if a in d or d in a), None)
        mb = next((d for d in dl if b == "any" or b in d or d in b), None)
        if ma and mb and ma != mb:
            key = tuple(sorted([ma, mb]))
            if key not in seen:
                seen.add(key)
                found.append({"a": ma.title(), "b": mb.title() if b != "any" else "G6PD-risk drug",
                               "sev": sev, "mech": mech, "effect": effect,
                               "mgmt": mgmt, "note": note})
    found.sort(key=lambda x: SEV_ORDER.get(x["sev"], 9))
    return found


def g6pd_check(drugs):
    dl = [d.lower().strip() for d in drugs]
    hi = [d for d in dl if any(r in d or d in r for r in G6PD_HIGH)]
    mo = [d for d in dl if any(r in d or d in r for r in G6PD_MOD)]
    return hi, mo


# ── App Header ────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding: 1rem 0 0.5rem 0;'>
  <div style='font-size:2.5rem;'>💊</div>
  <div style='font-size:1.4rem; font-weight:800; color:#008751;'>Nigeria Drug Checker</div>
  <div style='font-size:0.8rem; color:#666;'>🇳🇬 NLEM 2020 · Free · No internet needed</div>
</div>
""", unsafe_allow_html=True)

# ── Quick Combos ──────────────────────────────────────────────────────────────
st.markdown("<div class='section-title'>⚡ Quick Check</div>", unsafe_allow_html=True)
cols = st.columns(2)
for idx, (d1, d2, cond) in enumerate(COMBOS):
    with cols[idx % 2]:
        if st.button(f"{cond}", key=f"q_{idx}", use_container_width=True):
            st.session_state["d1"] = d1
            st.session_state["d2"] = d2

st.divider()

# ── Drug Input ────────────────────────────────────────────────────────────────
st.markdown("<div class='section-title'>💉 Enter Drugs</div>", unsafe_allow_html=True)
d1 = st.text_input("Drug 1 *", value=st.session_state.get("d1", ""),
                    placeholder="e.g. Artemether-Lumefantrine")
d2 = st.text_input("Drug 2 *", value=st.session_state.get("d2", ""),
                    placeholder="e.g. Efavirenz")
d3 = st.text_input("Drug 3 (optional)", placeholder="e.g. Cotrimoxazole")
d4 = st.text_input("Drug 4 (optional)", placeholder="e.g. Rifampicin")

st.markdown("<div class='section-title'>👤 Patient</div>", unsafe_allow_html=True)
patient = st.selectbox("Patient type", [
    "Adult", "Pregnant woman", "Child (under 12)",
    "Elderly (65+)", "G6PD deficiency", "Renal impairment", "Liver disease"
])

drugs = [x.strip() for x in [d1, d2, d3, d4] if x.strip()]
go = st.button("🔍 Check Interactions", type="primary", disabled=len(drugs) < 2)

# ── Results ───────────────────────────────────────────────────────────────────
if go and len(drugs) >= 2:
    results = check(drugs)
    hi_g6pd, mo_g6pd = g6pd_check(drugs)

    st.divider()

    # Summary badge
    if not results and not hi_g6pd:
        st.success("✅ No major interactions found.\n\nAlways verify with a pharmacist for complex cases.")
    else:
        worst = results[0]["sev"] if results else "MILD"
        st.markdown(f"""
        <div style='background:{"#FFEBEE" if worst in ("SEVERE","CONTRAINDICATED") else "#FFF3E0" if worst=="MODERATE" else "#FFFDE7"};
                    border-radius:12px; padding:1rem; text-align:center; margin-bottom:1rem;'>
            <div style='font-size:2rem;'>{SEV_EMOJI.get(worst,"🟡")}</div>
            <div style='font-size:1.1rem; font-weight:700;'>Highest Risk: {worst}</div>
            <div style='font-size:0.85rem; color:#555;'>{len(results)} interaction(s) found</div>
        </div>
        """, unsafe_allow_html=True)

    # Interaction cards
    for item in results:
        sev_color = {"SEVERE":"#FFEBEE","CONTRAINDICATED":"#FFEBEE",
                     "MODERATE":"#FFF3E0","MILD":"#FFFDE7"}.get(item["sev"],"#F1F8E9")
        border = {"SEVERE":"#D32F2F","CONTRAINDICATED":"#B71C1C",
                  "MODERATE":"#F57C00","MILD":"#F9A825"}.get(item["sev"],"#388E3C")
        with st.expander(
            f"{SEV_EMOJI.get(item['sev'],'🟡')} {item['a']} + {item['b']} — {item['sev']}",
            expanded=item["sev"] in ("SEVERE","CONTRAINDICATED")
        ):
            st.markdown(f"**⚙️ Why:** {item['mech']}")
            st.markdown(f"**⚡ Effect:** {item['effect']}")
            st.markdown(f"**✅ Action:** {item['mgmt']}")
            st.info(item["note"])

    # G6PD warning
    if hi_g6pd:
        st.error(f"⛔ **G6PD HIGH RISK:** {', '.join(hi_g6pd)}\n\nMUST screen for G6PD deficiency first!\n~20% of Nigerian males are affected.")
    if mo_g6pd:
        st.warning(f"⚠️ **G6PD CAUTION:** {', '.join(mo_g6pd)}\n\nUse carefully in G6PD deficiency.")

    # Patient warnings
    if patient == "Pregnant woman":
        st.warning("🤰 **Pregnancy:** Avoid tetracyclines, fluoroquinolones, metronidazole (1st trimester), primaquine.\n\nSafe malaria Rx: Quinine + clindamycin (1st trimester) or AL (2nd/3rd trimester).")
    elif patient == "Child (under 12)":
        st.warning("👶 **Paediatric:** Avoid fluoroquinolones and tetracyclines under 8 years. Use weight-based dosing.")
    elif patient == "Renal impairment":
        st.warning("🫘 **Renal:** Reduce/avoid: metformin, tenofovir, cotrimoxazole, nitrofurantoin. Monitor creatinine.")
    elif patient == "G6PD deficiency":
        st.error("🧬 **G6PD confirmed:** Avoid primaquine, dapsone, nitrofurantoin, high-dose sulphonamides.")

    # Download
    report = f"NIGERIA DRUG INTERACTION REPORT\n{'='*40}\n"
    report += f"Drugs: {' + '.join(drugs)}\nPatient: {patient}\nDate: {pd.Timestamp.now().strftime('%Y-%m-%d')}\n\n"
    for item in results:
        report += f"\n{item['sev']}: {item['a']} + {item['b']}\n  {item['mech']}\n  Action: {item['mgmt']}\n"
    report += "\n\nBased on Nigeria NLEM 2020. For clinical decision support only."
    st.download_button("⬇️ Save Report", report,
                       file_name="drug_check.txt", mime="text/plain")

# ── Reference ─────────────────────────────────────────────────────────────────
st.divider()
with st.expander("⚠️ G6PD Risk Drugs (Nigeria ~20% prevalence)"):
    st.markdown("""
| Risk | Drugs |
|------|-------|
| 🔴 HIGH | Primaquine, Dapsone, Nitrofurantoin |
| 🟠 MOD | Chloroquine, Cotrimoxazole, Quinolones |

**Always screen before prescribing HIGH risk drugs.**
""")

with st.expander("🦠 HIV/TB/Malaria Co-infection Quick Reference"):
    st.markdown("""
| Combo | Issue | Action |
|-------|-------|--------|
| RIF + EFV | EFV ↓26% | EFV 800mg if >60kg |
| RIF + NVP | NVP ↓58% | Switch to EFV |
| AL + EFV | Lume ↓40% | Monitor day 3 RDT |
| FLU + RIF | FLU ↓23% | Double fluconazole |

*Nigeria ART Guidelines 2021*
""")

with st.expander("ℹ️ About"):
    st.markdown("""
**Nigeria Drug Interaction Checker**
Built for Nigerian health workers — CHWs, nurses, doctors.

📋 **Data sources:**
- Nigeria NLEM 2020
- Nigeria ART Guidelines 2021  
- Nigeria Malaria Treatment Guidelines 2015
- WHO Model Formulary
- UNICEF/WHO G6PD Guidelines

⚠️ For clinical decision support only.
Always verify with a qualified pharmacist.

🔬 Part of the **Nigeria Health AI** project
""")

st.markdown("<div class='bottom-space'></div>", unsafe_allow_html=True)
