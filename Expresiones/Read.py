
from Instrucciones.Instruccion import Instruccion
from TablaArbol.Tipo  import TIPO
from tkinter import simpledialog
from GUI import start

# aqui se obtiene la ventana donde se ejecula todo el 
# solo devuelve el valor del id

class Read(Instruccion):
    def __init__(self, fila, columna):
        self.tipo = TIPO.CADENA
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        # para el read lo unico es usar un cuadro de dialogo que abra y listo se genera el read
        # lo unico es que no se valida si solo se da un aceptar ** esto ees igual a una cadena vacia ""***
        start.IngresaConsola("hohoho")
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

