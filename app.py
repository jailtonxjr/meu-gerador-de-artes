import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import os

# --- CONFIGURAÇÕES DE PÁGINA ---
st.set_page_config(page_title="Gerador de Artes - SECOM", layout="centered")

# --- FUNÇÕES DE PROCESSAMENTO ---
def cortar_cover(img, tamanho):
    largura, altura = img.size
    alvo_l, alvo_a = tamanho
    prop_img = largura / altura
    prop_alvo = alvo_l / alvo_a
    if prop_img > prop_alvo:
        nova_l = int(altura * prop_alvo)
        x = (largura - nova_l) // 2
        img = img.crop((x, 0, x + nova_l, altura))
    else:
        nova_a = int(largura / prop_alvo)
        y = (altura - nova_a) // 2
        img = img.crop((0, y, largura, y + nova_a))
    return img.resize(tamanho, Image.LANCZOS)

def remover_preto(img):
    img = img.convert("RGBA")
    dados = img.getdata()
    novo = [(0, 0, 0, 0) if r < 40 and g < 40 and b < 40 else (r, g, b, a) for r, g, b, a in dados]
    img.putdata(novo)
    return img

# --- INTERFACE E DESIGN ---
# DICA: Substitua o link abaixo pelo link 'Raw' da sua imagem no GitHub
LINK_BACKGROUND = "https://raw.githubusercontent.com/jailtonxjr/meu-gerador-de-artes/main/background.jpg"

st.markdown(f"""
    <style>
    .stApp {{
        background: url("{LINK_BACKGROUND}");
        background-size: cover;
        background-position: center;
    }}

    .main-container {{
        background-color: white;
        padding: 40px;
        border-radius: 28px;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.2);
        max-width: 450px;
        margin: auto;
        text-align: center;
    }}

    .stTextInput input {{
        background-color: #f0f2f5 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px !important;
    }}

    .stFileUploader section {{
        background-color: #0099ff !important;
        border: none !important;
        border-radius: 15px !important;
        color: white !important;
    }}
    
    .stFileUploader label {{
        color: #555 !important;
        font-weight: bold !important;
    }}

    #MainMenu, footer, header {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

# --- CONSTRUÇÃO DO CARD ---
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# O erro estava aqui: agora usamos HTML puro para o emoji grande
st.markdown('<p style="font-size: 50px; margin: 0;">🥳</p>', unsafe_allow_html=True)
st.markdown("### Gerador de Artes para os Aniversariantes Automático!")

nome = st.text_input("Nome e Sobrenome", placeholder="Ex: Fulano Primeiro...")
cargo = st.text_input("Cargo", placeholder="Ex: Secretária de...")
foto_upload = st.file_uploader("Suba a foto aqui", type=["jpg", "png", "jpeg"])

st.markdown("<br>", unsafe_allow_html=True)
st.caption("Desenvolvido por SECOM")
st.markdown('</div>', unsafe_allow_html=True)

# --- LÓGICA DE GERAÇÃO ---
if foto_upload and nome and cargo:
    POS_FOTO = (50, 285)
    TAM_FOTO = (995, 995)
    ROT_FOTO = -4
    CENTRO_X = 540

    base = Image.open("template.png").convert("RGBA")
    template_sem_preto = remover_preto(base)
    
    foto = Image.open(foto_upload).convert("RGBA")
    foto = cortar_cover(foto, TAM_FOTO)
    foto = foto.rotate(ROT_FOTO, resample=Image.BICUBIC, expand=True)
    
    nova_l, nova_a = foto.size
    pos_ajustada = (POS_FOTO[0] - (nova_l - TAM_FOTO[0]) // 2, POS_FOTO[1] - (nova_a - TAM_FOTO[1]) // 2)
    
    fundo = Image.new("RGBA", base.size, (0,0,0,0))
    fundo.paste(foto, pos_ajustada, foto)
    arte = Image.alpha_composite(fundo, template_sem_preto)
    
    draw = ImageDraw.Draw(arte)
    try:
        f_nome = ImageFont.truetype("Poppins-Bold.ttf", 60)
        f_cargo = ImageFont.truetype("Poppins-Regular.ttf", 34)
        
        w_n = draw.textbbox((0,0), nome, font=f_nome)[2]
        draw.text((CENTRO_X - w_n/2, 1115), nome, fill="white", font=f_nome)
        
        w_c = draw.textbbox((0,0), cargo.upper(), font=f_cargo)[2]
        draw.text((CENTRO_X - w_c/2, 1200), cargo.upper(), font=f_cargo, fill="white")
    except:
        st.warning("Fontes não encontradas, usando fonte padrão.")

    st.markdown("---")
    st.image(arte, caption="Prévia da Arte", use_container_width=True)
    
    img_byte_arr = io.BytesIO()
    arte.save(img_byte_arr, format='PNG')
    st.download_button(label="✅ Baixar Arte Pronta", data=img_byte_arr.getvalue(), file_name=f"aniversariante_{nome}.png", mime="image/png")
