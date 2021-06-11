from Excepcion import Excepcion

errores = []
reservadas = {

    'print' : 'PRINT',
    'var' : 'VAR',
    'null':'NULO',
    

    'if'        : 'RIF',
    'else'      : 'RELSE',
    'else if'   : 'RELSEIF',
    'while'     : 'RWHILE',
    'true'      : 'RTRUE',
    'false'     : 'RFALSE',
    'break'     : 'RBREAK',
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
    'SNOT',
    'SAND',
    'SOR',
    'DECIMAL',
    'ENTERO',
    'CADENA',
    'CHAR',
    'ID'
] + list(reservadas.values())

# Tokens
t_PTCOMA     = r';'
t_PARIZQ          = r'\('
t_PARDER        = r'\)'
t_LLAIZQ          = r'['
t_LAADER        = r']'
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
t_DIFERENTE=r'!='
t_SOR=r'\|\|'
t_SAND=r'&&'
t_SNOT =r'!'


def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t

def t_CHAR(t):
    r'(\'[a-zA-Z]+\')'
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

def t_ID(t):
     r'[a-zA-Z][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value.lower(),'ID')
     return t

def t_CADENA(t):
    r'(\".*?\")'
    t.value = t.value[1:-1] # remuevo las comillas
    return t

# Comentario simple // ...
def t_COMENTARIO_SIMPLE(t):
    r'\#.*\n'
    t.lexer.lineno += 1

# Comentario de multiples lineas #* hola comentario multilinea.. *#
def t_COMENTARIO_MULTILINEA(t):
    r'\#\*(.|\n)*?\*\#'
    t.lexer.lineno += t.value.count('\n')
# Caracteres ignorados
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    errores.append(Excepcion("Lexico","Error léxico." + t.value[0] , t.lexer.lineno, find_column(input, t)))
    t.lexer.skip(1)

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
    ('left', 'MENQUE', 'MAYQUE','IGUALIGUAL'),
    ('left', 'MAS', 'MENOS','POW'),
    ('left', 'POR', 'DIVIDIDO'),
    ('right','UMENOS'),
    

)
#Abstract
from Instruccion import Instruccion,Imprimir,Definicion,Asignacion
from expresiones import *
from Tipo import OperadorLogico,OperadorAritmetico,OperadorRelacional,TIPO

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
                     
    '''
    t[0] = t[1]


def p_finins(t) :
    '''final      : PTCOMA
                    | '''
    t[0] = None



def p_instruccion_error(t):
    '''instruccion      : error final'''
    errores.append(Excepcion("Sintáctico","Error Sintáctico. " + str(t[1].value) , t.lineno(1), find_column(input, t.slice[1])))
    t[0] = ""
#///////////////////////////////////////IMPRIMIR//////////////////////////////////////////////////

def p_imprimir(t) :
    '''imprimir_instr   : PRINT PARIZQ expresion PARDER '''
    t[0] = Imprimir(t[3], t.lineno(1), find_column(input, t.slice[1]))

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
    elif t[2] == '<=': t[0] = Relacional(OperadorRelacional.MENORQUE, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '>=': t[0] = Relacional(OperadorRelacional.MAYORQUE, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '%': t[0] = Aritmetica(OperadorAritmetico.MOD, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '!=': t[0] = Relacional(OperadorRelacional.DIFERENTE, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
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

def p_primitivo_decimal(t):
    'expresion : DECIMAL'
    t[0] = Primitivos(TIPO.DECIMAL, t[1], t.lineno(1), find_column(input, t.slice[1]))

def p_primitivo_cadena(t):
    'expresion : CADENA'
    t[0] = Primitivos(TIPO.CADENA,str(t[1]).replace('\\n', '\n'), t.lineno(1), find_column(input, t.slice[1]))

def p_primitivo_char(t):
    'expresion : CHAR'
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

def p_expresion_id(t):
    'expresion : ID'
    t[0] = ExpresionIdentificador(t[1], t.lineno(1), find_column(input, t.slice[1]))
#////////////////////////////////DEFINIR VARIABLE ////////////////////////

def p_instruccion_definicion(t) :
    '''definicion_instr   : VAR ID '''
    t[0] =Definicion(str(t[2]), t.lineno(1), find_column(input, t.slice[1]))

#////////////////////////////////ASIGNAR VARIABLE ////////////////////////

def p_asignacion_instr(t) :
    '''asignacion_instr   : ID IGUAL expresion '''
    t[0] =Asignacion(t[1], t[3], t.lineno(1), find_column(input, t.slice[1]))

# /////////////////////////////// IF //////////////////////////

def p_if1(t) :
    'if_instr     : RIF PARIZQ expresion PARDER LLAIZQ instrucciones LLADER'
    t[0] = If(t[3], t[6], None, None, t.lineno(1), find_column(input, t.slice[1]))

def p_if2(t) :
    'if_instr     : RIF PARIZQ expresion PARDER LLAIQZ instrucciones LLADER RELSE LLAIZQ instrucciones LLADER'
    t[0] = If(t[3], t[6], t[10], None, t.lineno(1), find_column(input, t.slice[1]))

def p_if3(t) :
    'if_instr     : RIF PARIZQ expresion PARDER LLAIZQ instrucciones LLADER RELSE if_instr'
    t[0] = If(t[3], t[6], None, t[9], t.lineno(1), find_column(input, t.slice[1]))


import ply.yacc as yacc
parser = yacc.yacc()
input = ''

def getErrores():
    return errores

def parse(inp) :
    global errores
    global lexer
    global parser
    errores = []
    lexer = lex.lex()
    parser = yacc.yacc()
    global input
    input = inp
    return parser.parse(inp)

#INTERFAZ

from Arbol import Arbol
from ts import TablaSimbolos
from Instruccion import NameVariable as variablesG
f = open("./entrada.txt", "r")
entrada = f.read()


instrucciones = parse(entrada) #ARBOL AST
ast = Arbol(instrucciones)
TSGlobal = TablaSimbolos()
ast.setTSglobal(TSGlobal)
for error in errores:                   #CAPTURA DE ERRORES LEXICOS Y SINTACTICOS
    ast.getExcepciones().append(error)
    ast.updateConsola(error.toString())

for instruccion in ast.getInstrucciones():      # REALIZAR LAS ACCIONES
    value = instruccion.interpretar(ast,TSGlobal)
    if isinstance(value, Excepcion) :
        ast.getExcepciones().append(value)
        ast.updateConsola(value.toString())

print(ast.getConsola())







'''
def analizador(entrada):
    variablesG.clear()
    instrucciones = parse(entrada) #ARBOL AST
    ast = Arbol(instrucciones)
    TSGlobal = TablaSimbolos()
    ast.setTSglobal(TSGlobal)
    for error in errores:                   #CAPTURA DE ERRORES LEXICOS Y SINTACTICOS
        ast.getExcepciones().append(error)
        ast.updateConsola(error.toString())
    for instruccion in ast.getInstrucciones():      # REALIZAR LAS ACCIONES
        value = instruccion.interpretar(ast,TSGlobal)
        if isinstance(value, Excepcion) :
            ast.getExcepciones().append(value)
            ast.updateConsola(value.toString())
    return ast.getConsola()
    



    
    
    
    
    
    '''

    