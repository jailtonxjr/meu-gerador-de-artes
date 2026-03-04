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

    /* 2. O Card Gemini (Centralizando o conteúdo interno) */
    .gemini-card {{
        background: rgba(30, 31, 32, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 28px;
        padding: 40px 30px;
        width: 100%;
        max-width: 450px;
        margin: auto;
        display: flex;
        flex-direction: column;
        align-items: center; /* Centraliza itens no eixo X */
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.6);
    }}

    /* 3. Textos (Emoji e Título) */
    .emoji {{ 
        font-size: 60px; 
        margin-bottom: 5px; 
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
    }}

    /* 4. Centralizando os Labels do Streamlit */
    .stTextInput label, .stFileUploader label {{
        color: #e3e3e3 !important;
        width: 100% !important;
        text-align: center !important; /* Centraliza o texto do label */
        display: block !important;
    }}

    .stTextInput input {{
        background-color: #1e1f20 !important;
        border: 1px solid #444746 !important;
        border-radius: 12px !important;
        color: white !important;
        text-align: center; /* Texto digitado centralizado */
    }}

    /* 5. Botão GERAR (Centralização e Estilo) */
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
        width: 100% !important; /* Faz o botão ocupar a largura do card */
        max-width: 250px; /* Mas limita para não ficar exagerado */
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

    /* Ajuste para o texto de rodapé */
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

# "Sanduíche" de HTML para garantir que os widgets fiquem dentro do card estilizado
st.markdown('<div class="gemini-card">', unsafe_allow_html=True)

st.markdown('<span class="emoji">✨</span>', unsafe_allow_html=True)
st.markdown('<div class="titulo">Gerador de Artes SECOM</div>', unsafe_allow_html=True)

# Widgets do Streamlit
nome = st.text_input("Nome do Aniversariante", placeholder="Digite aqui...")
cargo = st.text_input("Cargo ou Setor", placeholder="Ex: Coordenação...")
foto_upload = st.file_uploader("Escolha uma foto", type=["jpg", "png", "jpeg"])

# O botão de gerar (agora centralizado pelo CSS)
gerar_arte = st.button("GERAR ARTE")

st.markdown('<div class="footer-text">Inteligência e Design • SECOM 2024</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- MOTOR DE GERAÇÃO (Pillow) ---
if gerar_arte:
    if foto_upload and nome and cargo:
        with st.spinner('Construindo arte...'):
            try:
                # 1. Carregamento
                base = Image.open("template.png").convert("RGBA")
                foto = Image.open(foto_upload).convert("RGBA")
                
                # 2. Processamento da Foto (Redimensionar e girar)
                foto = foto.resize((995, 995), Image.LANCZOS)
                # Note: mudei para -4 ou 4 dependendo da inclinação do seu template
                foto = foto.rotate(-4, resample=Image.BICUBIC, expand=True) 
                
                # 3. Composição
                final = Image.new("RGBA", base.size, (0,0,0,0))
                # Ajuste esses números (35, 275) se a foto ficar fora do lugar
                final.paste(foto, (35, 275), foto) 
                final = Image.alpha_composite(final, base)
                
                # 4. Escrita do Texto
                draw = ImageDraw.Draw(final)
                try:
                    f_nome = ImageFont.truetype("Poppins-Bold.ttf", 60)
                    f_cargo = ImageFont.truetype("Poppins-Regular.ttf", 34)
                    
                    # Centralizar Nome (Largura do template é 1080)
                    w_n = draw.textbbox((0,0), nome, font=f_nome)[2]
                    draw.text(((1080 - w_n)/2, 1115), nome, fill="white", font=f_nome)
                    
                    # Centralizar Cargo
                    w_c = draw.textbbox((0,0), cargo.upper(), font=f_cargo)[2]
                    draw.text(((1080 - w_c)/2, 1200), cargo.upper(), font=f_cargo, fill="white")
                except:
                    st.error("Fontes não encontradas! Verifique os arquivos .ttf")

                # 5. Resultado
                st.markdown("---")
                st.image(final, caption="Arte Gerada com Sucesso!", use_container_width=True)
                
                buf = io.BytesIO()
                final.save(buf, format="PNG")
                st.download_button("📥 Baixar Arte Final", buf.getvalue(), f"niver_{nome}.png", "image/png")
                
            except Exception as e:
                st.error(f"Erro no processamento: {e}")
    else:
        st.info("⚠️ Preencha todos os campos e suba uma foto para gerar.")
