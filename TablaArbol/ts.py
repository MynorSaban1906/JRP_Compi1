from typing import Text
from TablaArbol.Tipo import TIPO
from TablaArbol.Excepcion import Excepcion

class TablaSimbolos:

    def __init__(self, anterior = None,entorno=None,declaracionTipo=None,treeview=None):
        self.tabla = {} # Diccionario Vacio
        self.anterior = anterior
        self.entorno=entorno
        self.declaracionTipo=declaracionTipo
        self.treeview=treeview

    def setTabla(self, simbolo):      # Agregar una variable
        if simbolo.id in self.tabla :
            return Excepcion("Semantico", "Variable " + simbolo.id + " ya existe", simbolo.fila, simbolo.columna)
        else:
            self.tabla[simbolo.id] = simbolo
            # datos de la tabla
            self.treeview.insert('','end', text=str(simbolo.id),
            value=[simbolo.id,self.declaracionTipo,simbolo.getTipo().name, self.entorno, simbolo.getValor(), simbolo.getFila(), simbolo.getColumna()])

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
                if tablaActual.tabla[simbolo.id].getTipo()==simbolo.getTipo() or  tablaActual.tabla[simbolo.id].getTipo()==TIPO.NULO or simbolo.getTipo()==TIPO.NULO:
                    tablaActual.tabla[simbolo.id].setValor(simbolo.getValor())
                    tablaActual.tabla[simbolo.id].setTipo(simbolo.getTipo())
                    return None
                return Excepcion("Semantico", "Tipo de diferente en la variable " + simbolo.id , simbolo.fila, simbolo.columna)
            else:
                tablaActual = tablaActual.anterior
        return Excepcion("Semantico", "Variable No encontrada en Asignacion", simbolo.getFila(), simbolo.getColumna())
        
    def getTablaCompleta(self):
        tablaActual = self
        while tablaActual != None:
                      # RETORNA SIMBOLO
            if tablaActual.tabla==None:
                tablaActual = tablaActual.anterior

            return tablaActual
            
        return None