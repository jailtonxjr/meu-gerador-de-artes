import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# --- FUNÇÕES DE IMAGE (IGUAIS ÀS SUAS) ---
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

# --- INTERFACE DO SITE ---
st.title("🎨 Gerador de Artes Automático")
st.sidebar.header("Configurações")

# Campos para preencher
nome = st.text_input("Nome completo", "Fulano de Tal")
cargo = st.text_input("Cargo", "Desenvolvedor")
foto_upload = st.file_uploader("Suba a foto aqui", type=["jpg", "png", "jpeg"])

if foto_upload:
    # Configurações fixas (seus parâmetros)
    POS_FOTO = (50, 285)
    TAM_FOTO = (995, 995)
    ROT_FOTO = 4
    CENTRO_X = 540
    
    # Processamento
    base = Image.open("template.png").convert("RGBA")
    template_sem_preto = remover_preto(base)
    
    foto = Image.open(foto_upload).convert("RGBA")
    foto = cortar_cover(foto, TAM_FOTO)
    foto = foto.rotate(ROT_FOTO, resample=Image.BICUBIC, expand=True)
    
    # Ajuste de posição
    nova_l, nova_a = foto.size
    pos_ajustada = (POS_FOTO[0] - (nova_l - TAM_FOTO[0]) // 2, POS_FOTO[1] - (nova_a - TAM_FOTO[1]) // 2)
    
    fundo = Image.new("RGBA", base.size, (0,0,0,0))
    fundo.paste(foto, pos_ajustada, foto)
    arte = Image.alpha_composite(fundo, template_sem_preto)
    
    # Desenhar textos
    draw = ImageDraw.Draw(arte)
    try:
        f_nome = ImageFont.truetype("Poppins-Bold.ttf", 60)
        f_cargo = ImageFont.truetype("Poppins-Regular.ttf", 34)
        
        # Centralizar Nome
        w_n = draw.textbbox((0,0), nome, font=f_nome)[2]
        draw.text((CENTRO_X - w_n/2, 1115), nome, fill="white", font=f_nome)
        
        # Centralizar Cargo
        w_c = draw.textbbox((0,0), cargo.upper(), font=f_cargo)[2]
        draw.text((CENTRO_X - w_c/2, 1200), cargo.upper(), font=f_cargo, fill="white")
    except:
        st.error("Erro ao carregar as fontes. Verifique se os arquivos .ttf estão na pasta.")

    # Mostrar prévia no site
    st.image(arte, caption="Sua arte pronta!", use_container_width=True)

    # Botão de Download
    img_byte_arr = io.BytesIO()
    arte.save(img_byte_arr, format='PNG')
    st.download_button(label="📥 Baixar Arte", data=img_byte_arr.getvalue(), file_name=f"arte_{nome}.png", mime="image/png")