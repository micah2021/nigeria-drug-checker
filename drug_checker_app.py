import streamlit as st
import urllib.parse
from datetime import datetime
import time

st.set_page_config(
    page_title="Nigeria Drug Checker",
    page_icon="💊",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════════════════════
# CONTACTS — Pharmacist & Doctor
# ══════════════════════════════════════════════════════════════════════════════
PHARMACIST_WHATSAPP = "234811938985"    # +234811938985
DOCTOR_WHATSAPP     = "2349064815363"   # +2349064815363

# ══════════════════════════════════════════════════════════════════════════════
# ✏️  ADVERTS — MCAIS is first (always shown), others rotate after
# ══════════════════════════════════════════════════════════════════════════════
ADVERTS = [
    {
        "name":     "MCAIS",
        "tagline":  "Your trusted health technology partner in Nigeria. Connecting patients, pharmacists & doctors seamlessly.",
        "whatsapp": "2349064815363",
        "cta":      "Contact MCAIS",
        "label":    "Official Partner",
        "color":    "blue",
        "emoji":    "🏥",
    },
    {
        "name":     "Emeka Pharmacy & Stores",
        "tagline":  "NAFDAC-certified drugs at the best prices in Lagos. Wholesale & retail available.",
        "whatsapp": "2348011111111",   # ← swap with real advertiser number
        "cta":      "Order on WhatsApp",
        "label":    "Verified Supplier",
        "color":    "green",
        "emoji":    "🏪",
    },
    {
        "name":     "HealthPlus Drug Warehouse",
        "tagline":  "Genuine medications delivered to your door across Nigeria. Fast & reliable.",
        "whatsapp": "2348022222222",   # ← swap with real advertiser number
        "cta":      "Chat with us",
        "label":    "Featured Partner",
        "color":    "orange",
        "emoji":    "🚚",
    },
]

# MCAIS always shows first on load, others rotate every 30s after
slot  = int(time.time() // 30) % len(ADVERTS)
advert = ADVERTS[slot]

COLOR_MAP = {
    "blue":   {"bg":"#eff6ff","border":"#2563eb","label_bg":"#2563eb","label_fg":"#ffffff","cta_bg":"#2563eb","cta_fg":"#ffffff","name_fg":"#1e3a8a","tag_fg":"#1e40af"},
    "green":  {"bg":"#f0fdf4","border":"#16a34a","label_bg":"#16a34a","label_fg":"#ffffff","cta_bg":"#16a34a","cta_fg":"#ffffff","name_fg":"#14532d","tag_fg":"#166534"},
    "orange": {"bg":"#fff7ed","border":"#ea580c","label_bg":"#ea580c","label_fg":"#ffffff","cta_bg":"#ea580c","cta_fg":"#ffffff","name_fg":"#7c2d12","tag_fg":"#9a3412"},
    "purple": {"bg":"#faf5ff","border":"#7c3aed","label_bg":"#7c3aed","label_fg":"#ffffff","cta_bg":"#7c3aed","cta_fg":"#ffffff","name_fg":"#3b0764","tag_fg":"#5b21b6"},
}
c = COLOR_MAP[advert["color"]]
wa_ad_url = f"https://wa.me/{advert['whatsapp']}?text={urllib.parse.quote('Hello MCAIS, I saw your advert on Nigeria Drug Checker. I would like to learn more.')}"

# ══════════════════════════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #f5f7fa !important; color: #1a1a2e !important; }
    .stApp { background: #f5f7fa; }

    .app-header { background:white; border-radius:16px; padding:1.5rem 2rem; margin-bottom:1rem; border:1px solid #e8ecf0; display:flex; align-items:center; gap:1rem; }
    .app-header h1 { margin:0; font-size:1.35rem; font-weight:700; color:#1a1a2e; }
    .app-header p  { margin:2px 0 0; font-size:0.82rem; color:#6b7280; }
    .icon-wrap { width:52px; height:52px; background:#e8f4fd; border-radius:14px; display:flex; align-items:center; justify-content:center; font-size:1.6rem; }

    .section-title { font-size:0.72rem; font-weight:700; letter-spacing:0.08em; text-transform:uppercase; color:#2563eb; margin-bottom:0.3rem; }
    .section-desc  { font-size:0.85rem; color:#6b7280; margin-bottom:1rem; line-height:1.5; }
    .step-badge { display:inline-flex; align-items:center; justify-content:center; width:20px; height:20px; background:#2563eb; color:white; border-radius:50%; font-size:0.7rem; font-weight:700; margin-right:6px; vertical-align:middle; }

    .result-safe   { background:#f0fdf4; border-left:4px solid #16a34a; border-radius:0 10px 10px 0; padding:1rem 1.25rem; margin:.75rem 0; color:#14532d; font-size:.9rem; line-height:1.7; white-space:pre-wrap; }
    .result-warn   { background:#fffbeb; border-left:4px solid #d97706; border-radius:0 10px 10px 0; padding:1rem 1.25rem; margin:.75rem 0; color:#78350f; font-size:.9rem; line-height:1.7; white-space:pre-wrap; }
    .result-danger { background:#fef2f2; border-left:4px solid #dc2626; border-radius:0 10px 10px 0; padding:1rem 1.25rem; margin:.75rem 0; color:#7f1d1d; font-size:.9rem; line-height:1.7; white-space:pre-wrap; }
    .result-info   { background:#eff6ff; border-left:4px solid #2563eb; border-radius:0 10px 10px 0; padding:1rem 1.25rem; margin:.75rem 0; color:#1e3a8a; font-size:.9rem; line-height:1.6; }

    .contact-card { background:white; border:1px solid #e8ecf0; border-radius:12px; padding:1rem 1.25rem; display:flex; align-items:center; justify-content:space-between; gap:1rem; flex-wrap:wrap; margin-bottom:0.75rem; }
    .contact-info h4 { margin:0 0 2px; font-size:14px; font-weight:600; color:#1a1a2e; }
    .contact-info p  { margin:0; font-size:12px; color:#6b7280; }

    .wa-btn { display:inline-block; background:#25d366; color:#fff !important; font-weight:600; padding:.6rem 1.3rem; border-radius:50px; text-decoration:none !important; font-size:.88rem; }
    .wa-btn:hover { background:#1ebe5d; }
    .doc-btn { display:inline-block; background:#2563eb; color:#fff !important; font-weight:600; padding:.6rem 1.3rem; border-radius:50px; text-decoration:none !important; font-size:.88rem; }

    .pill-safe   { display:inline-block; background:#dcfce7; color:#15803d; padding:3px 10px; border-radius:20px; font-size:.75rem; font-weight:600; margin-right:6px; }
    .pill-warn   { display:inline-block; background:#fef9c3; color:#a16207; padding:3px 10px; border-radius:20px; font-size:.75rem; font-weight:600; margin-right:6px; }
    .pill-danger { display:inline-block; background:#fee2e2; color:#b91c1c; padding:3px 10px; border-radius:20px; font-size:.75rem; font-weight:600; margin-right:6px; }
    .combo-row { padding:.7rem 0; border-bottom:1px solid #f0f0f0; font-size:.88rem; color:#374151; }
    .combo-row:last-child { border-bottom:none; }
    .combo-note { font-size:.8rem; color:#6b7280; margin-top:2px; }

    .stTextInput > div > div > input    { background:#f9fafb !important; border:1px solid #e5e7eb !important; border-radius:8px !important; color:#1a1a2e !important; }
    .stTextArea  > div > div > textarea { background:#f9fafb !important; border:1px solid #e5e7eb !important; border-radius:8px !important; color:#1a1a2e !important; }
    .stButton > button { background:#2563eb !important; color:white !important; border:none !important; border-radius:10px !important; font-weight:600 !important; padding:.6rem 1rem !important; }
    .stButton > button:hover    { background:#1d4ed8 !important; }
    .stButton > button:disabled { background:#9ca3af !important; }

    footer { visibility:hidden; }
    #MainMenu { visibility:hidden; }
    header { visibility:hidden; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="app-header">
  <div class="icon-wrap">💊</div>
  <div>
    <h1>Nigeria Drug Checker</h1>
    <p>Drug interactions · Photo enquiries · Reviews — contact your pharmacist or doctor via WhatsApp</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# MCAIS ADVERT BANNER (rotates with other adverts every 30s)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div style="
    background:{c['bg']};
    border:2px solid {c['border']};
    border-radius:14px;
    padding:1rem 1.25rem;
    margin-bottom:1.25rem;
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:1rem;
    flex-wrap:wrap;
">
  <div style="display:flex;align-items:center;gap:12px;flex:1;min-width:200px">
    <div style="width:46px;height:46px;border-radius:12px;background:{c['border']};display:flex;align-items:center;justify-content:center;font-size:1.4rem;flex-shrink:0">{advert['emoji']}</div>
    <div>
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:3px">
        <span style="font-size:15px;font-weight:700;color:{c['name_fg']}">{advert['name']}</span>
        <span style="background:{c['label_bg']};color:{c['label_fg']};font-size:10px;font-weight:600;padding:2px 9px;border-radius:20px">{advert['label']}</span>
      </div>
      <div style="font-size:12px;color:{c['tag_fg']};line-height:1.5">{advert['tagline']}</div>
    </div>
  </div>
  <div style="display:flex;flex-direction:column;align-items:flex-end;gap:4px;flex-shrink:0">
    <a href="{wa_ad_url}" target="_blank" style="
        display:inline-block;background:{c['cta_bg']};color:{c['cta_fg']} !important;
        font-weight:600;font-size:13px;padding:8px 18px;border-radius:50px;
        text-decoration:none;white-space:nowrap;
    ">📲 {advert['cta']}</a>
    <span style="font-size:10px;color:#9ca3af">Sponsored · Advertise here</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# INTERACTION DATABASE
# ══════════════════════════════════════════════════════════════════════════════
INTERACTIONS = {
    frozenset({"amoxicillin","metronidazole"}):     ("Moderate","Common for H. pylori and dental infections. Mild GI side effects possible. Generally acceptable.","Take with food. Monitor for nausea."),
    frozenset({"metformin","alcohol"}):             ("Severe","Significantly increases risk of lactic acidosis — dangerous build-up of lactic acid.","Avoid alcohol completely. Urgent pharmacist review if patient drinks regularly."),
    frozenset({"warfarin","aspirin"}):              ("Severe","Both thin the blood. Greatly increases internal bleeding risk.","Do NOT combine without specialist supervision. Refer to doctor immediately."),
    frozenset({"artemether","lumefantrine"}):       ("None","Standard fixed-dose combination (Coartem/ALu) — designed to be taken together for malaria.","Safe as prescribed. Standard Nigerian malaria treatment."),
    frozenset({"paracetamol","ibuprofen"}):         ("Low","Can be safely alternated short-term. Different mechanisms.","Safe short-term. Avoid in liver/kidney disease. Don't exceed recommended doses."),
    frozenset({"ciprofloxacin","antacid"}):         ("Moderate","Antacids reduce Ciprofloxacin absorption by up to 90% — antibiotic becomes ineffective.","Take Ciprofloxacin at least 2 hours before or 6 hours after any antacid."),
    frozenset({"lisinopril","potassium"}):          ("Moderate","ACE inhibitors raise blood potassium. Adding supplements risks dangerous hyperkalaemia.","Avoid potassium supplements unless prescribed. Monitor potassium levels."),
    frozenset({"diazepam","alcohol"}):              ("Severe","Both suppress the CNS. Dangerously suppress breathing — risk of coma and death.","Never combine. Counsel patient urgently."),
    frozenset({"amlodipine","simvastatin"}):        ("Moderate","Amlodipine raises Simvastatin levels — increases risk of muscle damage.","Limit Simvastatin to 20mg/day. Consider switching to Atorvastatin."),
    frozenset({"metronidazole","alcohol"}):         ("Severe","Severe disulfiram-like reaction — vomiting, flushing, palpitations. Very common mistake in Nigeria.","Avoid alcohol during treatment and 48 hours after finishing."),
    frozenset({"cotrimoxazole","warfarin"}):        ("Severe","Septrin greatly potentiates Warfarin — drastically increases bleeding risk.","Avoid. If essential, reduce Warfarin dose and monitor INR closely."),
    frozenset({"tramadol","ssri"}):                 ("Severe","Risk of serotonin syndrome — agitation, rapid heart rate, muscle twitching. Can be fatal.","Avoid. Refer to doctor. Flag urgently if patient is on antidepressants."),
    frozenset({"aspirin","ibuprofen"}):             ("Moderate","Both NSAIDs. Increases GI bleeding risk. Ibuprofen blocks aspirin's cardioprotective effect.","Avoid. If needed, take aspirin 30 mins before Ibuprofen."),
    frozenset({"chloroquine","antacid"}):           ("Moderate","Antacids reduce Chloroquine absorption — less effective malaria treatment.","Separate doses by at least 4 hours."),
    frozenset({"rifampicin","oral contraceptive"}): ("Severe","Rifampicin drastically reduces contraceptive effectiveness — high pregnancy risk.","Use condoms throughout TB treatment and 4 weeks after."),
}

def check_interaction(d1, d2):
    return INTERACTIONS.get(frozenset({d1.lower().strip(), d2.lower().strip()}), None)
def sev_cls(s):  return "danger" if s=="Severe" else "warn" if s in ("Moderate","Low") else "safe"
def sev_icon(s): return "🔴" if s=="Severe" else "🟠" if s=="Moderate" else "🟡" if s=="Low" else "🟢"

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — Drug Interaction Checker
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div style="background:white;border-radius:14px;padding:1.4rem 1.6rem;margin-bottom:1.25rem;border:1px solid #e8ecf0">
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
            cls = sev_cls(severity); icon = sev_icon(severity)
            st.markdown(f"""<div class="result-{cls}">
{icon} <strong>Severity: {severity}</strong>

📋 <strong>Interaction:</strong>
{explanation}

✅ <strong>Recommended action:</strong>
{action}
</div>""", unsafe_allow_html=True)
            ts  = datetime.now().strftime("%d %b %Y, %H:%M")
            msg = f"💊 *DRUG INTERACTION — Nigeria Drug Checker*\n🕐 {ts}\n\n👤 *Client:* {client_name1 or 'Anonymous'}\n💊 *Drug 1:* {drug1}\n💊 *Drug 2:* {drug2}\n🏥 *Condition:* {condition or 'Not specified'}\n\n⚠️ *Severity:* {severity}\n\n📋 *Interaction:*\n{explanation}\n\n✅ *Action:*\n{action}\n\n_Sent via Nigeria Drug Checker_"

            col_p, col_d = st.columns(2)
            with col_p:
                url_p = f"https://wa.me/{PHARMACIST_WHATSAPP}?text={urllib.parse.quote(msg)}"
                st.markdown(f'<a class="wa-btn" href="{url_p}" target="_blank">💊 Send to Pharmacist</a>', unsafe_allow_html=True)
            with col_d:
                url_d = f"https://wa.me/{DOCTOR_WHATSAPP}?text={urllib.parse.quote(msg)}"
                st.markdown(f'<a class="doc-btn" href="{url_d}" target="_blank">🩺 Send to Doctor</a>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="result-warn">🟡 <strong>Not in database</strong><br><br><strong>{drug1}</strong> + <strong>{drug2}</strong> is not in our local database. This does not mean it is safe — ask the pharmacist or doctor to verify.</div>', unsafe_allow_html=True)
            ts  = datetime.now().strftime("%d %b %Y, %H:%M")
            msg = f"💊 *DRUG QUERY — Nigeria Drug Checker*\n🕐 {ts}\n\n👤 *Client:* {client_name1 or 'Anonymous'}\n💊 *Drug 1:* {drug1}\n💊 *Drug 2:* {drug2}\n🏥 *Condition:* {condition or 'Not specified'}\n\n⚠️ Combination NOT in local database. Please advise.\n\n_Sent via Nigeria Drug Checker_"
            col_p, col_d = st.columns(2)
            with col_p:
                url_p = f"https://wa.me/{PHARMACIST_WHATSAPP}?text={urllib.parse.quote(msg)}"
                st.markdown(f'<a class="wa-btn" href="{url_p}" target="_blank">💊 Ask Pharmacist</a>', unsafe_allow_html=True)
            with col_d:
                url_d = f"https://wa.me/{DOCTOR_WHATSAPP}?text={urllib.parse.quote(msg)}"
                st.markdown(f'<a class="doc-btn" href="{url_d}" target="_blank">🩺 Ask Doctor</a>', unsafe_allow_html=True)
    else:
        st.warning("Please enter both drug names.")

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — Quick Reference
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div style="background:white;border-radius:14px;padding:1.4rem 1.6rem;margin-bottom:1.25rem;border:1px solid #e8ecf0">
  <div class="section-title"><span class="step-badge">2</span>Common Nigerian drug combinations</div>
  <div class="section-desc">Quick reference for the most important drug pairs in Nigerian clinical practice.</div>
""", unsafe_allow_html=True)

combos = [
    ("safe",   "Artemether + Lumefantrine (Coartem)",  "✅ Safe",      "Standard malaria treatment. Take with food."),
    ("danger", "Metronidazole + Alcohol",              "🔴 Dangerous", "Severe reaction. No alcohol during or 48hrs after."),
    ("danger", "Rifampicin + Oral Contraceptives",     "🔴 Dangerous", "TB drug makes contraceptives fail. Use condoms."),
    ("warn",   "Paracetamol + Ibuprofen",              "🟡 Caution",   "Short-term OK. Avoid in liver/kidney disease."),
    ("warn",   "Ciprofloxacin + Antacids",             "🟠 Moderate",  "Antacids block absorption. Separate by 2+ hours."),
    ("danger", "Septrin (Cotrimoxazole) + Warfarin",   "🔴 Dangerous", "Greatly increases bleeding risk. Avoid."),
    ("danger", "Diazepam + Alcohol",                   "🔴 Dangerous", "Risk of coma and breathing failure."),
]
for cls, name, label, note in combos:
    st.markdown(f'<div class="combo-row"><span class="pill-{cls}">{label}</span> <strong>{name}</strong><div class="combo-note">{note}</div></div>', unsafe_allow_html=True)
st.markdown("</div><br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — Drug Photo
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div style="background:white;border-radius:14px;padding:1.4rem 1.6rem;margin-bottom:1.25rem;border:1px solid #e8ecf0">
  <div class="section-title"><span class="step-badge">3</span>Send drug photo to pharmacist or doctor</div>
  <div class="section-desc">Upload a photo of your drug pack or label. We'll prepare a WhatsApp message for the pharmacist or doctor to review.</div>
</div>
""", unsafe_allow_html=True)

uploaded_file  = st.file_uploader("Upload drug image", type=["jpg","jpeg","png","webp"])
client_name3   = st.text_input("Your name", placeholder="e.g. Chukwuemeka Eze", key="cn3")
client_phone   = st.text_input("Your phone number (optional)", placeholder="e.g. 08012345678")
client_concern = st.text_area("Your question or concern", placeholder="e.g. Is this safe for my 4-year-old?", height=90)

if uploaded_file:
    st.image(uploaded_file, caption=uploaded_file.name, use_column_width=True)

if st.button("📲 Prepare WhatsApp message", use_container_width=True, disabled=uploaded_file is None):
    if not client_concern.strip():
        st.warning("Please describe your concern before sending.")
    else:
        ts  = datetime.now().strftime("%d %b %Y, %H:%M")
        msg = f"💊 *DRUG PHOTO ENQUIRY — Nigeria Drug Checker*\n🕐 {ts}\n\n👤 *Client:* {client_name3.strip() or 'Anonymous'}\n📞 *Phone:* {client_phone.strip() or 'Not provided'}\n\n❓ *Concern:*\n{client_concern.strip()}\n\n📸 *Image:* {uploaded_file.name}\n_(Client will attach the photo in this chat)_\n\n_Please review and advise. Sent via Nigeria Drug Checker_"
        st.markdown('<div class="result-info">✅ Message ready! Choose who to send it to, then tap 📎 in WhatsApp to attach the drug photo too.</div>', unsafe_allow_html=True)
        col_p, col_d = st.columns(2)
        with col_p:
            url_p = f"https://wa.me/{PHARMACIST_WHATSAPP}?text={urllib.parse.quote(msg)}"
            st.markdown(f'<a class="wa-btn" href="{url_p}" target="_blank">💊 Send to Pharmacist</a>', unsafe_allow_html=True)
        with col_d:
            url_d = f"https://wa.me/{DOCTOR_WHATSAPP}?text={urllib.parse.quote(msg)}"
            st.markdown(f'<a class="doc-btn" href="{url_d}" target="_blank">🩺 Send to Doctor</a>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — Contact cards
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div style="background:white;border-radius:14px;padding:1.4rem 1.6rem;margin-bottom:1.25rem;border:1px solid #e8ecf0">
  <div class="section-title"><span class="step-badge">4</span>Contact our pharmacist or doctor directly</div>
  <div class="section-desc">Have a general question? Reach out directly on WhatsApp.</div>
""", unsafe_allow_html=True)

ph_url  = f"https://wa.me/{PHARMACIST_WHATSAPP}?text={urllib.parse.quote('Hello, I have a drug question from Nigeria Drug Checker.')}"
doc_url = f"https://wa.me/{DOCTOR_WHATSAPP}?text={urllib.parse.quote('Hello Doctor, I have a medical question from Nigeria Drug Checker.')}"

st.markdown(f"""
<div class="contact-card">
  <div style="display:flex;align-items:center;gap:12px">
    <div style="width:42px;height:42px;background:#f0fdf4;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:1.3rem">💊</div>
    <div class="contact-info">
      <h4>Pharmacist</h4>
      <p>Drug queries · Dosage advice · Prescription checks</p>
    </div>
  </div>
  <a class="wa-btn" href="{ph_url}" target="_blank">📲 Chat on WhatsApp</a>
</div>

<div class="contact-card">
  <div style="display:flex;align-items:center;gap:12px">
    <div style="width:42px;height:42px;background:#eff6ff;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:1.3rem">🩺</div>
    <div class="contact-info">
      <h4>Doctor</h4>
      <p>Medical advice · Severe reactions · Urgent concerns</p>
    </div>
  </div>
  <a class="doc-btn" href="{doc_url}" target="_blank">📲 Chat on WhatsApp</a>
</div>
""", unsafe_allow_html=True)

st.markdown("</div><br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 5 — Reviews
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div style="background:white;border-radius:14px;padding:1.4rem 1.6rem;margin-bottom:1.25rem;border:1px solid #e8ecf0">
  <div class="section-title"><span class="step-badge">5</span>Leave a review</div>
  <div class="section-desc">Your review goes straight to the pharmacist on WhatsApp.</div>
</div>
""", unsafe_allow_html=True)

reviewer_name = st.text_input("Your name", placeholder="e.g. Adaeze Okonkwo", key="rn")
rating        = st.select_slider("Rating", options=["⭐ Very poor","⭐⭐ Poor","⭐⭐⭐ OK","⭐⭐⭐⭐ Good","⭐⭐⭐⭐⭐ Excellent"], value="⭐⭐⭐⭐⭐ Excellent")
review_text   = st.text_area("Your review", placeholder="Tell us about your experience…", height=90, key="rt")

if st.button("📲 Send review", use_container_width=True):
    if not review_text.strip():
        st.warning("Please write your review before sending.")
    else:
        ts  = datetime.now().strftime("%d %b %Y, %H:%M")
        msg = f"💬 *CLIENT REVIEW — Nigeria Drug Checker*\n🕐 {ts}\n\n👤 *From:* {reviewer_name.strip() or 'Anonymous'}\n{rating}\n\n📝 *Review:*\n{review_text.strip()}\n\n_Sent via Nigeria Drug Checker_"
        url = f"https://wa.me/{PHARMACIST_WHATSAPP}?text={urllib.parse.quote(msg)}"
        st.success("Review ready!")
        st.markdown(f'<a class="wa-btn" href="{url}" target="_blank">📲 Send review on WhatsApp</a>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""<div style="text-align:center;color:#9ca3af;font-size:0.78rem;padding-bottom:1rem">
💊 Nigeria Drug Checker &nbsp;·&nbsp; Powered by MCAIS &nbsp;·&nbsp; Free · No data stored<br>
Not a substitute for professional medical advice. Always consult your pharmacist or doctor.
</div>""", unsafe_allow_html=True)
