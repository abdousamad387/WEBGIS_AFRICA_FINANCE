#!/usr/bin/env python3
"""Build WebGIS data from Africa Finance database and GeoJSON."""
import json, os, sys
import pandas as pd
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(BASE)
EXCEL = os.path.join(PARENT, "AfricaFinance_Database_2000_2024.xlsx")
GEOJSON_IN = os.path.join(PARENT, "africa.geojson")
OUT_DIR = os.path.join(BASE, "data")

ISO3_MAP = {
    "Afrique du Sud":"ZAF","Algérie":"DZA","Angola":"AGO","Bénin":"BEN",
    "Botswana":"BWA","Burkina Faso":"BFA","Burundi":"BDI","Cabo Verde":"CPV",
    "Cameroun":"CMR","Centrafrique":"CAF","Comores":"COM","Congo":"COG",
    "Côte d'Ivoire":"CIV","Djibouti":"DJI","Égypte":"EGY","Érythrée":"ERI",
    "Eswatini":"SWZ","Éthiopie":"ETH","Gabon":"GAB","Gambie":"GMB",
    "Ghana":"GHA","Guinée":"GIN","Guinée-Bissau":"GNB","Guinée équatoriale":"GNQ",
    "Kenya":"KEN","Lesotho":"LSO","Liberia":"LBR","Libye":"LBY",
    "Madagascar":"MDG","Malawi":"MWI","Mali":"MLI","Maroc":"MAR",
    "Maurice":"MUS","Mauritanie":"MRT","Mozambique":"MOZ","Namibie":"NAM",
    "Niger":"NER","Nigeria":"NGA","Ouganda":"UGA","RD Congo":"COD",
    "Rwanda":"RWA","São Tomé":"STP","Sénégal":"SEN","Sierra Leone":"SLE",
    "Somalie":"SOM","Soudan":"SDN","Soudan du Sud":"SSD","Tanzanie":"TZA",
    "Tchad":"TCD","Togo":"TGO","Tunisie":"TUN","Zambie":"ZMB","Zimbabwe":"ZWE",
}
ISO3_TO_FR = {v: k for k, v in ISO3_MAP.items()}

def safe(v):
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return None
    if isinstance(v, (np.integer,)):
        return int(v)
    if isinstance(v, (np.floating,)):
        return round(float(v), 2)
    if isinstance(v, (np.bool_,)):
        return bool(v)
    return v

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return round(float(obj), 2) if not np.isnan(obj) else None
        if isinstance(obj, (np.bool_,)):
            return bool(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)

SHEETS = {
    "macro": "📊 Macroéconomie Annuelle",
    "bank":  "🏦 Secteur Bancaire Annuel",
    "fint":  "📱 Fintech & Mobile Money",
    "mfi":   "🏘️ Microfinance & Inclusion",
    "profil":"🌍 Profil Pays Finance",
    "crises":"⚠️ Crises & Chocs",
}

# Column mappings: Excel name → internal key
MACRO_MAP = {
    "PIB ($Mrd)":"pib_mrd", "Croissance PIB (%)":"croissance_pib", "PIB/hab ($)":"pib_hab",
    "Inflation (%)":"inflation", "Dette publique (% PIB)":"dette_publique",
    "FDI entrants ($Mrd)":"fdi_entrants", "Chômage (%)":"chomage",
    "IDH estimé":"idh", "Balance courante (% PIB)":"balance_courante",
    "Envois fonds ($Mrd)":"envois_de_fonds", "Croissance pop. (%)":"croissance_pop",
    "Réserves ($Mrd)":"reserves", "Taux directeur (%)":"taux_directeur",
}
BANK_MAP = {
    "Taux bancarisation (%)":"bancarisation", "NPL ratio (%)":"npl", "CAR (%)":"car",
    "ROE (%)":"roe", "ROA (%)":"roa", "NIM (%)":"nim",
    "Crédit au secteur privé (% PIB)":"credit_pib", "Spread taux (%)":"spread",
    "Nb banques":"nb_banques", "Dépôts (% PIB)":"depots_pib",
    "Succursales/100k hab.":"succursales", "ATM/100k hab.":"atm",
    "Score stabilité financière (0-10)":"score_stabilite",
}
FINT_MAP = {
    "Comptes mobile money (M)":"comptes_mm", "Transactions M-Money ($Mrd)":"transactions_mm",
    "% pop. avec compte M-Money":"pop_mm", "Nb startups Fintech":"nb_startups_fintech",
    "Investissements Fintech ($M)":"invest_fintech",
    "Paiements numériques (% transactions)":"paiements_numeriques",
    "Taux pénétration smartphone (%)":"penetration_smartphone",
    "Nb agents mobile money/100k":"agents_mm",
}
MFI_MAP = {
    "PAR30 (%)":"par30", "Autosuffisance opérationnelle (%)":"oss",
    "Score inclusion financière (0-10)":"score_inclusion",
    "Clients actifs (000)":"nb_clients_mf", "Nb IMF actives":"nb_imf",
    "Portefeuille microcrédit ($M)":"portefeuille_credits",
    "% clients femmes":"pct_femmes_clients", "Taux remboursement (%)":"taux_remboursement",
}

