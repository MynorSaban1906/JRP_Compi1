from TablaArbol.Excepcion import Excepcion
from TablaArbol.Tipo import OperadorAritmetico,TIPO
from abc import ABC, abstractmethod
from TablaArbol.Simbolo import Simbolo
from TablaArbol.ts import TablaSimbolos
from Instrucciones.Instruccion import Instruccion
from TablaArbol.NodoAST import NodoAST



class Asignacion(Instruccion) :

    def __init__(self, identificador, expresion, fila, columna):
        self.identificador = identificador
        self.expresion = expresion
        self.fila = fila
        self.columna = columna
        self.arreglo = False

    def interpretar(self, tree, table):

        value = self.expresion.interpretar(tree, table) # Valor a asignar a la variable
        if isinstance(value, Excepcion): return value

        simbolo = Simbolo(self.identificador.lower(), self.expresion.tipo,self.arreglo, self.fila, self.columna, value)
    
        result = table.actualizarTabla(simbolo)

        if isinstance(result, Excepcion): return result
        
      
        return None



    def getNodo(self):
        nodo=NodoAST("ASIGNACION")
        nodo.Agregar_Hijo(str(self.getIdentificador()))
        nodo.Agregar_Hijo("=")
        nodo.Agregar_Hijo_Nodo(self.getExpresion().getNodo())
        return nodo
        

    def getIdentificador(self):
        return self.identificador

    def setIdentificador(self, identificador):
        self.identificador=identificador

        
    def getTipo(self):
        return self.tipo

    def setTipo(self, tipo):
        self.tipo=tipo



    def getExpresion(self):
        return self.expresion

    def setExpresion(self,expresion):
        self.expresion= expresion

    def getFila(self):
        return self.fila

    def setFila(self, fila):
        self.fila= fila 

    def getColumna(self):
        return self.columna

    def setColumna(self, columna):
        self.columna= columna
