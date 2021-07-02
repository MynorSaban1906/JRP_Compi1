from TablaArbol.Excepcion import Excepcion
from TablaArbol.Tipo import OperadorAritmetico,TIPO
from abc import ABC, abstractmethod
from TablaArbol.Simbolo import Simbolo
from TablaArbol.ts import TablaSimbolos
from Instrucciones.Instruccion import Instruccion
from TablaArbol.NodoAST import NodoAST

class Imprimir(Instruccion):
    def __init__(self, expresion, fila, columna):
        self.expresion = expresion
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        value = self.expresion.interpretar(tree, table)  # RETORNA CUALQUIER VALOR
        if isinstance(value, Excepcion) :
            return value
        

        if self.expresion.tipo == TIPO.ARREGLO:
            return Excepcion("Semantico", "No se puede imprimir un arreglo completo", self.fila, self.columna)

        if self.expresion.tipo == TIPO.NULO:
            return Excepcion("Semantico", "No se puede imprimir un valor Null", self.fila, self.columna)


        tree.updateConsola(value)

    def getNodo(self):
        nodo=NodoAST("IMPRIMIR")
        nodo.Agregar_Hijo_Nodo(self.getExpresion().getNodo())
        
        return nodo


    def getFila(self):
        return self.fila

    def setFila(self, fila):
        self.fila= fila 

    def getColumna(self):
        return self.columna

    def setColumna(self, columna):
        self.columna= columna
        

    def getExpresion(self):
        return self.expresion

    def setExpresion(self, expresion):
        self.expresion=expresion 