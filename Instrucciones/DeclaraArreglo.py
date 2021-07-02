from TablaArbol.Tipo import TIPO
from TablaArbol.Excepcion import Excepcion
from TablaArbol.Simbolo import Simbolo
from Instrucciones.Instruccion import Instruccion
from TablaArbol.NodoAST import NodoAST
import copy

class DeclaraArreglo(Instruccion):
    def __init__(self, tipo1, dimensiones, identificador, tipo2, expresiones, fila, columna):
        self.identificador = identificador
        self.tipo1 = tipo1
        self.tipo2 = tipo2
        self.dimensiones = dimensiones
        self.expresiones = expresiones
        self.fila = fila
        self.columna = columna
        self.arreglo = True


    def interpretar(self, tree, table):
        if self.getTipo1() != self.getTipo2():        #VERIFICACION DE TIPOS
            return Excepcion("Semantico", "Tipo de dato diferente en declaracion de  Arreglo.", self.fila, self.columna)
        
        if self.getDimensiones() != len(self.getExpresiones()):   #VERIFICACION DE DIMENSIONES
            return Excepcion("Semantico", "Dimensiones diferentes en Arreglo.", self.fila, self.columna)

        # CREACION DEL ARREGLO
        ArregloDimension = self.crearDimensiones(tree, table, copy.copy(self.expresiones))     #RETORNA EL ARREGLO DE DIMENSIONES
        if isinstance(ArregloDimension, Excepcion): return ArregloDimension
        simbolo = Simbolo(str(self.getIdentificador()).lower(), self.getTipo1(), self.getArreglo(), self.getFila(), self.getColumna() ArregloDimension)
        result = table.setTabla(simbolo)
        if isinstance(result, Excepcion): return result
        return None




    def getNodo(self):
        nodo = NodoAST("DECLARACION ARREGLO")
        nodo.agregarHijo(str(self.getTipo1()))
        nodo.agregarHijo(str(self.getDimensiones()))
        nodo.agregarHijo(str(self.getIdentificador()))
        nodo.agregarHijo(str(self.getTipo2()))
        exp = NodoAST("DIMENSIONES ARREGLO")
        for expresion in self.getExpresiones():
            exp.agregarHijoNodo(expresion.getNodo())
        nodo.agregarHijoNodo(exp)
        return nodo



    def crearDimensiones(self, tree, table, expresiones):
        arr = []
        if len(expresiones) == 0:
            return None
        dimension = expresiones.pop(0)
        num = dimension.interpretar(tree, table)
        if isinstance(num, Excepcion): return num
        if dimension.getTipo() != TIPO.ENTERO:
            return Excepcion("Semantico", "Expresion diferente a ENTERO en Arreglo.", self.fila, self.columna)
        contador = 0
        while contador < num:
            arr.append(self.crearDimensiones(tree, table, copy.copy(expresiones)))
            contador += 1
        return arr





    def getIdentificador(self):
        return self.identificador

    def setIdentificador(self, identificador):
        self.identificador=identificador

    def getTipo1(self):
        return self.tipo1

    def setTipo1(self, tipo):
        self.tipo1=tipo

    def getTipo2(self):
        return self.tipo2

    def setTipo2(self, tipo2):
        self.tipo2=tipo2

    def getExpresiones(self):
        return self.expresiones

    def setExpresiones(self,expresion):
        self.expresiones= expresion

    def getDimensiones(self):
        return self.dimensiones

    def setDimensiones(self,expresion):
        self.dimensiones= expresion

    def getFila(self):
        return self.fila

    def setFila(self, fila):
        self.fila= fila 

    def getColumna(self):
        return self.columna

    def setColumna(self, columna):
        self.columna= columna

    def getArreglo(self):
        return self.arreglo

    def setArreglo(self, arreglo):
        self.arreglo= arreglo
