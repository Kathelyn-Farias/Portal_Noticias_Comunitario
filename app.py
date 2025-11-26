import os
from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from datetime import datetime
from markupsafe import escape
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)
app.secret_key = "segredo123"  # Necessário para flash messages

#configuração de upload de imagens
UPLOAD_FOLDER = os.path.join(app.root_path, "static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
# Lista de notícias (simulação de banco de dados)
DEFAULT_NOTICIAS = [
    {
        "titulo": "Reforço Escolar em Matemática e Português",
        "conteudo": "Estão abertas as vagas para o curso gratuito de reforço escolar, focado em alunos do Ensino Fundamental II (6º ao 9º ano). As aulas serão ministradas por professores voluntários, visando auxiliar no preparo para as provas finais. Local: Sala de Leitura do Centro Comunitário (Av. Beija-flor, Nº180)",
        "autor": "Jorge",
        "categoria": "Cultura",
        "data": "24/11/2025 15:02",
        "banner": "reforco_escolar.jpg"
    },
    {
        "titulo": "Novo Centro Comunitário - Inauguração",
        "conteudo": "Inauguração do novo centro comunitário com espaço para cursos, eventos e atividades.",
        "autor": "Jorge",
        "categoria": "Cultura",
        "data": "23/11/2025 12:56",
        "banner": "centro_comunitario.webp"
    },
    {
        "titulo": "Aberta inscrições para Escolinha de Futebol",
        "conteudo": "Inscrições abertas para crianças entre 6 e 12 anos. Traga documento de identidade.",
        "autor": "Cláudia",
        "categoria": "Esportes",
        "data": "23/11/2025 12:58",
        "banner": "escolinha_de_futebol.jpg"
    },
    {
        "titulo": "Mutirão de Vacinação contra a Gripe",
        "conteudo": "O Posto de Saúde realizará um mutirão de vacinação neste sábado, das 8h às 16h, para facilitar o acesso à vacina contra a gripe.É obrigatória a apresentação do cartão de vacinação e documento de identidade.",
        "autor": "Agente Comunitário de Saúde",
        "categoria": "Eventos",
        "data": "18/11/2025 15:47",
        "banner": "multirao_vacina.jpg"
    },

]

# PERSISTÊNCIA EM JSON 
DATA_DIR = os.path.join(app.root_path, "data")
os.makedirs(DATA_DIR, exist_ok=True)
DATA_FILE = os.path.join(DATA_DIR, "noticias.json")


def load_noticias():
    """Carrega notícias do arquivo JSON; se não existir, cria com DEFAULT_NOTICIAS."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            # Se o JSON estiver corrompido, cai para o padrão
            pass

    # Se não existe ou está inválido, cria com DEFAULT_NOTICIAS
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(DEFAULT_NOTICIAS, f, ensure_ascii=False, indent=4)
    return [dict(n) for n in DEFAULT_NOTICIAS]


def save_noticias(lista_noticias):
    """Salva a lista de notícias no arquivo JSON."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(lista_noticias, f, ensure_ascii=False, indent=4)


# Carrega as notícias na inicialização do app
noticias = load_noticias()

# ROTAS
@app.route("/")
def index():
    # Lê o cookie de tema; padrão 'claro'
    tema = request.cookies.get("tema", "claro")
    
        # categoria passada na URL: /?categoria=Esportes
    categoria_filtro = request.args.get("categoria")

    # lista de categorias existentes (pra montar os botões)
    categorias = sorted({n["categoria"] for n in noticias})

    if categoria_filtro:
        noticias_filtradas = [
            n for n in noticias if n["categoria"] == categoria_filtro
        ]
    else:
        noticias_filtradas = noticias


    return render_template("index.html", noticias=noticias_filtradas, tema=tema, categorias=categorias,
        categoria_atual=categoria_filtro)

@app.route("/adicionar_noticia", methods=["GET", "POST"])
def adicionar_noticia():
    tema = request.cookies.get("tema", "claro")
    if request.method == "POST":
        # Recupera e faz um escape básico
        titulo = escape(request.form.get("titulo", "").strip())
        conteudo = escape(request.form.get("conteudo", "").strip())
        autor = escape(request.form.get("autor", "").strip())
        categoria = escape(request.form.get("categoria", "").strip())
        
        # arquivo de imagem
        banner_file = request.files.get("banner")
        erros = []

        # Validação
        erros = []
        if not titulo:
            erros.append("Título é obrigatório.")
        elif len(titulo) > 100:
            erros.append("Título deve ter no máximo 100 caracteres.")
        if not conteudo:
            erros.append("Conteúdo é obrigatório.")
        if not autor:
            erros.append("Autor é obrigatório.")
        if not categoria:
            erros.append("Categoria é obrigatória.")


        # Validação do banner (se o usuário enviou)
        if banner_file and banner_file.filename:
            if not allowed_file(banner_file.filename):
                erros.append("Imagem inválida. Use JPG, PNG, GIF ou WEBP (até 2MB).")
                
        if erros:
            for e in erros:
                flash(e, "danger")
        else:
            # salva a imagem só se não houver erros
            banner_filename = None
            if banner_file and banner_file.filename:
                original = secure_filename(banner_file.filename)
                unique_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{original}"
                save_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_name)
                banner_file.save(save_path)
                banner_filename = unique_name
                
            data_str = datetime.now().strftime("%d/%m/%Y %H:%M")
            noticias.insert(0, {  # insere no topo
                "titulo": titulo,
                "conteudo": conteudo,
                "autor": autor,
                "categoria": categoria,
                "data": data_str,
                "banner": banner_filename  # <<< NÃO ESQUECER!
            })
            
            save_noticias(noticias)
            
            flash("Notícia adicionada com sucesso!", "success")
            return redirect(url_for("index"))

    # Em GET ou em caso de erro mostra o formulário (mantendo valores via request.form)
    return render_template("adicionar_noticia.html", tema=tema)

@app.route("/configuracoes", methods=["GET", "POST"])
def configuracoes():
    tema_atual = request.cookies.get("tema", "claro")

    if request.method == "POST":
        tema_selecionado = request.form.get("tema")
        resp = make_response(redirect(url_for("index")))
        if tema_selecionado in ["claro", "escuro"]:
            # salva cookie por 1 ano
            resp.set_cookie("tema", tema_selecionado, max_age=60*60*24*365, path="/")
            flash("Configurações salvas com sucesso!", "success")
        else:
            flash("Seleção de tema inválida.", "danger")
        return resp

    return render_template("configuracoes.html", tema=tema_atual)

# Pequena API para toggle via JS (opcional)
@app.route("/set_tema_js", methods=["POST"])
def set_tema_js():
    tema = request.form.get("tema")
    resp = make_response(('OK', 200))
    if tema in ["claro", "escuro"]:
        resp.set_cookie("tema", tema, max_age=60*60*24*365, path="/")
    return resp

# EXECUTANDO O SERVIDOR
if __name__ == "__main__":
    app.run(debug=True)