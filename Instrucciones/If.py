from Instrucciones.Continue import Continue
from TablaArbol.Excepcion import Excepcion
from TablaArbol.Tipo import TIPO
from TablaArbol.ts import TablaSimbolos
from Instrucciones.Instruccion import Instruccion
from Instrucciones.Break import Break
from Instrucciones.Return import Return
from TablaArbol.NodoAST import NodoAST



class If(Instruccion):
    def __init__(self, condicion, instruccionesIf, instruccionesElse, ElseIf, fila, columna):
        self.condicion = condicion
        self.instruccionesIf = instruccionesIf
        self.instruccionesElse = instruccionesElse
        self.elseIf = ElseIf
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        condicion = self.condicion.interpretar(tree, table)
        if isinstance(condicion, Excepcion): return condicion

        if self.condicion.tipo == TIPO.BOOLEANO:
            if bool(condicion) == True:   # VERIFICA SI ES VERDADERA LA CONDICION
                nuevaTabla = TablaSimbolos(table)       #NUEVO ENTORNO
                for instruccion in self.instruccionesIf:
                    result = instruccion.interpretar(tree, nuevaTabla) #EJECUTA INSTRUCCION ADENTRO DEL IF
                    if isinstance(result, Excepcion) :
                        tree.getExcepciones().append(result)
                        tree.updateConsola(result.toString())
                    if isinstance(result, Return): return result
                    if isinstance(result, Continue): return result
                    if isinstance(result, Break): return result
            else:               #ELSE
                if self.instruccionesElse != None:
                    nuevaTabla = TablaSimbolos(table)       #NUEVO ENTORNO
                    for instruccion in self.instruccionesElse:
                        result = instruccion.interpretar(tree, nuevaTabla) #EJECUTA INSTRUCCION ADENTRO DEL IF
                        if isinstance(result, Excepcion) :
                            tree.getExcepciones().append(result)
                            tree.updateConsola(result.toString()) 
                        if isinstance(result, Return): return result
                        if isinstance(result, Break): return result
                        if isinstance(result, Continue): return result
                elif self.elseIf != None:
                    result = self.elseIf.interpretar(tree, table)
                    if isinstance(result, Excepcion): return result
                    if isinstance(result, Return): return result
                    if isinstance(result, Break): return result
                    if isinstance(result, Continue): return result

        else:
            return Excepcion("Semantico", "Tipo de dato no booleano en IF.", self.fila, self.columna)

    def getNodo(self):
        nodo=NodoAST("IF")

        instruccionesIf=NodoAST("INSTRUCCIONES IF")
        for instr in self.instruccionesIf:
            instruccionesIf.Agregar_Hijo_Nodo(instr.getNodo())
        nodo.Agregar_Hijo_Nodo(instruccionesIf)

        if self.instruccionesElse != None:
            instruccionesElse=NodoAST("INSTRUCCIONES ELSE")
            for instr in self.instruccionesElse:
                instruccionesElse.Agregar_Hijo_Nodo(instr.getNodo())
            nodo.Agregar_Hijo_Nodo(instruccionesElse)

        elif self.elseIf != None:
            nodo.Agregar_Hijo_Nodo(self.elseIf.getNodo())
        
        return nodo