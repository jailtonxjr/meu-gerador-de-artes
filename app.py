import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps
import io

# --- CONFIGURAÇÕES DE PÁGINA ---
st.set_page_config(page_title="Gerador SECOM - Pro", layout="centered")

# --- CSS ESTILO GEMINI (CENTRALIZAÇÃO ABSOLUTA) ---
st.markdown(f"""
    <style>
    /* 1. Fundo Geral Estilo Gemini */
    [data-testid="stAppViewContainer"] {{
        background-color: #131314;
        background-image: radial-gradient(circle at top right, #1e1e20, #131314);
    }}
    
    [data-testid="stHeader"], [data-testid="stToolbar"] {{visibility: hidden;}}

    /* 2. Centralização de Textos */
    .emoji {{ 
        font-size: 65px; 
        text-align: center;
        display: block;
        margin-top: 30px;
    }}
    .titulo {{ 
        color: #e3e3e3; 
        font-family: 'Google Sans', sans-serif;
        font-size: 26px;
        font-weight: 500;
        margin-bottom: 40px;
        text-align: center;
    }}

    /* 3. Estilização dos Inputs (Dark Mode) */
    .stTextInput label, .stFileUploader label {{
        color: #e3e3e3 !important;
        text-align: center !important;
        display: block !important;
        width: 100% !important;
    }}

    .stTextInput input {{
        background-color: #1e1f20 !important;
        border: 1px solid #444746 !important;
        border-radius: 12px !important;
        color: white !important;
        text-align: center;
        height: 48px;
    }}

    /* 4. CENTRALIZAÇÃO TOTAL DO BOTÃO (FORÇA BRUTA) */
    /* Faz o container do botão ocupar toda a largura horizontal */
    [data-testid="stVerticalBlock"] > div:has(div.stButton), .stButton {{
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }}

    .stButton > button {{
        background: linear-gradient(90deg, #4285f4, #9b72cb, #d96570);
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 12px 60px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        transition: 0.3s ease;
        width: auto !important;
        min-width: 250px;
        margin-top: 20px;
    }}
    
    .stButton > button:hover {{
        transform: scale(1.05);
        box-shadow: 0 0 25px rgba(66, 133, 244, 0.4);
    }}

    /* Estilização do Drag and Drop */
    .stFileUploader section {{
        background-color: #1e1f20 !important;
        border: 1px dashed #444746 !important;
        border-radius: 12px !important;
    }}

    .footer-text {{
        color: #8e918f;
        font-size: 12px;
        margin-top: 40px;
        text-align: center;
        padding-bottom: 50px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- INTERFACE VISUAL ---
st.markdown('<span class="emoji">🥳</span>', unsafe_allow_html=True)
st.markdown('<div class="titulo">Gerador de Artes SECOM</div>', unsafe_allow_html=True)

nome = st.text_input("Nome do Aniversariante", placeholder="Digite o nome aqui...")
cargo = st.text_input("Cargo ou Setor", placeholder="Ex: Coordenação de Comunicação")
foto_upload = st.file_uploader("Suba a foto do aniversariante", type=["jpg", "png", "jpeg"])

# Botão Centralizado
gerar_arte = st.button("GERAR ARTE")

st.markdown('<div class="footer-text">Desenvolvido por Júnior • SECOM 2026</div>', unsafe_allow_html=True)

# --- MOTOR DE GERAÇÃO (CORTE REDONDO SEM DISTORÇÃO) ---
if gerar_arte:
    if foto_upload and nome and cargo:
        with st.spinner('Processando imagem...'):
            try:
                # 1. Carregar arquivos
                base = Image.open("template.png").convert("RGBA")
                foto_img = Image.open(foto_upload).convert("RGBA")
                
               # 2. Corte Central (Center Crop) Quadrado
                # Mantém a proporção e garante que a foto vire um quadrado de 995x995
                tamanho_alvo = 995
                foto_final = ImageOps.fit(foto_img, (tamanho_alvo, tamanho_alvo), Image.LANCZOS)
                
                # 3. Rotação (Ajuste para alinhar com a moldura inclinada)
                # Removendo a máscara, a foto agora rotaciona com os cantos retos (90°)
                foto_final = foto_final.rotate(4, resample=Image.BICUBIC, expand=True) 
                
                # 4. Composição
                canvas = Image.new("RGBA", base.size, (0,0,0,0))
                # Aqui a foto entra no seu template sem o corte redondo
                canvas.paste(foto_final, (35, 275), foto_final)
                
                # 5. Composição no Template
                canvas = Image.new("RGBA", base.size, (0,0,0,0))
                # Coordenadas X, Y para encaixar no buraco do template
                canvas.paste(foto_final, (25, 270), foto_final) 
                arte_final = Image.alpha_composite(canvas, base)
                
                # 6. Escrever Textos Centralizados
                draw = ImageDraw.Draw(arte_final)
                try:
                    f_nome = ImageFont.truetype("Poppins-Bold.ttf", 60)
                    f_cargo = ImageFont.truetype("Poppins-Regular.ttf", 34)
                    
                    # Nome
                    w_n = draw.textbbox((0,0), nome, font=f_nome)[2]
                    draw.text(((1080 - w_n)/2, 1115), nome, fill="white", font=f_nome)
                    
                    # Cargo
                    w_c = draw.textbbox((0,0), cargo.upper(), font=f_cargo)[2]
                    draw.text(((1080 - w_c)/2, 1200), cargo.upper(), font=f_cargo, fill="white")
                except:
                    st.warning("Fontes Poppins não encontradas. Verifique se os arquivos .ttf estão na pasta.")

                # 7. Exibição da Prévia e Download
                st.markdown("---")
                st.image(arte_final, caption="Sua arte foi gerada!", use_container_width=True)
                
                buf = io.BytesIO()
                arte_final.save(buf, format="PNG")
                
                # Botão de download também centralizado pelo CSS acima
                st.download_button(
                    label="📥 Baixar Arte Final",
                    data=buf.getvalue(),
                    file_name=f"niver_{nome}.png",
                    mime="image/png"
                )
                
            except Exception as e:
                st.error(f"Erro no processamento: {e}")
    else:
        st.warning("⚠️ Preencha todos os campos e selecione uma foto antes de continuar.")



