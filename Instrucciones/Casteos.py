from TablaArbol.Tipo import TIPO,OperadorLogico
from TablaArbol.Excepcion import Excepcion
from Instrucciones.Instruccion import Instruccion
from TablaArbol.Tipo import TIPO
from TablaArbol.NodoAST import NodoAST

class Casteos(Instruccion):
    def __init__(self, tipo, expresion, fila, columna):
        self.expresion = expresion
        self.fila = fila
        self.columna = columna
        self.tipo = tipo

    
    def interpretar(self, tree, table):
        expresion = self.expresion.interpretar(tree, table)
        

        if self.getTipo() == TIPO.DECIMAL:

            if self.getExpresion().getTipo()== TIPO.ENTERO:
                try:
                    return float(self.ObtenerValor(self.getExpresion().getTipo(), expresion))
                except:
                    return Excepcion("Semantico", "No se puede castear para Float.", self.fila, self.columna)
            
            elif self.getExpresion().getTipo() == TIPO.CADENA:
                try:
                    return float(self.ObtenerValor(self.getExpresion().getTipo(), expresion))
                except:
                    return Excepcion("Semantico", "No se puede castear para Float.", self.fila, self.columna)
            
            elif self.getExpresion().getTipo() == TIPO.CHARACTER:
                try:
                    return float(self.ObtenerValor(self.getExpresion().getTipo(), expresion))
                except:
                    return Excepcion("Semantico", "No se puede castear para Float.", self.fila, self.columna)
            
            return Excepcion("Semantico", "Tipo Erroneo de casteo para Double.", self.fila, self.columna)
      
        elif self.getTipo() == TIPO.ENTERO:

            if self.getExpresion().getTipo()== TIPO.DECIMAL:
                try:
                    return int(self.ObtenerValor(self.getExpresion().getTipo(), expresion))
                except:
                    return Excepcion("Semantico", "No se puede castear para Int.", self.fila, self.columna)
            elif self.getExpresion().getTipo() == TIPO.CADENA:
                try:
                    return int(self.ObtenerValor(self.getExpresion().getTipo(), expresion))
                except:
                    return Excepcion("Semantico", "No se puede castear para Int.", self.fila, self.columna)

            elif self.getExpresion().getTipo() == TIPO.CHARACTER:
                try:
                    return int(self.ObtenerValor(self.getExpresion().getTipo(), expresion))
                except:
                    return Excepcion("Semantico", "No se puede castear para Int.", self.fila, self.columna)
            return Excepcion("Semantico", "Tipo Erroneo de casteo para Int.", self.fila, self.columna)

        elif self.getTipo() == TIPO.CADENA:

            if self.getExpresion().getTipo()== TIPO.DECIMAL:
                try:
                    return str(self.ObtenerValor(self.getExpresion().getTipo(), expresion))
                except:
                    return Excepcion("Semantico", "No se puede castear para Int.", self.fila, self.columna)
            elif self.getExpresion().getTipo() == TIPO.ENTERO:
                try:
                    return str(self.ObtenerValor(self.getExpresion().getTipo(), expresion))
                except:
                    return Excepcion("Semantico", "No se puede castear para Cadena.", self.fila, self.columna)
            return Excepcion("Semantico", "Tipo Erroneo de casteo para Cadena.", self.fila, self.columna)

        elif self.getTipo() == TIPO.CHARACTER:

            if self.getExpresion().getTipo()== TIPO.ENTERO:
                try:
                    return chr(self.ObtenerValor(self.getExpresion().getTipo(), expresion))
                except:
                    return Excepcion("Semantico", "No se puede castear para Char.", self.fila, self.columna)
            return Excepcion("Semantico", "Tipo Erroneo de casteo para Char.", self.fila, self.columna)

        elif self.getTipo() == TIPO.BOOLEANO:

            if self.getExpresion().getTipo()== TIPO.CADENA:
                if expresion.lower() in ("true","false"):
                    if expresion.lower()=="true":
                        return True
                    else:
                        return False
                        
                return Excepcion("Semantico", "Tipo Erroneo de casteo para Booleno.", self.fila, self.columna)
            return Excepcion("Semantico", "Tipo Erroneo de casteo para Booleno.", self.fila, self.columna)


    def ObtenerValor(self, tipo, val):
        if tipo == TIPO.ENTERO:
            return int(val)
        elif tipo == TIPO.DECIMAL:
            return float(val)
        elif tipo == TIPO.BOOLEANO:
            return bool(val)
        elif tipo ==TIPO.CHARACTER:
            return ord(val)
        return str(val)


    def getNodo(self):
        nodo=NodoAST("CASTEO")
        nodo.Agregar_Hijo(self.simb(self.getTipo().name))
        nodo.Agregar_Hijo_Nodo(self.getExpresion().getNodo())
        return nodo
        

    def simb(self,tipo):
        if tipo=="ENTERO":
            return "Int"
        elif tipo=="CADENA":
            return "String"
        elif tipo=="BOOLEANO":
            return "Booleano"
        elif tipo=="CHARACTER":
            return "Char"
        elif tipo=="NULO":
            return "Null"
        elif tipo=="ARREGLO":
            return "ARREGLO"
        elif tipo=="DECIMAL":
            return "Double"

    def getTipo(self):
        return self.tipo

    def setTipo(self, tipo):
        self.tipo=tipo

    def getExpresion(self):
        return self.expresion

    def setExpresion(self,expresion):
        self.expresion= expresion

    def getFila(self):
        return self.fila

    def setFila(self, fila):
        self.fila= fila 

    def getColumna(self):
        return self.columna

    def setColumna(self, columna):
        self.columna= columna
