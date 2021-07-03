#se importan las clases necesarias 
from Instrucciones.ModificaArreglo import ModificaArreglo
from Instrucciones.AccesoArreglo import AcessoArreglo
import os
import sys
from TablaArbol.NodoAST import NodoAST
from Instrucciones.Casteos import Casteos
from Nativas.Round import Round
from Nativas.Typeof import Typeof
from Expresiones.Read import Read
from Nativas.Truncate import Truncate
from Instrucciones.Continue import Continue
from Nativas.ToLower import ToLower
import re
from Instrucciones.DeclaraArreglo import DeclaraArreglo

from Instrucciones.Asignacion import Asignacion
from Instrucciones.Break import Break
from Instrucciones.Declaracion import Declaracion
from Instrucciones.Definicion import Definicion
from Instrucciones.For import For
from Instrucciones.If import If
from Instrucciones.Imprimir import Imprimir
from Instrucciones.Inc_Dec import Inc_Dec
from Instrucciones.Main import Main
from Instrucciones.Switch import Switch
from Instrucciones.While import While
from Instrucciones.Case import Case
from Instrucciones.Funcion import Funcion
from Instrucciones.InvocaFuncion import InvocaFuncion
from Instrucciones.Return import Return

from Expresiones.Aritmetica import Aritmetica
from Expresiones.ExpresionIdentificador import ExpresionIdentificador
from Expresiones.Logica import Logica
from Expresiones.Primitivos import Primitivos
from Expresiones.Relacional import Relacional
from TablaArbol.Tipo import TIPO,OperadorAritmetico,OperadorLogico,OperadorRelacional
from TablaArbol.Excepcion import Excepcion
from TablaArbol.Arbol import Arbol
from TablaArbol.ts import TablaSimbolos
from Nativas.ToUpper import ToUpper
from Nativas.Length import Length


errores = []

reservadas = {

    'print' : 'PRINT',
    'var' : 'VAR',
    'null':'NULO',
    'int'       : 'RINT',
    'double'     : 'RDOUBLE',
    'string'    : 'RSTRING',
    'boolean'   : 'RBOOLEAN',
    'return'    : 'RRETURN',
    
    'if'        : 'RIF',
    'else'      : 'RELSE', 
    'true'      : 'RTRUE',
    'false'     : 'RFALSE',
    'while'     : 'RWHILE',
    'break'     : 'RBREAK',
    'for'       : 'RFOR',
    'switch'    : 'RSWITCH',
    'case'      : 'RCASE',
    'default'   : 'DEFAULT',
    'main'      : 'RMAIN',
    'func'      : 'RFUNC',
    'continue'  : 'RCONTINUE',
    'read'      : 'RREAD',
    'char'      : 'RCHAR',
    'new'       : 'RNEW'

}

tokens  = [
    'PTCOMA',
    'PARIZQ',
    'PARDER',
    "LLAIZQ",
    "LLADER",
    'MAS',
    'IGUAL',
    'MENOS',
    'POR',
    'POW',
    'DIVIDIDO',
    'MENQUE',
    'MAYQUE',
    'MODULO',
    'MENIGUAL',
    'MAYIGUAL',
    'IGUALIGUAL',
    'DIFERENTE',
    'NOT',
    'AND',
    'OR',
    'DECIMAL',
    'ENTERO',
    'CADENA',
    'CHAR',
    'ID',
    'AUMENTO',
    'DECRECI',
    'DPUNTOS',
    'COMA',
    'CORIZQ',
    'CORDER'



] + list(reservadas.values())

# Tokens
t_PTCOMA     = r';'
t_PARIZQ          = r'\('
t_PARDER        = r'\)'
t_LLAIZQ          = r'{'
t_LLADER        = r'}'
t_MAS           = r'\+'
t_MENOS           = r'-'
t_POR       = r'\*'
t_DIVIDIDO  = r'/'
t_IGUAL     = r'='
t_MENQUE   =r'<'
t_MAYQUE   =r'>'
t_IGUALIGUAL =r'=='
t_POW =r'\*\*'
t_MENIGUAL   =r'<='
t_MAYIGUAL  =r'>='
t_MODULO =r'%'
t_DIFERENTE=r'=!'
t_OR=r'\|\|'
t_AND=r'&&'
t_NOT =r'!'
t_AUMENTO= '\+\+'
t_DECRECI='--'
t_DPUNTOS=':'
t_COMA=','
t_CORDER='\]'
t_CORIZQ='\['

 
def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t

