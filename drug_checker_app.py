import streamlit as st
import urllib.parse
from datetime import datetime

st.set_page_config(
    page_title="Nigeria Drug Checker",
    page_icon="💊",
    layout="centered",
    initial_sidebar_state="collapsed",
)

PHARMACIST_WHATSAPP = "2348012345678"  # ← replace with real number (no +)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #f5f7fa !important;
        color: #1a1a2e !important;
    }
    .stApp { background: #f5f7fa; }

    /* Header */
    .app-header {
        background: white;
        border-radius: 16px;
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
        border: 1px solid #e8ecf0;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    .app-header .icon-wrap {
        width: 52px; height: 52px;
        background: #e8f4fd;
        border-radius: 14px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.6rem;
    }
    .app-header h1 {
        margin: 0; font-size: 1.35rem; font-weight: 700;
        color: #1a1a2e;
    }
    .app-header p {
        margin: 2px 0 0; font-size: 0.82rem;
        color: #6b7280;
    }

    /* Section cards */
    .section-card {
        background: white;
        border-radius: 14px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1.25rem;
        border: 1px solid #e8ecf0;
    }
    .section-title {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #2563eb;
        margin-bottom: 0.3rem;
    }
    .section-desc {
        font-size: 0.85rem;
        color: #6b7280;
        margin-bottom: 1rem;
        line-height: 1.5;
    }

    /* Step badge */
    .step-badge {
        display: inline-flex; align-items: center; justify-content: center;
        width: 20px; height: 20px;
        background: #2563eb; color: white;
        border-radius: 50%; font-size: 0.7rem; font-weight: 700;
        margin-right: 6px; vertical-align: middle;
    }

    /* Result boxes */
    .result-safe   { background:#f0fdf4; border-left:4px solid #16a34a; border-radius:0 10px 10px 0; padding:1rem 1.25rem; margin:0.75rem 0; color:#14532d; font-size:0.9rem; line-height:1.7; white-space:pre-wrap; }
    .result-warn   { background:#fffbeb; border-left:4px solid #d97706; border-radius:0 10px 10px 0; padding:1rem 1.25rem; margin:0.75rem 0; color:#78350f; font-size:0.9rem; line-height:1.7; white-space:pre-wrap; }
    .result-danger { background:#fef2f2; border-left:4px solid #dc2626; border-radius:0 10px 10px 0; padding:1rem 1.25rem; margin:0.75rem 0; color:#7f1d1d; font-size:0.9rem; line-height:1.7; white-space:pre-wrap; }
    .result-info   { background:#eff6ff; border-left:4px solid #2563eb; border-radius:0 10px 10px 0; padding:1rem 1.25rem; margin:0.75rem 0; color:#1e3a8a; font-size:0.9rem; line-height:1.6; }

    /* WhatsApp button */
    .wa-btn {
        display: inline-block;
        background: #25d366; color: #fff !important;
        font-weight: 600; padding: 0.65rem 1.5rem;
        border-radius: 50px; text-decoration: none !important;
        font-size: 0.9rem; margin-top: 0.75rem;
        border: none;
    }
    .wa-btn:hover { background: #1ebe5d; }

    /* Quick reference pills */
    .pill-safe   { display:inline-block; background:#dcfce7; color:#15803d; padding:3px 10px; border-radius:20px; font-size:0.75rem; font-weight:600; margin-right:6px; }
    .pill-warn   { display:inline-block; background:#fef9c3; color:#a16207; padding:3px 10px; border-radius:20px; font-size:0.75rem; font-weight:600; margin-right:6px; }
    .pill-danger { display:inline-block; background:#fee2e2; color:#b91c1c; padding:3px 10px; border-radius:20px; font-size:0.75rem; font-weight:600; margin-right:6px; }

    .combo-row {
        padding: 0.7rem 0;
        border-bottom: 1px solid #f0f0f0;
        font-size: 0.88rem;
        color: #374151;
    }
    .combo-row:last-child { border-bottom: none; }
    .combo-note { font-size: 0.8rem; color: #6b7280; margin-top: 2px; }

    /* Override Streamlit defaults for white bg */
    .stTextInput > div > div > input {
        background: #f9fafb !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 8px !important;
        color: #1a1a2e !important;
    }
    .stTextArea > div > div > textarea {
        background: #f9fafb !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 8px !important;
        color: #1a1a2e !important;
    }
    .stButton > button {
        background: #2563eb !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 0.6rem 1rem !important;
    }
    .stButton > button:hover { background: #1d4ed8 !important; }

    footer { visibility: hidden; }
    #MainMenu { visibility: hidden; }
    header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
  <div class="icon-wrap">💊</div>
  <div>
    <h1>Nigeria Drug Checker</h1>
    <p>Drug interactions · Photo enquiries · Reviews — sent to your pharmacist via WhatsApp</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# INTERACTION DATABASE
# ══════════════════════════════════════════════════════════════════════════════
INTERACTIONS = {
    frozenset({"amoxicillin", "metronidazole"}): ("Moderate","Common combination for H. pylori and dental infections. Mild GI side effects possible (nausea, vomiting). Generally acceptable.","Take with food. Monitor for nausea. Acceptable combination."),
    frozenset({"metformin", "alcohol"}): ("Severe","Significantly increases risk of lactic acidosis — dangerous build-up of lactic acid in the blood.","Avoid alcohol completely while on Metformin. Urgent pharmacist review if patient drinks regularly."),
    frozenset({"warfarin", "aspirin"}): ("Severe","Both drugs thin the blood. Greatly increases internal bleeding risk.","Do NOT combine without specialist supervision. Refer to doctor immediately."),
    frozenset({"artemether", "lumefantrine"}): ("None","Standard fixed-dose combination (Coartem/ALu) — designed to be taken together for malaria.","Safe as prescribed. Standard Nigerian malaria treatment."),
    frozenset({"paracetamol", "ibuprofen"}): ("Low","Can be safely alternated short-term. Different mechanisms. Paracetamol is liver-processed; Ibuprofen is anti-inflammatory.","Safe short-term. Avoid in liver/kidney disease. Don't exceed recommended doses."),
    frozenset({"ciprofloxacin", "antacid"}): ("Moderate","Antacids reduce Ciprofloxacin absorption by up to 90%, making the antibiotic ineffective.","Take Ciprofloxacin at least 2 hours before or 6 hours after any antacid."),
    frozenset({"lisinopril", "potassium"}): ("Moderate","ACE inhibitors raise blood potassium. Adding supplements risks hyperkalaemia — heart arrhythmia.","Avoid potassium supplements unless prescribed. Monitor potassium levels."),
    frozenset({"diazepam", "alcohol"}): ("Severe","Both suppress the CNS. Combined they dangerously suppress breathing — risk of coma and death.","Never combine. Counsel patient urgently."),
    frozenset({"amlodipine", "simvastatin"}): ("Moderate","Amlodipine raises Simvastatin levels — increases risk of muscle damage (myopathy).","Limit Simvastatin to 20mg/day with Amlodipine. Consider switching to Atorvastatin."),
    frozenset({"metronidazole", "alcohol"}): ("Severe","Causes severe disulfiram-like reaction — vomiting, flushing, palpitations. Very common mistake in Nigeria.","Strictly avoid alcohol during treatment and 48 hours after finishing."),
    frozenset({"cotrimoxazole", "warfarin"}): ("Severe","Septrin greatly potentiates Warfarin — drastically increases bleeding risk.","Avoid combination. If essential, reduce Warfarin dose and monitor INR closely."),
    frozenset({"tramadol", "ssri"}): ("Severe","Risk of serotonin syndrome — agitation, confusion, rapid heart rate, muscle twitching. Can be fatal.","Avoid. Refer to doctor. Flag urgently if patient is on antidepressants."),
    frozenset({"aspirin", "ibuprofen"}): ("Moderate","Both NSAIDs. Increases GI bleeding risk. Ibuprofen can block aspirin's cardioprotective effect.","Avoid combining. If needed, take aspirin 30 mins before Ibuprofen."),
    frozenset({"chloroquine", "antacid"}): ("Moderate","Antacids reduce Chloroquine absorption — less effective malaria treatment.","Separate doses by at least 4 hours."),
    frozenset({"rifampicin", "oral contraceptive"}): ("Severe","Rifampicin (TB drug) drastically reduces contraceptive effectiveness — high pregnancy risk.","Use condoms throughout TB treatment and 4 weeks after. Counsel patient clearly."),
}

def check_interaction(d1, d2):
    return INTERACTIONS.get(frozenset({d1.lower().strip(), d2.lower().strip()}), None)

def sev_cls(s):
    return "danger" if s == "Severe" else "warn" if s in ("Moderate","Low") else "safe"

def sev_icon(s):
    return "🔴" if s == "Severe" else "🟠" if s == "Moderate" else "🟡" if s == "Low" else "🟢"

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — Drug Interaction Checker
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="section-card">
  <div class="section-title"><span class="step-badge">1</span>Drug interaction checker</div>
  <div class="section-desc">Check if two drugs are safe to take together. Built-in Nigerian clinical database — no internet or AI needed.</div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    drug1 = st.text_input("Drug 1", placeholder="e.g. Metronidazole")
with col2:
    drug2 = st.text_input("Drug 2", placeholder="e.g. Alcohol")

condition    = st.text_input("Patient condition (optional)", placeholder="e.g. malaria, TB, pregnant")
client_name1 = st.text_input("Client name (optional)", placeholder="e.g. Emeka Obi", key="cn1")

if st.button("Check interaction", use_container_width=True):
    if drug1.strip() and drug2.strip():
        result = check_interaction(drug1, drug2)
        if result:
            severity, explanation, action = result
            cls  = sev_cls(severity)
            icon = sev_icon(severity)
            st.markdown(f"""<div class="result-{cls}">
{icon} <strong>Severity: {severity}</strong>

📋 <strong>Interaction:</strong>
{explanation}

✅ <strong>Recommended action:</strong>
{action}
</div>""", unsafe_allow_html=True)

            ts  = datetime.now().strftime("%d %b %Y, %H:%M")
            msg = f"""💊 *DRUG INTERACTION — Nigeria Drug Checker*\n🕐 {ts}\n\n👤 *Client:* {client_name1 or 'Anonymous'}\n💊 *Drug 1:* {drug1}\n💊 *Drug 2:* {drug2}\n🏥 *Condition:* {condition or 'Not specified'}\n\n⚠️ *Severity:* {severity}\n\n📋 *Interaction:*\n{explanation}\n\n✅ *Action:*\n{action}\n\n_Sent via Nigeria Drug Checker_"""
            url = f"https://wa.me/{PHARMACIST_WHATSAPP}?text={urllib.parse.quote(msg)}"
            st.markdown(f'<a class="wa-btn" href="{url}" target="_blank">📲 Send result to pharmacist on WhatsApp</a>', unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="result-warn">
🟡 <strong>Not in database</strong>

<strong>{drug1}</strong> + <strong>{drug2}</strong> is not in our local database. This does not mean it is safe — ask the pharmacist to verify.
</div>""", unsafe_allow_html=True)
            ts  = datetime.now().strftime("%d %b %Y, %H:%M")
            msg = f"""💊 *DRUG QUERY — Nigeria Drug Checker*\n🕐 {ts}\n\n👤 *Client:* {client_name1 or 'Anonymous'}\n💊 *Drug 1:* {drug1}\n💊 *Drug 2:* {drug2}\n🏥 *Condition:* {condition or 'Not specified'}\n\n⚠️ This combination is NOT in our local database.\nPlease advise whether it is safe.\n\n_Sent via Nigeria Drug Checker_"""
            url = f"https://wa.me/{PHARMACIST_WHATSAPP}?text={urllib.parse.quote(msg)}"
            st.markdown(f'<a class="wa-btn" href="{url}" target="_blank">📲 Ask pharmacist on WhatsApp</a>', unsafe_allow_html=True)
    else:
        st.warning("Please enter both drug names.")

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — Quick Reference
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="section-card">
  <div class="section-title"><span class="step-badge">2</span>Common Nigerian drug combinations</div>
  <div class="section-desc">Quick reference for the most important drug pairs in Nigerian clinical practice.</div>
""", unsafe_allow_html=True)

combos = [
    ("safe",   "Artemether + Lumefantrine (Coartem)",         "✅ Safe",      "Standard malaria treatment. Take with food."),
    ("danger", "Metronidazole + Alcohol",                     "🔴 Dangerous", "Severe reaction. No alcohol during or 48hrs after."),
    ("danger", "Rifampicin + Oral Contraceptives",            "🔴 Dangerous", "TB drug makes contraceptives fail. Use condoms."),
    ("warn",   "Paracetamol + Ibuprofen",                     "🟡 Caution",   "Short-term OK. Avoid in liver/kidney disease."),
    ("warn",   "Ciprofloxacin + Antacids",                    "🟠 Moderate",  "Antacids block absorption. Separate by 2+ hours."),
    ("danger", "Septrin (Cotrimoxazole) + Warfarin",          "🔴 Dangerous", "Greatly increases bleeding risk. Avoid."),
    ("danger", "Diazepam + Alcohol",                          "🔴 Dangerous", "Risk of coma and breathing failure."),
]

for cls, name, label, note in combos:
    pill_cls = f"pill-{cls}"
    st.markdown(f"""
<div class="combo-row">
  <span class="{pill_cls}">{label}</span> <strong>{name}</strong>
  <div class="combo-note">{note}</div>
</div>""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — Drug Photo
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="section-card">
  <div class="section-title"><span class="step-badge">3</span>Send drug photo to pharmacist</div>
  <div class="section-desc">Upload a photo of your drug pack or label. We'll prepare a WhatsApp message with your details for the pharmacist to review.</div>
</div>
""", unsafe_allow_html=True)

uploaded_file  = st.file_uploader("Upload drug image", type=["jpg","jpeg","png","webp"])
client_name3   = st.text_input("Your name", placeholder="e.g. Chukwuemeka Eze", key="cn3")
client_phone   = st.text_input("Your phone number (optional)", placeholder="e.g. 08012345678")
client_concern = st.text_area("Your question or concern", placeholder="e.g. Is this safe for my 4-year-old? Can I take it with Paracetamol?", height=90)

if uploaded_file:
    st.image(uploaded_file, caption=uploaded_file.name, use_column_width=True)

if st.button("📲 Prepare WhatsApp message", use_container_width=True, disabled=uploaded_file is None):
    if not client_concern.strip():
        st.warning("Please describe your concern before sending.")
    else:
        ts  = datetime.now().strftime("%d %b %Y, %H:%M")
        msg = f"""💊 *DRUG PHOTO ENQUIRY — Nigeria Drug Checker*\n🕐 {ts}\n\n👤 *Client:* {client_name3.strip() or 'Anonymous'}\n📞 *Phone:* {client_phone.strip() or 'Not provided'}\n\n❓ *Concern:*\n{client_concern.strip()}\n\n📸 *Image:* {uploaded_file.name}\n_(Client will attach the photo in this chat)_\n\n_Please review and advise. Sent via Nigeria Drug Checker_"""
        url = f"https://wa.me/{PHARMACIST_WHATSAPP}?text={urllib.parse.quote(msg)}"
        st.markdown(f"""<div class="result-info">✅ Message ready! Click below to open WhatsApp, then tap the 📎 attach button to send the drug photo in the same chat.</div>""", unsafe_allow_html=True)
        st.markdown(f'<a class="wa-btn" href="{url}" target="_blank">📲 Open WhatsApp & send to pharmacist</a>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — Review
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="section-card">
  <div class="section-title"><span class="step-badge">4</span>Leave a review for the pharmacist</div>
  <div class="section-desc">Your review goes straight to the pharmacist on WhatsApp.</div>
</div>
""", unsafe_allow_html=True)

reviewer_name = st.text_input("Your name", placeholder="e.g. Adaeze Okonkwo", key="rn")
rating = st.select_slider("Rating", options=["⭐ Very poor","⭐⭐ Poor","⭐⭐⭐ OK","⭐⭐⭐⭐ Good","⭐⭐⭐⭐⭐ Excellent"], value="⭐⭐⭐⭐⭐ Excellent")
review_text = st.text_area("Your review", placeholder="Tell the pharmacist about your experience…", height=90, key="rt")

if st.button("📲 Send review to pharmacist", use_container_width=True):
    if not review_text.strip():
        st.warning("Please write your review before sending.")
    else:
        ts  = datetime.now().strftime("%d %b %Y, %H:%M")
        msg = f"""💬 *CLIENT REVIEW — Nigeria Drug Checker*\n🕐 {ts}\n\n👤 *From:* {reviewer_name.strip() or 'Anonymous'}\n{rating}\n\n📝 *Review:*\n{review_text.strip()}\n\n_Sent via Nigeria Drug Checker_"""
        url = f"https://wa.me/{PHARMACIST_WHATSAPP}?text={urllib.parse.quote(msg)}"
        st.success("Review ready!")
        st.markdown(f'<a class="wa-btn" href="{url}" target="_blank">📲 Send review on WhatsApp</a>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""<div style="text-align:center;color:#9ca3af;font-size:0.78rem;padding-bottom:1rem">
💊 Nigeria Drug Checker &nbsp;·&nbsp; Free · No AI · No data stored<br>
Not a substitute for professional medical advice. Always consult your pharmacist.
</div>""", unsafe_allow_html=True)
