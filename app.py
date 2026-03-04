import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import base64

# --- CONFIGURAÇÕES ---
st.set_page_config(page_title="Gerador SECOM - Pro", layout="centered")

# --- CSS ESTILO GEMINI (DARK MODE & GLASSMORPHISM) ---
st.markdown(f"""
    <style>
    /* 1. Fundo Geral (Cinza Escuro Profundo) */
    [data-testid="stAppViewContainer"] {{
        background-color: #131314; /* Cor oficial do fundo do Gemini */
        background-image: radial-gradient(circle at top right, #1e1e20, #131314);
    }}
    
    [data-testid="stHeader"], [data-testid="stToolbar"] {{visibility: hidden;}}

    /* 3. Textos */
    .emoji {{ font-size: 50px; margin-bottom: 10px; }}
    .titulo {{ 
        color: #e3e3e3; 
        font-family: 'Google Sans', sans-serif;
        font-size: 22px;
        font-weight: 500;
        margin-bottom: 30px;
    }}

    /* 4. Customização dos Inputs (Estilo Dark) */
    .stTextInput label, .stFileUploader label {{
        color: #e3e3e3 !important;
        font-weight: 400 !important;
    }}

    .stTextInput input {{
        background-color: #1e1f20 !important;
        border: 1px solid #444746 !important;
        border-radius: 12px !important;
        color: white !important;
        padding: 12px !important;
    }}

    /* Botão com degradê estilo IA */
    .stButton > button {{
        background: linear-gradient(90deg, #4285f4, #9b72cb, #d96570);
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        width: 100% !important;
        height: 50px !important;
        margin-top: 20px;
        transition: transform 0.2s;
    }}
    
    .stButton > button:hover {{
        transform: scale(1.02);
        box-shadow: 0 0 15px rgba(66, 133, 244, 0.4);
    }}

    /* Drag and Drop Dark */
    .stFileUploader section {{
        background-color: #1e1f20 !important;
        border: 1px dashed #444746 !important;
        border-radius: 12px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- ESTRUTURA DA INTERFACE ---

st.markdown('<div class="gemini-card">', unsafe_allow_html=True)

st.markdown('<div class="emoji">✨</div>', unsafe_allow_html=True)
st.markdown('<div class="titulo">Gerador de Artes SECOM</div>', unsafe_allow_html=True)

nome = st.text_input("Nome do Aniversariante", placeholder="Digite o nome completo...")
cargo = st.text_input("Cargo ou Setor", placeholder="Ex: Coordenação de Comunicação")
foto_upload = st.file_uploader("Escolha uma foto", type=["jpg", "png", "jpeg"])

gerar_arte = st.button("GERAR ARTE")

st.markdown("<p style='color:#8e918f; font-size:12px; margin-top:25px;'>Inteligência e Design • SECOM 2024</p>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- MOTOR DE GERAÇÃO (Pillow) ---
if gerar_arte:
    if foto_upload and nome and cargo:
        with st.spinner('Processando arte...'):
            try:
                # Carrega arquivos
                base = Image.open("template.png").convert("RGBA")
                foto = Image.open(foto_upload).convert("RGBA")
                
                # Ajuste da foto (Redimensionar e girar -4 graus)
                foto = foto.resize((995, 995), Image.LANCZOS)
                foto = foto.rotate(4, resample=Image.BICUBIC, expand=True)
                
                # Composição
                final = Image.new("RGBA", base.size, (0,0,0,0))
                final.paste(foto, (35, 275), foto)
                final = Image.alpha_composite(final, base)
                
                # Texto
                draw = ImageDraw.Draw(final)
                try:
                    f_nome = ImageFont.truetype("Poppins-Bold.ttf", 60)
                    f_cargo = ImageFont.truetype("Poppins-Regular.ttf", 34)
                    
                    # Centralizar Nome
                    w_n = draw.textbbox((0,0), nome, font=f_nome)[2]
                    draw.text(((1080 - w_n)/2, 1115), nome, fill="white", font=f_nome)
                    
                    # Centralizar Cargo
                    w_c = draw.textbbox((0,0), cargo.upper(), font=f_cargo)[2]
                    draw.text(((1080 - w_c)/2, 1200), cargo.upper(), font=f_cargo, fill="white")
                except:
                    st.warning("Usando fonte padrão do sistema.")

                # Resultado
                st.markdown("---")
                st.image(final, caption="Sua arte personalizada", use_container_width=True)
                
                buf = io.BytesIO()
                final.save(buf, format="PNG")
                st.download_button("📥 Baixar Arte Final", buf.getvalue(), f"niver_{nome}.png", "image/png")
                
            except Exception as e:
                st.error(f"Ocorreu um erro: {e}")
    else:
        st.info("Preencha todos os campos para continuar.")

