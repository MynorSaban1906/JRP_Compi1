from Instrucciones.Continue import Continue
from TablaArbol.Excepcion import Excepcion
from TablaArbol.Tipo import OperadorAritmetico,TIPO
from abc import ABC, abstractmethod
from TablaArbol.Simbolo import Simbolo
from TablaArbol.ts import TablaSimbolos
from Instrucciones.Instruccion import Instruccion
from Instrucciones.Break import Break
from Instrucciones.Return import Return
from TablaArbol.NodoAST import NodoAST





class While(Instruccion):
    def __init__(self, condicion, instrucciones, fila, columna):
        self.condicion = condicion
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        while True:
            condicion = self.condicion.interpretar(tree, table)
            if isinstance(condicion, Excepcion): return condicion

            if self.condicion.tipo == TIPO.BOOLEANO:
                if bool(condicion) == True:   # VERIFICA SI ES VERDADERA LA CONDICION
                    nuevaTabla = TablaSimbolos(table," WHILE " ,declaracionTipo="variable",treeview=table.treeview)      #NUEVO ENTORNO
                    for instruccion in self.instrucciones:
                        result = instruccion.interpretar(tree, nuevaTabla) #EJECUTA INSTRUCCION ADENTRO DEL IF
                        if isinstance(result, Excepcion) :
                            tree.getExcepciones().append(result)
                            tree.updateConsola(result.toString())
                        if isinstance(result, Break): return None
                        if isinstance(result, Return): return result
                        if isinstance(result, Continue): break
                else:
                    break
            else:
                return Excepcion("Semantico", "Tipo de dato no booleano en while.", self.fila, self.columna)

    def getNodo(self):
        nodo=NodoAST("WHILE")

        instrucciones=NodoAST("INSTRUCCIONES")
        for instr in self.instrucciones:
            instrucciones.Agregar_Hijo_Nodo(instr.getNodo())

        nodo.Agregar_Hijo_Nodo(instrucciones)
        
        return nodo