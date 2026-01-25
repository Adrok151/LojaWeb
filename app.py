from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Produto

app = Flask(__name__)
app.config["SECRET_KEY"] = "chave_muito_secreta_aqui"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///meubanco.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin')
        admin.set_password('123')
        db.session.add(admin)

    if Produto.query.count() == 0:
        dadosIniciais = [
            {'nome': 'Burger', 'preco': 15, 'imagem': 'images/burger.jpg', 'descricao': 'Pão, carne e queijo', 'categoria': 'lanche'},
            {'nome': 'Pizza quatro queijos', 'preco': 45, 'imagem': 'images/pizza_1.jpg', 'descricao': 'Pizza grande de sabor quatro queijos', 'categoria': 'pizza'},
            {'nome': 'Pizza calabresa', 'preco': 45, 'images': 'images/pizza_2.jpg', 'descricao': 'Pizza grande de calabresa tradicional', 'categoria': 'pizza'}
        ]
        for itemData in dadosIniciais:
            novoItem = Produto(
                nome = itemData['nome'],
                preco = itemData['preco'],
                imagem = itemData['imagem'],
                descricao = itemData['descricao'],
                categoria = itemData['categoria']
            )
            db.session.add(novoItem)
    db.session.commit()


def formata(dados):
    dadosLista = []
    for each in dados:
        produto = {
            'id': each.id,
            'nome': each.nome,
            'preco': each.preco,
            'imagem': each.imagem,
            'descricao': each.descricao,
            'categoria': each.categoria
        }
        dadosLista.append(produto)
    return(dadosLista)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
            return redirect(url_for("menu"))
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash("Login realizado com sucesso!", "success")
            session['carrinho'] = []
            return redirect(url_for("menu"))
        else:
            flash("Usuário ou senha incorretos!", "danger")
            return render_template("login.html", error="Credenciais inválidas.")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout realizado.", "info")
    return redirect(url_for("login"))

@app.route("/menu")
@login_required
def menu():
    produtosFormat = formata(Produto.query.all())
    return render_template("menu.html", produtos = produtosFormat)

@app.route("/detalhes")
@login_required
def detalhes():
    id = request.args.get('id')
    busca = Produto.query.filter_by(id = id).first()
    if busca:
        return render_template("detalhes.html", produto = busca)
    else:
        produtosFormat = formata(Produto.query.all())
        return render_template("menu.html", produtos = produtosFormat, error="Nenhum resultado encontrado")

@app.route("/carrinho")
@login_required
def carrinho():
    if 'carrinho' not in session:
        session['carrinho'] = []
    if len(session['carrinho']) > 0:
        dadosLista = []
        for each in session['carrinho']:
            item = Produto.query.filter_by(id = each).first()
            produto = {
                'id': item.id,
                'nome': item.nome,
                'preco': item.preco,
                'imagem': item.imagem,
                'descricao': item.descricao,
                'categoria': item.categoria
            }
            dadosLista.append(produto)        
        return render_template("carrinho.html", produtos = dadosLista) 
    else:
        return render_template("carrinho.html", vazio = "O carrinho está vazio!") 
    
@app.route("/addCarrinho")
@login_required
def addCarrinho():
    if 'carrinho' not in session:
        session['carrinho'] = []
    id = request.args.get('id')
    session['carrinho'].append(id)
    session.modified = True
    busca = Produto.query.filter_by(id = id).first()
    return render_template("detalhes.html", produto = busca, success = 'O item foi adicionado ao carrinho')

@app.route("/removeCarrinho")
@login_required
def removeCarrinho():
    session['carrinho'] = []
    session.modified = True
    return render_template("carrinho.html", compraFeita = "Obrigado pela compra! (isto pe claro é apenas um teste de um conceito ;) )")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)