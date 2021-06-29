
from tkinter.constants import END
from Instrucciones.Instruccion import Instruccion
from TablaArbol.Tipo  import TIPO
from tkinter import simpledialog

# aqui se obtiene la ventana donde se ejecula todo el 
# solo devuelve el valor del id

class Read(Instruccion):
    def __init__(self, fila, columna):
        self.tipo = TIPO.CADENA
        self.fila = fila
        self.columna = columna
        self.tama=1
    def interpretar(self, tree, table):
        # para el read lo unico es usar un cuadro de dialogo que abra y listo se genera el read
        # lo unico es que no se valida si solo se da un aceptar ** esto ees igual a una cadena vacia ""***
        
        tree.getConsolaGUI().delete(1.0, END)
        tree.getConsolaGUI().insert("1.0",tree.getConsola())

        return simpledialog.askstring("Funcion Read","Ingresa tu texto")

    def getTipo(self):
        return self.tipo

    def setTipo(self, tipo):
        self.tipo=tipo

    def getFila(self):
        return self.fila

    def setFila(self, fila):
        self.fila= fila 

    def getColumna(self):
        return self.columna

    def setColumna(self, columna):
        self.columna= columna

