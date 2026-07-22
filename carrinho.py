from flask import render_template, request, session, jsonify, Blueprint
from flask_login import login_required
from models import Produto

carrinho_bp = Blueprint('carrinho', __name__)

@carrinho_bp.route('/')
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
    
@carrinho_bp.route("/addCarrinho", methods=["POST"])
@login_required
def addCarrinho():
    if 'carrinho' not in session:
        session['carrinho'] = []
    data = request.get_json()
    id = int(data.get('id'))
    session['carrinho'].append(id)
    session.modified = True
    return jsonify({"success": True})

@carrinho_bp.route("/removeCarrinho")
@login_required
def removeCarrinho():
    session['carrinho'] = []
    session.modified = True
    return render_template("carrinho.html", compraFeita = "Obrigado pela compra! (isto pe claro é apenas um teste de um conceito ;) )")
