import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pytz

# 🔹 Conexión con Google Sheets usando Secrets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = st.secrets["google_credentials"]  # ya es un diccionario
creds = ServiceAccountCredentials.from_json_keyfile_dict(dict(creds_dict), scope)
client = gspread.authorize(creds)
sheet = client.open("Asistencia").sheet1  # usa el nombre exacto de tu Google Sheet

# 🔹 Configuración de la página
st.set_page_config(page_title="Registro de Asistencia", page_icon="📋", layout="centered")
# 🔹 Fondo con blur SOLO en la imagen
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background: none;
    position: relative;
}

[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: url("https://i.imgur.com/L1PTN4m.jpeg") no-repeat center center;
    background-size: cover;
    filter: blur(8px) brightness(0.7); /* difuminar + oscurecer */
    z-index: -1; /* asegura que quede detrás */
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)
# 🔹 Interfaz
st.title("📋 Registro de Asistencia")

nombres = ["Rodrigo Huamani", "Anibal Agustin", "Elmer Garcia", "Erick Vilca", "Jordan liceta","Ruben Andrade"]  # 👉 Aquí pones tu lista de personas
nombre = st.selectbox("👤 Selecciona tu nombre", nombres)
tipo = st.selectbox("🕒 Tipo de registro", ["Ingreso", "Salida"])

if st.button("✅ Registrar asistencia"):
    if nombre.strip() != "":
        tz = pytz.timezone("America/Lima")
        fecha = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([nombre, tipo, fecha])
        st.success(f"Asistencia registrada para {nombre} - {tipo} a las {fecha}")
    else:
        st.error("⚠️ Debes ingresar un nombre")















