import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import base64

# --- CONFIGURAÇÕES ---
st.set_page_config(page_title="Gerador SECOM", layout="centered")

# Função para converter imagem local para Base64 (pro CSS ler)
def carregar_imagem_local(caminho):
    try:
        with open(caminho, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

# Carregando as imagens para o fundo
bg_base64 = carregar_imagem_local("background.jpg")

# --- INTERFACE HTML/CSS (O SEU DESIGN) ---
# Aqui você tem controle total de cada pixel
st.markdown(f"""
    <style>
    /* Reset do Streamlit para aceitar seu design */
    [data-testid="stAppViewContainer"] {{
        background: url("data:image/png;base64,{bg_base64}");
        background-size: cover;
        background-position: center;
    }}
    
    [data-testid="stHeader"], [data-testid="stToolbar"] {{visibility: hidden;}}

    /* Seu Card do Figma em CSS */
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
    .titulo {{ font-weight: bold; color: #222; margin-bottom: 25px; line-height: 1.2; }}
    .label-custom {{ text-align: left; color: #666; font-size: 14px; margin-bottom: 5px; font-weight: 600; }}
    
    /* Estilizando os inputs do Streamlit para parecerem HTML puro */
    .stTextInput input {{
        background-color: #F0F2F5 !important;
        border: none !important;
        border-radius: 12px !important;
    }}
    
    .stFileUploader section {{
        background-color: #00A3FF !important;
        border: none !important;
        border-radius: 15px !important;
        color: white !important;
    }}
    </style>

    <div class="figma-container">
        <div class="emoji">🥳</div>
        <div class="titulo">Gerador de Artes para os Aniversariantes Automático!</div>
    </div>
    """, unsafe_allow_html=True)

# --- O MOTOR EM PYTHON ---
# Os inputs ficam logo abaixo do título no seu card
with st.container():
    # Colocamos os inputs em colunas se quiser ou direto
    nome = st.text_input("Nome e Sobrenome", placeholder="Ex: Fulano Primeiro...")
    cargo = st.text_input("Cargo", placeholder="Ex: Secretária de...")
    foto_upload = st.file_uploader("Suba a foto aqui", type=["jpg", "png", "jpeg"])

    st.markdown("<p style='text-align:center; color:#999; font-size:12px; margin-top:20px;'>Desenvolvido por <b>SECOM</b></p>", unsafe_allow_html=True)

# --- LÓGICA DE PROCESSAMENTO ---
if foto_upload and nome and cargo:
    try:
        # Carrega o template
        base = Image.open("template.png").convert("RGBA")
        
        # Processa a foto
        foto = Image.open(foto_upload).convert("RGBA")
        foto = foto.resize((995, 995), Image.LANCZOS)
        foto = foto.rotate(4, resample=Image.BICUBIC, expand=True)
        
        # Cria a composição
        canvas = Image.new("RGBA", base.size, (0,0,0,0))
        canvas.paste(foto, (35, 275), foto)
        final = Image.alpha_composite(canvas, base)
        
        # Escreve os nomes
        draw = ImageDraw.Draw(final)
        try:
            f_nome = ImageFont.truetype("Poppins-Bold.ttf", 60)
            f_cargo = ImageFont.truetype("Poppins-Regular.ttf", 34)
            
            # Centralização X (Template tem 1080px de largura)
            w_n = draw.textbbox((0,0), nome, font=f_nome)[2]
            draw.text(((1080 - w_n)/2, 1115), nome, fill="white", font=f_nome)
            
            w_c = draw.textbbox((0,0), cargo.upper(), font=f_cargo)[2]
            draw.text(((1080 - w_c)/2, 1200), cargo.upper(), font=f_cargo, fill="white")
        except:
            pass # Usa fonte padrão se falhar

        # Exibe resultado
        st.write("---")
        st.image(final, use_container_width=True)
        
        # Botão de Download
        buf = io.BytesIO()
        final.save(buf, format="PNG")
        st.download_button("📥 Baixar Arte Pronta", buf.getvalue(), f"niver_{nome}.png", "image/png")
        
    except Exception as e:
        st.error(f"Erro no motor: {e}")
