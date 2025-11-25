import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage

# -------------------------------
# Configuración inicial
# -------------------------------
st.set_page_config(page_title="Chatbot Básico", page_icon="🤖")
st.title("🤖 Tobbs Chatbot")
st.markdown("Este es un *chatbot de ejemplo* construido con LangChain + Streamlit.")

# -------------------------------
# Sidebar con controles
# -------------------------------
st.sidebar.title("⚙️ Configuración")

# Selector de modelo
modelos_disponibles = [
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-2.0-flash-lite",
    "gemini-1.5-pro"
]

if "modelo" not in st.session_state:
    st.session_state.modelo = modelos_disponibles[0]

st.session_state.modelo = st.sidebar.selectbox(
    "Modelo",
    modelos_disponibles,
    index=modelos_disponibles.index(st.session_state.modelo)
)

# Slider para temperatura
if "temperatura" not in st.session_state:
    st.session_state.temperatura = 0.7

st.session_state.temperatura = st.sidebar.slider(
    "Temperatura",
    min_value=0.0,
    max_value=1.5,
    step=0.1,
    value=st.session_state.temperatura
)

# Botón para limpiar chat
if st.sidebar.button("🗑️ Limpiar conversación"):
    st.session_state.mensajes = []
    st.rerun()

# -------------------------------
# Crear modelo con la configuración
# -------------------------------
chat_model = ChatGoogleGenerativeAI(
    model=st.session_state.modelo,
    temperature=st.session_state.temperatura
)

# -------------------------------
# Inicializar historial
# -------------------------------
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# -------------------------------
# Mostrar historial de mensajes
# -------------------------------
for msg in st.session_state.mensajes:
    rol = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(rol):
        st.markdown(msg.content)

# -------------------------------
# Entrada del usuario
# -------------------------------
pregunta = st.chat_input("Escribe tu mensaje:")

if pregunta:
    # guardar y mostrar mensaje del usuario
    st.session_state.mensajes.append(HumanMessage(content=pregunta))
    with st.chat_message("user"):
        st.markdown(pregunta)

    # generar respuesta
    respuesta = chat_model.invoke(st.session_state.mensajes)

    # mostrar y guardar respuesta
    with st.chat_message("assistant"):
        st.markdown(respuesta.content)

    st.session_state.mensajes.append(respuesta)
