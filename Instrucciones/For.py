from TablaArbol.NodoAST import NodoAST
from Instrucciones.Continue import Continue
from TablaArbol.Excepcion import Excepcion
from TablaArbol.Tipo import OperadorAritmetico,TIPO
from abc import ABC, abstractmethod
from TablaArbol.Simbolo import Simbolo
from TablaArbol.ts import TablaSimbolos
from Instrucciones.Instruccion import Instruccion
from Instrucciones.Break import Break
from Instrucciones.Return import Return

class For(Instruccion):
    def __init__(self, inicial,condicion,paso,instrucciones, fila, columna):
        self.inicial=inicial
        self.condicion = condicion
        self.paso=paso
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        nuevaTabla = TablaSimbolos(table,"FOR ",declaracionTipo="variable",treeview=table.treeview)       #NUEVO ENTORNO
        declaracion = self.inicial.interpretar(tree, nuevaTabla)
        if isinstance(declaracion, Excepcion): return declaracion # retorna error si no es correcta

        while True:
            #verifica la expresiones para ingresar al for 
            expresion = self.condicion.interpretar(tree, nuevaTabla)
            if isinstance(expresion, Excepcion): return expresion
            if self.condicion.tipo== TIPO.BOOLEANO:
                if bool(expresion) == True:   # VERIFICA SI ES VERDADERA LA CONDICION
                    nuevaTabla2 = TablaSimbolos(nuevaTabla ,"Funcion ",declaracionTipo="variable",treeview=table.treeview)       #NUEVO ENTORNO
                    for instruccion in self.instrucciones:
                        result = instruccion.interpretar(tree, nuevaTabla2) #EJECUTA INSTRUCCION ADENTRO DEL IF
                        if isinstance(result, Excepcion) :
                            tree.getExcepciones().append(result)
                            tree.updateConsola(result.toString())

                        if isinstance(result, Break): return None
                        if isinstance(result, Return): return result
                        if isinstance(result, Continue): return None

                    #aumenta la variable para la siguiente iteracion
                    paso= self.paso.interpretar(tree,nuevaTabla2)
                    if isinstance(paso,Excepcion): return paso

                else:
                    break

            else:
                return Excepcion("Semantico", "Tipo de dato no booleano en ciclo for.", self.fila, self.columna)
    def getNodo(self):
        nodo=NodoAST("FOR")
        nodo.Agregar_Hijo_Nodo(self.inicial.getNodo())
        nodo.Agregar_Hijo_Nodo(self.condicion.getNodo())
        nodo.Agregar_Hijo_Nodo(self.paso.getNodo())
        
        instrucciones=NodoAST("INSTRUCCIONES")
        for instr in self.instrucciones:
            instrucciones.Agregar_Hijo_Nodo(instr.getNodo())

        nodo.Agregar_Hijo_Nodo(instrucciones)
        
        return nodo