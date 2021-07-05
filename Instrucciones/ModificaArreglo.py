from typing import List
from TablaArbol.Tipo import TIPO
from TablaArbol.Excepcion import Excepcion
from TablaArbol.Simbolo import Simbolo
from Instrucciones.Instruccion import Instruccion
from TablaArbol.NodoAST import NodoAST
import copy



class ModificaArreglo(Instruccion):

    def __init__(self,identificador, lista, valor, fila, columna):
        self.identificador = identificador
        self.listaexpresion=lista
        self.valor=valor
        self.fila = fila
        self.columna = columna
        self.tipo=None

    def interpretar(self, tree, table):
        value = self.getValor().interpretar(tree, table) # Valor a asignar a la posicion del arreglo especificado
        if isinstance(value, Excepcion): return value

        simbolo = table.getTabla(str(self.getIdentificador()).lower()) # obtinene el el arreglo si no existe da error

        if simbolo == None: 
            return Excepcion("Semantico", "Variable " + self.getIdentificador() + " no encontrada.", self.getFila(), self.getColumna() )
        
        if not simbolo.getArreglo(): 
            return Excepcion("Semantico", "Variable " + self.getIdentificador() + " no es un arreglo.", self.getFila(), self.getColumna() )

        if simbolo.getTipo() != self.getValor().getTipo():
            return Excepcion("Semantico", "Tipo de dato diferente al arreglo en Modificacion.", self.getFila(), self.getColumna() )

        # BUSQUEDA DEL ARREGLO
        value = self.modificarDimensiones(tree, table, copy.copy(self.getListaExpresion()), simbolo.getValor(), value)     #RETORNA EL VALOR SOLICITADO
        if isinstance(value, Excepcion): return value
  
        return value

    def getNodo(self):
        nodo = NodoAST("MODIFICACION ARREGLO")
        nodo.Agregar_Hijo(str(self.identificador))
        exp = NodoAST("EXPRESIONES DE LAS DIMENSIONES")
        for expresion in self.getListaExpresion():
            exp.Agregar_Hijo_Nodo(expresion.getNodo())
        nodo.Agregar_Hijo_Nodo(exp)
        nodo.Agregar_Hijo_Nodo(self.valor.getNodo())
        
        return nodo

    def modificarDimensiones(self, tree, table, expresiones, arreglo, valor):
        if len(expresiones) == 0:
            if isinstance(arreglo, list):
                return Excepcion("Semantico", "Modificacion a Arreglo incompleto.",  self.getFila(), self.getColumna() )
            return valor
        if not isinstance(arreglo, list):
            return Excepcion("Semantico", "Accesos de más en un Arreglo.",  self.getFila(), self.getColumna() )
        dimension = expresiones.pop(0)
        num = dimension.interpretar(tree, table)
        if isinstance(num, Excepcion): return num
        if dimension.tipo != TIPO.ENTERO:
            return Excepcion("Semantico", "Expresion diferente a ENTERO en Arreglo.",  self.getFila(), self.getColumna() )
        try:
            value = self.modificarDimensiones(tree, table, copy.copy(expresiones), arreglo[num], valor)
        except:
            return Excepcion("Semantico", "No se puede acceder a la posicion del arreglo  "+ self.getIdentificador() ,  self.getFila(), self.getColumna() )
        if isinstance(value, Excepcion): return value
        if value != None:
            arreglo[num] = value

        return None


    def getIdentificador(self):
        return self.identificador

    def setIdentificador(self, identificador):
        self.identificador=identificador

    def getFila(self):
        return self.fila

    def setFila(self, fila):
        self.fila= fila 

    def getColumna(self):
        return self.columna

    def setColumna(self, columna):
        self.columna= columna

    def getListaExpresion(self):
        return self.listaexpresion

    def setListaExpresion(self, arreglo):
        self.listaexpresion=arreglo

    def getTipo(self):
        return self.tipo

    def setTipo(self, tipo):
        self.tipo=tipo

    def getValor(self):
        return self.valor

    def setValor(self, valor):
        self.valor=valor



