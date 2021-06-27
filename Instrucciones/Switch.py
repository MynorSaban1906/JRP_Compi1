from TablaArbol.Excepcion import Excepcion
from TablaArbol.Tipo import OperadorAritmetico,TIPO
from abc import ABC, abstractmethod
from TablaArbol.Simbolo import Simbolo
from TablaArbol.ts import TablaSimbolos
from Instrucciones.Instruccion import Instruccion
from Instrucciones.Break import Break
from Instrucciones.Return import Return
class Switch(Instruccion):
    def __init__(self, expresion,listaInstrucciones,default, fila, columna):
        self.expresion = expresion # valor que se encuentra dentro del switch
        self.listaInstrucciones=listaInstrucciones
        self.default=default
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        nuevaTabla = TablaSimbolos(table)       #NUEVO ENTORNO
        expresion = self.expresion.interpretar(tree, nuevaTabla)
        if isinstance(expresion, Excepcion): return expresion # retorna error si no es correcta
        bandera= None
        while True:
            if self.listaInstrucciones!=None:
                for instruccion in self.listaInstrucciones:
                    #obtiene la expresion que tiene el case<EXPRESION>
                    expresioncase = instruccion.interpretar(tree, nuevaTabla) 

                    # compara la expresion switch con la del case, si son iguales entra
                    if str(expresioncase)==str(expresion): 
                        tablaCase = TablaSimbolos(table)       #NUEVO ENTORNO
                        for instcase in instruccion.getInstrucciones():
                            #obtiene las instrucciones dentro del case y las ejecuta
                            InstruccionesCase = instcase.interpretar(tree, tablaCase ) 
                            if isinstance(InstruccionesCase, Excepcion) :
                                tree.getExcepciones().append(InstruccionesCase)
                                tree.updateConsola(InstruccionesCase.toString())
                            if isinstance(InstruccionesCase, Return): return InstruccionesCase
                            if isinstance(InstruccionesCase, Break): 
                                bandera=True 
                                return None
                            bandera=False # SI EL CASE NO TIENE BREAK SIGUE EVALUANDO LOS DEMAS CASOS
                    elif bandera==False and (self.default==None or str(expresioncase)==str(expresion)):
                        tablaCase1 = TablaSimbolos(table)
                        for instcase in instruccion.getInstrucciones():
                            #obtiene las instrucciones dentro del case y las ejecuta
                            InstruccionesCase = instcase.interpretar(tree, tablaCase1) 
                            if isinstance(InstruccionesCase, Excepcion) :
                                tree.getExcepciones().append(InstruccionesCase)
                                tree.updateConsola(InstruccionesCase.toString())
                            if isinstance(InstruccionesCase, Break): return None
                            if isinstance(InstruccionesCase, Return): return InstruccionesCase

                
                if self.default!=None:
                    tablaCase = TablaSimbolos(table)       #NUEVO ENTORNO
                    for instrucciones in self.default:
                        #obtiene las instrucciones dentro del case y las ejecuta
                        Instrucciones = instrucciones.interpretar(tree, tablaCase ) 
                        if isinstance(Instrucciones, Excepcion) :
                            tree.getExcepciones().append(Instrucciones)
                            tree.updateConsola(Instrucciones.toString())
                        if isinstance(Instrucciones, Break):  return None
                    else:
                        break
                else:
                    break
            elif self.default!=None:

                tablaCase = TablaSimbolos(table)       #NUEVO ENTORNO
                for instrucciones in self.default:
                    #obtiene las instrucciones dentro del case y las ejecuta
                    Instrucciones = instrucciones.interpretar(tree, tablaCase ) 
                    if isinstance(Instrucciones, Excepcion) :
                        tree.getExcepciones().append(Instrucciones)
                        tree.updateConsola(Instrucciones.toString())
                    if isinstance(Instrucciones, Break):  return None
                else:
                    break

    