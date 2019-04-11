from clientes import Client
from produtos import Products

class Vendas:
    __id = None
    __idCliente = None
    __idProduto = None
    __quantidadeProduto = None
    __total = None

    def __init__(self, id, idCliente, idProduto, qtd, total):
        self.__id = id
        self.__idCliente = idCliente
        self.__idProduto = idProduto
        self.__quantidadeProduto = qtd
        self.__total = total
        
    def getVendaId(self):
        return self.__id

    def getVendaIdCliente(self):
        return self.__idCliente

    def getVendaProduto(self):
        return self.__idProduto

    def getVendaQtd(self):
        return self.__quantidadeProduto

    def getTotalVenda(self):
        return self.__total