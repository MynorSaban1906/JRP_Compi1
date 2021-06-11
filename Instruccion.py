
from Excepcion import Excepcion
from Tipo import TIPO
from abc import ABC, abstractmethod
from ts import Simbolo,TablaSimbolos

NameVariable = TablaSimbolos() #hago referencia a la tabla de simbolf=f0iaso fkopds jkaesjdk fn]o

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
    def __init__(self, id, fila, columna) :
        self.expresion = id
        self.fila = fila
        self.tipo=TIPO.NULO
        self.columna = columna

    def interpretar(self, tree, table):
        value = self.expresion
        declaracion =  Simbolo(str(self.expresion),self.tipo ,self.fila,self.columna,None)

        if isinstance(value, Excepcion) :
            return value

        response= table.setTabla(declaracion)
        if isinstance(value, Excepcion) :
            return response
        


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

class IfElse(Instruccion) : 
    '''
        Esta clase representa la instrucción if-else.
        La instrucción if-else recibe como parámetro una expresión lógica y la lista
        de instrucciones a ejecutar si la expresión lógica es verdadera y otro lista de instrucciones
        a ejecutar si la expresión lógica es falsa.
    '''

    def __init__(self, expLogica, instrIfVerdadero = [], instrIfFalso = []) :
        self.expLogica = expLogica
        self.instrIfVerdadero = instrIfVerdadero
        self.instrIfFalso = instrIfFalso

 
class Mientras(Instruccion) :
    '''
        Esta clase representa la instrucción mientras.
        La instrucción mientras recibe como parámetro una expresión lógica y la lista
        de instrucciones a ejecutar si la expresión lógica es verdadera.
    '''

    def __init__(self, expLogica, instrucciones = []) :
        self.expLogica = expLogica
        self.instrucciones = instrucciones

class Break(Instruccion):
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        return self