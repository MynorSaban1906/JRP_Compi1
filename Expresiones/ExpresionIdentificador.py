from TablaArbol.Simbolo import Simbolo
from TablaArbol.Excepcion import Excepcion
from Instrucciones.Instruccion import Instruccion


# identifica que que tipo y obtiene el valor de ella 
# aqui se verifica si ya existe y si no lo guarda la variable
class ExpresionIdentificador(Instruccion) :

    def __init__(self, identificador, fila, columna):
        self.identificador = identificador
        self.fila = fila
        self.columna = columna
        self.tipo = None

    def interpretar(self, tree, table):
        simbolo = table.getTabla(self.identificador.lower())
        
        if simbolo == None:
            return Excepcion("Semantico", "Variable " + self.identificador + " no encontrada.", self.fila, self.columna)

        self.tipo = simbolo.getTipo()
        
        return simbolo.getValor()
    def getIdentificador(self):
        return self.identificador

    def setIdentificador(self, identificador):
        self.identificador=identificador
