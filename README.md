---

# **Portal de Notícias Comunitário**

Projeto desenvolvido para a disciplina de desenvolvimento web conforme as especificações do edital.
O sistema permite visualizar, cadastrar e personalizar notícias utilizando Flask, Bootstrap e cookies.

---

# **Descrição do Projeto**

O **Portal de Notícias Comunitário** é uma aplicação web simples e responsiva onde usuários podem:

* Visualizar notícias na página inicial
* Adicionar novas notícias através de um formulário
* Escolher tema claro/escuro usando cookies
* Navegar por uma interface moderna construída com Bootstrap

O projeto utiliza **Flask**, **templates Jinja2**, **cookies**, **validação de formulários** e **componentes visuais do Bootstrap 5**.

---

# **Funcionalidades**

### Página Inicial (`/`)

* Exibe lista de notícias em formato de cards
* Mostra título, conteúdo, autor, data e categoria
* Layout responsivo utilizando grid Bootstrap
* Navbar com navegação para todas as páginas
* Exibe mensagens *flash* (sucesso/erro)

### Adicionar Notícia (`/adicionar_noticia`)

* Formulário para cadastrar novas notícias
* Campos:

  * Título (obrigatório, máximo 100 caracteres)
  * Conteúdo (texto longo, obrigatório)
  * Autor (obrigatório)
  * Categoria (select: Política, Esportes, Cultura, Tecnologia etc.)
* Validação server-side com mensagens de erro/sucesso
* Estilizado com classes Bootstrap

### Configurações (`/configuracoes`)

* Permite selecionar tema **claro** ou **escuro**
* Preferência salva em um cookie
* Tema aplicado automaticamente em todas as páginas
* Interface visual usando Bootstrap

---

# **Templates e Design**

O projeto utiliza herança de templates:

```
templates/
│── base.html
│── index.html
│── adicionar_noticia.html
└── configuracoes.html
```

* `base.html`: estrutura principal, navbar, footer e inclusão do Bootstrap
* `index.html`: exibe os cards de notícias
* `adicionar_noticia.html`: formulário de cadastro
* `configuracoes.html`: seletor de tema

CSS customizado em:

```
static/estilo.css
```

---

# **Cookies**

O sistema armazena no navegador a preferência de tema:

* `tema=claro`
* `tema=escuro`

O Flask lê o cookie e aplica dinamicamente a classe no `<body>` para alterar o visual da página.

---

# **Como Executar o Projeto**

### 1. Requisitos

* Python 3.10+
* Flask instalado

Instale as dependências:

```bash
pip install flask
```

### 2. Executar o servidor

No diretório raiz do projeto:

```bash
python app.py
```

Ou:

```bash
flask run
```

### 3. Acessar no navegador

```
http://127.0.0.1:5000/
```

---

# **Estrutura do Projeto**

```
/project
│── app.py
│── README.txt
│── /templates
│     ├── base.html
│     ├── index.html
│     ├── adicionar_noticia.html
│     └── configuracoes.html
└── /static
      └── estilo.css
```

---
