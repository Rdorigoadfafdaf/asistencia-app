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
sheet = client.open("Asistencia")
sheet_asistencia = sheet.worksheet("Asistencia")   # pestaña donde se registran asistencias
sheet_usuarios = sheet.worksheet("Usuarios")       # pestaña con datos de usuarios

# Obtener usuarios
usuarios = sheet_usuarios.get_all_records()
nombres = [u["Nombre"] for u in usuarios]

# 🔹 Configuración de la página
st.set_page_config(page_title="Registro de Asistencia", page_icon="📋", layout="centered")

# 🔹 Fondo personalizado (foto de Imgur)
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://i.imgur.com/L1PTN4m.jpeg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

/* 🔹 Estilos globales para bloques de datos */
.block {
    background-color:#1c1c1c;
    padding:10px;
    border-radius:8px;
    margin-bottom:10px;
}
.block label {
    font-size:13px;
    color:#ccc;
}
.block span {
    font-size:16px;
    color:white;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# 🔹 Interfaz
st.title("📋 Registro de Asistencia")

# Campo: Selección de nombre (label integrado al recuadro)
nombre = st.selectbox("Selecciona tu nombre", nombres, key="nombre", label_visibility="visible")

# Buscar datos del usuario seleccionado
usuario = next((u for u in usuarios if u["Nombre"] == nombre), None)
if usuario:
 if usuario:
    st.text_input("Puesto", usuario.get("Puesto", "No definido"), key="puesto", disabled=True)
    st.text_input("Área", usuario.get("Área", usuario.get("Area", "No definido")), key="area", disabled=True)

    # Foto del usuario (si existe en la hoja)
    if usuario.get("Foto"):
        st.image(usuario["Foto"], width=150)

    # Foto del usuario (si existe en la hoja)
    if usuario.get("Foto"):
        st.image(usuario["Foto"], width=150)

# Campo: Selección de tipo de registro (label integrado al recuadro)
tipo = st.selectbox("Tipo de registro", ["Ingreso", "Salida"], key="tipo_registro", label_visibility="visible")

# Emoji dinámico según tipo
emoji = "✅" if tipo == "Ingreso" else "❌"

# Botón registrar
if st.button(f"{emoji} Registrar {tipo}", key="btn_registro"):
    tz = pytz.timezone("America/Lima")
    fecha = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    sheet_asistencia.append_row([
        nombre,
        usuario.get("Puesto", ""),
        usuario.get("Área", usuario.get("Area", "")),
        tipo,
        fecha
    ])
    st.success(f"Asistencia registrada para {nombre} - {tipo} a las {fecha}")




















