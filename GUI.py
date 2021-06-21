"""
    Universidad de san carlos de Guatemala
    Mynor Alison Isai Saban Che 201800516
    Codigo ayuda  de Jose Puac auxiliar de compiladores 1 vaciones 2021 primer semestre
"""





from tkinter import *            # ventana
from tkinter import Menu            # barra de tareas
from tkinter import scrolledtext    # textarea
from tkinter import messagebox      # message box
from tkinter import filedialog as fd # filechooser
from tkinter import messagebox as mb
from tkinter import Canvas,Frame
import tkinter as tk
import webbrowser
import re
from gramatica import listaErrores,analizador


reservadas = {

    'print',
    'var' ,
    'null',
    'if',
    'else', 
    'true',
    'false',
    'while',
    'break',
    'for',
    'switch',
    'case',
    'default',
    'main',
    'func',
    'null'

}


class GUI:
 # Metodo que contiene la definicion de la interfaz grafica 
    
   
    def __init__(self):
        self.window = Tk()
        
        self.nameFile=""
        self.Entrada = Entry(self.window,width=10)
        self.Consola = Entry(self.window,width=10)
        # Propiedades de la ventana
        self.window.title("ANALIZADOR - JPR - Vacaciones 2021 Junio")
        self.window.geometry('1600x1000')
        self.window.configure(bg = 'light slate gray')
              
        self.Inicial = Label(self.window, text="Proyecto 1 - Fase 1", font=("Times New Roman", 18), bg='turquoise1')
        self.Inicial.pack(fill=X) 
                
        # creacion del menu
        self.menu = Menu(self.window)
        #creacion de los submenu
        self.file_item = Menu(self.menu,tearoff=0)   #SUB MENU FUNCIONALIDADES 
        self.file_item.add_command(label='Crear archivo', command=self.nuevo_archivo)
        self.file_item.add_command(label='Abrir archivos', command=self.abrirFile)
        self.file_item.add_command(label='Guardar', command=self.guardar)
        self.file_item.add_command(label='Guardar como', command=self.guardarcomo)
        self.file_item.add_command(label='abrir', command=self.ayuda)

        self.herramienta_item = Menu(self.menu,tearoff=0)    # SUB MENU HERRAMIENTAS
        self.herramienta_item.add_command(label='Interpretar',command=self.analizar)
        self.herramienta_item.add_command(label='Debugger')
        
        self.report_item = Menu(self.menu,tearoff=0)    # SUB MENU REPORTES
        self.report_item.add_command(label='Reporte de Errores',command=self.reporte1)
        self.report_item.add_command(label='Arbol AST')
        self.report_item.add_command(label='Tabla de Simbolos')


        self.menu.add_cascade(label='Archivo', menu=self.file_item)
        self.menu.add_cascade(label='herramientas', menu=self.herramienta_item)
        self.menu.add_cascade(label='Reportes', menu=self.report_item) 
        self.window.config(menu=self.menu)


        # propiedades del textarea
       # self.Entrada = scrolledtext.ScrolledText(self.window,width=80,height=25)   # textArea Entrada

        self.Entrada= TextoAccion(self.Entrada)
        self.Entrada.place(x=50, y = 50) 


        self.Consola = scrolledtext.ScrolledText(self.window,width=70,height=25, background="black")   # textConsola area para la consola 
        self.Consola.place(x=750, y =50) 
        self.Consola.config(fg="lawn green",bg="gray20")      


        self.posicion = Label(self.window,text=f" Linea: 0      Columa: 0", font=("Times New Roman", 13), bg='deep sky blue')
        self.posicion.pack(side = BOTTOM, fill= X)

        self.Entrada.text.bind("<Button-1>", self.ObtenerFilaColumna) # Clik derecho 
        self.Entrada.text.bind("<Button-2>", self.ObtenerFilaColumna) # Click izquierdo
        self.Entrada.text.bind("<Button-3>", self.ObtenerFilaColumna) # ruedita  

        self.window.mainloop()

    def ayuda(self):
        self.nameFile=fd.askopenfilename(title = "Seleccione archivo",filetypes = (("jpr files","*.jpr"),("All Files","*.*")))
        if self.nameFile!="":
            archi1=open(self.nameFile, "r", encoding="utf-8")
            contenido=archi1.read()
            archi1.close()
            self.Entrada.delete("1.0", END)
            self.Entrada.insert("1.0", contenido)
            self.Consola.delete("1.0","end") 

    # Dispara el Filechooser
    def abrirFile(self):
        self.nameFile=fd.askopenfilename(title = "Seleccione archivo",filetypes = (("jpr files","*.jpr"),("All Files","*.*")))
        if self.nameFile!="":
            archi1=open(self.nameFile, "r", encoding="utf-8")
            contenido=archi1.read()
            archi1.close()
            self.Entrada.delete("1.0", END)
            for letra in self.pintar(contenido):
                self.Entrada.insert(INSERT,letra[1],letra[0])

            self.Consola.delete("1.0","end") 

    def guardarcomo(self):
        self.nameFile=fd.asksaveasfilename(initialdir = "/",title = "Guardar como",filetypes = (("jpr files","*.jpr"),("todos los archivos","*.*")))
        if self.nameFile!="":
            self.nameFile=self.nameFile
            archi1=open(self.nameFile, "w", encoding="utf-8")
            archi1.write(self.Entrada.get("1.0", END))
            archi1.close()
            mb.showinfo("Información", "Los datos fueron guardados en el archivo.")
        
    def guardar(self):
        if self.nameFile!="":
            contenido =self.Entrada.get(1.0,'end-1c')
            fichero=open(self.nameFile,'w+')
            fichero.write(contenido)
            fichero.close()

            mb.showinfo("Información", "Archivo actualizado.")
        else:
            self.guardarcomo()

    def nuevo_archivo(self):
        self.Entrada.delete(1.0, END)

    def analizar(self):
        self.Consola.delete(1.0, END)
        entrada= self.Entrada.get("1.0",END) # FILA 1 COLUMNA 0
        scanner= analizador(entrada)
        self.Consola.insert("1.0",scanner)        


    def reporte1(self):
        contador=1
        f = open('Reporte.html','w')

        mensaje = """
        <!doctype html>
        <html lang="en">
        <head>
            <!-- Required meta tags -->
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

            <!-- Bootstrap CSS -->
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

            <title>Hello, world!</title>
        </head>
        <body>

            <h1 class ="bg-success text-center">Tablas de Errores <h1>
            </br>
            <div class= container>
                <h4 class ="bg-warning">Errores lexicos y Sintacticos <h4>
                <table class="table  table-hover   table-bordered"" >
                <thead class="thead-dark"  >
                    <tr>
                    <th scope="col">#</th>
                    <th scope="col">Tipo de Error</th>
                    <th scope="col">Descripcion</th>
                    <th scope="col">Fila</th>
                    <th scope="col">Columna</th>
                    </tr>
                </thead>
                <tbody>

        """
        datos="<tr>"
        for x in listaErrores():
            datos+="\n<th scope=\"row\">" +str(contador)+"</th>\n<td>"+x.tipo+"</td>\n<td>"+x.descripcion+"</td><td>"+str(x.fila)+"</td><td>"+str(x.columna)+"</td><tr>"
            contador=contador +1

        mensaje2="""    <tr>
            </tbody>
                </table>

            </div>

            <!-- Optional JavaScript -->
            <!-- jQuery first, then Popper.js, then Bootstrap JS -->
            <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
        </body>
        </html>
            
        
        
        
        
        
        
        
        
        
        """

        f.write(mensaje+datos+mensaje2)
        f.close()

        webbrowser.open_new_tab('Reporte.html')

    def ObtenerFilaColumna(self, event):
        self.Entrada.text.bind("<Button-1>", self.ObtenerFilaColumna) # Clik derecho 
        self.Entrada.text.bind("<Button-2>", self.ObtenerFilaColumna) # Click izquierdo
        self.Entrada.text.bind("<Button-3>", self.ObtenerFilaColumna) # ruedita 
        
        info = self.Entrada.text.index(INSERT).split(".")
        fila= info[0]
        columna= info[1]

        self.posicion.config(text=f" Linea: "+fila+"      Columa:  "+columna)


    def pintar(self,texto):
        #para pintar se realiza un analizador a patita, se hace para cuando haga match entonces pinte de un color
        lista = [] #para guardar las palabras
        palabra = ''
        caracter=''
        contador = 0
        
        # recorre la entrada 
        while contador<len(texto): # cuenta todas las letras que se ingreso en el cuadro de texto
            caracter = texto[contador]
            # verifica si lo que entra se encuentra entre letra o numero  estado letra o digito
            if re.search(r"[a-zA-Z0-9]", caracter): 
                palabra += caracter # para identificar un id o palabra reservada
            
            #estado de cadena con comilla doble
            elif caracter== '"': 
                if re.match(r'[a-zA-Z][a-zA-Z0-9_]*',palabra):
                    id=[]
                    id.append("variable")
                    id.append(palabra)
                    lista.append(id)
                    palabra=''

                elif re.match(r'(\d+\.\d+|\d+)',palabra):
                    num=[]
                    num.append("numero")
                    num.append(palabra)
                    lista.append(num)
                    palabra=''
                    
                while(contador < len(texto)):
                    caracter=texto[contador]
                    palabra+=caracter
                    if re.match(r'\"(\\"|.)*?\"',palabra):
                        cadena=[]
                        cadena.append("cadena")
                        cadena.append(palabra)
                        lista.append(cadena)
                        palabra=''
                        break
                    contador+=1

                    
                        
            # estado de cadena con comilla simple                        
            elif caracter=="'":
                if re.match(r'[a-zA-Z][a-zA-Z0-9_]*',palabra):
                    id=[]
                    id.append("variable")
                    id.append(palabra)
                    lista.append(id)
                    palabra=''

                elif re.match(r'(\d+\.\d+|\d+)',palabra):
                    num=[]
                    num.append("numero")
                    num.append(palabra)
                    lista.append(num)
                    palabra=''

                copia=contador
                verifi=0
                while(True):
                    caracter=texto[contador]
                    palabra+=caracter
                    if re.match(r'\'(\\"|.)*?\'',palabra):
                        cadena=[]
                        cadena.append("cadena")
                        cadena.append(palabra)
                        lista.append(cadena)
                        palabra=''
                        break
                    contador+=1
                    verifi+=1
                    if verifi>3:
                        err=[]
                        palabra=''
                        palabra=texto[copia:len(texto)]
                        err.append("err")
                        err.append(palabra)
                        lista.append(err)
                        palabra=''
                        contador=len(texto)+1
                        break                                    
            
            # estado de comentarios
            elif caracter=='#':
                if re.match(r'[a-zA-Z][a-zA-Z0-9_]*',palabra):
                    id=[]
                    id.append("variable")
                    id.append(palabra)
                    lista.append(id)
                    palabra=''

                elif re.match(r'(\d+\.\d+|\d+)',palabra):
                    num=[]
                    num.append("numero")
                    num.append(palabra)
                    lista.append(num)
                    palabra=''
                palabra +=caracter
                
                if texto[contador+1]!='*':
                    while(caracter!="\n"):
                        contador+=1
                        caracter=texto[contador]
                        palabra+=caracter
                    if re.match(r'\#.*\n',palabra): # si si es igual crea el comentario
                        comentario=[]
                        comentario.append("comentario")
                        comentario.append(palabra)
                        lista.append(comentario)
                        palabra=''
                else:
                    while(True):
                        if caracter=="*" and texto[contador+1]=="#":
                            contador+=1
                            caracter=texto[contador]
                            palabra+=caracter
                            break
                        contador+=1
                        caracter=texto[contador]
                        palabra+=caracter
                        
                        
                       

                    if re.match(r'\#\*(.|\n)*?\*\#',palabra):
                        comentario=[]
                        comentario.append("comentario")
                        comentario.append(palabra)
                        lista.append(comentario)

                        palabra=''
                        
            #estado de aceptacion            
            else:
                if re.search(r'[a-zA-Z][a-zA-Z0-9_]*',palabra):
                    id=[]
                    id.append("variable")
                    id.append(palabra)
                    lista.append(id)
                    palabra=''


                elif re.match(r'(\d+\.\d+|\d+)',palabra):
                    num=[]
                    num.append("numero")
                    num.append(palabra)
                    lista.append(num)
                    palabra=''

                
                otros=[]
                otros.append("otro")
                otros.append(texto[contador])
                lista.append(otros)
            
            contador+=1
        
        for pal in lista:
            if pal[1].lower() in reservadas:
                pal[0]="reservadas"


        return lista

