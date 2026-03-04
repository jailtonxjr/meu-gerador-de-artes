import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import base64

# --- CONFIGURAÇÕES DE PÁGINA ---
st.set_page_config(page_title="Gerador de Artes - SECOM", layout="centered")

# --- FUNÇÃO PARA IMAGEM DE FUNDO (LOCAL OU GITHUB) ---
def get_base64(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return ""

# Tente carregar seu background.jpg local
bin_str = get_base64('background.jpg')
bg_img = f"data:image/png;base64,{bin_str}" if bin_str else "https://raw.githubusercontent.com/jailtonxjr/meu-gerador-de-artes/main/background.jpg"

# --- CSS DEFINITIVO (CARD UNIFICADO) ---
st.markdown(f"""
    <style>
    /* 1. Fundo da Tela */
    .stApp {{
        background: url("{bg_img}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* 2. O MOLDURA BRANCA (A MÁGICA) */
    /* Criamos um retângulo branco fixo atrás do conteúdo principal */
    .stApp::before {{
        content: "";
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 100%;
        max-width: 450px;
        height: 650px; /* Ajuste a altura conforme necessário */
        background-color: white;
        border-radius: 35px;
        box-shadow: 0px 20px 40px rgba(0,0,0,0.4);
        z-index: 0;
    }}

    /* 3. Ajustando o conteúdo para ficar sobre o card */
    [data-testid="stVerticalBlock"] {{
        position: relative;
        z-index: 1;
        background-color: transparent !important;
    }}

    /* Remove fundos extras das caixas do Streamlit */
    [data-testid="stVerticalBlock"] > div {{
        background-color: transparent !important;
    }}

    /* 4. Estilização dos Elementos Internos */
    h3, p, label {{
        color: #333 !important;
        text-align: center !important;
    }}

    .stTextInput input {{
        background-color: #f0f2f5 !important;
        border: none !important;
        border-radius: 10px !important;
    }}

    .stFileUploader section {{
        background-color: #0099ff !important;
        border: none !important;
        border-radius: 15px !important;
        color: white !important;
    }}

    /* Esconder Header e Footer */
    header, footer, #MainMenu {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

# --- CONTEÚDO VISUAL ---
# Emoji centralizado
st.markdown('<p style="font-size: 60px; margin-top: 50px;">🥳</p>', unsafe_allow_html=True)

# Título
st.markdown('<h3>Gerador de Artes para os Aniversariantes Automático!</h3>', unsafe_allow_html=True)

# Formulário (dentro do espaço do card)
nome = st.text_input("Nome e Sobrenome", placeholder="Ex: Fulano Primeiro...")
cargo = st.text_input("Cargo", placeholder="Ex: Secretária de...")
foto_upload = st.file_uploader("Suba a foto aqui", type=["jpg", "png", "jpeg"])

# Rodapé
st.markdown("<p style='color: #888; font-size: 13px; margin-top: 30px;'>Desenvolvido por <b>SECOM</b></p>", unsafe_allow_html=True)

# --- LÓGICA DE PROCESSAMENTO (O MOTOR) ---
if foto_upload and nome and cargo:
    try:
        # Carregamento e Processamento
        base = Image.open("template.png").convert("RGBA")
        
        # Função simples de remover fundo preto/escuro do template
        def remover_preto(img):
            dados = img.getdata()
            novo = [(0,0,0,0) if r<40 and g<40 and b<40 else (r,g,b,a) for r,g,b,a in dados]
            img.putdata(novo)
            return img
        
        template = remover_preto(base)
        
        # Foto do usuário
        foto = Image.open(foto_upload).convert("RGBA")
        foto = foto.resize((995, 995), Image.LANCZOS)
        foto = foto.rotate(4, resample=Image.BICUBIC, expand=True)
        
        # Montagem
        arte_final = Image.new("RGBA", base.size, (0,0,0,0))
        # Ajuste fino da posição para alinhar com o template
        arte_final.paste(foto, (35, 270), foto) 
        arte_final = Image.alpha_composite(arte_final, template)
        
        # Adição de Texto
        draw = ImageDraw.Draw(arte_final)
        try:
            f_nome = ImageFont.truetype("Poppins-Bold.ttf", 60)
            f_cargo = ImageFont.truetype("Poppins-Regular.ttf", 34)
            
            # Centralização do texto
            w_n = draw.textbbox((0,0), nome, font=f_nome)[2]
            draw.text(((1080 - w_n)/2, 1115), nome, fill="white", font=f_nome)
            
            w_c = draw.textbbox((0,0), cargo.upper(), font=f_cargo)[2]
            draw.text(((1080 - w_c)/2, 1200), cargo.upper(), font=f_cargo, fill="white")
        except:
            st.warning("Fontes não encontradas, usando fonte padrão.")

        # Resultado
        st.write("---")
        st.image(arte_final, use_container_width=True)
        
        # Download
        buf = io.BytesIO()
        arte_final.save(buf, format="PNG")
        st.download_button("📥 Baixar Arte Agora", buf.getvalue(), f"{nome}.png", "image/png")
        
    except Exception as e:
        st.error(f"Erro: {e}")

