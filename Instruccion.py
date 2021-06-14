

from Excepcion import Excepcion
from Tipo import OperadorAritmetico, TIPO
from abc import ABC, abstractmethod
from ts import Simbolo,TablaSimbolos

class Instruccion(ABC):
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
        super().__init__()

    @abstractmethod
    def interpretar(self, tree, table):
        pass

class Imprimir(Instruccion):
    def __init__(self, expresion, fila, columna):
        self.expresion = expresion
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        value = self.expresion.interpretar(tree, table)  # RETORNA CUALQUIER VALOR
        if isinstance(value, Excepcion) :
            return value
        

        if self.expresion.tipo == TIPO.ARREGLO:
            return Excepcion("Semantico", "No se puede imprimir un arreglo completo", self.fila, self.columna)


        tree.updateConsola(value)


class Definicion(Instruccion) :
    def __init__(self, identificador, fila, columna) :
        self.identificador=identificador
        self.fila = fila
        self.tipo=TIPO.NULO
        self.columna = columna

    def interpretar(self, tree, table):
        simbolo = Simbolo(self.identificador,self.tipo,self.fila,self.columna,None)
        result = table.setTabla(simbolo)
        
        if isinstance(result,Excepcion): return result
        
        return None

class Asignacion(Instruccion) :

    def __init__(self, identificador, expresion, fila, columna):
        self.identificador = identificador
        self.expresion = expresion
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):

        value = self.expresion.interpretar(tree, table) # Valor a asignar a la variable
        if isinstance(value, Excepcion): return value

        simbolo = Simbolo(self.identificador, self.expresion.tipo, self.fila, self.columna, value)
    
        result = table.actualizarTabla(simbolo)

        if isinstance(result, Excepcion): return result
        

        return None




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
                    if isinstance(result, Break): return result
            else:               #ELSE
                if self.instruccionesElse != None:
                    nuevaTabla = TablaSimbolos(table)       #NUEVO ENTORNO
                    for instruccion in self.instruccionesElse:
                        result = instruccion.interpretar(tree, nuevaTabla) #EJECUTA INSTRUCCION ADENTRO DEL IF
                        if isinstance(result, Excepcion) :
                            tree.getExcepciones().append(result)
                            tree.updateConsola(result.toString()) 
                        if isinstance(result, Break): return result
                elif self.elseIf != None:
                    result = self.elseIf.interpretar(tree, table)
                    if isinstance(result, Excepcion): return result
                    if isinstance(result, Break): return result

        else:
            return Excepcion("Semantico", "Tipo de dato no booleano en IF.", self.fila, self.columna)



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
                    nuevaTabla = TablaSimbolos(table)       #NUEVO ENTORNO
                    for instruccion in self.instrucciones:
                        result = instruccion.interpretar(tree, nuevaTabla) #EJECUTA INSTRUCCION ADENTRO DEL IF
                        if isinstance(result, Excepcion) :
                            tree.getExcepciones().append(result)
                            tree.updateConsola(result.toString())
                        if isinstance(result, Break): return None
                else:
                    break
            else:
                return Excepcion("Semantico", "Tipo de dato no booleano en while.", self.fila, self.columna)

class Break(Instruccion):
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        return self


class Declaracion(Instruccion):
    def __init__(self, tipo, identificador, fila, columna, expresion=None):
        self.identificador = identificador
        self.tipo = tipo
        self.expresion = expresion
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        value = self.expresion.interpretar(tree, table) # Valor a asignar a la variable
        if isinstance(value, Excepcion): return value

        simbolo = Simbolo(self.identificador, self.expresion.tipo , self.fila, self.columna, value)

        result = table.setTabla(simbolo)

        if isinstance(result, Excepcion): return result
        
        return None



class For(Instruccion):
    def __init__(self, inicial,condicion,paso,instrucciones, fila, columna):
        self.inicial=inicial
        self.condicion = condicion
        self.paso=paso
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        declaracion = self.inicial.interpretar(tree, table)
        if isinstance(declaracion, Excepcion): return declaracion # retorna error si no es correcta

        while True:
            #verifica la expresiones para ingresar al for 
            expresion = self.condicion.interpretar(tree, table)
            if isinstance(expresion, Excepcion): return expresion
            if self.condicion.tipo== TIPO.BOOLEANO:
                if bool(expresion) == True:   # VERIFICA SI ES VERDADERA LA CONDICION
                    nuevaTabla = TablaSimbolos(table)       #NUEVO ENTORNO
                    for instruccion in self.instrucciones:
                        result = instruccion.interpretar(tree, nuevaTabla) #EJECUTA INSTRUCCION ADENTRO DEL IF
                        if isinstance(result, Excepcion) :
                            tree.getExcepciones().append(result)
                            tree.updateConsola(result.toString())
                        if isinstance(result, Break): return None
                    #aumenta la variable para la siguiente iteracion
                    paso= self.paso.interpretar(tree,nuevaTabla)
                    if isinstance(paso,Excepcion): return paso

                else:
                    break

            else:
                return Excepcion("Semantico", "Tipo de dato no booleano en ciclo for.", self.fila, self.columna)




class Inc_Dec(Instruccion):
    def __init__(self, expresion,identificador, tipo, fila, columna):
        self.expresion = expresion
        self.identificador=identificador
        self.tipo =tipo
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        value = self.expresion.interpretar(tree, table) # Valor a asignar a la variable
        if isinstance(value, Excepcion): return value
        
        if self.tipo==OperadorAritmetico.AUMENTO:
            simbolo= Simbolo(self.identificador,self.expresion.tipo,self.fila,self.columna,value + 1)
        elif self.tipo==OperadorAritmetico.DECREMENTO:
            simbolo= Simbolo(self.identificador,self.expresion.tipo,self.fila,self.columna,value - 1)

        else:
            return Excepcion("Semantico", "error en caracter de incremento o decremento ", self.fila, self.columna)
            
        result=table.actualizarTabla(simbolo)
        self.tipo=simbolo.getTipo()
        if isinstance(result,Excepcion): return result


        return simbolo.getValor()


class Case(Instruccion):
    def __init__(self, expresion,recibido, fila, columna):
        self.expresion = expresion
        self.identificador=recibido
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        while True:
            condicion = self.condicion.interpretar(tree, table)
            if isinstance(condicion, Excepcion): return condicion

            if self.condicion.tipo == TIPO.BOOLEANO:
                if bool(condicion) == True:   # VERIFICA SI ES VERDADERA LA CONDICION
                    nuevaTabla = TablaSimbolos(table)       #NUEVO ENTORNO
                    for instruccion in self.instrucciones:
                        result = instruccion.interpretar(tree, nuevaTabla) #EJECUTA INSTRUCCION ADENTRO DEL IF
                        if isinstance(result, Excepcion) :
                            tree.getExcepciones().append(result)
                            tree.updateConsola(result.toString())
                        if isinstance(result, Break): return None
                else:
                    break
            else:
                return Excepcion("Semantico", "Tipo de dato no booleano en while.", self.fila, self.columna)
