from TablaArbol.Simbolo import Simbolo
from TablaArbol.Tipo import TIPO,OperadorLogico
from TablaArbol.Excepcion import Excepcion
from Instrucciones.Instruccion import Instruccion
from TablaArbol.NodoAST import NodoAST

class Logica(Instruccion):
    def __init__(self, operador, OperacionIzq, OperacionDer, fila, columna):
        self.operador = operador
        self.OperacionIzq = OperacionIzq
        self.OperacionDer = OperacionDer
        self.fila = fila
        self.columna = columna
        self.tipo = TIPO.BOOLEANO

    # operaciones logicas 
    # se inerpretan cada instruccion segun el operador en este caso es el simbolo 
    # lo cual debe de generar una respuesta booleana
    def interpretar(self, tree, table):
        izq = self.OperacionIzq.interpretar(tree, table)
        if isinstance(izq, Excepcion): return izq
        if self.OperacionDer != None:
            der = self.OperacionDer.interpretar(tree, table)
            if isinstance(der, Excepcion): return der

        if self.operador == OperadorLogico.AND:
            if self.OperacionIzq.tipo == TIPO.BOOLEANO and self.OperacionDer.tipo == TIPO.BOOLEANO:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) and self.obtenerVal(self.OperacionDer.tipo, der)
            return Excepcion("Semantico", "Tipo Erroneo de operacion para AND &&. ", self.fila, self.columna)
        elif self.operador == OperadorLogico.OR:
            if self.OperacionIzq.tipo == TIPO.BOOLEANO and self.OperacionDer.tipo == TIPO.BOOLEANO:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) or self.obtenerVal(self.OperacionDer.tipo, der)
            return Excepcion("Semantico", "Tipo Erroneo de operacion para OR ||. ", self.fila, self.columna)
        elif self.operador == OperadorLogico.NOT:
            if self.OperacionIzq.tipo == TIPO.BOOLEANO:
                return not self.obtenerVal(self.OperacionIzq.tipo, izq)
            return Excepcion("Semantico", "Tipo Erroneo de operacion para NOT !. ", self.fila, self.columna)
        return Excepcion("Semantico", "Tipo de Operacion no Especificado. ", self.fila, self.columna)

    def obtenerVal(self, tipo, val):
        if tipo == TIPO.ENTERO:
            return int(val)
        elif tipo == TIPO.DECIMAL:
            return float(val)
        elif tipo == TIPO.BOOLEANO:
            return bool(val)
        return str(val)


    def getNodo(self):
        nodo= NodoAST("LOGICA")  
        if self.OperacionDer != None:
            nodo.Agregar_Hijo_Nodo(self.OperacionIzq.getNodo())
            nodo.Agregar_Hijo(str(self.operador))
            nodo.Agregar_Hijo_Nodo(self.OperacionDer.getNodo())
        else:
            nodo.Agregar_Hijo(str(self.operador))
            nodo.Agregar_Hijo_Nodo(self.OperacionIzq.getNodo())
            
        return nodo