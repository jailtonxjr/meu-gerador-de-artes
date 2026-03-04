import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps
import io

# --- CONFIGURAÇÕES DE PÁGINA ---
st.set_page_config(page_title="Gerador SECOM - Pro", layout="centered")

# --- CSS ESTILO GEMINI (SEM CARD, APENAS INTERFACE LIMPA) ---
st.markdown(f"""
    <style>
    /* 1. Fundo Geral Estilo Gemini */
    [data-testid="stAppViewContainer"] {{
        background-color: #131314;
        background-image: radial-gradient(circle at top right, #1e1e20, #131314);
    }}
    
    [data-testid="stHeader"], [data-testid="stToolbar"] {{visibility: hidden;}}

    /* 2. Centralização de Textos e Widgets */
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
        font-weight: 400 !important;
    }}

    .stTextInput input {{
        background-color: #1e1f20 !important;
        border: 1px solid #444746 !important;
        border-radius: 12px !important;
        color: white !important;
        text-align: center;
        height: 48px;
    }}

    /* 4. Botão GERAR (Degradê Centralizado) */
    .stButton {{
        display: flex;
        justify-content: center;
        margin-top: 30px;
    }}

    .stButton > button {{
        background: linear-gradient(90deg, #4285f4, #9b72cb, #d96570);
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 12px 60px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        transition: 0.3s;
    }}
    
    .stButton > button:hover {{
        transform: scale(1.05);
        box-shadow: 0 0 25px rgba(66, 133, 244, 0.4);
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
        margin-top: 40px;
        text-align: center;
        padding-bottom: 50px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- INTERFACE VISUAL ---
st.markdown('<span class="emoji">🥳</span>', unsafe_allow_html=True)
st.markdown('<div class="titulo">Gerador de Artes SECOM</div>', unsafe_allow_html=True)

# Widgets centralizados automaticamente pelo layout=centered
nome = st.text_input("Nome do Aniversariante", placeholder="Digite o nome aqui...")
cargo = st.text_input("Cargo ou Setor", placeholder="Ex: Coordenação de Comunicação")
foto_upload = st.file_uploader("Suba a foto do aniversariante", type=["jpg", "png", "jpeg"])

gerar_arte = st.button("GERAR ARTE")

st.markdown('<div class="footer-text">Desenvolvido por Júnior • SECOM 2024</div>', unsafe_allow_html=True)

# --- MOTOR DE GERAÇÃO (LÓGICA DE MÁSCARA REDONDA) ---
if gerar_arte:
    if foto_upload and nome and cargo:
        with st.spinner('Processando imagem e textos...'):
            try:
                # 1. Carregar Template e Foto
                base = Image.open("template.png").convert("RGBA")
                foto_img = Image.open(foto_upload).convert("RGBA")
                
                # 2. Lógica de Center Crop (Corte Centralizado)
                # Mantém a proporção sem achatar a pessoa
                tamanho_alvo = 995
                foto_img = ImageOps.fit(foto_img, (tamanho_alvo, tamanho_alvo), Image.LANCZOS)
                
                # 3. Criar Máscara Circular (Deixa a foto redonda)
                mask = Image.new('L', (tamanho_alvo, tamanho_alvo), 0)
                draw_mask = ImageDraw.Draw(mask)
                draw_mask.ellipse((0, 0, tamanho_alvo, tamanho_alvo), fill=255)
                
                # Aplica a máscara na foto cortada
                foto_redonda = Image.new("RGBA", (tamanho_alvo, tamanho_alvo), (0,0,0,0))
                foto_redonda.paste(foto_img, (0, 0), mask)
                
                # 4. Rotação (Ajuste para 4 graus se o seu template for inclinado)
                # Se o seu template for reto, mude para 0
                foto_final = foto_redonda.rotate(4, resample=Image.BICUBIC, expand=True) 
                
                # 5. Composição no Canvas
                # (35, 275) são as coordenadas X, Y onde a foto "encaixa" no template
                canvas = Image.new("RGBA", base.size, (0,0,0,0))
                canvas.paste(foto_final, (35, 275), foto_final) 
                arte_final = Image.alpha_composite(canvas, base)
                
                # 6. Escrever Textos
                draw = ImageDraw.Draw(arte_final)
                try:
                    f_nome = ImageFont.truetype("Poppins-Bold.ttf", 60)
                    f_cargo = ImageFont.truetype("Poppins-Regular.ttf", 34)
                    
                    # Centralizar texto no template (Largura 1080px)
                    w_n = draw.textbbox((0,0), nome, font=f_nome)[2]
                    draw.text(((1080 - w_n)/2, 1115), nome, fill="white", font=f_nome)
                    
                    w_c = draw.textbbox((0,0), cargo.upper(), font=f_cargo)[2]
                    draw.text(((1080 - w_c)/2, 1200), cargo.upper(), font=f_cargo, fill="white")
                except:
                    st.warning("Fontes Poppins não encontradas. Usando fonte padrão.")

                # 7. Exibição e Download
                st.markdown("---")
                st.image(arte_final, caption="Arte Pronta para Compartilhar", use_container_width=True)
                
                buf = io.BytesIO()
                arte_final.save(buf, format="PNG")
                st.download_button(
                    label="📥 Baixar em Alta Resolução",
                    data=buf.getvalue(),
                    file_name=f"niver_{nome}.png",
                    mime="image/png"
                )
                
            except Exception as e:
                st.error(f"Erro no processamento: {e}")
    else:
        st.warning("⚠️ Por favor, preencha todos os campos e selecione uma foto.")
