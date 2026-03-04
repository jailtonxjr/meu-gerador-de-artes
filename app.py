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

# --- INTERFACE HTML/CSS ---
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background: url("data:image/png;base64,{bg_base64}");
        background-size: cover;
        background-position: center;
    }}
    
    [data-testid="stHeader"], [data-testid="stToolbar"] {{visibility: hidden;}}

    .figma-container {{
        background: white;
        border-radius: 35px;
        padding: 40px;
        box-shadow: 0px 20px 50px rgba(0,0,0,0.3);
        text-align: center;
        max-width: 400px;
        margin: auto;
        font-family: 'Segoe UI', sans-serif;
    }}

    .emoji {{ font-size: 50px; margin-bottom: 10px; }}
    .titulo {{ font-weight: bold; color: #222; margin-bottom: 25px; line-height: 1.2; font-size: 20px; }}
    
    /* MUDANÇA DA COR DO PLACEHOLDER */
    ::placeholder {{
        color: #888888 !important; /* Cinza claro */
        opacity: 1; 
    }}

    .stTextInput input {{
        background-color: #F0F2F5 !important;
        border: none !important;
        border-radius: 12px !important;
        color: #333 !important;
    }}
    
    /* Estilo do Botão Azul de Gerar */
    .stButton > button {{
        background-color: #00A3FF !important;
        color: white !important;
        border-radius: 15px !important;
        border: none !important;
        width: 100% !important;
        height: 50px !important;
        font-weight: bold !important;
        transition: 0.3s;
    }}
    
    .stButton > button:hover {{
        background-color: #0082CC !important;
        transform: scale(1.02);
    }}

    .stFileUploader section {{
        background-color: #F0F2F5 !important;
        border: 2px dashed #00A3FF !important;
        border-radius: 15px !important;
        color: #00A3FF !important;
    }}
    </style>

    <div class="figma-container">
        <div class="emoji">🥳</div>
        <div class="titulo">Gerador de Artes para os Aniversariantes Automático!</div>
    </div>
    """, unsafe_allow_html=True)

# --- CAMPOS DE ENTRADA ---
with st.container():
    nome = st.text_input("Nome e Sobrenome", placeholder="Ex: Fulano Primeiro...")
    cargo = st.text_input("Cargo", placeholder="Ex: Secretária de...")
    foto_upload = st.file_uploader("Suba a foto aqui", type=["jpg", "png", "jpeg"])
    
    # O BOTÃO DE DISPARO
    gerar_arte = st.button("🚀 CRIAR ARTE AGORA")

    st.markdown("<p style='text-align:center; color:#999; font-size:12px; margin-top:20px;'>Desenvolvido por <b>SECOM</b></p>", unsafe_allow_html=True)

# --- LÓGICA DO MOTOR (SÓ EXECUTA SE CLICAR NO BOTÃO) ---
if gerar_arte:
    if not foto_upload or not nome or not cargo:
        st.warning("⚠️ Por favor, preencha todos os campos e suba uma foto antes de gerar!")
    else:
        with st.spinner('Construindo sua arte...'):
            try:
                # Motor de Imagem
                base = Image.open("template.png").convert("RGBA")
                
                # Processamento da Foto
                foto = Image.open(foto_upload).convert("RGBA")
                foto = foto.resize((995, 995), Image.LANCZOS)
                foto = foto.rotate(4, resample=Image.BICUBIC, expand=True)
                
                # Composição
                canvas = Image.new("RGBA", base.size, (0,0,0,0))
                canvas.paste(foto, (35, 275), foto)
                final = Image.alpha_composite(canvas, base)
                
                # Textos
                draw = ImageDraw.Draw(final)
                try:
                    f_nome = ImageFont.truetype("Poppins-Bold.ttf", 60)
                    f_cargo = ImageFont.truetype("Poppins-Regular.ttf", 34)
                    
                    w_n = draw.textbbox((0,0), nome, font=f_nome)[2]
                    draw.text(((1080 - w_n)/2, 1115), nome, fill="white", font=f_nome)
                    
                    w_c = draw.textbbox((0,0), cargo.upper(), font=f_cargo)[2]
                    draw.text(((1080 - w_c)/2, 1200), cargo.upper(), font=f_cargo, fill="white")
                except:
                    st.error("Fontes não encontradas! Verifique os arquivos .ttf")

                # EXIBIÇÃO DA PRÉVIA
                st.write("---")
                st.image(final, caption="Sua arte está pronta!", use_container_width=True)
                
                # BOTÃO DE DOWNLOAD
                buf = io.BytesIO()
                final.save(buf, format="PNG")
                st.download_button("📥 Baixar Imagem", buf.getvalue(), f"niver_{nome}.png", "image/png")
                
            except Exception as e:
                st.error(f"Erro ao processar: {e}")
