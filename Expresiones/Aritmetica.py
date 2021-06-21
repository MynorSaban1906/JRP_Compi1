from TablaArbol.Simbolo import Simbolo
from TablaArbol.Tipo import TIPO,OperadorAritmetico
from Expresiones.ExpresionIdentificador import ExpresionIdentificador
from TablaArbol.Excepcion import Excepcion
from Instrucciones.Instruccion import Instruccion


class Aritmetica(Instruccion):
    def __init__(self, operador, OperacionIzq, OperacionDer, fila, columna):
        self.operador = operador
        self.OperacionIzq = OperacionIzq
        self.OperacionDer = OperacionDer
        self.fila = fila
        self.columna = columna
        self.tipo = None


    def interpretar(self, tree, table):
        # verifica las instrucciones de cada operador
        #el . interprete sirve para que ejecute las instrucciones que se adecuen al tipo de operacion
        izq = self.OperacionIzq.interpretar(tree, table)
        if isinstance(izq, Excepcion): return izq
        if self.OperacionDer != None:
            der = self.OperacionDer.interpretar(tree, table)
            if isinstance(der, Excepcion): return der

        # aqui se verifica el tipo de operaciones aritmeticas que se realizar 
        if self.operador == OperadorAritmetico.MAS: #SUMA
            # OPERACION SOLO DE ENTEROS
            if self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.ENTERO:
                self.tipo = TIPO.ENTERO
                return self.obtenerVal(self.OperacionIzq.tipo, izq) + self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.DECIMAL:
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo, izq) + self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.CADENA:
                self.tipo = TIPO.CADENA
                return str(self.obtenerVal(self.OperacionIzq.tipo, izq)) + self.obtenerVal(self.OperacionDer.tipo, der)
                # SOLO FALTA LOS BOLEANOS TENGO DUDA DE ESO AUN            
            elif self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.BOOLEANO: 
                self.tipo = TIPO.ENTERO
                return self.obtenerVal(self.OperacionIzq.tipo, izq) + self.obtenerVal(self.OperacionDer.tipo, der) 

            # OPERACION SOLO DE DECIMALES
            if self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.ENTERO:
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo, izq) + self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.DECIMAL:
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo, izq) + self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.CADENA:
                self.tipo = TIPO.CADENA
                return str(self.obtenerVal(self.OperacionIzq.tipo, izq)) + self.obtenerVal(self.OperacionDer.tipo, der)
                # SOLO FALTA LOS BOLEANOS TENGO DUDA DE ESO AUN            
            elif self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.BOOLEANO: 
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo, izq) + self.obtenerVal(self.OperacionDer.tipo, der) 

            # OPERACION SOLO DE BOLEANO
            if self.OperacionIzq.tipo == TIPO.BOOLEANO and self.OperacionDer.tipo == TIPO.ENTERO:
                self.tipo = TIPO.ENTERO
                return self.obtenerVal(self.OperacionIzq.tipo, izq) + self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == TIPO.BOOLEANO and self.OperacionDer.tipo == TIPO.DECIMAL:
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo, izq) + self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == TIPO.BOOLEANO and self.OperacionDer.tipo == TIPO.CADENA:
                self.tipo = TIPO.CADENA
                return str(self.obtenerVal(self.OperacionIzq.tipo, izq)) + self.obtenerVal(self.OperacionDer.tipo, der)
            # SOLO FALTA LOS BOLEANOS TENGO DUDA DE ESO AUN            
            elif self.OperacionIzq.tipo == TIPO.BOOLEANO and self.OperacionDer.tipo == TIPO.BOOLEANO: 
                self.tipo = TIPO.ENTERO
                return self.obtenerVal(self.OperacionIzq.tipo, izq) + self.obtenerVal(self.OperacionDer.tipo, der) 
                        

            # OPERACION SOLO DE CHAR
            if self.OperacionIzq.tipo == TIPO.CHARACTER and self.OperacionDer.tipo == TIPO.CHARACTER:
                self.tipo = TIPO.CADENA
                return self.obtenerVal(self.OperacionIzq.tipo, izq) + self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == TIPO.CHARACTER and self.OperacionDer.tipo == TIPO.CADENA:
                self.tipo = TIPO.CADENA
                return self.obtenerVal(self.OperacionIzq.tipo, izq) + self.obtenerVal(self.OperacionDer.tipo, der)

            # OPERACION SOLO DE STRING
            if self.OperacionIzq.tipo == TIPO.CADENA and self.OperacionDer.tipo == TIPO.ENTERO:
                self.tipo = TIPO.CADENA
                return self.obtenerVal(self.OperacionIzq.tipo, izq) + str(self.obtenerVal(self.OperacionDer.tipo, der))
            elif self.OperacionIzq.tipo == TIPO.CADENA and self.OperacionDer.tipo == TIPO.DECIMAL:
                self.tipo = TIPO.CADENA
                return self.obtenerVal(self.OperacionIzq.tipo, izq)+ str(self.obtenerVal(self.OperacionDer.tipo, der))
            elif self.OperacionIzq.tipo == TIPO.CADENA and self.OperacionDer.tipo == TIPO.CHARACTER:
                self.tipo = TIPO.CADENA
                return str(self.obtenerVal(self.OperacionIzq.tipo, izq)) + self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == TIPO.CADENA and self.OperacionDer.tipo == TIPO.CADENA:
                self.tipo = TIPO.CADENA
                return str(self.obtenerVal(self.OperacionIzq.tipo, izq)) + self.obtenerVal(self.OperacionDer.tipo, der)
                # SOLO FALTA LOS BOLEANOS TENGO DUDA DE ESO AUN            
            elif self.OperacionIzq.tipo == TIPO.CADENA and self.OperacionDer.tipo == TIPO.BOOLEANO: 
                self.tipo = TIPO.CADENA
                return str(self.obtenerVal(self.OperacionIzq.tipo, izq)) + str(self.obtenerVal(self.OperacionDer.tipo, der))


            return Excepcion("Semantico", "Tipo Erroneo de operacion para +.", self.fila, self.columna)

        elif self.operador == OperadorAritmetico.MENOS:#RESTA
            if self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.ENTERO:
                self.tipo = TIPO.ENTERO
                return self.obtenerVal(self.OperacionIzq.tipo, izq) - self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.DECIMAL:
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo, izq) - self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.BOOLEANO:
                self.tipo = TIPO.ENTERO
                return self.obtenerVal(self.OperacionIzq.tipo, izq) - self.obtenerVal(self.OperacionDer.tipo, der)

            # OPERACION SOLO DE DECIMALES
            if self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.ENTERO:
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo, izq) - self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.DECIMAL:
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo, izq) - self.obtenerVal(self.OperacionDer.tipo, der)
               # SOLO FALTA LOS BOLEANOS TENGO DUDA DE ESO AUN            
            elif self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.BOOLEANO: 
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo, izq) - self.obtenerVal(self.OperacionDer.tipo, der) 

            # OPERACION SOLO DE BOLEANOS
            if self.OperacionIzq.tipo == TIPO.BOOLEANO and self.OperacionDer.tipo == TIPO.ENTERO:
                self.tipo = TIPO.ENTERO
                return self.obtenerVal(self.OperacionIzq.tipo, izq) - self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == TIPO.BOOLEANO and self.OperacionDer.tipo == TIPO.DECIMAL:
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo, izq) - self.obtenerVal(self.OperacionDer.tipo, der)

            return Excepcion("Semantico", "Tipo Erroneo de operacion para -.", self.fila, self.columna)

        elif self.operador == OperadorAritmetico.POR:#Multiplicacion
            if self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.ENTERO:
                self.tipo = TIPO.ENTERO
                return self.obtenerVal(self.OperacionIzq.tipo, izq) * self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.DECIMAL:
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo, izq) * self.obtenerVal(self.OperacionDer.tipo, der)
                
                #PARA DECIMAL
            elif self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.ENTERO:
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo, izq) * self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.DECIMAL:
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo, izq) * self.obtenerVal(self.OperacionDer.tipo, der)

            return Excepcion("Semantico", "Tipo Erroneo de operacion para *.", self.fila, self.columna)
        
        elif self.operador == OperadorAritmetico.DIV:#DIVISION
            if der!=0:
                if self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.ENTERO:
                    self.tipo = TIPO.ENTERO
                    return self.obtenerVal(self.OperacionIzq.tipo, izq) / self.obtenerVal(self.OperacionDer.tipo, der)
                elif self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.DECIMAL:
                    self.tipo = TIPO.DECIMAL
                    return self.obtenerVal(self.OperacionIzq.tipo, izq) / self.obtenerVal(self.OperacionDer.tipo, der)
                    
                    #PARA DECIMAL
                elif self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.ENTERO:
                    self.tipo = TIPO.DECIMAL
                    return self.obtenerVal(self.OperacionIzq.tipo, izq) / self.obtenerVal(self.OperacionDer.tipo, der)
                elif self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.DECIMAL:
                    self.tipo = TIPO.DECIMAL
                    return self.obtenerVal(self.OperacionIzq.tipo, izq) / self.obtenerVal(self.OperacionDer.tipo, der)
                return Excepcion("Semantico", "Tipo Erroneo de operacion para /.", self.fila, self.columna)
            else:
                return Excepcion("Semantico", "Error de operacion Division entre 0 No permitido", self.fila, self.columna)

        elif self.operador == OperadorAritmetico.UMENOS:#NEGATIVIDAD UMENOS
            if self.OperacionIzq.tipo == TIPO.ENTERO :
                self.tipo = TIPO.ENTERO
                return -self.obtenerVal(self.OperacionIzq.tipo, izq)
            elif self.OperacionIzq.tipo == TIPO.DECIMAL :
                self.tipo = TIPO.DECIMAL
                return -self.obtenerVal(self.OperacionIzq.tipo, izq)
            return Excepcion("Semantico", "Tipo Erroneo de operacion para menos unario.", self.fila, self.columna)

        elif self.operador == OperadorAritmetico.POT:#POTENCIA
            
            if self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.ENTERO:
                self.tipo = TIPO.ENTERO
                return self.obtenerVal(self.OperacionIzq.tipo, izq) ** self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.DECIMAL:
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo, izq) ** self.obtenerVal(self.OperacionDer.tipo, der)
                
                #PARA DECIMAL
            elif self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.ENTERO:
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo, izq) ** self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.DECIMAL:
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo, izq) ** self.obtenerVal(self.OperacionDer.tipo, der)
            return Excepcion("Semantico", "Tipo Erroneo de operacion para **.", self.fila, self.columna)

        elif self.operador == OperadorAritmetico.MOD:#MODULO
            if der !=0:
                if self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.ENTERO:
                    self.tipo = TIPO.ENTERO
                    return self.obtenerVal(self.OperacionIzq.tipo, izq) % self.obtenerVal(self.OperacionDer.tipo, der)
                elif self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.DECIMAL:
                    self.tipo = TIPO.DECIMAL
                    return self.obtenerVal(self.OperacionIzq.tipo, izq) % self.obtenerVal(self.OperacionDer.tipo, der)
                    
                    #PARA DECIMAL
                elif self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.ENTERO:
                    self.tipo = TIPO.DECIMAL
                    return self.obtenerVal(self.OperacionIzq.tipo, izq) % self.obtenerVal(self.OperacionDer.tipo, der)
                elif self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.DECIMAL:
                    self.tipo = TIPO.DECIMAL
                    return self.obtenerVal(self.OperacionIzq.tipo, izq) % self.obtenerVal(self.OperacionDer.tipo, der)
                return Excepcion("Semantico", "Tipo Erroneo de operacion para % .", self.fila, self.columna)
            else:
                return Excepcion("Semantico", "Operacion no valida modulo de 0 .", self.fila, self.columna)
        
        elif self.operador in (OperadorAritmetico.AUMENTO,OperadorAritmetico.DECREMENTO):# AUMENTO Y DECREMENTO
            if not isinstance(self.OperacionIzq,ExpresionIdentificador): return Excepcion("Semantico", " Decremento no identificador", self.fila, self.columna)
            if self.operador==OperadorAritmetico.AUMENTO:
                simbolo= Simbolo(self.OperacionIzq.identificador,self.OperacionIzq.tipo,self.fila,self.columna,self.obtenerVal(self.OperacionIzq.tipo, izq) + 1)
            elif self.operador==OperadorAritmetico.DECREMENTO:
                simbolo= Simbolo(self.OperacionIzq.identificador,self.OperacionIzq.tipo,self.fila,self.columna,self.obtenerVal(self.OperacionIzq.tipo, izq) - 1)
            
            result=table.actualizarTabla(simbolo)
            
            if isinstance(result,Excepcion): return result

            self.tipo= self.OperacionIzq.tipo

            return simbolo.getValor()


    #se castea el valor que tiene para que no de error al ejecutarse en el interprete
    def obtenerVal(self, tipo, val):
        if tipo == TIPO.ENTERO:
            return int(val)
        elif tipo == TIPO.DECIMAL:
            return float(val)
        elif tipo == TIPO.BOOLEANO:
            return bool(val)
        return str(val)
        