import streamlit as st
import urllib.parse
from datetime import datetime

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nigeria Drug Checker",
    page_icon="💊",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Constants ─────────────────────────────────────────────────────────────────
PHARMACIST_WHATSAPP = "2348012345678"   # ← replace with real Nigerian number (no +)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');
    html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; }
    .stApp { background: #0f1117; color: #e8e8e8; }
    h1, h2, h3 { font-family: 'IBM Plex Mono', monospace; }

    .header-bar {
        background: #00c853; color: #0a0a0a;
        padding: 1rem 1.5rem; border-radius: 8px; margin-bottom: 1.5rem;
    }
    .header-bar h1 { margin: 0; font-size: 1.3rem; color: #0a0a0a; }
    .header-bar p  { margin: 0; font-size: 0.8rem; opacity: 0.75; }

    .section-label {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.7rem; letter-spacing: 0.1em;
        color: #00c853; text-transform: uppercase; margin-bottom: 0.5rem;
    }
    .step-num {
        display: inline-block; background: #00c853; color: #000;
        font-family: 'IBM Plex Mono', monospace; font-size: 0.75rem;
        font-weight: 600; width: 22px; height: 22px; border-radius: 50%;
        text-align: center; line-height: 22px; margin-right: 8px;
    }

    .result-box {
        background: #1a1d27; border: 1px solid #2a2d3a;
        border-left: 3px solid #00c853; border-radius: 0 8px 8px 0;
        padding: 1rem 1.25rem; margin: 0.75rem 0;
        font-size: 0.9rem; line-height: 1.7; white-space: pre-wrap;
    }
    .result-box.warn   { border-left-color: #ff9800; }
    .result-box.danger { border-left-color: #f44336; }
    .result-box.safe   { border-left-color: #00c853; }

    .info-box {
        background: #1a1d27; border: 1px solid #2a2d3a;
        border-left: 3px solid #00c853; border-radius: 0 8px 8px 0;
        padding: 1rem 1.25rem; margin: 0.75rem 0; font-size: 0.9rem; line-height: 1.6;
    }

    .wa-btn {
        display: inline-block; background: #25d366; color: #000 !important;
        font-weight: 600; padding: 0.7rem 1.6rem; border-radius: 50px;
        text-decoration: none !important; font-size: 0.95rem; margin-top: 0.75rem;
    }
    .wa-btn:hover { opacity: 0.85; }

    .divider { border: none; border-top: 1px solid #2a2d3a; margin: 1.5rem 0; }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-bar">
  <span style="font-size:1.8rem">💊</span>
  <div>
    <h1>Nigeria Drug Checker</h1>
    <p>Drug interactions · Photo enquiries · Reviews — all sent to your pharmacist via WhatsApp</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# BUILT-IN DRUG INTERACTION DATABASE (no AI needed)
# ══════════════════════════════════════════════════════════════════════════════
INTERACTIONS = {
    # format: frozenset({drug_a, drug_b}): (severity, explanation, action)
    frozenset({"amoxicillin", "metronidazole"}): (
        "Moderate", 
        "Combining these two antibiotics is common in Nigeria for H. pylori and dental infections. Mild risk of increased GI side effects (nausea, vomiting). No major danger.",
        "Monitor for nausea. Take with food. Common combination — generally acceptable."
    ),
    frozenset({"metformin", "alcohol"}): (
        "Severe",
        "Alcohol combined with Metformin significantly increases the risk of lactic acidosis — a dangerous build-up of lactic acid in the blood. Very dangerous.",
        "Avoid alcohol completely while taking Metformin. Urgent pharmacist review if patient drinks regularly."
    ),
    frozenset({"warfarin", "aspirin"}): (
        "Severe",
        "Both drugs thin the blood. Combining them greatly increases bleeding risk — internal bleeding, stroke complications.",
        "Do NOT combine without specialist supervision. Refer to doctor immediately."
    ),
    frozenset({"artemether", "lumefantrine"}): (
        "None",
        "This is a standard fixed-dose combination (Coartem/ALu) — the two drugs are designed to be taken together for malaria treatment in Nigeria.",
        "Safe to use together as prescribed. Standard malaria treatment."
    ),
    frozenset({"paracetamol", "ibuprofen"}): (
        "Low",
        "These two can be safely alternated or combined short-term for pain/fever. Different mechanisms — Paracetamol is liver-processed, Ibuprofen is anti-inflammatory.",
        "Safe for short-term use. Avoid in patients with liver or kidney disease. Do not exceed recommended doses."
    ),
    frozenset({"ciprofloxacin", "antacid"}): (
        "Moderate",
        "Antacids containing magnesium or aluminium (e.g. Milk of Magnesia, Gaviscon) reduce Ciprofloxacin absorption by up to 90%, making the antibiotic ineffective.",
        "Take Ciprofloxacin at least 2 hours before or 6 hours after any antacid."
    ),
    frozenset({"lisinopril", "potassium"}): (
        "Moderate",
        "ACE inhibitors like Lisinopril raise blood potassium levels. Adding potassium supplements can cause dangerously high potassium (hyperkalaemia) — risk of heart arrhythmia.",
        "Avoid potassium supplements unless prescribed. Monitor potassium levels regularly."
    ),
    frozenset({"diazepam", "alcohol"}): (
        "Severe",
        "Both are CNS depressants. Combined, they dangerously suppress breathing and consciousness. Risk of coma and death.",
        "Never combine. Urgent warning to patient. Pharmacist must counsel strongly."
    ),
    frozenset({"amlodipine", "simvastatin"}): (
        "Moderate",
        "Amlodipine raises Simvastatin blood levels, increasing risk of muscle damage (myopathy/rhabdomyolysis).",
        "Limit Simvastatin dose to 20mg/day if taking Amlodipine. Consider switching to Atorvastatin."
    ),
    frozenset({"metronidazole", "alcohol"}): (
        "Severe",
        "Causes a dangerous disulfiram-like reaction — severe nausea, vomiting, flushing, palpitations, headache. Very common mistake in Nigeria.",
        "Strictly avoid alcohol during Metronidazole treatment and for 48 hours after finishing."
    ),
    frozenset({"cotrimoxazole", "warfarin"}): (
        "Severe",
        "Cotrimoxazole (Septrin) significantly potentiates Warfarin — drastically increases bleeding risk.",
        "Avoid combination. If essential, reduce Warfarin dose and monitor INR very closely."
    ),
    frozenset({"tramadol", "ssri"}): (
        "Severe",
        "Risk of serotonin syndrome — agitation, confusion, rapid heart rate, high blood pressure, muscle twitching. Can be fatal.",
        "Avoid combination. Refer to doctor. If patient is on antidepressants, flag urgently."
    ),
    frozenset({"aspirin", "ibuprofen"}): (
        "Moderate",
        "Both are NSAIDs. Combining increases risk of stomach ulcers and GI bleeding. Ibuprofen can also block aspirin's cardioprotective effect.",
        "Avoid combining. If patient needs both, take aspirin 30 mins before Ibuprofen."
    ),
    frozenset({"chloroquine", "antacid"}): (
        "Moderate",
        "Antacids reduce Chloroquine absorption. Less effective malaria or lupus treatment.",
        "Separate doses by at least 4 hours."
    ),
    frozenset({"rifampicin", "oral contraceptive"}): (
        "Severe",
        "Rifampicin (TB drug) dramatically reduces effectiveness of oral contraceptives — high risk of unintended pregnancy.",
        "Use additional contraception (condoms) throughout TB treatment and for 4 weeks after. Counsel patient clearly."
    ),
}

def check_interaction(drug1: str, drug2: str):
    """Look up interaction between two drugs. Returns (severity, explanation, action) or None."""
    key = frozenset({drug1.lower().strip(), drug2.lower().strip()})
    return INTERACTIONS.get(key, None)

def severity_class(severity: str) -> str:
    if severity == "Severe": return "danger"
    if severity in ("Moderate", "Low"): return "warn"
    return "safe"

def build_wa_interaction(drug1, drug2, condition, severity, explanation, action, client_name=""):
    timestamp = datetime.now().strftime("%d %b %Y, %H:%M")
    return f"""💊 *DRUG INTERACTION QUERY — Nigeria Drug Checker*
🕐 {timestamp}

👤 *Client:* {client_name or 'Anonymous'}
💊 *Drug 1:* {drug1}
💊 *Drug 2:* {drug2}
🏥 *Condition:* {condition or 'Not specified'}

⚠️ *Severity:* {severity}

📋 *Interaction:*
{explanation}

✅ *Recommended Action:*
{action}

─────────────────────────
_Sent via Nigeria Drug Checker_"""

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — Drug Interaction Checker
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-label"><span class="step-num">1</span> Drug interaction checker</div>', unsafe_allow_html=True)
st.caption("Check if two drugs are safe to take together. Results are based on a built-in Nigerian clinical database — no internet or AI needed.")

col1, col2 = st.columns(2)
with col1:
    drug1 = st.text_input("Drug 1", placeholder="e.g. Metronidazole")
with col2:
    drug2 = st.text_input("Drug 2", placeholder="e.g. Alcohol")

condition   = st.text_input("Patient condition (optional)", placeholder="e.g. malaria, TB, pregnant, hypertension")
client_name_1 = st.text_input("Client name (optional)", placeholder="e.g. Emeka Obi", key="cn1")

if st.button("Check interaction", use_container_width=True):
    if drug1.strip() and drug2.strip():
        result = check_interaction(drug1, drug2)

        if result:
            severity, explanation, action = result
            cls = severity_class(severity)
            icon = "🔴" if severity == "Severe" else "🟠" if severity == "Moderate" else "🟡" if severity == "Low" else "🟢"

            st.markdown(f"""
<div class="result-box {cls}">
{icon} <strong>Severity: {severity}</strong>

📋 <strong>Interaction:</strong>
{explanation}

✅ <strong>Action:</strong>
{action}
</div>""", unsafe_allow_html=True)

            # WhatsApp button
            wa_msg = build_wa_interaction(drug1, drug2, condition, severity, explanation, action, client_name_1)
            wa_url = f"https://wa.me/{PHARMACIST_WHATSAPP}?text={urllib.parse.quote(wa_msg)}"
            st.markdown(f'<a class="wa-btn" href="{wa_url}" target="_blank">📲 Send result to pharmacist on WhatsApp</a>', unsafe_allow_html=True)

        else:
            # Not in database — ask pharmacist
            st.markdown(f"""
<div class="result-box warn">
🟡 <strong>Not found in database</strong>

The combination of <strong>{drug1}</strong> and <strong>{drug2}</strong> is not in our local database.
This does not mean it is safe — it means the pharmacist should verify this manually.

We will prepare a WhatsApp message to ask the pharmacist directly.
</div>""", unsafe_allow_html=True)

            unknown_msg = f"""💊 *DRUG INTERACTION QUERY — Nigeria Drug Checker*
🕐 {datetime.now().strftime("%d %b %Y, %H:%M")}

👤 *Client:* {client_name_1 or 'Anonymous'}
💊 *Drug 1:* {drug1}
💊 *Drug 2:* {drug2}
🏥 *Condition:* {condition or 'Not specified'}

⚠️ This combination was NOT found in the local database.
Please advise the client whether it is safe to combine these drugs.

─────────────────────────
_Sent via Nigeria Drug Checker_"""
            wa_url = f"https://wa.me/{PHARMACIST_WHATSAPP}?text={urllib.parse.quote(unknown_msg)}"
            st.markdown(f'<a class="wa-btn" href="{wa_url}" target="_blank">📲 Ask pharmacist on WhatsApp</a>', unsafe_allow_html=True)

    else:
        st.warning("Please enter both drug names.")

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — Common Nigerian drug combos quick reference
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-label"><span class="step-num">2</span> Common Nigerian drug combinations — quick reference</div>', unsafe_allow_html=True)

combos = [
    ("Coartem (Artemether + Lumefantrine)", "✅ Safe", "safe", "Standard malaria treatment in Nigeria. Take with food."),
    ("Metronidazole + Alcohol", "🔴 Dangerous", "danger", "Severe reaction. Avoid alcohol during and 48hrs after treatment."),
    ("Rifampicin + Oral Contraceptives", "🔴 Dangerous", "danger", "TB drug makes contraceptives ineffective. Use condoms throughout."),
    ("Paracetamol + Ibuprofen", "🟡 Caution", "warn", "Short-term use OK. Avoid in liver/kidney disease."),
    ("Ciprofloxacin + Antacids", "🟠 Moderate", "warn", "Antacids block absorption. Separate by at least 2 hours."),
    ("Septrin + Warfarin", "🔴 Dangerous", "danger", "Greatly increases bleeding risk. Avoid combination."),
]

for name, label, cls, note in combos:
    st.markdown(f'<div class="result-box {cls}"><strong>{label} — {name}</strong><br><span style="opacity:0.85">{note}</span></div>', unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — Drug photo → WhatsApp
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-label"><span class="step-num">3</span> Send drug photo to pharmacist</div>', unsafe_allow_html=True)
st.caption("Upload a photo of your drug pack, tablet, or label. We'll prepare a WhatsApp message with all your details for the pharmacist to review.")

uploaded_file   = st.file_uploader("Upload drug image", type=["jpg", "jpeg", "png", "webp"])
client_name_3   = st.text_input("Your name", placeholder="e.g. Chukwuemeka Eze", key="cn3")
client_phone    = st.text_input("Your phone number (optional)", placeholder="e.g. 08012345678")
client_concern  = st.text_area("Your question or concern", placeholder="e.g. Is this drug safe for my 4-year-old? Can I take it with Paracetamol?", height=100)

if uploaded_file:
    st.image(uploaded_file, caption="Preview — " + uploaded_file.name, use_column_width=True)

if st.button("📲 Prepare WhatsApp message", use_container_width=True, disabled=uploaded_file is None):
    if not client_concern.strip():
        st.warning("Please describe your question or concern before sending.")
    else:
        wa_photo_msg = f"""💊 *DRUG PHOTO ENQUIRY — Nigeria Drug Checker*
🕐 {datetime.now().strftime("%d %b %Y, %H:%M")}

👤 *Client:* {client_name_3.strip() or 'Anonymous'}
📞 *Phone:* {client_phone.strip() or 'Not provided'}

❓ *Question/Concern:*
{client_concern.strip()}

📸 *Image file:* {uploaded_file.name}
_(Client will attach the photo in this WhatsApp chat)_

─────────────────────────
Please review the drug image and advise the client.
_Sent via Nigeria Drug Checker_"""

        wa_url = f"https://wa.me/{PHARMACIST_WHATSAPP}?text={urllib.parse.quote(wa_photo_msg)}"

        st.markdown(
            '<div class="info-box">✅ Message ready! Click below to open WhatsApp. '
            '<strong>After sending the text, tap the 📎 attach button in the same chat to send the drug photo too.</strong></div>',
            unsafe_allow_html=True,
        )
        st.markdown(f'<a class="wa-btn" href="{wa_url}" target="_blank">📲 Open WhatsApp &amp; send to pharmacist</a>', unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — Client review → WhatsApp
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-label"><span class="step-num">4</span> Leave a review for the pharmacist</div>', unsafe_allow_html=True)
st.caption("Share your experience. Your review goes straight to the pharmacist on WhatsApp.")

reviewer_name = st.text_input("Your name", placeholder="e.g. Adaeze Okonkwo", key="rev_name")
rating = st.select_slider(
    "Your rating",
    options=["⭐ Very poor", "⭐⭐ Poor", "⭐⭐⭐ OK", "⭐⭐⭐⭐ Good", "⭐⭐⭐⭐⭐ Excellent"],
    value="⭐⭐⭐⭐⭐ Excellent",
)
review_text = st.text_area("Your review", placeholder="Tell the pharmacist about your experience…", height=100, key="rev_text")

if st.button("📲 Send review to pharmacist", use_container_width=True):
    if not review_text.strip():
        st.warning("Please write your review before sending.")
    else:
        wa_review = f"""💬 *NEW CLIENT REVIEW — Nigeria Drug Checker*
🕐 {datetime.now().strftime("%d %b %Y, %H:%M")}

👤 *From:* {reviewer_name.strip() or 'Anonymous'}
{rating}

📝 *Review:*
{review_text.strip()}

─────────────────────────
_Sent via Nigeria Drug Checker_"""

        wa_url = f"https://wa.me/{PHARMACIST_WHATSAPP}?text={urllib.parse.quote(wa_review)}"
        st.success("Review ready!")
        st.markdown(f'<a class="wa-btn" href="{wa_url}" target="_blank">📲 Send review on WhatsApp</a>', unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;color:#555;font-size:0.8rem;padding-bottom:1rem">
  💊 Nigeria Drug Checker &nbsp;·&nbsp; Free to use &nbsp;·&nbsp; No AI required &nbsp;·&nbsp; No data stored<br>
  Not a substitute for professional medical advice. Always consult your pharmacist.
</div>
""", unsafe_allow_html=True)
