from TablaArbol.NodoAST import NodoAST
from TablaArbol.Excepcion import Excepcion
from Instrucciones.Instruccion import Instruccion


                        
            
class Case(Instruccion):
    def __init__(self, expresion,instrucciones, fila, columna):
        self.expresion = expresion
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna
        self.valor=None

    def interpretar(self, tree, table):
        retorno = self.expresion.interpretar(tree, table)  # RETORNA CUALQUIER VALOR
        if isinstance(retorno, Excepcion) :
            return retorno
        self.valor=retorno
        return retorno
        

    def getNodo(self):
        nodo=NodoAST("CASE ")
        nodo.Agregar_Hijo_Nodo(self.expresion.getNodo())

        instrucciones=NodoAST("INSTRUCCIONES")
        for instr in self.instrucciones:
            instrucciones.Agregar_Hijo_Nodo(instr.getNodo())

        nodo.Agregar_Hijo_Nodo(instrucciones)
        return nodo



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

