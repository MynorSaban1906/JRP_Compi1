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

    def getFila(self):
        return self.fila

    def setFila(self, fila):
        self.fila= fila 

    def getColumna(self):
        return self.columna

    def setColumna(self, columna):
        self.columna= columna


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

    def getTabla(self, id):            # obtener una variable
        tablaActual = self
        while tablaActual != None:
            if id in tablaActual.tabla :
                return tablaActual.tabla[id]           # RETORNA SIMBOLO
            else:
                tablaActual = tablaActual.anterior
        return None

    def actualizarTabla(self, simbolo):
        tablaActual = self
        while tablaActual != None: 
            if simbolo.id in tablaActual.tabla :
                if tablaActual.tabla[simbolo.id].getTipo()==simbolo.getTipo() or  self.tabla[simbolo.id].getTipo()==TIPO.NULO or simbolo.getTipo()==TIPO.NULO:
                    tablaActual.tabla[simbolo.id].setValor(simbolo.getValor())
                    tablaActual.tabla[simbolo.id].setTipo(simbolo.getTipo())
                    return None
                return Excepcion("Semantico", "Tipo de diferente en la variable " + simbolo.id , simbolo.fila, simbolo.columna)
            else:
                tablaActual = tablaActual.anterior
        return Excepcion("Semantico", "Variable No encontrada en Asignacion", simbolo.getFila(), simbolo.getColumna())
        