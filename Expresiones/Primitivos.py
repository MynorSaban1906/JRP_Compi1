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

