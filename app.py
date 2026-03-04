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

# --- INTERFACE E DESIGN (A MÁGICA ESTÁ AQUI) ---
# DICA: Verifique se o nome da imagem no seu GitHub é exatamente background.jpg
LINK_BACKGROUND = "https://raw.githubusercontent.com/jailtonxjr/meu-gerador-de-artes/main/background.jpg"

st.markdown(f"""
    <style>
    /* 1. Fundo da Página */
    .stApp {{
        background: url("{LINK_BACKGROUND}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* 2. Transformando o bloco principal no seu Card Branco */
    [data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {{
        background-color: white;
        padding: 50px 30px !important;
        border-radius: 30px;
        box-shadow: 0px 15px 35px rgba(0,0,0,0.3);
        max-width: 480px;
        margin: auto;
    }}

    /* 3. Estilizando Títulos e Textos */
    h3 {{
        color: #333 !important;
        text-align: center;
        font-family: 'Poppins', sans-serif;
    }}
    
    .stMarkdown p {{
        text-align: center;
    }}

    /* 4. Inputs e Botões */
    .stTextInput input {{
        background-color: #f0f2f5 !important;
        border: none !important;
        border-radius: 10px !important;
        color: #333 !important;
    }}

    .stFileUploader section {{
        background-color: #0099ff !important;
        border: none !important;
        border-radius: 15px !important;
        color: white !important;
    }}

    /* Esconde cabeçalhos e menus padrão do Streamlit */
    header, footer, #MainMenu {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

# --- CONTEÚDO DO SITE ---
# O emoji e o título
st.markdown('<p style="font-size: 60px; margin: 0;">🥳</p>', unsafe_allow_html=True)
st.markdown("### Gerador de Artes para os Aniversariantes Automático!")

# Espaçamento manual
st.write("")

# Campos de preenchimento
nome = st.text_input("Nome e Sobrenome", placeholder="Ex: Fulano Primeiro...")
cargo = st.text_input("Cargo", placeholder="Ex: Secretária de...")
foto_upload = st.file_uploader("Suba a foto aqui", type=["jpg", "png", "jpeg"])

# Rodapé simples
st.markdown("<p style='color: #888; font-size: 13px; margin-top: 20px;'>Desenvolvido por <b>SECOM</b></p>", unsafe_allow_html=True)

# --- LÓGICA DE GERAÇÃO DA ARTE ---
if foto_upload and nome and cargo:
    try:
        # Carregamento das imagens
        base = Image.open("template.png").convert("RGBA")
        template_sem_preto = remover_preto(base)
        
        foto = Image.open(foto_upload).convert("RGBA")
        foto = cortar_cover(foto, (995, 995))
        foto = foto.rotate(-4, resample=Image.BICUBIC, expand=True)
        
        # Ajuste de posição final
        nova_l, nova_a = foto.size
        pos_ajustada = (50 - (nova_l - 995) // 2, 285 - (nova_a - 995) // 2)
        
        fundo = Image.new("RGBA", base.size, (0,0,0,0))
        fundo.paste(foto, pos_ajustada, foto)
        arte = Image.alpha_composite(fundo, template_sem_preto)
        
        # Desenho dos textos
        draw = ImageDraw.Draw(arte)
        try:
            f_nome = ImageFont.truetype("Poppins-Bold.ttf", 60)
            f_cargo = ImageFont.truetype("Poppins-Regular.ttf", 34)
            w_n = draw.textbbox((0,0), nome, font=f_nome)[2]
            draw.text((540 - w_n/2, 1115), nome, fill="white", font=f_nome)
            w_c = draw.textbbox((0,0), cargo.upper(), font=f_cargo)[2]
            draw.text((540 - w_c/2, 1200), cargo.upper(), font=f_cargo, fill="white")
        except:
            st.warning("Fontes .ttf não encontradas. Verifique se estão na pasta do GitHub.")

        # Área de Resultado (aparece abaixo do card)
        st.write("---")
        st.image(arte, caption="Sua arte pronta!", use_container_width=True)
        
        img_byte_arr = io.BytesIO()
        arte.save(img_byte_arr, format='PNG')
        st.download_button(
            label="✅ Baixar Arte em PNG", 
            data=img_byte_arr.getvalue(), 
            file_name=f"aniversariante_{nome}.png", 
            mime="image/png"
        )
    except Exception as e:
        st.error(f"Erro ao processar imagem: {e}")
