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
