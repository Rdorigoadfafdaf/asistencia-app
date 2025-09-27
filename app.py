import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import json

# 🔹 Conexión con Google Sheets usando Secrets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(st.secrets["google_credentials"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open("Asistencia").sheet1  # usa el nombre exacto de tu Google Sheet

# 🔹 Interfaz Streamlit
st.set_page_config(page_title="Registro de Asistencia", page_icon="📋", layout="centered")

st.title("📋 Registro de Asistencia")

nombre = st.text_input("👤 Nombre")
tipo = st.selectbox("🕒 Tipo de registro", ["Ingreso", "Salida"])

if st.button("✅ Registrar asistencia"):
    if nombre.strip() != "":
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([nombre, tipo, fecha])
        st.success(f"Asistencia registrada para {nombre} - {tipo} a las {fecha}")
    else:
        st.error("⚠️ Debes ingresar un nombre")


