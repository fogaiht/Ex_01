from flask import Flask, url_for, request, json, jsonify
from produtos import Products
from clientes import Client
from vendas import Vendas

from json import dumps

app = Flask(__name__)
exVendas = []
exClientes = []
exProdutos = []

@app.route('/')
def api_root():
    return 'Seja Bem Vindo!!'

#ROTA PARA ADICIONAR DADOS (ESCOLHER ENTRE produto E cliente)
@app.route('/inputdata', methods = ['POST'])
def api_newdata():
    global exClientes
    global exProdutos
    req_data = request.get_json()

    if(req_data['type'] == 'produto'):
        id = req_data['id']
        nome = req_data['nome']
        preco = req_data['preco']
        new_prod = Products(id, nome, preco)
        exProdutos.append(new_prod)
        res = {'status': 'ok'}
        return jsonify(res)

    elif(req_data['type'] == 'cliente'):
        id = req_data['id']
        nome = req_data['nome']
        new_client = Client(id, nome)
        exClientes.append(new_client)
        
        res = {'status': 'ok'}
        return jsonify(res)

    else:
        res = {'status': 'TYPE ERROR'}
        return jsonify(res)

#ROTA PARA FAZER UMA VENDA
@app.route('/makevenda', methods = ['POST'])
def api_getvenda():
    global exVendas
    global exClientes
    global exProdutos
    
    req_data = request.get_json()

    if(req_data['type'] == 'venda'):
        # Variaveis
        id = req_data['idVenda']
        idCliente = req_data['idCliente']
        idProduto = req_data['idProduto']
        qtd = req_data['qtd']
        idCliente_Venda = ''
        idProduto_Venda = ''
        total = ''
        priceProduto = ''

        for elem in exClientes:
            if(int(idCliente) == int(elem.getClientId())):
                idCliente_Venda = idCliente                

        for elem in exProdutos:
            if(int(idProduto) == int(elem.getIdProduto())):
                idProduto_Venda = idProduto
                priceProduto = elem.getPrecoProduto()
                total = float(priceProduto) * int(qtd)

        if (idCliente_Venda == '' or idProduto_Venda == ''):
            if (idCliente_Venda == ''):
                res = {'status': 'Cliente não existe'}
            elif (idProduto_Venda == ''):
                res = {'status': 'Produto não existe'}
        else:
            new_venda = Vendas(id, idCliente_Venda, idProduto_Venda, qtd, total)
            exVendas.append(new_venda)
            res = {'status': 'Venda Feita com sucesso!'}
        return jsonify(res)

#ROTA PARA LISTAR TODOS OS PRODUTOS CADASTRADOS
@app.route('/listprodutos', methods = ['GET'])
def api_listprodutos():
    payload = []
    content = {}
    
    for elem in exProdutos:        
        content = {'id': str(elem.getIdProduto()),'[Nome]': elem.getNomeProduto(), '[Preco]': 'R$ ' + str(elem.getPrecoProduto())}
        payload.append(content)
        content = {}

    res =  json.dumps(payload)       
    
    return jsonify(ProductList=res)

#ROTA PARA LISTAR TODOS OS CLIENTES CADASTRADOS
@app.route('/listclients', methods = ['GET'])
def api_listclients():
    payload = []
    content = {}
    
    for elem in exClientes:        
        content = {'id': elem.getClientId(), '[Nome]': elem.getClientNome()}
        payload.append(content)
        content = {}

    res =  json.dumps(payload)       
    
    return jsonify(ClientList=res)

#ROTA PARA LISTAR TODAS AS VENDAS FEITAS
@app.route('/listvenda', methods = ['GET'])
def api_listvendas():
    payload = []
    content = {}
    
    for elem in exVendas:        
        content = {
            'id': str(elem.getVendaId()),
            'idCliente': elem.getVendaIdCliente(),
            'idProduto': elem.getVendaProduto(),
            'qtd': elem.getVendaQtd(),
            'total': elem.getTotalVenda()}
        payload.append(content)
        content = {}

    res =  json.dumps(payload)       
    
    return jsonify(VendasList=res)

#ROTA PARA CRIAR UMA LISTA DE PRODUTOS PRÉ-ESTABELECIDA
@app.route('/createproducts', methods = ['GET'])
def api_createproducts():
    global exProdutos

    exProdutos.append(Products('1', 'Galaxy S10', '3900.00'))
    exProdutos.append(Products('2', 'Galaxy S9', '2200.00'))
    exProdutos.append(Products('3', 'Xiaomi mi3', '1450.80'))
    exProdutos.append(Products('4', 'Galaxy A9', '1598.50'))
    exProdutos.append(Products('5', 'iPhone X', '4900.00'))
    res = {'status': 'ok'}
    return jsonify(res)

#ROTA PARA CRIAR UMA LISTA DE CLIENTES PRÉ-ESTABELECIDA
@app.route('/createclients', methods = ['GET'])
def api_createclients():
    global exClientes
    exClientes.append(Client('1', 'Joao'))
    exClientes.append(Client('2', 'Pedro'))
    exClientes.append(Client('3', 'Jorge'))
    exClientes.append(Client('4', 'Valdir'))
    exClientes.append(Client('5', 'Antonio'))
    res = {'status': 'ok'}
    return jsonify(res)

#ROTA PARA BUSCAR CLIENTE PELO ID
@app.route('/getclientbyid', methods = ['POST'])
def api_getclientbyid():
    global exClientes

    req_data = request.get_json()

    id = req_data['id']
    for elem in exClientes:
        if(int(id) == int(elem.getClientId())):
            res = {'id': id, 'nome': elem.getClientNome()}
            return jsonify(res)
        else:
            res = {'status':'Cliente não encontrado'}
            return jsonify(res)

#ROTA PARA BUSCAR PRODUTO PELO ID
@app.route('/getproductbyid', methods = ['POST'])
def api_getproductbyid():
    global exProdutos

    req_data = request.get_json()

    id = req_data['id']
    for elem in exProdutos:
        if(int(id) == int(elem.getIdProduto)):
            res = {'id': str(elem.getIdProduto()),'[Nome]': elem.getNomeProduto(), '[Preco]': 'R$ ' + str(elem.getPrecoProduto())}
            return jsonify(res)
        else:
            res = {'status':'Produto não encontrado'}
            return jsonify(res)

#ROTA PARA BUSCAR TODAS AS COMPRAS DE UM CLIENTE PELO ID DO MESMO
@app.route('/getvendasbyidcliente', methods = ['POST'])
def api_getvendasbyidcliente():
    global exClientes
    global exVendas

    req_data = request.get_json()
    payload = []
    content = {}

    NomeCliente = ''
    res = ''

    id = req_data['idCliente']
    for elem in exClientes:
        if(int(id) == int(elem.getClientId())):
            NomeCliente = elem.getClientNome()
            res = str(NomeCliente)
    for elem in exVendas:
        if(int(id) == int(elem.getVendaIdCliente())):
            content = {
            'id': str(elem.getVendaId()),
            'idCliente': elem.getVendaIdCliente(),
            'idProduto': elem.getVendaProduto(),
            'qtd': elem.getVendaQtd(),
            'total': elem.getTotalVenda()}
            payload.append(content)
            content = {}
            resVendaCliente =  json.dumps(payload)       
    
            return jsonify(Nome=res, Compras=resVendaCliente)
        else:
            res = {'status':'Cliente não encontrado'}
            return jsonify(res)

if __name__ == '__main__':
    app.run()
