from Instrucciones.Instruccion import Instruccion
from TablaArbol.NodoAST import NodoAST


class Continue(Instruccion):
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        return self

    def getNodo(self):
        nodo=NodoAST("CONTINUE")
        return nodo