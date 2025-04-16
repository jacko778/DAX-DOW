
import streamlit as st
import pandas as pd
import investpy
from datetime import datetime

st.set_page_config(page_title="Tableau éco - Dow & DAX", layout="wide")
st.title("📈 Données économiques temps réel - Dow Jones 🇺🇸 et DAX 🇩🇪")
st.caption(f"Mise à jour : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} (source: Investing.com via investpy)")

# Fonction d'impact automatique simple
def impact_analyse(label, actual, forecast):
    try:
        a = float(actual.replace('%','').replace(',','.'))
        f = float(forecast.replace('%','').replace(',','.'))
    except:
        return "🔍 À interpréter"
    if "PIB" in label or "GDP" in label:
        return "📈 Haussier" if a > f else "📉 Baissier"
    if "Inflation" in label or "IPC" in label:
        return "📉 Baissier" if a > f else "📈 Haussier"
    if "Chômage" in label or "Unemployment" in label:
        return "📈 Haussier" if a < f else "📉 Baissier"
    if "ISM" in label or "IFO" in label or "ZEW" in label:
        return "📈 Haussier" if a > f else "📉 Baissier"
    return "🔍 À interpréter"

# Liste des indicateurs à extraire
indicateurs = [
    ("GDP Growth Rate QoQ", "united states"),
    ("Inflation Rate YoY", "united states"),
    ("Unemployment Rate", "united states"),
    ("Retail Sales MoM", "united states"),
    ("ISM Manufacturing PMI", "united states"),

    ("GDP Growth Rate QoQ", "germany"),
    ("Inflation Rate YoY", "germany"),
    ("Unemployment Rate", "germany"),
    ("Balance of Trade", "germany"),
    ("ZEW Economic Sentiment", "germany"),
    ("IFO Business Climate", "germany")
]

data_rows = []
for name, country in indicateurs:
    try:
        events = investpy.economic_calendar(time_zone='GMT', countries=[country.title()], 
                                            from_date='2024-01-01', to_date='2025-12-31')
        events = events[events['event'] == name]
        if not events.empty:
            row = events.iloc[0]
            data_rows.append({
                "Indicateur": name,
                "Pays": country.title(),
                "Date": row['date'],
                "Actuel": row['actual'],
                "Prévision": row['forecast'],
                "Précédent": row['previous'],
                "Impact": impact_analyse(name, row['actual'], row['forecast'])
            })
    except Exception as e:
        data_rows.append({
            "Indicateur": name,
            "Pays": country.title(),
            "Date": "Erreur",
            "Actuel": "N/A",
            "Prévision": "N/A",
            "Précédent": "N/A",
            "Impact": "Erreur"
        })

df = pd.DataFrame(data_rows)

# Séparation par tableau
df_dow = df[df['Pays'] == "United States"]
df_dax = df[df['Pays'] == "Germany"]

st.subheader("🇺🇸 Données US - Impact sur le Dow Jones")
st.dataframe(df_dow.reset_index(drop=True), use_container_width=True)

st.subheader("🇩🇪 Données Allemagne - Impact sur le DAX")
st.dataframe(df_dax.reset_index(drop=True), use_container_width=True)
