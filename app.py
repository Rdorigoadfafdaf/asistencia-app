import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pytz

# 🔹 Configuración de la página
st.set_page_config(page_title="Registro de Asistencia", page_icon="📋", layout="centered")

# 🔹 Fondo personalizado (foto de Imgur) y estilos
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
.block {
    background-color:#1c1c1c;
    padding:10px;
    border-radius:8px;
    margin-bottom:10px;
    font-size:16px;
    color:white;
}
h1 {
    color: white;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# 🔹 Título
st.title("📋 Registro de Asistencia")

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

# --- Placeholders ---
opciones_nombre = ["Selecciona un nombre..."] + nombres
opciones_tipo = ["Selecciona tipo de registro..."] + ["Ingreso", "Salida"]

# Campo: Selección de nombre con foto al costado
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("**Selecciona tu nombre**", unsafe_allow_html=True)
    nombre = st.selectbox("", opciones_nombre, key="nombre", label_visibility="collapsed")

usuario = None
with col2:
    if nombre != "Selecciona un nombre...":
        usuario = next((u for u in usuarios if u["Nombre"] == nombre), None)
        if usuario and usuario.get("Foto"):
            st.image(usuario["Foto"], width=100)

# Mostrar Puesto y Área debajo (solo si se eligió nombre válido)
if usuario:
    st.markdown("**Puesto**", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="block">
        {usuario.get('Puesto', 'No definido')}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Área**", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="block">
        {usuario.get('Área', usuario.get('Area', 'No definido'))}
    </div>
    """, unsafe_allow_html=True)

# Campo: Selección de tipo de registro
st.markdown("**Tipo de registro**", unsafe_allow_html=True)
tipo = st.selectbox("", opciones_tipo, key="tipo_registro", label_visibility="collapsed")

# Botón Registrar (verde con estilo)
button_css = """
<style>
div.stButton > button:first-child {
    background-color: #28a745;
    color: white;
    font-size: 18px;
    font-weight: bold;
    padding: 12px 20px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    width: 100%;
}
div.stButton > button:hover {
    background-color: #218838;
    color: white;
}
</style>
"""
st.markdown(button_css, unsafe_allow_html=True)

if st.button("✅ Registrar"):
    if nombre != "Selecciona un nombre..." and tipo != "Selecciona tipo de registro...":
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
    else:
        st.error("⚠️ Debes seleccionar un nombre y un tipo de registro antes de continuar.")























