from TablaArbol.Excepcion import Excepcion
from TablaArbol.Simbolo import Simbolo
from TablaArbol.ts import TablaSimbolos
from Instrucciones.Instruccion import Instruccion
from Instrucciones.Break import Break
from Instrucciones.Funcion import Funcion
from Instrucciones.Return import  Return

class InvocaFuncion(Instruccion):
    def __init__(self, nombre,parametros,fila, columna):
        self.identificador = nombre
        self.fila = fila
        self.parametros=parametros  
        self.columna = columna
        self.tipo =None

        
    def interpretar(self, tree, table):
        #se obtiene la funcion , este esta en el arbol que nunca se cambia simpre es el mismo
        funcion = tree.getFuncion(self.identificador)
        if funcion==None: # si no encontro la funcion entonces  genera un errro
            return Excepcion("Semantico", "No se encontro la funcion "+ self.identificador, self.fila, self.columna)
        nuevaTabla=TablaSimbolos(table)
        # obtener los parametros 
        if len(funcion.getParametros())==len(self.getParametros()): # si trae los msmos parametros que la funcion 
            contador=0
            for expresion in self.getParametros(): # se obtiene el valor del parametro en la llamada
                resultadoExpresion=expresion.interpretar(tree,nuevaTabla)

                if isinstance(resultadoExpresion,Excepcion): return resultadoExpresion

                # se debe validar que sean del mismo tipo, los parametrso de la llamada con los parametros de la funcion
                if funcion.parametros[contador]['tipo']== expresion.getTipo():
                    #creacion de simbolo e ingresandolo a la tabla de simbolo
                    simbolo = Simbolo(str(funcion.parametros[contador]['identificador']).lower(), funcion.parametros[contador]['tipo'], self.getFila(), self.getColumna(),resultadoExpresion)
                    result=nuevaTabla.setTabla(simbolo)
                    if isinstance(result,Excepcion): return result


                else:
                    return Excepcion("Semantico", "Tipo Diferente en los parametros de llamada ", self.getFila(), self.getColumna())
                
                contador+=1 # para ir paralelamente en los parametros


            resultado = funcion.interpretar(tree,nuevaTabla) # para ejecutar lo que tenga dentro de la funcion

            if isinstance(resultado,Excepcion): return resultado
            
            self.tipo= funcion.getTipo() # es el tipo de la funcion
            #para saber si lo que devuelve es algun primitivo
            
            return resultado
            
        else :

            return Excepcion("Semantico", "Cantidad de parametros para la funcion \""+self.getIdentificador() + "\" NO VALIDO ", self.getFila(), self.getColumna())


    def getIdentificador(self):
        return self.identificador

    def setIdentificador(self, identificador):
        self.identificador=identificador

    def getTipo(self):
        return self.tipo

    def setTipo(self, tipo):
        self.tipo=tipo

    def getParametros(self):
        return self.parametros

    def setParametros(self, parametros):
        self.parametros=parametros

        
    def getFila(self):
        return self.fila

    def setFila(self, fila):
        self.fila= fila 

    def getColumna(self):
        return self.columna

    def setColumna(self, columna):
        self.columna= columna
