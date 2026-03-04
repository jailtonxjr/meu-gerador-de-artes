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
# IMPORTANTE: Coloque o link real da sua imagem aqui
LINK_BACKGROUND = "https://raw.githubusercontent.com/seu-usuario/seu-repo/main/background.jpg"

st.markdown(f"""
    <style>
    /* Fundo da Página */
    .stApp {{
        background: url("{LINK_BACKGROUND}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Container Principal (O Card Branco) */
    .main-card {{
        background-color: white;
        padding: 40px 30px;
        border-radius: 30px;
        box-shadow: 0px 15px 35px rgba(0,0,0,0.3);
        margin: 20px auto;
        width: 100%;
        max-width: 450px;
        text-align: center;
    }}

    /* Estilização de Textos e Títulos */
    .main-card h3 {{
        color: #333 !important;
        font-family: 'Poppins', sans-serif;
        margin-top: 10px;
    }}

    /* Inputs do Streamlit */
    .stTextInput input {{
        background-color: #f0f2f5 !important;
        border: none !important;
        border-radius: 10px !important;
        color: #333 !important;
    }}

    /* Botão de Upload Azul */
    .stFileUploader section {{
        background-color: #0099ff !important;
        border: none !important;
        border-radius: 15px !important;
        color: white !important;
    }}
    
    .stFileUploader label {{
        color: #444 !important;
        font-weight: 600 !important;
    }}

    /* Esconder elementos padrão */
    #MainMenu, footer, header {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

# --- CONSTRUÇÃO DO CARD (TUDO DENTRO DA DIV) ---
# Usamos um container do Streamlit para agrupar tudo visualmente
with st.container():
    # Início do Card
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    
    st.markdown('<p style="font-size: 50px; margin-bottom: 0;">🥳</p>', unsafe_allow_html=True)
    st.markdown("### Gerador de Artes para os Aniversariantes Automático!")
    
    nome = st.text_input("Nome e Sobrenome", placeholder="Ex: Fulano Primeiro...")
    cargo = st.text_input("Cargo", placeholder="Ex: Secretária de...")
    foto_upload = st.file_uploader("Suba a foto aqui", type=["jpg", "png", "jpeg"])
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<p style='color: #888; font-size: 13px;'>Desenvolvido por <b>SECOM