def read_sheet(xl, name):
    df = pd.read_excel(xl, name, skiprows=1)
    for c in df.columns:
        if c not in ("Pays", "Région", "Année", "Trimestre", "Bourse"):
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df

def extract_cols(row, col_map):
    d = {}
    for excel_col, key in col_map.items():
        if excel_col in row.index:
            d[key] = safe(row[excel_col])
    return d

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    print("== Africa Finance WebGIS Builder ==")

    # --- GeoJSON ---
    print("  Loading GeoJSON...")
    with open(GEOJSON_IN, "r", encoding="utf-8") as f:
        geo = json.load(f)
    keep = ["NAME","NAME_LONG","NAME_FR","NAME_EN","ADMIN","ISO_A3","ADM0_A3",
            "REGION_WB","SUBREGION","POP_EST","GDP_MD","LABEL_X","LABEL_Y",
            "INCOME_GRP","ECONOMY","ISO_A2"]
    for feat in geo["features"]:
        p = feat["properties"]
        feat["properties"] = {k: p.get(k) for k in keep if k in p}
    with open(os.path.join(OUT_DIR, "africa.geojson"), "w", encoding="utf-8") as f:
        json.dump(geo, f, ensure_ascii=False)
    print(f"  -> {len(geo['features'])} features saved")

    # --- Excel ---
    print("  Loading Excel...")
    xl = pd.ExcelFile(EXCEL, engine="openpyxl")
    macro = read_sheet(xl, SHEETS["macro"])
    bank  = read_sheet(xl, SHEETS["bank"])
    fint  = read_sheet(xl, SHEETS["fint"])
    mfi   = read_sheet(xl, SHEETS["mfi"])

    # Rename key columns for consistency
    for df in [macro, bank, fint, mfi]:
        if "Région" in df.columns:
            df.rename(columns={"Région": "Region"}, inplace=True)
        if "Année" in df.columns:
            df.rename(columns={"Année": "Annee"}, inplace=True)

    # --- Region mapping (from data) ---
    region_map = {}
    for _, r in macro.drop_duplicates("Pays").iterrows():
        iso = ISO3_MAP.get(r["Pays"])
        if iso and pd.notna(r.get("Region")):
            region_map[iso] = r["Region"]

    # --- Indicators per year ---
    years = sorted(macro["Annee"].dropna().unique().astype(int))
    indicators = {}

    for year in years:
        ym  = macro[macro["Annee"]==year]
        yb  = bank[bank["Annee"]==year]
        yf  = fint[fint["Annee"]==year]
        ymfi= mfi[mfi["Annee"]==year]
        yd = {}
        for pays in ym["Pays"].unique():
            iso = ISO3_MAP.get(pays)
            if not iso:
                continue
            d = {"pays": pays, "region": region_map.get(iso)}
            pm = ym[ym["Pays"]==pays]
            if len(pm):
                d.update(extract_cols(pm.iloc[0], MACRO_MAP))
            pb = yb[yb["Pays"]==pays]
            if len(pb):
                d.update(extract_cols(pb.iloc[0], BANK_MAP))
            pf = yf[yf["Pays"]==pays]
            if len(pf):
                d.update(extract_cols(pf.iloc[0], FINT_MAP))
            pmfi2 = ymfi[ymfi["Pays"]==pays]
            if len(pmfi2):
                d.update(extract_cols(pmfi2.iloc[0], MFI_MAP))
            yd[iso] = d
        indicators[str(year)] = yd

    # --- KPIs (2024) ---
    m24 = macro[macro["Annee"]==2024]; b24 = bank[bank["Annee"]==2024]
    f24 = fint[fint["Annee"]==2024]; mfi24 = mfi[mfi["Annee"]==2024]
    kpis = {
        "pib_total": safe(m24["PIB ($Mrd)"].sum()),
        "croissance_avg": safe(m24["Croissance PIB (%)"].mean()),
        "inflation_avg": safe(m24["Inflation (%)"].mean()),
        "bancarisation_avg": safe(b24["Taux bancarisation (%)"].mean()),
        "npl_avg": safe(b24["NPL ratio (%)"].mean()),
        "car_avg": safe(b24["CAR (%)"].mean()),
        "roe_avg": safe(b24["ROE (%)"].mean()),
        "nim_avg": safe(b24["NIM (%)"].mean()),
        "mm_accounts": safe(f24["Comptes mobile money (M)"].sum()),
        "startups": safe(f24["Nb startups Fintech"].sum()),
        "fdi_total": safe(m24["FDI entrants ($Mrd)"].sum()),
        "dette_avg": safe(m24["Dette publique (% PIB)"].mean()),
        "nb_pays": int(m24["Pays"].nunique()),
        "credit_pib_avg": safe(b24["Crédit au secteur privé (% PIB)"].mean()),
        "score_inclusion_avg": safe(mfi24["Score inclusion financière (0-10)"].mean()),
        "pop_mm_avg": safe(f24["% pop. avec compte M-Money"].mean()),
    }

    # --- Continental time series ---
    ts = []
    for year in years:
        ym = macro[macro["Annee"]==year]; yb = bank[bank["Annee"]==year]
        yf = fint[fint["Annee"]==year]; ymfi2 = mfi[mfi["Annee"]==year]
        ts.append({
            "year": year,
            "pib_total": safe(ym["PIB ($Mrd)"].sum()),
            "croissance": safe(ym["Croissance PIB (%)"].mean()),
            "inflation": safe(ym["Inflation (%)"].mean()),
            "dette": safe(ym["Dette publique (% PIB)"].mean()),
            "bancarisation": safe(yb["Taux bancarisation (%)"].mean()),
            "npl": safe(yb["NPL ratio (%)"].mean()),
            "pop_mm": safe(yf["% pop. avec compte M-Money"].mean()),
            "fdi": safe(ym["FDI entrants ($Mrd)"].sum()),
            "score_inclusion": safe(ymfi2["Score inclusion financière (0-10)"].mean()),
        })

    # --- Country time series ---
    country_ts = {}
    for pays in macro["Pays"].unique():
        iso = ISO3_MAP.get(pays)
        if not iso:
            continue
        pm = macro[macro["Pays"]==pays].sort_values("Annee")
        pb = bank[bank["Pays"]==pays].sort_values("Annee")
        pf = fint[fint["Pays"]==pays].sort_values("Annee")
        country_ts[iso] = {
            "annees": [int(a) for a in pm["Annee"]],
            "pib": [safe(v) for v in pm["PIB ($Mrd)"]],
            "croissance": [safe(v) for v in pm["Croissance PIB (%)"]],
            "inflation": [safe(v) for v in pm["Inflation (%)"]],
            "dette": [safe(v) for v in pm["Dette publique (% PIB)"]],
            "bancarisation": [safe(v) for v in pb["Taux bancarisation (%)"]] if len(pb) else [],
            "npl": [safe(v) for v in pb["NPL ratio (%)"]] if len(pb) else [],
            "pop_mm": [safe(v) for v in pf["% pop. avec compte M-Money"]] if len(pf) else [],
        }

    # --- Rankings (2024) ---
    rankings = {}
    rvars = {
        "pib_hab": ("PIB/hab ($)", macro, True),
        "croissance": ("Croissance PIB (%)", macro, True),
        "bancarisation": ("Taux bancarisation (%)", bank, True),
        "npl": ("NPL ratio (%)", bank, False),
        "inflation": ("Inflation (%)", macro, False),
        "credit_pib": ("Crédit au secteur privé (% PIB)", bank, True),
        "score_inclusion": ("Score inclusion financière (0-10)", mfi, True),
        "dette": ("Dette publique (% PIB)", macro, False),
        "fdi": ("FDI entrants ($Mrd)", macro, True),
        "pop_mm": ("% pop. avec compte M-Money", fint, True),
    }
    for key, (col, df, higher_good) in rvars.items():
        d24 = df[df["Annee"]==2024][["Pays", col]].dropna()
        d24 = d24.sort_values(col, ascending=not higher_good)
        rankings[key] = {
            "top": [{"pays": r["Pays"], "val": safe(r[col])} for _, r in d24.head(10).iterrows()],
            "bottom": [{"pays": r["Pays"], "val": safe(r[col])} for _, r in d24.tail(10).iterrows()],
        }

    # --- Profiles ---
    profils = {}
    try:
        prof = read_sheet(xl, SHEETS["profil"])
        for _, r in prof.iterrows():
            iso = ISO3_MAP.get(r.get("Pays"))
            if not iso:
                continue
            profils[iso] = {
                "lat": safe(r.get("Latitude")), "lon": safe(r.get("Longitude")),
                "population": safe(r.get("Population 2024 (M)")),
                "monnaie": str(r.get("Monnaie","")) if pd.notna(r.get("Monnaie")) else "",
                "banque_centrale": str(r.get("Banque centrale","")) if pd.notna(r.get("Banque centrale")) else "",
                "capitale": "",
                "bourse": str(r.get("Bourse nationale","")) if pd.notna(r.get("Bourse nationale")) else "",
            }
    except Exception as e:
        print(f"  Warning: Profiles sheet error: {e}")

    # --- Crises ---
    crises = []
    try:
        cr = read_sheet(xl, SHEETS["crises"])
        if "Région" in cr.columns:
            cr.rename(columns={"Région": "Region"}, inplace=True)
        if "Année" in cr.columns:
            cr.rename(columns={"Année": "Annee"}, inplace=True)
        for _, r in cr.iterrows():
            if pd.isna(r.get("Pays")):
                continue
            crises.append({
                "pays": str(r["Pays"]), "annee": safe(r.get("Annee")),
                "type": str(r.get("Type de crise","")) if pd.notna(r.get("Type de crise")) else "",
                "severite": safe(r.get("Sévérité (1-5)")),
                "impact_pib": safe(r.get("Impact PIB (%)")),
                "region": str(r.get("Region","")) if pd.notna(r.get("Region")) else "",
            })
    except Exception as e:
        print(f"  Warning: Crises sheet error: {e}")

    # --- Output ---
    data = {
        "indicators": indicators,
        "years": [int(y) for y in years],
        "kpis": kpis,
        "timeseries": ts,
        "country_ts": country_ts,
        "rankings": rankings,
        "profils": profils,
        "crises": crises,
        "region_map": region_map,
        "iso3_map": ISO3_MAP,
        "regions": {
            "Afrique Australe": "#00e5a0",
            "Afrique Centrale": "#a78bfa",
            "Afrique du Nord": "#58a6ff",
            "Afrique Occidentale": "#f59e0b",
            "Afrique Orientale": "#f472b6",
        },
    }
    out_path = os.path.join(OUT_DIR, "indicators.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, cls=NpEncoder)
    geo_size = os.path.getsize(os.path.join(OUT_DIR, "africa.geojson")) / 1024
    ind_size = os.path.getsize(out_path) / 1024
    print(f"  -> africa.geojson  : {geo_size:.0f} KB")
    print(f"  -> indicators.json : {ind_size:.0f} KB")
    print(f"  -> {len(years)} years, {len(ISO3_MAP)} countries, {len(kpis)} KPIs")
    print("== Done ==")

if __name__ == "__main__":
    main()
