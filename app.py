import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import base64

# --- CONFIGURAÇÕES ---
st.set_page_config(page_title="Gerador SECOM", layout="centered")

def carregar_imagem_local(caminho):
    try:
        with open(caminho, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

bg_base64 = carregar_imagem_local("background.jpg")

# --- INTERFACE HTML/CSS RESPONSIVA ---
st.markdown(f"""
    <style>
    /* 1. Fundo da Página */
    [data-testid="stAppViewContainer"] {{
        background: url("data:image/png;base64,{bg_base64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    [data-testid="stHeader"], [data-testid="stToolbar"] {{visibility: hidden;}}

    /* 2. Reset de containers do Streamlit para Mobile */
    [data-testid="stVerticalBlock"] {{
        padding: 0px !important;
        gap: 0px !important;
    }}

    /* 3. O Container Branco "Mestre" */
    .main-card {{
        background: white;
        border-radius: 35px;
        padding: 30px;
        box-shadow: 0px 20px 50px rgba(0,0,0,0.3);
        text-align: center;
        width: 90%; /* Ocupa 90% da tela no mobile */
        max-width: 420px; /* Limite de largura no desktop */
        margin: 40px auto; /* Centraliza vertical e horizontalmente */
        font-family: 'Segoe UI', sans-serif;
        position: relative;
        z-index: 10;
    }}

    /* Estilo dos textos internos */
    .emoji {{ font-size: 50px; margin-bottom: 5px; }}
    .titulo {{ 
        font-weight: bold; 
        color: #222; 
        margin-bottom: 20px; 
        font-size: 1.2rem; 
        padding: 0 10px;
    }}

    /* Ajuste para que os inputs do Streamlit fiquem dentro do card */
    .stTextInput, .stFileUploader, .stButton {{
        margin-bottom: 15px !important;
    }}

    /* Estilização dos campos */
    ::placeholder {{ color: #888 !important; }}
    
    .stTextInput input {{
        background-color: #F0F2F5 !important;
        border: none !important;
        border-radius: 12px !important;
    }}
    
    .stButton > button {{
        background-color: #00A3FF !important;
        color: white !important;
        border-radius: 15px !important;
        width: 100% !important;
        font-weight: bold !important;
        height: 50px;
    }}

    /* Ajustes Mobile */
    @media (max-width: 480px) {{
        .main-card {{
            padding: 20px 15px;
            margin: 20px auto;
        }}
        .titulo {{ font-size: 1rem; }}
    }}
    </style>
    """, unsafe_allow_html=True)

# --- ESTRUTURA DO SITE ---

# Abrimos a "casca" branca
st.markdown('<div class="main-card">', unsafe_allow_html=True)

# Conteúdo do Topo
st.markdown('<div class="emoji">🥳</div>', unsafe_allow_html=True)
st.markdown('<div class="titulo">Gerador de Artes para os Aniversariantes Automático!</div>', unsafe_allow_html=True)

# Inputs (O Streamlit vai colocar eles aqui dentro)
nome = st.text_input("Nome e Sobrenome", placeholder="Ex: Fulano Primeiro...")
cargo = st.text_input("Cargo", placeholder="Ex: Secretária de...")
foto_upload = st.file_uploader("Suba a foto aqui", type=["jpg", "png", "jpeg"])

# Botão de Gerar
gerar_arte = st.button("🚀 CRIAR ARTE AGORA")

st.markdown("<p style='color:#999; font-size:11px; margin-top:20px;'>Desenvolvido por <b>SECOM</b></p>", unsafe_allow_html=True)

# Fechamos a "casca" branca
st.markdown('</div>', unsafe_allow_html=True)


# --- LÓGICA DO MOTOR (FORA DO CARD PARA NÃO EMPURRAR O LAYOUT) ---
if gerar_arte:
    if not foto_upload or not nome or not cargo:
        st.error("Preencha todos os campos!")
    else:
        with st.spinner('Gerando...'):
            try:
                base = Image.open("template.png").convert("RGBA")
                foto = Image.open(foto_upload).convert("RGBA")
                
                # Motor de redimensionamento e rotação
                foto = foto.resize((995, 995), Image.LANCZOS)
                foto = foto.rotate(-4, resample=Image.BICUBIC, expand=True)
                
                canvas = Image.new("RGBA", base.size, (0,0,0,0))
                canvas.paste(foto, (35, 275), foto)
                final = Image.alpha_composite(canvas, base)
                
                draw = ImageDraw.Draw(final)
                try:
                    f_nome = ImageFont.truetype("Poppins-Bold.ttf", 60)
                    f_cargo = ImageFont.truetype("Poppins-Regular.ttf", 34)
                    
                    w_n = draw.textbbox((0,0), nome, font=f_nome)[2]
                    draw.text(((1080 - w_n)/2, 1115), nome, fill="white", font=f_nome)
                    
                    w_c = draw.textbbox((0,0), cargo.upper(), font=f_cargo)[2]
                    draw.text(((1080 - w_c)/2, 1200), cargo.upper(), font=f_cargo, fill="white")
                except:
                    pass

                # Prévia embaixo de tudo
                st.markdown("### ✅ Prévia da sua Arte")
                st.image(final, use_container_width=True)
                
                buf = io.BytesIO()
                final.save(buf, format="PNG")
                st.download_button("📥 Baixar Imagem", buf.getvalue(), f"{nome}.png", "image/png")
                
            except Exception as e:
                st.error(f"Erro: {e}")