class TextoAccion(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        # bg -> color de fondo --- foreground -> color al texto --- selectbrackgroud -> color a lo que seleccione ---
        # inserbackgroud -> color al puntero
        self.text = tk.Text(self, bg='#103045', foreground="white", selectbackground="steel blue",
                            insertbackground='white',  width=78, height=25)
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.text.yview)
        self.text.configure(yscrollcommand=self.scrollbar.set)

        self.nLineas = TextoLinea(self, width=30, bg='azure')
        self.nLineas.attach(self.text)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.nLineas.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
        self.text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)


        self.scrollbar.bind("<Motion>", self.onScrollRelease)
        self.text.bind("<Motion>", self.nLineas.redraw)
        self.text.bind("<Key>", self.onPressDelay)
        self.text.bind("<Button-1>", self.nLineas.redraw)
        self.scrollbar.bind("<Button-1>", self.onScrollPress)
        self.scrollbar.bind("<Motion>", self.nLineas.redraw)
        self.text.bind("<MouseWheel>", self.onPressDelay)


        self.text.tag_config('comentario', foreground='gray')
        self.text.tag_config('otro', foreground='white')
        self.text.tag_config('reservadas', foreground='sky blue')
        self.text.tag_config('cadena', foreground='orange')
        self.text.tag_config('variable', foreground='white')
        self.text.tag_config('err', foreground='red')
        self.text.tag_config('numero', foreground='DarkOrchid1')

    def onScrollPress(self, *args):
        self.scrollbar.bind("<B1-Motion>", self.nLineas.redraw)

    def onScrollRelease(self, *args):
        self.scrollbar.unbind("<B1-Motion>", self.nLineas.redraw)

    def onPressDelay(self, *args):
        self.after(2, self.nLineas.redraw)

    def get(self, *args, **kwargs):
        return self.text.get(*args, **kwargs)

    def insert(self, *args, **kwargs):
        return self.text.insert(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.text.delete(*args, **kwargs)

    def index(self, *args, **kwargs):
        return self.text.index(*args, **kwargs)

    def redraw(self):
        self.nLineas.redraw()

    def tag_configure(self, tagName, cnf=None, **kw):
        """Configure a tag TAGNAME."""
        return self._configure(('tag', 'configure', tagName), cnf, kw)

class TextoLinea(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs, highlightthickness=0)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        self.delete("all")
        i = self.textwidget.index("@0,0")
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2, y, anchor="nw", text=linenum, fill="#606366")
            i = self.textwidget.index("%s+1line" % i)


start = GUI()