from enum import Enum

class TIPO(Enum):
    ENTERO = 1
    DECIMAL = 2
    BOOLEANO = 3
    CHARACTER = 4
    CADENA = 5
    NULO = 6
    ARREGLO = 7
    ID=8

class OperadorAritmetico(Enum):
    MAS = 1
    MENOS = 2
    POR = 3
    DIV = 4
    POT = 5
    MOD = 6
    UMENOS = 7

class OperadorRelacional(Enum):
    MENORQUE = 1
    MAYORQUE = 2
    IGUALIGUAL = 3
    DIFERENTE = 4
    MENORIGUAL = 5
    MAYORIGUAL = 6

class OperadorLogico(Enum):
    NOT = 1
    AND = 2
    OR = 3