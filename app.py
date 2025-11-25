from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from datetime import datetime
from markupsafe import escape

app = Flask(__name__)
app.secret_key = "segredo123"  # Necessário para flash messages

# Lista de notícias (simulação de banco de dados)
noticias = [
    {
        "titulo": "Novo Centro Comunitário - Inauguração",
        "conteudo": "Inauguração do novo centro comunitário com espaço para cursos, eventos e atividades.",
        "autor": "Admin",
        "categoria": "Cultura",
        "data": "23/11/2025 12:56"
    },
    {
        "titulo": "Aberta inscrições para Escolinha de Futebol",
        "conteudo": "Inscrições abertas para crianças entre 6 e 12 anos. Traga documento de identidade.",
        "autor": "Cláudia",
        "categoria": "Esportes",
        "data": "23/11/2025 12:58"
    }
]

# ROTAS
@app.route("/")
def index():
    # Lê o cookie de tema; padrão 'claro'
    tema = request.cookies.get("tema", "claro")
    return render_template("index.html", noticias=noticias, tema=tema)

@app.route("/adicionar_noticia", methods=["GET", "POST"])
def adicionar_noticia():
    tema = request.cookies.get("tema", "claro")
    if request.method == "POST":
        # Recupera e faz um escape básico
        titulo = escape(request.form.get("titulo", "").strip())
        conteudo = escape(request.form.get("conteudo", "").strip())
        autor = escape(request.form.get("autor", "").strip())
        categoria = escape(request.form.get("categoria", "").strip())

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

        if erros:
            for e in erros:
                flash(e, "danger")
        else:
            data_str = datetime.now().strftime("%d/%m/%Y %H:%M")
            noticias.insert(0, {  # insere no topo
                "titulo": titulo,
                "conteudo": conteudo,
                "autor": autor,
                "categoria": categoria,
                "data": data_str
            })
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