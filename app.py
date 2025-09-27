import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pytz

# 🔹 Conexión con Google Sheets usando Secrets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = st.secrets["google_credentials"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(dict(creds_dict), scope)
client = gspread.authorize(creds)

# Hojas
sheet_asistencia = client.open("Asistencia").worksheet("Asistencia")  # donde se registran asistencias
sheet_usuarios = client.open("Asistencia").worksheet("Usuarios")      # datos de usuarios

# Obtener usuarios
usuarios = sheet_usuarios.get_all_records()
nombres = [u["Nombre"] for u in usuarios]

# 🔹 Interfaz
st.set_page_config(page_title="Registro de Asistencia", page_icon="📋", layout="centered")
st.title("📋 Registro de Asistencia")

# Selección de nombre
nombre = st.selectbox("👤 Selecciona tu nombre", nombres)

# Mostrar datos del usuario automáticamente
usuario = next((u for u in usuarios if u["Nombre"] == nombre), None)
if usuario:
    st.write(f"**Puesto:** {usuario['Puesto']}")
    st.write(f"**Área:** {usuario['Área']}")
    st.image(usuario["Foto"], width=150)

# Selección de tipo de registro
tipo = st.selectbox("🕒 Tipo de registro", ["Ingreso", "Salida"])

# Botón registrar
if st.button("✅ Registrar asistencia"):
    tz = pytz.timezone("America/Lima")
    fecha = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    sheet_asistencia.append_row([nombre, usuario["Puesto"], usuario["Área"], tipo, fecha])
    st.success(f"Asistencia registrada para {nombre} - {tipo} a las {fecha}")


# 🔹 Configuración de la página
st.set_page_config(page_title="Registro de Asistencia", page_icon="📋", layout="centered")
# 🔹 Fondo personalizado con tu foto de Imgur
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://i.imgur.com/Zbz8oAQ.jpeg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);  /* header transparente */
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# 🔹 Interfaz
st.title("📋 Registro de Asistencia")

nombres = ["Anibal Agustin", "Elmer Garcia", "Elvis Camarena","Erick Vilca","Jacinto Vargas", "Jordan liceta","Rodrigo Huamani","Ruben Andrade"]  # 👉 Aquí pones tu lista de personas
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



















