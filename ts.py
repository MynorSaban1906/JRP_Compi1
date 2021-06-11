from Tipo import TIPO
from Excepcion import Excepcion


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


class TablaSimbolos:

    def __init__(self, anterior = None):
        self.tabla = {} # Diccionario Vacio
        self.anterior = anterior
        self.funciones = []

    def setTabla(self, simbolo):      # Agregar una variable
        if simbolo.id in self.tabla :
            return Excepcion("Semantico", "Variable " + simbolo.id + " ya existe", simbolo.fila, simbolo.columna)
        else:
            self.tabla[simbolo.id] = simbolo
            return None

    def getTabla(self, id,fila,columna):            # obtener una variable
        tablaActual = self
        while tablaActual != None:
            if id in self.tabla :
                return self.tabla[id]
            else:
                tablaActual = tablaActual.anterior
        return Excepcion("Semantico", "Variable " + id + " no existe", fila, columna)

    def actualizarTabla(self, simbolo):
        tablaActual = self
        while tablaActual != None: 
            if simbolo.id in self.tabla :
                if self.tabla[simbolo.id].getTipo()==simbolo.getTipo() or  self.tabla[simbolo.id].getTipo()==TIPO.NULO or simbolo.getTipo()==TIPO.NULO:
                    self.tabla[simbolo.id].setValor(simbolo.getValor())
                    self.tabla[simbolo.id].setTipo(simbolo.getTipo())
                    return None
                return Excepcion("Semantico", "Tipo de asignacion diferente en asignar" + simbolo.id , simbolo.fila, simbolo.columna)
            else:
                tablaActual = tablaActual.anterior
        return Excepcion("Semantico", "Variable No encontrada en Asignacion", simbolo.getFila(), simbolo.getColumna())
        