from enum import Enum
import Excepcion


class Simbolo:
    
    def __init__(self, identificador, tipo, fila, columna, valor ):
        self.id = identificador
        self.tipo = tipo
        self.fila = fila
        self.columna = columna
        self.valor = valor

    def getID(self):
        return self.id

    def setID(self, id):
        self.id = id

    def getTipo(self):
        return self.tipo

    def setTipo(self, tipo):
        self.tipo = tipo  

    def getValor(self):
        return self.valor

    def setValor(self, valor):
        self.valor = valor

class nada:
    
    def __init__(self ):
        self.id = None
        self.tipo = None
        self.fila = None
        self.columna = None
        self.valor = None
class TablaSimbolos:

    def __init__(self, anterior = None):
        self.tabla = {} # Diccionario Vacio
        self.anterior = anterior
        self.funciones = []

    def setTabla(self, simbolo):      # Agregar una variable
        if simbolo.id in self.tabla :
            return ("Semantico"+ "- Variable " + simbolo.id + " ya existe ["+ str(simbolo.fila)+" ,"+ str(simbolo.columna)+"]")
        else:
            self.tabla[simbolo.id] = simbolo
            return "VARIABLE GUARDADA"

    def getTabla(self, id,fila,columna):            # obtener una variable
        tablaActual = self
        while tablaActual != None:
            if id in self.tabla :
                return self.tabla[id].getValor()
            else:
                tablaActual = tablaActual.anterior
        return  ("Semantico"+ "- Variable " + id + " no existe ["+ str(fila)+" ,"+ str(columna)+"]")

    def actualizarTabla(self, simbolo):
        tablaActual = self
        while tablaActual != None: 
            if simbolo.id in self.tabla :
                self.tabla[simbolo.id].setValor(simbolo.getValor())
                return "Variable Actualizada"
            else:
                tablaActual = tablaActual.anterior
        return ("Semantico"+ "- Variable " + simbolo.id + " no existe ["+ str(simbolo.fila)+" ,"+ str(simbolo.columna)+"]")
        