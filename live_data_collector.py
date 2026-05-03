"""
live_data_collector.py
======================
Fetches live Nigerian disease data from the WHO Global Health Observatory API.
Runs weekly to update the database with real 2024-2026 data.

Usage:
    python live_data_collector.py              # fetch all diseases
    python live_data_collector.py --disease malaria
    python live_data_collector.py --test       # test connection only
"""

import argparse
import json
import logging
import sqlite3
import time
from datetime import datetime, date
from pathlib import Path

import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("live_collector")

# ── Config ────────────────────────────────────────────────────────────────────
DB_PATH  = "./nigeria_live.db"
BASE_URL = "https://ghoapi.azureedge.net/api"

# WHO GHO indicator codes for Nigeria diseases
# Find more at: https://ghoapi.azureedge.net/api/Indicator
DISEASE_INDICATORS = {
    "malaria": [
        "MALARIA_CASES",           # Confirmed malaria cases
        "MALARIA_EST_INCIDENCE",   # Estimated incidence rate
        "MALARIA_DEATHS",          # Malaria deaths
    ],
    "tuberculosis": [
        "MDG_0000000020",          # TB incidence per 100,000
        "TB_e_inc_num",            # Estimated TB incidence number
    ],
    "cholera": [
        "CHOLERA_0000000001",      # Cholera cases reported
        "CHOLERA_0000000002",      # Cholera deaths
    ],
    "yellow_fever": [
        "WHS3_50",                 # Yellow fever - number of reported cases ✓
        "VACCINECOVERAGE_YFV",     # Yellow fever vaccine coverage
    ],
    "meningitis": [
        "MENING_2",                # Number of suspected meningitis cases reported ✓
        "MENING_1",                # Number of suspected meningitis deaths reported ✓
        "MENING_3",                # Number of meningitis epidemic districts ✓
    ],
    "typhoid": [
        "WHS3_43",                 # Enteric fever (typhoid) reported cases
        "WHS3_44",                 # Enteric fever deaths
    ],
    "lassa_fever": [
        "WHS3_53",                 # Viral haemorrhagic fever cases (includes Lassa)
        "WHS3_54",                 # Viral haemorrhagic fever deaths
    ],
    "diarrhoeal": [
        "WSH_10",                  # Diarrhoea deaths from inadequate WASH
        "WSH_30",                  # Diarrhoea DALYs from inadequate WASH
        "UNICEF_ORS",              # Children with diarrhoea receiving ORS
    ],
}

# WHO country code for Nigeria
NIGERIA_CODE = "NGA"

# ── Database Setup ────────────────────────────────────────────────────────────
SCHEMA = """
CREATE TABLE IF NOT EXISTS live_disease_data (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    disease         TEXT    NOT NULL,
    indicator_code  TEXT    NOT NULL,
    indicator_name  TEXT,
    year            INTEGER NOT NULL,
    value           REAL,
    unit            TEXT,
    source          TEXT    DEFAULT 'WHO_GHO',
    fetched_at      TEXT    DEFAULT (datetime('now')),
    UNIQUE(disease, indicator_code, year)
);

CREATE TABLE IF NOT EXISTS live_climate_data (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    year            INTEGER NOT NULL,
    month           INTEGER NOT NULL,
    indicator_code  TEXT    NOT NULL,
    indicator_name  TEXT,
    value           REAL,
    unit            TEXT,
    source          TEXT    DEFAULT 'WHO_GHO',
    fetched_at      TEXT    DEFAULT (datetime('now')),
    UNIQUE(indicator_code, year, month)
);

CREATE TABLE IF NOT EXISTS fetch_log (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    run_at      TEXT    DEFAULT (datetime('now')),
    disease     TEXT,
    indicator   TEXT,
    records     INTEGER,
    status      TEXT,
    message     TEXT
);
"""


def setup_db(db_path: str):
    """Create the live database schema."""
    conn = sqlite3.connect(db_path)
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()
    log.info("Database ready: %s", db_path)


# ── API Helpers ───────────────────────────────────────────────────────────────
def fetch_indicator(indicator_code: str, country: str = NIGERIA_CODE,
                    retries: int = 3) -> list[dict]:
    """Fetch data for one WHO GHO indicator for Nigeria."""
    url = (
        f"{BASE_URL}/{indicator_code}"
        f"?$filter=SpatialDim eq '{country}'"
        f"&$select=TimeDim,NumericValue,Low,High,Comments,Dim1"
        f"&$orderby=TimeDim desc"
    )

    for attempt in range(retries):
        try:
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            records = data.get("value", [])
            log.info("  %s: %d records", indicator_code, len(records))
            return records
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                log.warning("  %s: indicator not found (404)", indicator_code)
                return []
            log.warning("  %s: attempt %d failed: %s", indicator_code, attempt+1, e)
        except Exception as e:
            log.warning("  %s: attempt %d error: %s", indicator_code, attempt+1, e)

        if attempt < retries - 1:
            time.sleep(2 ** attempt)

    return []


def get_indicator_name(indicator_code: str) -> str:
    """Get human-readable name for an indicator."""
    try:
        url = f"{BASE_URL}/Indicator?$filter=IndicatorCode eq '{indicator_code}'"
        resp = requests.get(url, timeout=15)
        data = resp.json()
        items = data.get("value", [])
        if items:
            return items[0].get("IndicatorName", indicator_code)
    except Exception:
        pass
    return indicator_code


def search_indicators(keyword: str) -> list[dict]:
    """Search WHO GHO for indicators matching a keyword."""
    url = f"{BASE_URL}/Indicator?$filter=contains(IndicatorName,'{keyword}')"
    try:
        resp = requests.get(url, timeout=30)
        data = resp.json()
        return data.get("value", [])[:20]
    except Exception as e:
        log.error("Search failed: %s", e)
        return []


