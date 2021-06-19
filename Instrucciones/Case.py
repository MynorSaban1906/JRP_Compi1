from TablaArbol.Excepcion import Excepcion
from TablaArbol.Tipo import OperadorAritmetico,TIPO
from abc import ABC, abstractmethod
from TablaArbol.Simbolo import Simbolo
from TablaArbol.ts import TablaSimbolos
from Instrucciones.Instruccion import Instruccion


                        
            
class Case(Instruccion):
    def __init__(self, expresion,instrucciones, fila, columna):
        self.expresion = expresion
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        retorno = self.expresion.interpretar(tree, table)  # RETORNA CUALQUIER VALOR
        if isinstance(retorno, Excepcion) :
            return retorno

        return retorno
        
    def getExpresion(self):
        return self.expresion

    def setExpresion(self, expresion):
        self.expresion = expresion

    def getInstrucciones(self):
        return self.instrucciones

    def setInstrucciones(self, instrucciones):
        self.instrucciones = instrucciones

    def getFila(self):
        return self.fila

    def setFila(self, fila):
        self.fila= fila 

    def getColumna(self):
        return self.columna

    def setColumna(self, columna):
        self.columna= columna

