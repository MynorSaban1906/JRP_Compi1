
from Instrucciones.Funcion import Funcion
from TablaArbol.Tipo import TIPO
from TablaArbol.Excepcion import Excepcion
import math

class Round(Funcion):
    def __init__(self, nombre,parametros,instrucciones,fila, columna):
        self.identificador = nombre
        self.fila = fila
        self.parametros=parametros  
        self.instrucciones = instrucciones
        self.columna = columna
        self.tipo = TIPO.NULO

    def interpretar(self, tree, table):
        simbolo = table.getTabla("round##param1") # crea una variable con el nombre complicado, algo que nunca vendra
        
        if simbolo ==None:
            return Excepcion("Semantico", "No se encontro el parametro de la funcion Round ", self.getFila(),self.getColumna())

        if simbolo.getTipo() not in(TIPO.ENTERO, TIPO.DECIMAL): # si no es igual al tipo entero o decimal este entraria en un error
            return Excepcion("Semantico", "No se puede usar la funcion Round  "  , simbolo.getFila(),simbolo.getColumna())


        self.setTipo(TIPO.ENTERO) # se pasa el tipo de dato el cual siempre seria tipo entero
        
        return round(simbolo.getValor())# se devuelve el valor ya redondeado "lista para imprimir" 



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
