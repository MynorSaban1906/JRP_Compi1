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
            return Excepcion("Semantico", "Tipo de dato diferente en declaracion de  Arreglo.", self.getFila(), self.getColumna() )
        
        if self.getDimensiones() != len(self.getExpresiones()):   #VERIFICACION DE DIMENSIONES
            return Excepcion("Semantico", "Dimensiones diferentes en Arreglo.", self.getFila(), self.getColumna() )

        # se crea el arrreglo
        ArregloDimension = self.crearDimensiones(tree, table, copy.copy(self.getExpresiones()))     #RETORNA EL ARREGLO DE DIMENSIONES
       
       
        if isinstance(ArregloDimension, Excepcion): return ArregloDimension
        simbolo = Simbolo(str(self.getIdentificador()).lower(), self.getTipo1(), self.getArreglo(), self.getFila(), self.getColumna() ,ArregloDimension)
        result = table.setTabla(simbolo)
        simbolo.setDimension(self.getDimensiones())
        if isinstance(result, Excepcion): return result

        return None




    def getNodo(self):
        nodo = NodoAST("DECLARACION ARREGLO")
        nodo.Agregar_Hijo(str(self.getTipo1() ))
        nodo.Agregar_Hijo(str(self.getDimensiones()))
        nodo.Agregar_Hijo(str(self.getIdentificador()))
        nodo.Agregar_Hijo(str(self.getTipo2()))
        exp = NodoAST("DIMENSIONES ARREGLO")
        for expresion in self.getExpresiones():
            exp.Agregar_Hijo_Nodo(expresion.getNodo())
        nodo.Agregar_Hijo_Nodo(exp)
        return nodo



    def crearDimensiones(self, tree, table, expresiones):
        arr = [] # este sirve para que se guarde la recursividad

        if len(expresiones) == 0: # este es el metodo de salida para la recursividad
            # si ya no hay datos en expresiones devuelve un none
            # asi empieza a salir de la recursividad
            return None
        
        dimension = expresiones.pop(0) # va a sacar el primero
        
        num = dimension.interpretar(tree, table) #  interpreta el valor de la expresion
        
        if isinstance(num, Excepcion): return num # verifica si hay algun error
       
        if dimension.getTipo() != TIPO.ENTERO: # verifica  si el dato que tiene dimension se compara que aley tiene que ser entero
            return Excepcion("Semantico", "Expresion diferente a ENTERO en Arreglo.", self.fila, self.columna)
        contador = 0

        while contador < num: #  contador debe se ser menor al contador de parametros
            arr.append(self.crearDimensiones(tree, table, copy.copy(expresiones))) # el copy sirve para referenciar al valor 
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
