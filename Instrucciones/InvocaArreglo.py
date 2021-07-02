from TablaArbol.Excepcion import Excepcion
from TablaArbol.Simbolo import Simbolo
from TablaArbol.ts import TablaSimbolos
from Instrucciones.Instruccion import Instruccion
from TablaArbol.NodoAST import NodoAST


class InvocaArreglo(Instruccion):
    def __init__(self, nombre,parametros,fila, columna):
        self.identificador = nombre
        self.fila = fila
        self.parametros=parametros  
        self.columna = columna
        self.tipo =None
    

    def interpretar(self, tree, table):
        pass

    def getNodo(self):
        pass

    def getIdentificador(self):
        return self.identificador

    def setIdentificador(self, identificador):
        self.identificador=identificador

    def getTipo(self):
        return self.tipo

    def setTipo(self, tipo):
        self.tipo=tipo

    def getParametros(self):
        return self.parametros

    def setParametros(self, parametros):
        self.parametros=parametros

        
    def getFila(self):
        return self.fila

    def setFila(self, fila):
        self.fila= fila 

    def getColumna(self):
        return self.columna

    def setColumna(self, columna):
        self.columna= columna
