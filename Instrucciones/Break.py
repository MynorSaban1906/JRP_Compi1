from TablaArbol.Excepcion import Excepcion
from TablaArbol.Tipo import OperadorAritmetico,TIPO
from abc import ABC, abstractmethod
from TablaArbol.Simbolo import Simbolo
from TablaArbol.ts import TablaSimbolos
from Instrucciones.Instruccion import Instruccion


class Break(Instruccion):
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        return self