# ── Data Storage ──────────────────────────────────────────────────────────────
def save_disease_records(db_path: str, disease: str,
                          indicator_code: str, indicator_name: str,
                          records: list[dict]) -> int:
    """Save fetched records to the live database."""
    conn = sqlite3.connect(db_path)
    rows = []
    for r in records:
        year = r.get("TimeDim")
        value = r.get("NumericValue")
        if year and value is not None:
            rows.append((disease, indicator_code, indicator_name,
                         int(year), float(value), "per 100,000 or count"))

    if rows:
        conn.executemany("""
            INSERT OR REPLACE INTO live_disease_data
                (disease, indicator_code, indicator_name, year, value, unit)
            VALUES (?,?,?,?,?,?)
        """, rows)
        conn.commit()

    conn.close()
    return len(rows)


def log_fetch(db_path: str, disease: str, indicator: str,
              records: int, status: str, message: str = ""):
    """Log each fetch run."""
    conn = sqlite3.connect(db_path)
    conn.execute("""
        INSERT INTO fetch_log (disease, indicator, records, status, message)
        VALUES (?,?,?,?,?)
    """, (disease, indicator, records, status, message))
    conn.commit()
    conn.close()


# ── Main Collector ────────────────────────────────────────────────────────────
def collect_disease(db_path: str, disease: str):
    """Collect all indicators for one disease."""
    indicators = DISEASE_INDICATORS.get(disease, [])
    if not indicators:
        log.warning("No indicators configured for: %s", disease)
        return 0

    log.info("Collecting: %s (%d indicators)", disease, len(indicators))
    total = 0

    for code in indicators:
        indicator_name = get_indicator_name(code)
        records = fetch_indicator(code)

        if records:
            n = save_disease_records(db_path, disease, code,
                                     indicator_name, records)
            log_fetch(db_path, disease, code, n, "ok")
            total += n
        else:
            log_fetch(db_path, disease, code, 0, "no_data")

        time.sleep(0.5)  # Be polite to the API

    return total


def collect_all(db_path: str):
    """Collect data for all configured diseases."""
    log.info("=" * 55)
    log.info("Nigeria Live Data Collector — WHO GHO API")
    log.info("Run at: %s", datetime.now().strftime("%Y-%m-%d %H:%M"))
    log.info("=" * 55)

    setup_db(db_path)
    grand_total = 0

    for disease in DISEASE_INDICATORS:
        n = collect_disease(db_path, disease)
        grand_total += n
        log.info("  %s: %d records saved", disease, n)
        time.sleep(1)

    log.info("=" * 55)
    log.info("Total records saved: %d", grand_total)
    log.info("Database: %s", db_path)

    # Show summary
    conn = sqlite3.connect(db_path)
    print("\n📊 Data Summary by Disease:")
    rows = conn.execute("""
        SELECT disease, COUNT(*) as records,
               MIN(year) as from_year, MAX(year) as to_year
        FROM live_disease_data
        GROUP BY disease
        ORDER BY disease
    """).fetchall()
    for r in rows:
        print(f"  {r[0]:20s}  {r[1]:>5} records  ({r[2]}–{r[3]})")
    conn.close()


def test_connection():
    """Quick test to verify API is accessible."""
    log.info("Testing WHO GHO API connection...")
    try:
        resp = requests.get(f"{BASE_URL}/Indicator?$top=1", timeout=10)
        resp.raise_for_status()
        log.info("✅ Connection successful! Status: %s", resp.status_code)

        # Test Nigeria-specific data
        log.info("Testing Nigeria malaria data...")
        records = fetch_indicator("MALARIA_CASES")
        if records:
            log.info("✅ Nigeria malaria data: %d records", len(records))
            latest = records[0]
            log.info("   Latest year: %s, Value: %s",
                     latest.get("TimeDim"), latest.get("NumericValue"))
        else:
            log.info("⚠️  No malaria records returned (indicator may differ)")
            log.info("   Searching for malaria indicators...")
            results = search_indicators("malaria")
            log.info("   Found %d malaria indicators:", len(results))
            for r in results[:5]:
                log.info("   Code: %-30s Name: %s",
                         r.get("IndicatorCode"), r.get("IndicatorName"))
        return True
    except Exception as e:
        log.error("❌ Connection failed: %s", e)
        return False


def find_indicators(keyword: str):
    """Search and print matching indicators."""
    print(f"\n🔍 Searching WHO GHO for '{keyword}'...")
    results = search_indicators(keyword)
    if not results:
        print("No results found.")
        return
    print(f"Found {len(results)} indicators:\n")
    for r in results:
        print(f"  Code: {r.get('IndicatorCode', 'N/A')}")
        print(f"  Name: {r.get('IndicatorName', 'N/A')}")
        print()


# ── CLI ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Nigeria Live Disease Data Collector — WHO GHO API"
    )
    parser.add_argument("--disease", type=str,
                        help="Collect specific disease only")
    parser.add_argument("--test", action="store_true",
                        help="Test API connection only")
    parser.add_argument("--find", type=str,
                        help="Search for indicators by keyword")
    parser.add_argument("--db", type=str, default=DB_PATH,
                        help=f"Database path (default: {DB_PATH})")
    args = parser.parse_args()

    if args.test:
        test_connection()
    elif args.find:
        find_indicators(args.find)
    elif args.disease:
        setup_db(args.db)
        n = collect_disease(args.db, args.disease)
        log.info("Done: %d records saved for %s", n, args.disease)
    else:
        collect_all(args.db)
