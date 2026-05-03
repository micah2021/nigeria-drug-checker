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

# ── MCAIS Logo (base64 embedded so it works on Streamlit Cloud) ──────────────
MCAIS_LOGO_B64 = "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AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB/9k="

# PWA — installs with MCAIS logo on home screen
st.markdown(f"""
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#2563eb">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="Nigeria Drug Checker">
<link rel="apple-touch-icon" href="data:image/png;base64,{MCAIS_LOGO_B64}">
<script>
if ('serviceWorker' in navigator) {{
  const manifest = {{
    name: 'Nigeria Drug Checker',
    short_name: 'DrugChecker',
    description: 'Check drug interactions. Powered by MCAIS.',
    start_url: window.location.href,
    display: 'standalone',
    background_color: '#f5f7fa',
    theme_color: '#2563eb',
    icons: [
      {{ src: 'data:image/png;base64,{MCAIS_LOGO_B64}', sizes: '512x512', type: 'image/png' }}
    ]
  }};
  const blob = new Blob([JSON.stringify(manifest)], {{type: 'application/manifest+json'}});
  const url = URL.createObjectURL(blob);
  const link = document.createElement('link');
  link.rel = 'manifest';
  link.href = url;
  document.head.appendChild(link);
}}
</script>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# CONTACTS — Pharmacist & Doctor
# ══════════════════════════════════════════════════════════════════════════════
PHARMACIST_WHATSAPP = "2348119389385"   # +2348119389385
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
st.markdown(f"""
<div class="app-header">
  <div class="icon-wrap" style="background:#000;padding:4px">
    <img src="data:image/png;base64,{MCAIS_LOGO_B64}" style="width:44px;height:44px;border-radius:8px;object-fit:cover">
  </div>
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
def make_interactions():
    raw = {
        # ── ANTIBIOTICS ───────────────────────────────────────────────────────
        ("amoxicillin","metronidazole"):      ("Low","Common Nigerian combination for dental infections, H. pylori and mixed bacterial infections. Generally well tolerated.","Take with food. Monitor for nausea and diarrhoea. Acceptable combination."),
        ("flagyl","amoxicillin"):             ("Low","Flagyl (Metronidazole) + Amoxicillin is a common Nigerian antibiotic pair for dental, gut and gynaecological infections. Generally safe.","Take with food. Avoid alcohol throughout course. Complete full course."),
        ("flagyl","ampiclox"):               ("Low","Common Nigerian combination. Ampicillin/Cloxacillin + Metronidazole used for mixed infections. Generally acceptable.","Take with food. Avoid alcohol. Do not exceed recommended doses."),
        ("flagyl","tetracycline"):            ("Low","Used together for H. pylori eradication in Nigeria. Acceptable short-term combination.","Take Tetracycline on empty stomach. Avoid dairy with Tetracycline. Avoid alcohol with Flagyl."),
        ("flagyl","ciprofloxacin"):           ("Low","Common combination for abdominal, pelvic and GI infections in Nigeria. Generally safe short-term.","Take with food. Avoid alcohol. Complete full antibiotic course."),
        ("flagyl","doxycycline"):             ("Low","Common for pelvic inflammatory disease (PID) and mixed infections in Nigeria. Generally acceptable.","Avoid alcohol with Flagyl. Take Doxycycline with food and plenty of water. Avoid dairy within 2hrs."),
        ("amoxicillin","clavulanate"):        ("None","Augmentin is a fixed combination — Amoxicillin + Clavulanate designed to be taken together. Standard Nigerian prescription.","Safe as prescribed. Take with food to reduce GI upset."),
        ("ampicillin","cloxacillin"):         ("None","Ampiclox is a fixed combination of Ampicillin and Cloxacillin. Designed to be taken together. Common in Nigeria.","Safe as prescribed. Complete full course."),
        ("ciprofloxacin","antacid"):          ("Moderate","Antacids (Milk of Magnesia, Gelusil) reduce Ciprofloxacin absorption by up to 90% — antibiotic becomes ineffective.","Take Ciprofloxacin at least 2 hours before or 6 hours after any antacid."),
        ("ciprofloxacin","metronidazole"):    ("Low","Common combination for abdominal, GI and urinary infections. Acceptable short-term.","Take with food. Monitor for dizziness and GI effects. Avoid alcohol with Metronidazole."),
        ("doxycycline","antacid"):            ("Moderate","Antacids, iron and dairy reduce Doxycycline absorption significantly — makes antibiotic less effective.","Take Doxycycline 2 hours before or 6 hours after antacids, iron or dairy."),
        ("cotrimoxazole","warfarin"):         ("Severe","Septrin dramatically potentiates Warfarin — drastically increases bleeding risk.","Avoid combination. If essential, reduce Warfarin dose and monitor INR very closely."),
        ("rifampicin","oral contraceptive"):  ("Severe","Rifampicin (TB drug) drastically reduces oral contraceptive effectiveness — very high unintended pregnancy risk. Very common in Nigeria.","Use condoms throughout TB treatment and for 4 weeks after stopping Rifampicin. Counsel patient clearly."),
        ("rifampicin","metformin"):           ("Moderate","Rifampicin reduces Metformin effectiveness, leading to poorer blood sugar control in TB+diabetes patients.","Monitor blood sugar more closely. Dose adjustment may be needed."),

        # ── MALARIA DRUGS ─────────────────────────────────────────────────────
        ("artemether","lumefantrine"):        ("None","Coartem/ALu — standard fixed-dose malaria treatment in Nigeria. These two drugs are designed to be taken together.","Safe as prescribed. Always take with food or milk to improve absorption."),
        ("coartem","paracetamol"):            ("None","Paracetamol is commonly used alongside Coartem for fever during malaria treatment in Nigeria. Safe combination.","Safe. Take Coartem with food. Standard Nigerian malaria management."),
        ("chloroquine","antacid"):            ("Moderate","Antacids reduce Chloroquine absorption — less effective malaria or lupus treatment.","Separate doses by at least 4 hours."),
        ("chloroquine","paracetamol"):        ("None","Common Nigerian malaria treatment combination. No significant interaction.","Safe. Monitor for GI upset. Take Chloroquine with food."),
        ("artemether","doxycycline"):         ("None","Doxycycline is used as a companion drug in some malaria regimens. Generally acceptable.","Take Doxycycline with food and water. Avoid dairy within 2 hours."),
        ("quinine","paracetamol"):            ("None","Commonly combined in Nigeria for severe malaria. No significant interaction at standard doses.","Safe. Monitor for quinine side effects — tinnitus, dizziness."),
        ("quinine","antacid"):               ("Moderate","Antacids reduce Quinine absorption, making malaria treatment less effective.","Separate by at least 2 hours."),

        # ── PAIN / FEVER ──────────────────────────────────────────────────────
        ("paracetamol","ibuprofen"):          ("Low","Can be safely alternated or combined short-term for pain and fever. Work via different mechanisms.","Safe short-term. Avoid in liver or kidney disease. Do not exceed recommended doses."),
        ("paracetamol","codeine"):            ("None","Co-codamol — a recognised pain combination. Paracetamol + Codeine work synergistically.","Safe at recommended doses. Do not exceed 8 tablets/day. Risk of dependence with long-term Codeine use."),
        ("ibuprofen","antacid"):             ("None","Antacids can help reduce ibuprofen-related stomach irritation. Common combination.","Safe. Useful for patients with GI sensitivity to NSAIDs."),
        ("tramadol","paracetamol"):           ("None","Common Nigerian pain combination. Tramadol + Paracetamol work synergistically. Recognised fixed combination (Ultracet).","Safe at standard doses. Avoid alcohol. Do not exceed recommended doses. Avoid in seizure history."),
        ("tramadol","codeine"):              ("Severe","Both are opioids. Combining significantly increases risk of respiratory depression, sedation and death.","Never combine. Use one opioid only. Refer to doctor."),
        ("tramadol","alcohol"):              ("Severe","Combined CNS depression — serious risk of respiratory failure, coma and death.","Never combine. Counsel patient urgently."),
        ("tramadol","ssri"):                 ("Severe","Risk of serotonin syndrome — agitation, confusion, rapid heart rate, muscle twitching. Can be fatal.","Avoid. Refer to doctor urgently if patient is on antidepressants."),
        ("aspirin","ibuprofen"):             ("Moderate","Both NSAIDs. Combined increases GI bleeding risk. Ibuprofen blocks aspirin's heart-protective effect.","Avoid combining. If needed, take aspirin 30 mins before Ibuprofen."),
        ("diclofenac","antacid"):            ("None","Antacids help reduce Diclofenac GI irritation. Common combination.","Safe. Take Diclofenac with food."),
        ("diclofenac","aspirin"):            ("Moderate","Both NSAIDs — increased risk of GI bleeding and ulcers. Aspirin's cardioprotective effect may be reduced.","Avoid combining unless prescribed. Take with food and antacid if necessary."),

        # ── BLOOD PRESSURE / HEART ────────────────────────────────────────────
        ("amlodipine","lisinopril"):          ("None","Very common Nigerian antihypertensive combination. Calcium channel blocker + ACE inhibitor. Generally safe and effective.","Safe as prescribed. Monitor blood pressure regularly. Watch for ankle swelling and dry cough."),
        ("amlodipine","simvastatin"):         ("Moderate","Amlodipine raises Simvastatin blood levels — increases risk of muscle damage (myopathy/rhabdomyolysis).","Limit Simvastatin to 20mg/day when taking Amlodipine. Consider switching to Atorvastatin."),
        ("lisinopril","potassium"):           ("Moderate","ACE inhibitors raise blood potassium. Adding supplements risks dangerous hyperkalaemia — heart arrhythmia.","Avoid potassium supplements unless prescribed. Monitor potassium levels regularly."),
        ("warfarin","aspirin"):              ("Severe","Both thin the blood. Combined greatly increases internal and GI bleeding risk.","Do NOT combine without specialist supervision. Refer to doctor immediately."),
        ("warfarin","ibuprofen"):            ("Severe","NSAIDs increase Warfarin levels and GI bleeding risk significantly.","Avoid. Use Paracetamol for pain instead. Monitor INR if unavoidable."),
        ("warfarin","flagyl"):               ("Severe","Metronidazole significantly potentiates Warfarin — major bleeding risk.","Avoid. If essential, reduce Warfarin dose and monitor INR very closely."),
        ("amlodipine","atorvastatin"):        ("None","Common Nigerian combination for hypertension + high cholesterol. No clinically significant interaction.","Safe as prescribed. Monitor for muscle aches."),
        ("hydrochlorothiazide","lisinopril"): ("None","Common antihypertensive combination in Nigeria. Generally safe and often prescribed together.","Safe. Monitor blood pressure, potassium and kidney function periodically."),

        # ── DIABETES ──────────────────────────────────────────────────────────
        ("metformin","alcohol"):             ("Severe","Significantly increases risk of lactic acidosis — a dangerous and potentially fatal build-up of lactic acid.","Avoid alcohol completely while on Metformin. Urgent pharmacist review if patient drinks regularly."),
        ("metformin","glibenclamide"):        ("None","Common Nigerian diabetes combination. Biguanide + Sulphonylurea. Generally well tolerated.","Safe. Monitor blood sugar. Watch for hypoglycaemia especially if meals are skipped."),
        ("insulin","alcohol"):               ("Severe","Alcohol masks hypoglycaemia symptoms and lowers blood sugar further — risk of dangerous undetected low blood sugar.","Avoid alcohol. If unavoidable, eat food with alcohol and monitor blood sugar closely."),
        ("glibenclamide","alcohol"):          ("Moderate","Alcohol can cause unpredictable blood sugar changes and may enhance hypoglycaemic effect.","Avoid alcohol. Eat regularly. Monitor blood sugar."),

        # ── ALCOHOL COMBINATIONS ──────────────────────────────────────────────
        ("metronidazole","alcohol"):          ("Severe","Causes severe disulfiram-like reaction — vomiting, flushing, rapid heartbeat, headache. Very common dangerous mistake in Nigeria.","Strictly avoid ALL alcohol during Metronidazole treatment and for 48 hours after finishing."),
        ("flagyl","alcohol"):                ("Severe","Flagyl is Metronidazole. Causes severe disulfiram-like reaction with alcohol — vomiting, flushing, palpitations.","Strictly avoid ALL alcohol during Flagyl treatment and for 48 hours after finishing."),
        ("diazepam","alcohol"):              ("Severe","Both depress the central nervous system. Combined — dangerous respiratory depression, coma, death.","Never combine. Counsel patient urgently."),
        ("tramadol","beer"):                 ("Severe","Alcohol (including beer) with Tramadol causes severe CNS depression — breathing failure, coma, death.","Never combine. Urgent patient counselling required."),

        # ── VITAMINS / SUPPLEMENTS ────────────────────────────────────────────
        ("ciprofloxacin","iron"):            ("Moderate","Iron supplements significantly reduce Ciprofloxacin absorption — antibiotic may become ineffective.","Separate Ciprofloxacin and iron by at least 2 hours."),
        ("doxycycline","iron"):              ("Moderate","Iron reduces Doxycycline absorption by up to 80%.","Take Doxycycline at least 2 hours before or 3 hours after iron supplements."),
        ("paracetamol","vitamin c"):         ("None","No significant interaction. Vitamin C may slightly increase Paracetamol absorption.","Safe combination. Standard doses only."),
        ("folic acid","metformin"):          ("None","Metformin may reduce Folate absorption long-term. Common to prescribe together especially in pregnancy.","Safe. Ensure adequate folic acid supplementation with long-term Metformin use."),

        # ── COMMON NIGERIAN BRANDED COMBINATIONS ─────────────────────────────
        ("septrin","warfarin"):              ("Severe","Cotrimoxazole (Septrin) greatly potentiates Warfarin — drastically increases bleeding risk.","Avoid combination. If essential, reduce Warfarin and monitor INR closely."),
        ("septrin","metformin"):             ("Moderate","Septrin can mask hypoglycaemia and may enhance blood sugar-lowering effect.","Monitor blood sugar carefully. Counsel patient."),
        ("gelusil","ciprofloxacin"):         ("Moderate","Gelusil (antacid) reduces Ciprofloxacin absorption significantly — antibiotic less effective.","Separate by at least 2 hours."),
        ("piriton","alcohol"):               ("Moderate","Chlorphenamine (Piriton) + alcohol causes excessive sedation and drowsiness.","Avoid alcohol. Do not drive after taking Piriton."),
        ("phenergan","alcohol"):             ("Moderate","Promethazine (Phenergan) + alcohol causes dangerous sedation. Very common combination in Nigeria.","Avoid alcohol. Do not drive. Avoid machinery."),
        ("penicillin","alcohol"):            ("Low","Alcohol does not directly interact with Penicillin but reduces immune function and impairs recovery.","Avoid alcohol during antibiotic course. Rest and hydrate well."),
    }

    result = {}
    for key_tuple, val in raw.items():
        result[frozenset(key_tuple)] = val
    return result

INTERACTIONS = make_interactions()

# Brand name → generic name map
BRAND_TO_GENERIC = {
    "flagyl":"metronidazole","coartem":"artemether","alu":"lumefantrine",
    "ampiclox":"ampicillin","augmentin":"amoxicillin","septrin":"cotrimoxazole",
    "gelusil":"antacid","gaviscon":"antacid","milk of magnesia":"antacid",
    "maalox":"antacid","zantac":"ranitidine","losec":"omeprazole",
    "piriton":"chlorphenamine","phenergan":"promethazine","valium":"diazepam",
    "lexotan":"bromazepam","penicillin v":"penicillin","amoxil":"amoxicillin",
    "ciproxin":"ciprofloxacin","vibramycin":"doxycycline","panado":"paracetamol",
    "panadol":"paracetamol","emzor paracetamol":"paracetamol","hedex":"paracetamol",
    "advil":"ibuprofen","brufen":"ibuprofen","feldene":"piroxicam",
    "voltaren":"diclofenac","cataflam":"diclofenac","indocin":"indomethacin",
    "ultram":"tramadol","tramal":"tramadol","beer":"alcohol","stout":"alcohol",
    "palm wine":"alcohol","ogogoro":"alcohol","spirit":"alcohol","wine":"alcohol",
    "glucophage":"metformin","diabex":"metformin","daonil":"glibenclamide",
    "euglucon":"glibenclamide","actrapid":"insulin","mixtard":"insulin",
    "norvasc":"amlodipine","zestril":"lisinopril","prinivil":"lisinopril",
    "zocor":"simvastatin","lipitor":"atorvastatin","crestor":"rosuvastatin",
    "coumadin":"warfarin","aspro":"aspirin","cafenol":"aspirin",
    "rifampicin":"rifampicin","rifampin":"rifampicin","isoniazid":"isoniazid",
    "ethambutol":"ethambutol","pyrazinamide":"pyrazinamide",
    "folic acid":"folic acid","folate":"folic acid","vitamin c":"vitamin c",
    "ascorbic acid":"vitamin c","ferrous sulphate":"iron","feroglobin":"iron",
    "astymin":"vitamin","multivitamin":"vitamin",
}

def normalise(name):
    n = name.lower().strip()
    return BRAND_TO_GENERIC.get(n, n)

def check_interaction(d1, d2):
    n1, n2 = normalise(d1), normalise(d2)
    key = frozenset({n1, n2})
    if key in INTERACTIONS:
        return INTERACTIONS[key]
    # Try partial match — e.g. "flagyl 400mg" → "flagyl"
    for k, v in INTERACTIONS.items():
        klist = list(k)
        if (n1 in klist[0] or klist[0] in n1) and (n2 in klist[1] or klist[1] in n2):
            return v
        if (n1 in klist[1] or klist[1] in n1) and (n2 in klist[0] or klist[0] in n2):
            return v
    return None

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
