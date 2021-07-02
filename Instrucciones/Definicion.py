from TablaArbol.NodoAST import NodoAST
from TablaArbol.Excepcion import Excepcion
from TablaArbol.Tipo import OperadorAritmetico,TIPO
from abc import ABC, abstractmethod
from TablaArbol.Simbolo import Simbolo
from TablaArbol.ts import TablaSimbolos
from Instrucciones.Instruccion import Instruccion



class Definicion(Instruccion) :
    def __init__(self, identificador, fila, columna) :
        self.identificador=identificador
        self.fila = fila
        self.tipo=TIPO.NULO
        self.columna = columna

    def interpretar(self, tree, table):
        simbolo = Simbolo(self.identificador.lower(),self.tipo,self.fila,self.columna,None)
        result = table.setTabla(simbolo)
        
        if isinstance(result,Excepcion): return result
        
        return None


    def getNodo(self):
        nodo=NodoAST("DECLARACION")
        nodo.Agregar_Hijo("var")
        nodo.Agregar_Hijo(str(self.getIdentificador()))
        return nodo
        
    def getIdentificador(self):
        return self.identificador

    def setIdentificador(self, identificador):
        self.identificador=identificador

        
    def getTipo(self):
        return self.tipo

    def setTipo(self, tipo):
        self.tipo=tipo

    def getFila(self):
        return self.fila

    def setFila(self, fila):
        self.fila= fila 

    def getColumna(self):
        return self.columna

    def setColumna(self, columna):
        self.columna= columna
