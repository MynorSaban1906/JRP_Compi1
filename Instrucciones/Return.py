from TablaArbol.Tipo import TIPO
from TablaArbol.Excepcion import Excepcion
from Instrucciones.Instruccion import Instruccion


from TablaArbol.NodoAST import NodoAST
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
        # obtiene el tipo de dato que trae la funcion y lo guarda el return para igualarlo a una variable o retornarla
        # se obtiene de la sig: opera la expresiones y obtiene el resultado y luego lo devuelve
        #pero en este caso se obtiene el tipo de dato que tiene la expresion 
        #y se iguala al tipo de dato del return
        self.setTipo(self.getExpresion().getTipo())
        self.result=result         # aqui se devuelve el valor en si, lo que se quiere devolver da la funcion o ciclo

        return self


    def getNodo(self):
        nodo=NodoAST("BREAK")
        nodo.Agregar_Hijo_Nodo(self.getExpresion().getNodo())
        return nodo


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