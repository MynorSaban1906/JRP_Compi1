
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
        self.tipo=None
        self.columna = columna

    def interpretar(self, tree, table):
        response=""
        value =  Simbolo(self.expresion,self.tipo ,self.fila,self.columna,0)

        if isinstance(value, Excepcion) :
            return value

        response= NameVariable.setTabla(value)

        tree.updateConsola(response)


class Asignacion(Instruccion) :

    def __init__(self, id, expNumerica,fila,columna) :
        self.id = id
        self.Tipo=None
        self.expNumerica = expNumerica
        self.fila = fila
        self.columna= columna

    def interpretar(self, tree, table):
        response=""
        value =  Simbolo(self.id,self.Tipo,self.fila,self.columna,self.expNumerica)
        self.Tipo=TIPO.ENTERO
                        
        if isinstance(value, Excepcion) :
            return value

        response= NameVariable.actualizarTabla(value)

        tree.updateConsola(self.Tipo)

class If(Instruccion) : 
    '''
        Esta clase representa la instrucción if.
        La instrucción if recibe como parámetro una expresión lógica y la lista
        de instrucciones a ejecutar si la expresión lógica es verdadera.
    '''

    def __init__(self, expLogica, instrucciones = []) :
        self.expLogica = expLogica
        self.instrucciones = instrucciones

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

