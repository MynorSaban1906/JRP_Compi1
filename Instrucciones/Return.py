from TablaArbol.ts import TablaSimbolos
from Instrucciones.Funcion import Funcion
from TablaArbol.Tipo import TIPO
from TablaArbol.Excepcion import Excepcion
from Instrucciones.Instruccion import Instruccion


class Return(Instruccion):
    
    def __init__(self, expresion, fila, columna):
        self.expresion = expresion
        self.fila = fila
        self.columna = columna
        self.tipo = None
        self.result = None

    def interpretar(self, tree, table):
        result = self.expresion.interpretar(tree, table)
        if isinstance(result, Excepcion): return result

        self.setTipo(self.getExpresion().getTipo())#TIPO DEL RESULT
        self.setNodo(result )          #VALOR DEL RESULT

        return self

    def getExpresion(self):
        return self.expresion

    def setExpresion(self, expresion):
        self.expresion = expresion

        
    def getFila(self):
        return self.fila

    def setFila(self, fila):
        self.fila= fila 

    def getColumna(self):
        return self.columna

    def setColumna(self, columna):
        self.columna= columna
 
    def getTipo(self):
        return self.tipo

    def setTipo(self, tipo):
        self.tipo=tipo

    def getNodo(self):
        return self.result

    def setNodo(self, result):
        self.result =result