def t_CHAR(t):
    r'(\'([a-zA-Z]|\\\'|\\"|\\t|\\n|\\\\|.)\')'
    t.value = t.value[1:-1] # remuevo las comillas
    return t

def t_ENTERO(t): 
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t
def t_CADENA(t):
    r'\"(\\"|.)*?\"'
    t.value = t.value[1:-1] # remuevo las comillas
    return t

# Comentario de multiples lineas #* hola comentario multilinea.. *#
def t_COMENTARIO_MULTILINEA(t):
    r'\#\*(.|\n)*?\*\#'
    t.lexer.lineno += t.value.count('\n')


# Comentario simple // ...
def t_COMENTARIO_SIMPLE(t):
    r'\#.*\n'
    t.lexer.lineno += 1


# Caracteres ignorados
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
def t_error(t):
    errores.append(Excepcion("Lexico","El caracter \"" + t.value[0]+"\" no pertenece al lenguaje" , t.lexer.lineno, find_column(input, t)))
    t.lexer.skip(1)

def t_ID(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value.lower(),'ID')    # Check for reserved words
     return t


# Compute column.
#     input is the input text string
#     token is a token instance
def find_column(inp, token):
    line_start = inp.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

# Construyendo el analizador léxico
import ply.lex as lex
lexer = lex.lex()

