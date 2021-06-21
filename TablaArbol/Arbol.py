class Arbol:
    def __init__(self, instrucciones ):
        self.instrucciones = instrucciones # son de tipo instrucciones
        self.excepciones = [] #para las excepciones, estas se guardan en objetos en esta tabla
        self.funciones=[]   # para las funcioes
        self.consola = ""
        self.TablaSimboloGlobal = None # al inicial inicia en NOne

    def getInstrucciones(self):
        return self.instrucciones

    def setInstrucciones(self, instrucciones):
        self.instrucciones = instrucciones

    def getExcepciones(self):
        return self.excepciones

    def setExcepciones(self, excepciones):
        self.excepciones = excepciones

    def getConsola(self):
        return self.consola
    
    def setConsola(self, consola):
        self.consola = consola

    def updateConsola(self,cadena):
        self.consola += str(cadena) + '\n'

    def getTablaSimboloGlobal(self):
        return self.TablaSimboloGlobal
    
    def setTablaSimboloGlobal(self, TablaSimboloGlobal):
        self.TablaSimboloGlobal = TablaSimboloGlobal


    def getFunciones(self):
        return self.funciones

    def getFuncion(self, nombre):
        for funcion in self.funciones:
            if funcion.nombre == nombre:
                return funcion
        return None
    
    def addFuncion(self, funcion):
        self.funciones.append(funcion)