from Instrucciones.Instruccion import Instruccion
from TablaArbol.Tipo  import TIPO

# solo devuelve el valor del id
class Read(Instruccion):
    def __init__(self, fila, columna):
        self.tipo = TIPO.CADENA
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        print(tree.getConsola()) # imprime lo que ya estaba en la consola 
        tree.setConsola("")     # resetea la consola pero esto es una prueba en visual
        lectura = input("Ingreso a un READ. Ingrese el valor : ") # obtiene el valor que se ingresa pero este solo es en string
        return lectura 

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
