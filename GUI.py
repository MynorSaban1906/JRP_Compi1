from tkinter import *            # ventana
from tkinter import Menu            # barra de tareas
from tkinter import scrolledtext    # textarea
from tkinter import messagebox      # message box
from tkinter import filedialog as fd # filechooser
from tkinter import messagebox as mb
from tkinter import Canvas,Frame
import tkinter as tk

class GUI:
 # Metodo que contiene la definicion de la interfaz grafica 
    
   
    def __init__(self):
        self.window = Tk()
        
        self.nameFile=""
        self.txtEntrada = Entry(self.window,width=10)
        self.txtConsola = Entry(self.window,width=10)
        # Propiedades de la ventana
        self.window.title("ANALIZADOR - JPR")
        self.window.geometry('1600x1000')
        self.window.configure(bg = 'gray90')
              
        self.lbl = Label(self.window, text="Proyecto 1 - JPR", font=("Arial Bold", 15), bg='#24C14A')
        self.lbl.pack(fill=X)  # Label estirado por el eje X en su posicion
                
        # creacion del menu
        self.menu = Menu(self.window)
        #creacion de los submenu
        self.file_item = Menu(self.menu,tearoff=0)   #SUB MENU FUNCIONALIDADES 
        self.file_item.add_command(label='Crear archivo', command=self.nuevo_archivo)
        self.file_item.add_command(label='Abrir archivos', command=self.abrirFile)
        self.file_item.add_command(label='Guardar', command=self.guardar)
        self.file_item.add_command(label='Guardar como', command=self.guardarcomo)
 
        self.herramienta_item = Menu(self.menu,tearoff=0)    # SUB MENU HERRAMIENTAS
        self.herramienta_item.add_command(label='Interpretar')
        self.herramienta_item.add_command(label='Debugger')
        
        self.report_item = Menu(self.menu,tearoff=0)    # SUB MENU REPORTES
        self.report_item.add_command(label='Reporte de Errores')
        self.report_item.add_command(label='Arbol AST')
        self.report_item.add_command(label='Tabla de Simbolos')


        self.menu.add_cascade(label='Archivo', menu=self.file_item)
        self.menu.add_cascade(label='herramientas', menu=self.herramienta_item)
        self.menu.add_cascade(label='Reportes', menu=self.report_item) 
        self.window.config(menu=self.menu)


        # propiedades del textarea
       # self.txtEntrada = scrolledtext.ScrolledText(self.window,width=80,height=25)   # textArea Entrada
        self.txtEntrada= ScrollTextUwU.text(self.txtEntrada)
        self.txtEntrada.place(x=50, y = 50)
 
        self.txtConsola = scrolledtext.ScrolledText(self.window,width=70,height=25, background="black")   # textConsola area para la consola 
        self.txtConsola.place(x=750, y =50) 
        self.txtConsola.config(fg="green3",bg="gray20")      


        self.window.mainloop()



    # Dispara el Filechooser
    def abrirFile(self):
        self.nameFile=fd.askopenfilename(title = "Seleccione archivo",filetypes = (("jpr files","*.jpr"),("All Files","*.*")))
        if self.nameFile!="":
            archi1=open(self.nameFile, "r", encoding="utf-8")
            contenido=archi1.read()
            archi1.close()
            self.txtEntrada.delete("1.0", END)
            self.txtEntrada.insert("1.0", contenido) 

    def guardarcomo(self):
        self.nameFile=fd.asksaveasfilename(initialdir = "/",title = "Guardar como",filetypes = (("jpr files","*.jpr"),("todos los archivos","*.*")))
        if self.nameFile!="":
            self.nameFile=self.nameFile+".jpr"
            archi1=open(self.nameFile, "w", encoding="utf-8")
            archi1.write(self.txtEntrada.get("1.0", END))
            archi1.close()
            mb.showinfo("Información", "Los datos fueron guardados en el archivo.")
        
    def guardar(self):
        if self.nameFile!="":
            contenido =self.txtEntrada.get(1.0,'end-1c')
            fichero=open(self.nameFile,'w+')
            fichero.write(contenido)
            fichero.close()

            mb.showinfo("Información", "Archivo actualizado.")
        else:
            self.guardarcomo()

    def nuevo_archivo(self):
        self.txtEntrada.delete(0, 'end')


# -------- CLASE PARA PODER COLOCAR NUMEROS EN LA CONSOLA DE ENTRADA -----------
class ScrollTextUwU(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        # bg -> color de fondo --- foreground -> color al texto --- selectbrackgroud -> color a lo que seleccione ---
        # inserbackgroud -> color al puntero
        self.text = tk.Text(self, bg='#FFFFFF', foreground="#000000", selectbackground="#C8C8C8",
                            insertbackground='#000000',  width=80, height=25)
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.text.yview)
        self.text.configure(yscrollcommand=self.scrollbar.set)

        self.numero_lineas = TextoLinea(self, width=35, bg='#D5D5D5')
        self.numero_lineas.attach(self.text)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.numero_lineas.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
        self.text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.text.bind("<Key>", self.onPressDelay)
        self.text.bind("<Button-1>", self.numero_lineas.redraw)
        self.scrollbar.bind("<Button-1>", self.onScrollPress)
        self.text.bind("<MouseWheel>", self.onPressDelay)

    def onScrollPress(self, *args):
        self.scrollbar.bind("<B1-Motion>", self.numero_lineas.redraw)

    def onScrollRelease(self, *args):
        self.scrollbar.unbind("<B1-Motion>", self.numero_lineas.redraw)

    def onPressDelay(self, *args):
        self.after(2, self.numero_lineas.redraw)

    def get(self, *args, **kwargs):
        return self.text.get(*args, **kwargs)

    def insert(self, *args, **kwargs):
        return self.text.insert(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.text.delete(*args, **kwargs)

    def index(self, *args, **kwargs):
        return self.text.index(*args, **kwargs)

    def redraw(self):
        self.numero_lineas.redraw()

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