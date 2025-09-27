import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# 🔹 Conexión con Google Sheets usando Secrets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = st.secrets["google_credentials"]  # ya es un diccionario
creds = ServiceAccountCredentials.from_json_keyfile_dict(dict(creds_dict), scope)
client = gspread.authorize(creds)
sheet = client.open("Asistencia").sheet1  # usa el nombre exacto de tu Google Sheet

# 🔹 Configuración de la página
st.set_page_config(page_title="Registro de Asistencia", page_icon="📋", layout="centered")

# 🔹 Interfaz
st.title("📋 Registro de Asistencia")

nombres = ["Rodrigo Huamani", "Anibal Agustin", "Elmer Garcia", "Erick Vilca", "Jordan liceta","Ruben Andrade"]  # 👉 Aquí pones tu lista de personas
nombre = st.selectbox("👤 Selecciona tu nombre", nombres)
tipo = st.selectbox("🕒 Tipo de registro", ["Ingreso", "Salida"])

if st.button("✅ Registrar asistencia"):
    if nombre.strip() != "":
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([nombre, tipo, fecha])
        st.success(f"Asistencia registrada para {nombre} - {tipo} a las {fecha}")
    else:
        st.error("⚠️ Debes ingresar un nombre")




