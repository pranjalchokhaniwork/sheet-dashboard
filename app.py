import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Auth
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Load Sheet
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/15XcIvqDKs2MNQfMmCas5gIOT84qfEJagJF-3pXYcc00")
df23 = pd.DataFrame(sheet.worksheet("23-24 Session").get_all_records())
df24 = pd.DataFrame(sheet.worksheet("24-25 Session").get_all_records())
df25 = pd.DataFrame(sheet.worksheet("25-26 Session").get_all_records())

df23["Year"] = "AY24"
df24["Year"] = "AY25"
df25["Year"] = "AY26"

df = pd.concat([df23, df24, df25])
df = df[df["Student f code"].notna() & (df["Student f code"] != "")]

# Filters
st.title("Live Dashboard from Google Sheet")
sccity = st.selectbox("sccity", [""] + sorted(df["sccity"].dropna().unique().tolist()))
stream = st.selectbox("stream", [""] + sorted(df["streamx"].dropna().unique().tolist()))
grade = st.selectbox("grade", [""] + sorted(df["classvalue"].dropna().unique().tolist()))

filtered = df.copy()
if sccity: filtered = filtered[filtered["sccity"] == sccity]
if stream: filtered = filtered[filtered["streamx"] == stream]
if grade: filtered = filtered[filtered["classvalue"] == grade]

def summary(key):
    return (filtered
            .groupby([key, "Year"])
            .size()
            .unstack(fill_value=0)
            .reset_index()
            .sort_values(by="AY26", ascending=False))

st.subheader("State-wise Summary")
st.dataframe(summary("Home state"))

st.subheader("District-wise Summary")
st.dataframe(summary("Home district"))

st.subheader("PinCode-wise Summary")
st.dataframe(summary("PinCode"))
