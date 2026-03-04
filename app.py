import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# --- CONFIGURAÇÕES ---
st.set_page_config(page_title="Gerador SECOM - Pro", layout="centered")

# --- CSS ESTILO GEMINI (CENTRALIZAÇÃO TOTAL) ---
st.markdown(f"""
    <style>
    /* 1. Fundo Geral */
    [data-testid="stAppViewContainer"] {{
        background-color: #131314;
        background-image: radial-gradient(circle at top right, #1e1e20, #131314);
    }}
    
    [data-testid="stHeader"], [data-testid="stToolbar"] {{visibility: hidden;}}

    /* 3. Textos (Emoji e Título) */
    .emoji {{ 
        font-size: 60px; 
        margin-bottom: 5px; 
        text-align: center;
        display: block;
        width: 100%;
    }}
    .titulo {{ 
        color: #e3e3e3; 
        font-family: 'Google Sans', sans-serif;
        font-size: 24px;
        font-weight: 500;
        margin-bottom: 30px;
        width: 100%;
        text-align: center;
    }}

    /* 4. Centralizando os Labels e Inputs */
    .stTextInput, .stFileUploader {{
        width: 100%;
    }}
    
    .stTextInput label, .stFileUploader label {{
        color: #e3e3e3 !important;
        width: 100% !important;
        display: block !important;
        text-align: center !important; /* Centraliza o texto do label */
    }}

    .stTextInput input {{
        background-color: #1e1f20 !important;
        border: 1px solid #444746 !important;
        border-radius: 12px !important;
        color: white !important;
        text-align: center; /* Centraliza o cursor dentro do input */
    }}

    /* 5. BOTÃO GERAR CENTRALIZADO */
    .stButton {{
        width: 100%;
        display: flex;
        justify-content: center;
        width: 100%;
    }}

    .stButton > button {{
        background: linear-gradient(90deg, #4285f4, #9b72cb, #d96570);
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 12px 40px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        width: 100% !important;
        max-width: 280px; /* Largura do botão */
        height: 54px !important;
        margin-top: 20px;
        transition: 0.3s;
    }}
    
    .stButton > button:hover {{
        transform: scale(1.05);
        box-shadow: 0 0 20px rgba(66, 133, 244, 0.5);
    }}

    /* Drag and Drop Dark */
    .stFileUploader section {{
        background-color: #1e1f20 !important;
        border: 1px dashed #444746 !important;
        border-radius: 12px !important;
    }}

    .footer-text {{
        color: #8e918f;
        font-size: 12px;
        margin-top: 25px;
        width: 100%;
        text-align: center;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- ESTRUTURA DA INTERFACE ---

st.markdown('<div class="gemini-card">', unsafe_allow_html=True)

st.markdown('<span class="emoji">🥳</span>', unsafe_allow_html=True)
st.markdown('<div class="titulo">Gerador de Artes SECOM</div>', unsafe_allow_html=True)

nome = st.text_input("Nome do Aniversariante", placeholder="Digite aqui...")
cargo = st.text_input("Cargo ou Setor", placeholder="Ex: Coordenação...")
foto_upload = st.file_uploader("Escolha uma foto", type=["jpg", "png", "jpeg"])

gerar_arte = st.button("GERAR ARTE")

st.markdown('<div class="footer-text">Desenvolvido por Júnior - SECOM</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# --- CONFIGURAÇÕES ---
st.set_page_config(page_title="Gerador SECOM - Pro", layout="centered")

# --- CSS ESTILO GEMINI (CENTRALIZAÇÃO TOTAL) ---
st.markdown(f"""
    <style>
    /* 1. Fundo Geral */
    [data-testid="stAppViewContainer"] {{
        background-color: #131314;
        background-image: radial-gradient(circle at top right, #1e1e20, #131314);
    }}
    
    [data-testid="stHeader"], [data-testid="stToolbar"] {{visibility: hidden;}}

    /* 2. CARD CENTRALIZADO (O segredo está aqui) */
    .gemini-card {{
        background: rgba(30, 31, 32, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 28px;
        padding: 40px 30px;
        width: 100%;
        max-width: 450px;
        margin: auto;
        display: flex; /* Habilita o Flexbox */
        flex-direction: column; /* Empilha os itens */
        align-items: center; /* Centraliza horizontalmente */
        justify-content: center;
    }}

    /* 3. Textos (Emoji e Título) */
    .emoji {{ 
        font-size: 60px; 
        margin-bottom: 5px; 
        text-align: center;
        display: block;
        width: 100%;
    }}
    .titulo {{ 
        color: #e3e3e3; 
        font-family: 'Google Sans', sans-serif;
        font-size: 24px;
        font-weight: 500;
        margin-bottom: 30px;
        width: 100%;
        text-align: center;
    }}

    /* 4. Centralizando os Labels e Inputs */
    .stTextInput, .stFileUploader {{
        width: 100%;
    }}
    
    .stTextInput label, .stFileUploader label {{
        color: #e3e3e3 !important;
        width: 100% !important;
        display: block !important;
        text-align: center !important; /* Centraliza o texto do label */
    }}

    .stTextInput input {{
        background-color: #1e1f20 !important;
        border: 1px solid #444746 !important;
        border-radius: 12px !important;
        color: white !important;
        text-align: center; /* Centraliza o cursor dentro do input */
    }}

    /* 5. BOTÃO GERAR CENTRALIZADO */
    .stButton {{
        display: flex;
        justify-content: center;
        width: 100%;
    }}

    .stButton > button {{
        background: linear-gradient(90deg, #4285f4, #9b72cb, #d96570);
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 12px 40px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        width: 100% !important;
        max-width: 280px; /* Largura do botão */
        height: 54px !important;
        margin-top: 20px;
        transition: 0.3s;
    }}
    
    .stButton > button:hover {{
        transform: scale(1.05);
        box-shadow: 0 0 20px rgba(66, 133, 244, 0.5);
    }}

    /* Drag and Drop Dark */
    .stFileUploader section {{
        background-color: #1e1f20 !important;
        border: 1px dashed #444746 !important;
        border-radius: 12px !important;
    }}

    .footer-text {{
        color: #8e918f;
        font-size: 12px;
        margin-top: 25px;
        width: 100%;
        text-align: center;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- ESTRUTURA DA INTERFACE ---

st.markdown('<div class="gemini-card">', unsafe_allow_html=True)

st.markdown('<span class="emoji">🥳</span>', unsafe_allow_html=True)
st.markdown('<div class="titulo">Gerador de Artes SECOM</div>', unsafe_allow_html=True)

nome = st.text_input("Nome do Aniversariante", placeholder="Digite aqui...")
cargo = st.text_input("Cargo ou Setor", placeholder="Ex: Coordenação...")
foto_upload = st.file_uploader("Escolha uma foto", type=["jpg", "png", "jpeg"])

gerar_arte = st.button("GERAR ARTE")

st.markdown('<div class="footer-text">Desenvolvido por Júnior - SECOM</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- MOTOR DE GERAÇÃO ---
if gerar_arte:
    if foto_upload and nome and cargo:
        with st.spinner('Construindo arte...'):
            try:
                base = Image.open("template.png").convert("RGBA")
                foto = Image.open(foto_upload).convert("RGBA")
                
                foto = foto.resize((995, 995), Image.LANCZOS)
                foto = foto.rotate(4, resample=Image.BICUBIC, expand=True) 
                
                final = Image.new("RGBA", base.size, (0,0,0,0))
                final.paste(foto, (35, 275), foto) 
                final = Image.alpha_composite(final, base)
                
                draw = ImageDraw.Draw(final)
                try:
                    f_nome = ImageFont.truetype("Poppins-Bold.ttf", 60)
                    f_cargo = ImageFont.truetype("Poppins-Regular.ttf", 34)
                    
                    w_n = draw.textbbox((0,0), nome, font=f_nome)[2]
                    draw.text(((1080 - w_n)/2, 1115), nome, fill="white", font=f_nome)
                    
                    w_c = draw.textbbox((0,0), cargo.upper(), font=f_cargo)[2]
                    draw.text(((1080 - w_c)/2, 1200), cargo.upper(), font=f_cargo, fill="white")
                except:
                    st.error("Fontes não encontradas!")

                st.markdown("---")
                st.image(final, caption="Arte Gerada com Sucesso!", use_container_width=True)
                
                buf = io.BytesIO()
                final.save(buf, format="PNG")
                st.download_button("📥 Baixar Arte Final", buf.getvalue(), f"niver_{nome}.png", "image/png")
                
            except Exception as e:
                st.error(f"Erro: {e}")
    else:
        st.info("⚠️ Preencha todos os campos para gerar.")
