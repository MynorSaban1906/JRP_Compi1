from TablaArbol.Excepcion import Excepcion
from TablaArbol.Tipo import OperadorAritmetico,TIPO
from abc import ABC, abstractmethod
from TablaArbol.Simbolo import Simbolo
from TablaArbol.ts import TablaSimbolos
from Instrucciones.Instruccion import Instruccion



class Inc_Dec(Instruccion):
    def __init__(self, expresion,identificador, tipo, fila, columna):
        self.expresion = expresion
        self.identificador=identificador
        self.tipo =tipo
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        value = self.expresion.interpretar(tree, table) # Valor a asignar a la variable
        if isinstance(value, Excepcion): return value
        
        if self.tipo==OperadorAritmetico.AUMENTO:
            simbolo= Simbolo(self.identificador,self.expresion.tipo,self.fila,self.columna,value + 1)
        elif self.tipo==OperadorAritmetico.DECREMENTO:
            simbolo= Simbolo(self.identificador,self.expresion.tipo,self.fila,self.columna,value - 1)

        else:
            return Excepcion("Semantico", "error en caracter de incremento o decremento ", self.fila, self.columna)
            
        result=table.actualizarTabla(simbolo)
        
        if isinstance(result,Excepcion): return result


        return simbolo.getValor()
