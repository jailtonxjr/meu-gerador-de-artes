<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gerador SECOM Pro - JS Edition</title>
    <style>
        /* CSS ESTILO GEMINI */
        body {
            background: radial-gradient(circle at top right, #1e1e20, #131314);
            color: #e3e3e3;
            font-family: 'Google Sans', 'Segoe UI', sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            overflow-x: hidden;
        }

        .container {
            width: 100%;
            max-width: 450px;
            padding: 30px;
            text-align: center;
        }

        h1 { font-weight: 500; font-size: 24px; margin-bottom: 30px; }

        .input-group { margin-bottom: 20px; text-align: left; }

        label { display: block; margin-bottom: 8px; font-size: 14px; color: #8e918f; text-align: center; }

        input {
            width: 100%;
            padding: 14px;
            background: #1e1f20;
            border: 1px solid #444746;
            border-radius: 12px;
            color: white;
            box-sizing: border-box;
            text-align: center;
            transition: border 0.3s;
        }

        input:focus { border-color: #4285f4; outline: none; }

        /* Estilo unificado para os botões */
        .btn-acao {
            background: linear-gradient(90deg, #4285f4, #9b72cb, #d96570);
            border: none;
            padding: 16px;
            border-radius: 50px;
            color: white;
            font-weight: 600;
            font-size: 16px;
            cursor: pointer;
            width: 100%;
            margin-top: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            transition: transform 0.2s;
            text-decoration: none;
            display: inline-block;
            box-sizing: border-box;
        }

        .btn-acao:hover { transform: scale(1.02); }

        canvas { display: none; } 

        #preview-container { margin-top: 30px; display: none; }

        #resultado-final {
            width: 100%;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }
    </style>
</head>
<body>

<div class="container">
    <div class="emoji" style="font-size: 50px;">✨</div>
    <h1>Gerador de Artes SECOM</h1>

    <div class="input-group">
        <label>Nome do Aniversariante</label>
        <input type="text" id="nome" placeholder="Ex: Fulano da Silva">
    </div>

    <div class="input-group">
        <label>Cargo ou Setor</label>
        <input type="text" id="cargo" placeholder="Ex: Secretário de ...">
    </div>

    <div class="input-group">
        <label>Foto do Aniversariante</label>
        <input type="file" id="foto-input" accept="image/*">
    </div>

    <button class="btn-acao" onclick="processarArte()">CRIAR ARTE AGORA</button>

    <div id="preview-container">
        <img id="resultado-final" src="" alt="Arte Final">
        <a id="link-download" class="btn-acao" download="aniversariante.png">📥 BAIXAR IMAGEM</a>
    </div>

    <canvas id="motorCanvas" width="1080" height="1920"></canvas>
</div>

<script>
    function formatarTexto(texto) {
        if (!texto) return "";
        const excecoes = ['de', 'da', 'do', 'dos', 'das', 'e', 'em', 'no', 'na'];
        return texto.toLowerCase().split(' ').map(palavra => {
            if (excecoes.includes(palavra) && palavra !== "") {
                return palavra;
            }
            return palavra.charAt(0).toUpperCase() + palavra.slice(1);
        }).join(' ');
    }

    async function processarArte() {
        const nomeBruto = document.getElementById('nome').value;
        const cargoBruto = document.getElementById('cargo').value;
        
        const nome = formatarTexto(nomeBruto);
        const cargo = formatarTexto(cargoBruto);
        const fotoInput = document.getElementById('foto-input').files[0];
        
        if(!nome || !cargo || !fotoInput) {
            alert("Preencha todos os campos!");
            return;
        }

        const canvas = document.getElementById('motorCanvas');
        const ctx = canvas.getContext('2d');

        const imgTemplate = new Image();
        imgTemplate.crossOrigin = "anonymous"; 
        imgTemplate.src = 'template.png'; 

        imgTemplate.onload = async () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            const imgFoto = await carregarImagem(fotoInput);
            const tamanhoAlvo = 995;
            const coordsCrop = calcularCenterCrop(imgFoto, tamanhoAlvo);

            ctx.save();
            ctx.translate(35 + (tamanhoAlvo/2), 275 + (tamanhoAlvo/2)); 
            ctx.rotate(-4 * Math.PI / 180); 
            ctx.drawImage(
                imgFoto, 
                coordsCrop.x, coordsCrop.y, coordsCrop.width, coordsCrop.height, 
                -tamanhoAlvo/2, -tamanhoAlvo/2, tamanhoAlvo, tamanhoAlvo 
            );
            ctx.restore();

            ctx.drawImage(imgTemplate, 0, 0);

            ctx.fillStyle = "white";
            ctx.textAlign = "center";
            
            // Nome - Aumentado para 70px
            ctx.font = "bold 70px Poppins, Segoe UI, sans-serif";
            ctx.fillText(nome, 540, 1178);

            // Cargo
            ctx.font = "34px Poppins, Segoe UI, sans-serif";
            ctx.fillText(cargo, 540, 1250); // Ajustado levemente para baixo devido ao nome maior

            try {
                const dataURL = canvas.toDataURL("image/png");
                document.getElementById('resultado-final').src = dataURL;
                document.getElementById('link-download').href = dataURL;
                document.getElementById('preview-container').style.display = 'block';
                window.scrollTo(0, document.body.scrollHeight);
            } catch (e) {
                console.error(e);
                alert("Erro ao gerar imagem. Use o link do GitHub Pages.");
            }
        };
    }

    function carregarImagem(file) {
        return new Promise((resolve) => {
            const reader = new FileReader();
            reader.onload = (e) => {
                const img = new Image();
                img.onload = () => resolve(img);
                img.src = e.target.result;
            };
            reader.readAsDataURL(file);
        });
    }

    function calcularCenterCrop(img, targetSize) {
        let x, y, width, height;
        const aspect = img.width / img.height;
        if (aspect > 1) { 
            height = img.height; width = img.height;
            x = (img.width - img.height) / 2; y = 0;
        } else { 
            width = img.width; height = img.width;
            x = 0; y = (img.height - img.width) / 2;
        }
        return { x, y, width, height };
    }
</script>

</body>
</html>
