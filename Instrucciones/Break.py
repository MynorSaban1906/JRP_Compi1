from TablaArbol.NodoAST import NodoAST
from Instrucciones.Instruccion import Instruccion


class Break(Instruccion):
    def __init__(self, fila, columna):
        self.fila = fila

    def interpretar(self, tree, table):
        return self


    def getNodo(self):
        nodo=NodoAST("BREAK")
        return nodo