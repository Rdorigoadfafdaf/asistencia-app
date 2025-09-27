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
st.markdown("""
<style>
h1 {
    color: white; /* o #FFD700, #FF8000, #0055FF */
    text-shadow: 2px 2px 4px rgba(0,0,0,0.8); /* sombra para contraste */
}
</style>
""", unsafe_allow_html=True)

# Campo: Selección de nombre
st.markdown("**Selecciona tu nombre**", unsafe_allow_html=True)
nombre = st.selectbox("", nombres, key="nombre", label_visibility="collapsed")

# Buscar datos del usuario seleccionado
usuario = next((u for u in usuarios if u["Nombre"] == nombre), None)
if usuario:
    # Campo: Puesto (label arriba, valor en caja)
    st.markdown("**Puesto**", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="
        background-color:#1c1c1c; 
        padding:10px; 
        border-radius:8px; 
        margin-bottom:10px;
        font-size:16px; 
        color:white;
    ">
        {usuario.get('Puesto', 'No definido')}
    </div>
    """, unsafe_allow_html=True)

    # Campo: Área (label arriba, valor en caja)
    st.markdown("**Área**", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="
        background-color:#1c1c1c; 
        padding:10px; 
        border-radius:8px; 
        margin-bottom:10px;
        font-size:16px; 
        color:white;
    ">
        {usuario.get('Área', usuario.get('Area', 'No definido'))}
    </div>
    """, unsafe_allow_html=True)

    # Foto del usuario (si existe en la hoja)
    if usuario.get("Foto"):
        st.image(usuario["Foto"], width=150)

# Campo: Selección de tipo de registro
st.markdown("**Tipo de registro**", unsafe_allow_html=True)
tipo = st.selectbox("", ["Ingreso", "Salida"], key="tipo_registro", label_visibility="collapsed")

# Emoji dinámico según tipo
emoji = "✅" if tipo == "Ingreso" else "❌"

# Botón Registrar (verde fijo con estilo)
button_html = """
<style>
.register-btn {
    background-color: #28a745; /* verde tipo Bootstrap */
    color: white;
    font-size: 18px;
    font-weight: bold;
    padding: 12px 20px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    width: 100%;
    text-align: center;
}
.register-btn:hover {
    background-color: #218838; /* verde más oscuro al pasar el mouse */
}
</style>

<form action="#" method="post">
    <button class="register-btn" type="submit">✅ Registrar</button>
</form>
"""
st.markdown(button_html, unsafe_allow_html=True)


























