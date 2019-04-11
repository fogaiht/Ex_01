class Products:
    __id = None
    __nomeProduto = None
    __preco = None

    def __init__(self, id, nomeProduto, preco):
        self.__id = id
        self.__nomeProduto = nomeProduto
        self.__preco = preco
    
    def getIdProduto(self):
        return self.__id
    def getNomeProduto(self):
        return self.__nomeProduto
    def getPrecoProduto(self):
        return self.__preco
