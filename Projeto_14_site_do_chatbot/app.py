import os

import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# ==================================================
# CONFIGURAÇÃO
# ==================================================

load_dotenv()

st.set_page_config(
    page_title="Groq Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)

API_KEY = os.getenv("GROQ_API_KEY")
MODEL = "openai/gpt-oss-120b"

# ==================================================
# ESTILO VISUAL
# ==================================================

st.markdown(
    """
    <style>
    .stApp {
        background-color: #0e1117;
    }

    [data-testid="stHeader"] {
        background: rgba(14, 17, 23, 0.8);
    }

    .block-container {
        max-width: 900px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .hero {
        text-align: center;
        padding: 1.5rem 0 2rem 0;
    }

    .hero h1 {
        font-size: 2.6rem;
        font-weight: 800;
        margin-bottom: 0.4rem;
        background: linear-gradient(
            90deg, #60a5fa, #a78bfa
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero p {
        color: #9ca3af;
        font-size: 1rem;
    }

    [data-testid="stChatMessage"] {
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 16px;
        padding: 1rem;
        margin-bottom: 0.8rem;
    }

    [data-testid="stChatInput"] {
        border-color: #374151;
    }

    .status {
        text-align: center;
        color: #9ca3af;
        font-size: 0.8rem;
        margin-top: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==================================================
# SESSÃO E HISTÓRICO
# ==================================================

if "historico" not in st.session_state:
    st.session_state.historico = []

# ==================================================
# BARRA LATERAL
# ==================================================

with st.sidebar:
    st.title("🤖 Papo de Retardado")
    st.caption("Seu Retardado Inteligente(eu acho)")

    st.divider()

    st.markdown("### ⚙️ Configurações")
    st.write(f"**Modelo:** `{MODEL}`")
    st.write("**Provedor:** Groq")

    if st.button(
        "🗑️ Limpar conversa",
        use_container_width=True,
    ):
        st.session_state.historico = []
        st.rerun()

    st.divider()
    st.caption("Desenvolvido com Python + Streamlit")

# ==================================================
# CABEÇALHO
# ==================================================

st.markdown(
    """
    <div class="hero">
        <h1>Papo de Retardado</h1>
        <p>Converse, descubra e encontre respostas com IA.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==================================================
# VALIDAÇÃO DA API
# ==================================================

if not API_KEY:
    st.error(
        "A chave GROQ_API_KEY não foi encontrada. "
        "Configure sua chave no arquivo .env."
    )
    st.stop()

client = Groq(api_key=API_KEY)

# ==================================================
# MENSAGEM INICIAL
# ==================================================

if not st.session_state.historico:
    st.info(
        "👋 Olá! Sou seu assistente virtual. "
        "Envie uma mensagem abaixo para começar."
    )

# ==================================================
# EXIBIÇÃO DO HISTÓRICO
# ==================================================

for mensagem in st.session_state.historico:
    with st.chat_message(mensagem["role"]):
        st.markdown(mensagem["content"])

# ==================================================
# ENTRADA E RESPOSTA DO CHATBOT
# ==================================================

pergunta = st.chat_input(
    "Digite sua mensagem aqui..."
)

if pergunta:
    # Salva e exibe a pergunta do usuário
    st.session_state.historico.append(
        {
            "role": "user",
            "content": pergunta,
        }
    )

    with st.chat_message("user"):
        st.markdown(pergunta)

    # Instrução inicial do assistente
    mensagens_api = [
        {
            "role": "system",
            "content": (
                "Você é o assistente virtual deste site. "
                "Responda em português brasileiro por padrão, "
                "com clareza, educação e objetividade. "
                "Ajude o usuário a entender as funcionalidades "
                "do site e responda às perguntas recebidas. "
                "Não afirme que executou ações que não realizou."
            ),
        },
        *st.session_state.historico,
    ]

    # Chamada à API da Groq
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                resposta = client.chat.completions.create(
                    model=MODEL,
                    messages=mensagens_api,
                    temperature=0.7,
                    max_completion_tokens=2048,
                )

                texto = resposta.choices[0].message.content

                if not texto:
                    texto = "Não consegui gerar uma resposta. Tente novamente."

                st.markdown(texto)

                # Guarda a resposta para manter o contexto
                st.session_state.historico.append(
                    {
                        "role": "assistant",
                        "content": texto,
                    }
                )

            except Exception:
                st.error(
                    "Não foi possível obter uma resposta da Groq. "
                    "Verifique sua conexão, a chave da API, "
                    "o modelo configurado e os limites da conta."
                )

st.markdown(
    '<p class="status">Powered by Groq · IA conversacional</p>',
    unsafe_allow_html=True,
)