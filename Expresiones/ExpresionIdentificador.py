from TablaArbol.Tipo import TIPO
from TablaArbol.Simbolo import Simbolo
from TablaArbol.Excepcion import Excepcion
from Instrucciones.Instruccion import Instruccion
from TablaArbol.NodoAST import NodoAST


# identifica que que tipo y obtiene el valor de ella 
# aqui se verifica si ya existe y si no lo guarda la variable
class ExpresionIdentificador(Instruccion) :

    def __init__(self, identificador, fila, columna):
        self.identificador = identificador
        self.fila = fila
        self.columna = columna
        self.tipo = None
        self.tipo_arreglo=None
        
    def interpretar(self, tree, table):
        simbolo = table.getTabla(self.identificador.lower())
        
        if simbolo == None:
            return Excepcion("Semantico", "Variable " + self.identificador + " no encontrada.", self.fila, self.columna)
        
        if simbolo.getArreglo():
            self.tipo_arreglo=TIPO.ARREGLO
            
        self.tipo = simbolo.getTipo()
        simbolo.declaracionTipo="VARIABLE"
        
        return simbolo.getValor()


    def getNodo(self):
        nodo=NodoAST("IDENTIFICADOR")
        nodo.Agregar_Hijo(str(self.getIdentificador()))
        return nodo
        


    def getIdentificador(self):
        return self.identificador

    def setIdentificador(self, identificador):
        self.identificador=identificador

        
    def getTipo(self):
        return self.tipo

    def setTipo(self, tipo):
        self.tipo=tipo