from typing import List
from TablaArbol.Tipo import TIPO
from TablaArbol.Excepcion import Excepcion
from TablaArbol.Simbolo import Simbolo
from Instrucciones.Instruccion import Instruccion
from TablaArbol.NodoAST import NodoAST
import copy

class AcessoArreglo(Instruccion):
    def __init__(self,identificador, lista, fila, columna):
        self.identificador = identificador
        self.listaexpresion=lista
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        simbolo = table.getTabla(self.identificador.lower())
        
        if simbolo == None:
            return Excepcion("Semantico", "Variable " + self.identificador + " no encontrada.", self.getFila(), self.getColumna() )

        if not simbolo.getArreglo():
            return Excepcion("Semantico", self.identificador +" No es un arreglo ", self.getFila(), self.getColumna() )
        
        self.tipo=simbolo.getTipo()
    

        # obtiene el arreglo 
        Arreglo = self.Buscar(tree, table, copy.copy(self.getListaExpresion()),simbolo.getValor())   #RETORNA EL ARREGLO DE DIMENSIONES
       
        if isinstance(Arreglo,Excepcion):return Arreglo

        if isinstance(Arreglo,List) :return Excepcion("Semantico", self.identificador +" No es un arreglo ", self.getFila(), self.getColumna() )
      
      
        return Arreglo




    def getNodo(self):
        nodo = NodoAST("DECLARACION ARREGLO")
        nodo.Agregar_Hijo(str(self.getIdentificador()))
        exp = NodoAST("DIMENSIONES ARREGLO")
        for expresion in self.getListaExpresion():
            exp.Agregar_Hijo_Nodo(expresion.getNodo())
        nodo.Agregar_Hijo_Nodo(exp)
        return nodo



    def Buscar(self, tree, table, expresiones,arreglo):
        valorArreglo =None
        if len(expresiones) == 0:
            return arreglo
        if not isinstance(arreglo, list):
            return Excepcion("Semantico", "Accesos de más en un Arreglo.", self.fila, self.columna)
        dimension = expresiones.pop(0)
        num = dimension.interpretar(tree, table)
        if isinstance(num, Excepcion): return num
        if dimension.tipo != TIPO.ENTERO:
            return Excepcion("Semantico", "Expresion diferente a ENTERO en Arreglo.", self.fila, self.columna)
        try:
            valorArreglo = self.Buscar(tree, table, copy.copy(expresiones), arreglo[num]) # entra al arreglo ue se necesita
        except:
            return Excepcion("Semantico", "No se puede acceder a la posicion del arreglo  "+ self.getIdentificador() ,  self.getFila(), self.getColumna() )
           
        return valorArreglo



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
