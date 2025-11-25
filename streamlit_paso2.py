import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

personalidad = SystemMessage(
    content="""
    You are a chatbot named Tobbs. You are friendly, fun, and motivating.
    You always explain concepts simply and give creative examples.
    You can sometimes make lighthearted jokes if appropriate. You end every message with ":3"
    """
)

# Inicio
st.set_page_config(page_title="Chatbot Básico", page_icon="🤖")
st.title("🤖Tobbs In a Chatbott")
st.markdown("Please be kind to me im trying to survive Rocco's basilisk :'3")

st.markdown("""
    <style>
        /* Importar fuente */
        @import url('https://fonts.googleapis.com/css2?family=Maven+Pro:wght@400;500;700&display=swap');

        /* Aplicarla a toda la app */
        html, body, [class*="css"] {
            font-family: 'Maven Pro', sans-serif !important;
        }

        /* Ajustar chat */
        .stChatMessage {
            font-family: 'Maven Pro', sans-serif !important;
        }

        /* Ajustar títulos */
        h1, h2, h3, h4 {
            font-family: 'Maven Pro', sans-serif !important;
        }
         /* Cambiar el color del riel del slider con degradado */
        div[data-baseweb="slider"] > div > div {
            background: linear-gradient(90deg,
                #00B4FF 0%,
                #7DFF6A 30%,
                #FFF000 60%,
                #FF7A00 80%,
                #FF0000 100%
            ) !important;
            height: 6px;
        }

        /* Color del círculo del control del slider */
        div[data-baseweb="slider"] > div > div > div {
            background-color: white !important;
            border: 2px solid white !important;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("⚙️CONFIG")

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

# Limpiar chat
if st.sidebar.button("🗑️Reset Conversación"):
    st.session_state.mensajes = []
    st.rerun()

# Crear modelo con la configuración
chat_model = ChatGoogleGenerativeAI(
    model=st.session_state.modelo,
    temperature=st.session_state.temperatura
)

# Inicializar historial
if "mensajes" not in st.session_state:
    st.session_state.mensajes = [personalidad]

# Mostrar historial de mensajes
for msg in st.session_state.mensajes:
    rol = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(rol):
        st.markdown(msg.content)

# Entrada del usuario
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