#Precedencia   solo estan las basicas
precedence = (

    ('left','OR'),
    ('left','AND'),
    ('right','UNOT'),
    ('left', 'MENQUE', 'MAYQUE','IGUALIGUAL','MENIGUAL', 'MAYIGUAL'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIVIDIDO','MODULO'),
    ('left','POW'),
    ('right','UMENOS'),
    ('left','AUMENTO','DECRECI'),
    

)
#Abstract


def p_init(t) :
    'init            : instrucciones'
    t[0] = t[1]

def p_instrucciones_instrucciones_instruccion(t) :
    'instrucciones    : instrucciones instruccion'
    if t[2] != "":
        t[1].append(t[2])
    t[0] = t[1]
    
#///////////////////////////////////////INSTRUCCIONES//////////////////////////////////////////////////

def p_instrucciones_instruccion(t) :
    'instrucciones    : instruccion'
    if t[1] == "":
        t[0] = []
    else:    
        t[0] = [t[1]]

#///////////////////////////////////////INSTRUCCION//////////////////////////////////////////////////

def p_instruccion(t) :
    '''instruccion      :   imprimir_instr final   
                        |   definicion_instr final
                        |   asignacion_instr final
                        |   if_instr
                        |   break_instr final
                        |   while_instr
                        |   inc_dec final
                        |   for_instr
                        |   switch_instr
                        |   main_instr
                        |   funcion_instr 
                        |   llamadaFuncion final
                        |   return_instr final
                        |   continue_instr final
                        |   definicionArreglo_instr final
                        |   modificacionArreglo_instr final
    '''
    t[0] = t[1]


def p_finins(t) :
    '''final      : PTCOMA
                    | '''
    t[0] = None



def p_instruccion_error(t):
    '''instruccion      : error final'''
    errores.append(Excepcion("Sintactico","Error Sintactico con " + str(t[1].value) , t.lineno(1), find_column(input, t.slice[1])))
    t[0] = ""
#///////////////////////////////////////IMPRIMIR//////////////////////////////////////////////////

def p_imprimir(t) :
    '''imprimir_instr   : PRINT PARIZQ expresion PARDER '''
    t[0] = Imprimir(t[3], t.lineno(1), find_column(input, t.slice[1]))



#/////////////////////////////////////// incremento y decrecimiento +++ --  //////////////////////////////////////////////////

def p_incremento_expresion(t):
    '''expresion : expresion AUMENTO 
                | expresion DECRECI'''
    if t[2]=='++': t[0] = Aritmetica(OperadorAritmetico.AUMENTO, t[1],None, t.lineno(2), find_column(input, t.slice[2]))
    elif t[2]=='--':t[0] = Aritmetica(OperadorAritmetico.DECREMENTO, t[1],None, t.lineno(2), find_column(input, t.slice[2]))



#///////////////////////////////////////EXPRESION//////////////////////////////////////////////////


def p_expresion_binaria(t):
    '''
    expresion : expresion MAS expresion
            | expresion MENOS expresion
            | expresion POR expresion
            | expresion DIVIDIDO expresion
            | expresion MENQUE expresion
            | expresion MAYQUE expresion
            | expresion IGUALIGUAL expresion
            | expresion POW expresion
            | expresion MENIGUAL expresion
            | expresion MAYIGUAL expresion
            | expresion MODULO expresion
            | expresion DIFERENTE expresion
            | expresion AND expresion
            | expresion OR expresion
    '''
    if t[2] == '+':   t[0] = Aritmetica(OperadorAritmetico.MAS, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '-': t[0] = Aritmetica(OperadorAritmetico.MENOS, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '*':   t[0] = Aritmetica(OperadorAritmetico.POR, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '/':   t[0] = Aritmetica(OperadorAritmetico.DIV, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '<': t[0] = Relacional(OperadorRelacional.MENORQUE, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '>': t[0] = Relacional(OperadorRelacional.MAYORQUE, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '==':   t[0] = Relacional(OperadorRelacional.IGUALIGUAL, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '**':   t[0] = Aritmetica(OperadorAritmetico.POT, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '<=': t[0] = Relacional(OperadorRelacional.MENORIGUAL, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '>=': t[0] = Relacional(OperadorRelacional.MAYORIGUAL, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '%': t[0] = Aritmetica(OperadorAritmetico.MOD, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '=!': t[0] = Relacional(OperadorRelacional.DIFERENTE, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '&&': t[0] = Logica(OperadorLogico.AND, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '||': t[0] = Logica(OperadorLogico.OR, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))



def p_expresion_unaria(t):
    '''
    expresion : MENOS expresion %prec UMENOS 
            | NOT expresion %prec UNOT 
    '''
    if t[1] == '-':
        t[0] = Aritmetica(OperadorAritmetico.UMENOS, t[2],None, t.lineno(1), find_column(input, t.slice[1]))
    elif t[1] == '!':
        t[0] = Logica(OperadorLogico.NOT, t[2],None, t.lineno(1), find_column(input, t.slice[1]))


def p_expresion_agrupacion(t):
    'expresion : PARIZQ expresion PARDER'
    t[0]=t[2]
         

def p_expresion_entero(t):
    'expresion : ENTERO'
    t[0] = Primitivos(TIPO.ENTERO,t[1], t.lineno(1), find_column(input, t.slice[1]))


def p_expresion_read(t):
    'expresion : RREAD PARIZQ PARDER'
    t[0] = Read(t.lineno(1), find_column(input, t.slice[1]))



def p_primitivo_decimal(t):
    'expresion : DECIMAL'
    t[0] = Primitivos(TIPO.DECIMAL, t[1], t.lineno(1), find_column(input, t.slice[1]))

def p_primitivo_cadena(t):
    'expresion : CADENA'
    t[1]=str(t[1]).replace('\\t','\t')
    t[1]=str(t[1]).replace('\\n','\n')
    t[1]=str(t[1]).replace('\\\\','\\')
    t[1]=str(t[1]).replace("\\'","\'")
    t[1]=str(t[1]).replace('\\"','"')
    t[0] = Primitivos(TIPO.CADENA,str(t[1]), t.lineno(1), find_column(input, t.slice[1]))

def p_primitivo_char(t):
    'expresion : CHAR'
    t[1]=str(t[1]).replace('\\t','\t')
    t[1]=str(t[1]).replace('\\n','\n')
    t[1]=str(t[1]).replace('\\\\','\\')
    t[1]=str(t[1]).replace("\\'","\'")
    t[1]=str(t[1]).replace('\\"','"')
    t[0] = Primitivos(TIPO.CHARACTER,str(t[1]).replace('\\n', '\n'), t.lineno(1), find_column(input, t.slice[1]))

def p_primitivo_nulo(t):
    'expresion : NULO'
    t[0] = Primitivos(TIPO.NULO,None, t.lineno(1), find_column(input, t.slice[1]))
def p_primitivo_true(t):
    '''expresion : RTRUE'''
    t[0] = Primitivos(TIPO.BOOLEANO, True, t.lineno(1), find_column(input, t.slice[1]))

def p_primitivo_false(t):
    '''expresion : RFALSE'''
    t[0] = Primitivos(TIPO.BOOLEANO, False, t.lineno(1), find_column(input, t.slice[1]))

def p_casteos(t):
    '''expresion : PARIZQ tipo PARDER expresion'''
    t[0] = Casteos(t[2],t[4], t.lineno(1), find_column(input, t.slice[1]))



def p_expresion_id(t):
    'expresion : ID'
    t[0] = ExpresionIdentificador(t[1], t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_llamada(t):
    'expresion : llamadaFuncion '
    t[0] = t[1]

#////////////////////////////////DEFINIR VARIABLE ////////////////////////

def p_instrucion_definicion(t):
    '''definicion_instr     : definicion_instr1
                            | definicion_instr2'''
    t[0]=t[1]

def p_instruccion_definicion1(t):
    'definicion_instr1       : VAR ID IGUAL expresion'
    t[0]=   Declaracion(t[1], str(t[2]).lower(), t.lineno(2), find_column(input, t.slice[2]), t[4])

def p_instruccion_definicion(t) :
    '''definicion_instr2     : VAR ID
        '''
    t[0] =Definicion(str(t[2]).lower(), t.lineno(1), find_column(input, t.slice[1]))

 
#////////////////////////////////ASIGNAR VARIABLE ////////////////////////

def p_asignacion_instr(t) :
    '''asignacion_instr   : ID IGUAL expresion '''
    t[0] =Asignacion(t[1], t[3], t.lineno(1), find_column(input, t.slice[1]))

# /////////////////////////////// IF //////////////////////////

def p_if1(t) :
    'if_instr     : RIF PARIZQ expresion PARDER LLAIZQ instrucciones LLADER'
    t[0] = If(t[3], t[6], None, None, t.lineno(1), find_column(input, t.slice[1]))

def p_if2(t) :
    'if_instr     : RIF PARIZQ expresion PARDER LLAIZQ instrucciones LLADER RELSE LLAIZQ instrucciones LLADER'
    t[0] = If(t[3], t[6], t[10], None, t.lineno(1), find_column(input, t.slice[1]))

def p_if3(t) :
    'if_instr     : RIF PARIZQ expresion PARDER LLAIZQ instrucciones LLADER RELSE if_instr'
    t[0] = If(t[3], t[6], None, t[9], t.lineno(1), find_column(input, t.slice[1]))

#///////////////////////////////////////BREAK//////////////////////////////////////////////////

def p_break(t) :
    'break_instr     : RBREAK'
    t[0] = Break(t.lineno(1), find_column(input, t.slice[1]))


def p_continue(t) :
    'continue_instr     : RCONTINUE'
    t[0] = Continue(t.lineno(1), find_column(input, t.slice[1]))


#///////////////////////////////////////WHILE//////////////////////////////////////////////////

def p_while(t) :
    'while_instr     : RWHILE PARIZQ expresion PARDER LLAIZQ instrucciones LLADER'
    t[0] = While(t[3], t[6], t.lineno(1), find_column(input, t.slice[1]))

def p_inicio_for(t):
    '''inicial_for  :   definicion_instr1
                    |   asignacion_instr
    '''
    t[0]=t[1]


def p_cicloFor(t) :
    'for_instr     : RFOR PARIZQ inicial_for PTCOMA expresion PTCOMA inc_dec_for PARDER LLAIZQ  instrucciones LLADER'
    t[0] = For(t[3], t[5],t[7],t[10], t.lineno(1), find_column(input, t.slice[1]))

def p_forpaso(t) :
    '''inc_dec_for     : inc_dec
                       | asignacion_instr'''
    t[0] = t[1]



def p_incremento_instruccion(t):
    '''inc_dec : ID AUMENTO  
                | ID DECRECI '''
    if t[2]=='++': t[0] = Inc_Dec(ExpresionIdentificador(t[1], t.lineno(1), find_column(input, t.slice[2])),t[1],OperadorAritmetico.AUMENTO, t.lineno(1), find_column(input, t.slice[2]))
    elif t[2]=='--': t[0] = Inc_Dec(ExpresionIdentificador(t[1], t.lineno(1), find_column(input, t.slice[2])),t[1],OperadorAritmetico.DECREMENTO, t.lineno(1), find_column(input, t.slice[2]))


def p_switch(t) :
    'switch_instr     : RSWITCH PARIZQ expresion PARDER LLAIZQ cases_lista LLADER'
    t[0] = Switch(t[3], t[6],None, t.lineno(1), find_column(input, t.slice[1]))

def p_switch1(t) :
    'switch_instr     : RSWITCH PARIZQ expresion PARDER LLAIZQ cases_lista  defecto LLADER'
    t[0] = Switch(t[3], t[6],t[7], t.lineno(1), find_column(input, t.slice[1]))

def p_switch2(t) :
    'switch_instr     : RSWITCH PARIZQ expresion PARDER LLAIZQ defecto LLADER'
    t[0] = Switch(t[3], None,t[6], t.lineno(1), find_column(input, t.slice[1]))

def p_lista_casos(t) :
    'cases_lista    : cases_lista case'
    if t[2] != "":
        t[1].append(t[2])
    t[0] = t[1]

    
def p_lista_casos_caso(t) :
    'cases_lista    : case'
    if t[1] == "":
        t[0] = []
    else:    
        t[0] = [t[1]]

def p_case_instruccion(t) :
    '''case     :   RCASE expresion DPUNTOS instrucciones
    '''
    t[0] = Case(t[2],t[4], t.lineno(1), find_column(input, t.slice[1]))

def p_default(t):
    '''defecto      : DEFAULT DPUNTOS instrucciones'''
    t[0]=t[3]




#///////////////////////////////////////MAIN//////////////////////////////////////////////////

def p_main(t) :
    'main_instr     : RMAIN PARIZQ PARDER LLAIZQ instrucciones LLADER'
    t[0] = Main(t[5], t.lineno(1), find_column(input, t.slice[1]))


#/////////////////////////////////////// Funciones sin parametros //////////////////////////////////////////////////

def p_FuncionParametros(t):
    'funcion_instr  : RFUNC ID PARIZQ parametros PARDER LLAIZQ instrucciones LLADER'
    t[0] = Funcion(t[2],t[4],t[7], t.lineno(1), find_column(input, t.slice[1]))

def p_FuncionSinParametros(t):
    'funcion_instr  : RFUNC ID PARIZQ  PARDER LLAIZQ instrucciones LLADER'
    t[0] = Funcion(t[2],[],t[6], t.lineno(1), find_column(input, t.slice[1]))

#///////////////////////////////////////PARAMETROS//////////////////////////////////////////////////

def p_parametros_1(t) :
    'parametros     : parametros COMA parametro'
    t[1].append(t[3])
    t[0] = t[1]
    
def p_parametros_2(t) :
    'parametros    : parametro'
    t[0] = [t[1]]

#///////////////////////////////////////PARAMETRO//////////////////////////////////////////////////

def p_parametro(t) :
    'parametro     : tipo ID'
    t[0] = {'tipo':t[1],'identificador':t[2]}



#///////////////////////////////////////TIPO//////////////////////////////////////////////////

def p_tipo(t) :
    '''tipo     : RINT
                | RDOUBLE
                | RSTRING
                | RBOOLEAN 
                | RCHAR'''
    if t[1].lower() == 'int':
        t[0] = TIPO.ENTERO
    elif t[1].lower() == 'double':
        t[0] = TIPO.DECIMAL
    elif t[1].lower() == 'string':
        t[0] = TIPO.CADENA
    elif t[1].lower() == 'boolean':
        t[0] = TIPO.BOOLEANO
    elif t[1].lower() == 'char':
        t[0] = TIPO.CHARACTER


    

#///////////////////////////////////////llamada de  Funciones sin parametros //////////////////////////////////////////////////

def p_llamadaFuncion(t):
    'llamadaFuncion  : ID PARIZQ PARDER '
    t[0] = InvocaFuncion(t[1], [],t.lineno(2), find_column(input, t.slice[2]))


def p_llamadaFuncionParametro (t):
    'llamadaFuncion  : ID PARIZQ parametros_llamada PARDER '
    t[0] = InvocaFuncion(t[1], t[3],t.lineno(2), find_column(input, t.slice[2]))

#///////////////////////////////////////PARAMETROS LLAMADA A FUNCION//////////////////////////////////////////////////

def p_parametrosLL_1(t) :
    'parametros_llamada     : parametros_llamada COMA parametro_llamada'
    t[1].append(t[3])
    t[0] = t[1]
    
def p_parametrosLL_2(t) :
    'parametros_llamada    : parametro_llamada'
    t[0] = [t[1]]

#///////////////////////////////////////PARAMETRO LLAMADA A FUNCION//////////////////////////////////////////////////

def p_parametroLL(t) :
    'parametro_llamada     : expresion'
    t[0] = t[1]

def p_retorno(t) :
    'return_instr     : RRETURN expresion'
    t[0] = Return(t[2],t.lineno(1), find_column(input, t.slice[1]))



# ...................   DECLARACION DE ARREGLOS ...............
'''
def p_declaraArreglo(t) :
    definicionArreglo_instr     : tipo1
    t[0] = t[1]

'''


def p_tipo1(t):
    '''definicionArreglo_instr     : tipo lista_Dimension ID IGUAL RNEW tipo lista_expresiones'''
    t[0] = DeclaraArreglo(t[1], t[2], t[3], t[6], t[7], t.lineno(3), find_column(input, t.slice[3]))

def p_lista_Dim1(t) :
    'lista_Dimension     : lista_Dimension CORIZQ  CORDER'
    t[0] = t[1] + 1
    
def p_lista_Dim2(t) :
    'lista_Dimension    : CORIZQ  CORDER'
    t[0] = 1

def p_lista_expresiones_1(t) :
    'lista_expresiones     : lista_expresiones CORIZQ expresion CORDER'
    t[1].append(t[3])
    t[0] = t[1]
    
def p_lista_expresiones_2(t) :
    'lista_expresiones    : CORIZQ expresion CORDER'
    t[0] = [t[2]]



# .............. ACCESO A ARREGLOS ..................

def p_Acceso_Arreglo(t) :
    'expresion    : ID lista_expresiones'
    t[0] = AcessoArreglo(t[1], t[2] ,t.lineno(1), find_column(input, t.slice[1]))

# .............. MODIFICACION DE ARREGLOS ..................

def p_Modificacion_Arreglos(t) :
    'modificacionArreglo_instr   : ID lista_expresiones IGUAL expresion'
    t[0] = ModificaArreglo(t[1], t[2],t[4] ,t.lineno(3), find_column(input, t.slice[3]))




import ply.yacc as yacc

sys.setrecursionlimit(3000)

parser = yacc.yacc()
input = ''

def crearNativas(ast):
    nombre = "toUpper"
    parametros = [{'tipo':TIPO.CADENA,'identificador':'toUpper##Param1'}]
    instrucciones = []
    toUpper = ToUpper(nombre.lower(), parametros, instrucciones, -1, -1)
    ast.addFuncion(toUpper)     # GUARDAR LA FUNCION EN "MEMORIA" (EN EL ARBOL)

    nombre = "toLower"
    parametros = [{'tipo':TIPO.CADENA,'identificador':'toLower##Param1'}]
    toLower = ToLower(nombre.lower(), parametros, instrucciones, -1, -1)
    ast.addFuncion(toLower)     # GUARDAR LA FUNCION EN "MEMORIA" (EN EL ARBOL)

    nombre = "Truncate"
    parametros = [{'tipo':TIPO.NULO,'identificador':'truncate##param1'}]
    truncado = Truncate(nombre.lower(), parametros, instrucciones, -1, -1)
    ast.addFuncion(truncado)     # GUARDAR LA FUNCION EN "MEMORIA" (EN EL ARBOL)

    nombre = "Typeof"
    parametros = [{'tipo':TIPO.NULO,'identificador':'typeof##param1'}]
    typeof = Typeof(nombre.lower(), parametros, instrucciones, -1, -1)
    ast.addFuncion(typeof)     # GUARDAR LA FUNCION EN "MEMORIA" (EN EL ARBOL)

    nombre = "round"
    parametros = [{'tipo':TIPO.ENTERO,'identificador':'round##param1'}]
    round = Round(nombre.lower(), parametros, instrucciones, -1, -1)
    ast.addFuncion(round)     # GUARDAR LA FUNCION EN "MEMORIA" (EN EL ARBOL)

    nombre = "length"
    parametros = [{'tipo':TIPO.NULO,'identificador':'length##param1'}]
    length = Length(nombre.lower(), parametros, instrucciones, -1, -1)
    ast.addFuncion(length)     # GUARDAR LA FUNCION EN "MEMORIA" (EN EL ARBOL)


def getErrores():
    return errores 

def parse(inp) :
    global errores
    global lexer
    global parser
    errores = []
    parser = yacc.yacc()
    global input
    input = inp
    return parser.parse(inp)

#INTERFAZ
'''
archivo=open("entrada.jpr","r")
entrada=archivo.read()

instrucciones = parse(entrada) #ARBOL AST
Arbol_ast = Arbol(instrucciones)
TablaSimboloGlobal = TablaSimbolos()
Arbol_ast.setTablaSimboloGlobal(TablaSimboloGlobal)
crearNativas(Arbol_ast)
for error in errores:                   #CAPTURA DE ERRORES LEXICOS Y SINTACTICOS
    Arbol_ast.getExcepciones().append(error)
    Arbol_ast.updateConsola(error.toString())


for instruccion in Arbol_ast.getInstrucciones():      # 1ERA PASADA (DECLARACIONES Y ASIGNACIONES)
    if isinstance(instruccion, Declaracion) or isinstance(instruccion, Asignacion) or isinstance(instruccion, Definicion)or isinstance(instruccion, DeclaraArreglo):
        value = instruccion.interpretar(Arbol_ast,TablaSimboloGlobal)
        if isinstance(value, Excepcion) :
            Arbol_ast.getExcepciones().append(value)
            Arbol_ast.updateConsola(value.toString())
        if isinstance(value, Break): 
            err = Excepcion("Semantico", "Sentencia BREAK fuera de ciclo 1", instruccion.fila, instruccion.columna)
            Arbol_ast.getExcepciones().append(err)
            Arbol_ast.updateConsola(err.toString())
    if isinstance(instruccion,Funcion):
        Arbol_ast.addFuncion(instruccion)
        
for instruccion in Arbol_ast.getInstrucciones():      # 2DA PASADA (MAIN)
    contador = 0

    if isinstance(instruccion, Main):
        contador += 1
        if contador == 2: # VERIFICAR LA DUPLICIDAD
            err = Excepcion("Semantico", "Existen 2 funciones Main", instruccion.fila, instruccion.columna)
            Arbol_ast.getExcepciones().append(err)
            Arbol_ast.updateConsola(err.toString())
            break
        value = instruccion.interpretar(Arbol_ast,TablaSimboloGlobal)
        if isinstance(value, Excepcion) :
            Arbol_ast.getExcepciones().append(value)
            Arbol_ast.updateConsola(value.toString())
        if isinstance(value, Break): 
            err = Excepcion("Semantico", "Sentencia BREAK fuera de un ciclo 2", instruccion.fila, instruccion.columna)
            Arbol_ast.getExcepciones().append(err)
            Arbol_ast.updateConsola(err.toString())
        if isinstance(value, Return): 
            err = Excepcion("Semantico", "Sentencia RETURN fuera de un ciclo", instruccion.fila, instruccion.columna)
            Arbol_ast.getExcepciones().append(err)
            Arbol_ast.updateConsola(err.toString())
        if isinstance(value, Continue): 
            err = Excepcion("Semantico", "Sentencia Continue fuera de un ciclo", instruccion.fila, instruccion.columna)
            Arbol_ast.getExcepciones().append(err)
            Arbol_ast.updateConsola(err.toString())



for instruccion in Arbol_ast.getInstrucciones():    # 3ERA PASADA (SENTENCIAS FUERA DE MAIN)
    if not (isinstance(instruccion, Main) or isinstance(instruccion, Declaracion) or isinstance(instruccion, Asignacion) or isinstance(instruccion, Definicion)
            or isinstance(instruccion, Funcion) or isinstance(instruccion,DeclaraArreglo)):
        err = Excepcion("Semantico", "Sentencias fuera de Main", instruccion.fila, instruccion.columna)
        Arbol_ast.getExcepciones().append(err)
        Arbol_ast.updateConsola(err.toString())



print(Arbol_ast.getConsola())



'''

def analizador(entrada,consola):
    instrucciones = parse(entrada) #ARBOL AST
    Arbol_ast = Arbol(instrucciones)
    TablaSimboloGlobal = TablaSimbolos()
    Arbol_ast.setTablaSimboloGlobal(TablaSimboloGlobal)
    crearNativas(Arbol_ast)
    for error in errores:                   #CAPTURA DE ERRORES LEXICOS Y SINTACTICOS
        Arbol_ast.getExcepciones().append(error)
        Arbol_ast.updateConsola(error.toString())


    for instruccion in Arbol_ast.getInstrucciones():      # 1ERA PASADA (DECLARACIONES Y ASIGNACIONES)
        if isinstance(instruccion, Declaracion) or isinstance(instruccion, Asignacion) or isinstance(instruccion, Definicion)or isinstance(instruccion, DeclaraArreglo):
            value = instruccion.interpretar(Arbol_ast,TablaSimboloGlobal)
            if isinstance(value, Excepcion) :
                Arbol_ast.getExcepciones().append(value)
                Arbol_ast.updateConsola(value.toString())
            if isinstance(value, Break): 
                err = Excepcion("Semantico", "Sentencia BREAK fuera de ciclo 1", instruccion.fila, instruccion.columna)
                Arbol_ast.getExcepciones().append(err)
                Arbol_ast.updateConsola(err.toString())
        if isinstance(instruccion,Funcion):
            Arbol_ast.addFuncion(instruccion)
            
    for instruccion in Arbol_ast.getInstrucciones():      # 2DA PASADA (MAIN)
        contador = 0

        if isinstance(instruccion, Main):
            contador += 1
            if contador == 2: # VERIFICAR LA DUPLICIDAD
                err = Excepcion("Semantico", "Existen 2 funciones Main", instruccion.fila, instruccion.columna)
                Arbol_ast.getExcepciones().append(err)
                Arbol_ast.updateConsola(err.toString())
                break
            value = instruccion.interpretar(Arbol_ast,TablaSimboloGlobal)
            if isinstance(value, Excepcion) :
                Arbol_ast.getExcepciones().append(value)
                Arbol_ast.updateConsola(value.toString())
            if isinstance(value, Break): 
                err = Excepcion("Semantico", "Sentencia BREAK fuera de un ciclo 2", instruccion.fila, instruccion.columna)
                Arbol_ast.getExcepciones().append(err)
                Arbol_ast.updateConsola(err.toString())
            if isinstance(value, Return): 
                err = Excepcion("Semantico", "Sentencia RETURN fuera de un ciclo", instruccion.fila, instruccion.columna)
                Arbol_ast.getExcepciones().append(err)
                Arbol_ast.updateConsola(err.toString())
            if isinstance(value, Continue): 
                err = Excepcion("Semantico", "Sentencia Continue fuera de un ciclo", instruccion.fila, instruccion.columna)
                Arbol_ast.getExcepciones().append(err)
                Arbol_ast.updateConsola(err.toString())



    for instruccion in Arbol_ast.getInstrucciones():    # 3ERA PASADA (SENTENCIAS FUERA DE MAIN)
        if not (isinstance(instruccion, Main) or isinstance(instruccion, Declaracion) or isinstance(instruccion, Asignacion) or isinstance(instruccion, Definicion)
                or isinstance(instruccion, Funcion) or isinstance(instruccion,DeclaraArreglo)):
            err = Excepcion("Semantico", "Sentencias fuera de Main", instruccion.fila, instruccion.columna)
            Arbol_ast.getExcepciones().append(err)
            Arbol_ast.updateConsola(err.toString())

            

    init = NodoAST("RAIZ")
    instr = NodoAST("INSTRUCCIONES")

    for instruccion in Arbol_ast.getInstrucciones():
        instr.Agregar_Hijo_Nodo(instruccion.getNodo())

    init.Agregar_Hijo_Nodo(instr)
    grafo = Arbol_ast.getDot(init) #DEVUELVE EL CODIGO GRAPHVIZ DEL AST

    dirname = os.path.dirname(__file__)
    direcc = os.path.join(dirname, 'ast.dot')
    arch = open(direcc, "w+")
    arch.write(grafo)
    arch.close()
    os.system('dot -T svg -o ast.svg ast.dot')


    return Arbol_ast.getConsola()
    
def listaErrores():
    return errores
