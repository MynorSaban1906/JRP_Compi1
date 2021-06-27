from TablaArbol.Excepcion import Excepcion
from TablaArbol.Simbolo import Simbolo
from TablaArbol.ts import TablaSimbolos
from Instrucciones.Instruccion import Instruccion
from Instrucciones.Break import Break
import Instrucciones.Return
from TablaArbol.Tipo import TIPO
from Instrucciones.Return import Return


class Funcion(Instruccion):
    def __init__(self, identificador,parametros, instrucciones, fila, columna):
        self.identificador = identificador
        self.parametros =parametros
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna
        self.tipo=TIPO.NULO

    def interpretar(self, tree, table):
        tablaNueva = TablaSimbolos(table)
        for instruccion in self.instrucciones:      # recorrre las instruciones dentro de las funciones
            value = instruccion.interpretar(tree,tablaNueva)
            if isinstance(value, Excepcion) :
                tree.getExcepciones().append(value)
                tree.updateConsola(value.toString())
            if isinstance(value, Break): 
                err = Excepcion("Semantico", "Sentencia BREAK fuera de ciclo", instruccion.fila, instruccion.columna)
                tree.getExcepciones().append(err)
                tree.updateConsola(err.toString())

            if isinstance(value, Return): # cuando encuetre un Return 
                self.setTipo(value.getTipo()) # tomaria el tipo de lo que devuelve la funcion
                return value.getNodo() # si encontro el return entonces devulve el valor que tenia el return

        return None # por defecto



    def getIdentificador(self):
        return self.identificador

    def setIdentificador(self, identificador):
        self.identificador=identificador

    def getTipo(self):
        return self.tipo

    def setTipo(self, tipo):
        self.tipo=tipo


    def getParametros(self):
        return self.parametros

    def setParametros(self, parametros):
        self.parametros=parametros