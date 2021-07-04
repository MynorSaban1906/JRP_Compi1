from TablaArbol.Excepcion import Excepcion
from TablaArbol.Simbolo import Simbolo
from TablaArbol.ts import TablaSimbolos
from Instrucciones.Instruccion import Instruccion
from Instrucciones.Break import Break
from TablaArbol.Tipo import TIPO
from Instrucciones.Return import Return
from TablaArbol.NodoAST import NodoAST


class Funcion(Instruccion):
    def __init__(self, identificador,parametros, instrucciones, fila, columna):
        self.identificador = identificador.lower()
        self.parametros =parametros
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna
        self.tipo=TIPO.NULO

    def interpretar(self, tree, table):
        tablaNueva = TablaSimbolos(table,"Funcion "+ str(self.getIdentificador()),declaracionTipo="variable",treeview=table.treeview)
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


    def getNodo(self):
        nodo=NodoAST("FUNCION")
        nodo.Agregar_Hijo(str(self.getIdentificador()))
        parametros =NodoAST("PARAMETROS")
        for param in self.getParametros():
            parametro= NodoAST("PARAMETRO")
            parametro.Agregar_Hijo(param["tipo"])
            parametro.Agregar_Hijo(param["identificador"])
            parametros.Agregar_Hijo_Nodo(parametro)
            
        nodo.Agregar_Hijo_Nodo(parametros)

        instrucciones=NodoAST("INSTRUCCIONES")
        for instr in self.instrucciones:
            instrucciones.Agregar_Hijo_Nodo(instr.getNodo())

        nodo.Agregar_Hijo_Nodo(instrucciones)
        
        return nodo

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