from TablaArbol.Simbolo import Simbolo
from TablaArbol.Tipo import TIPO
from TablaArbol.Excepcion import Excepcion
from Instrucciones.Instruccion import Instruccion


# solo devuelve el valor del id
class Primitivos(Instruccion):
    def __init__(self, tipo, valor, fila, columna):
        self.tipo = tipo
        self.valor = valor
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        return self.valor

    def getTipo(self):
        return self.tipo

    def setTipo(self, tipo):
        self.tipo=tipo

    def getValor(self):
        return self.valor

    def setValor(self, valor):
        self.valor = valor

        
    def getFila(self):
        return self.fila

    def setFila(self, fila):
        self.fila= fila 

    def getColumna(self):
        return self.columna

    def setColumna(self, columna):
        self.columna= columna
