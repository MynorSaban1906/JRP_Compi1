from tkinter import *               # ventana
from tkinter import Menu            # barra de tareas
from tkinter import scrolledtext    # textarea
from tkinter import messagebox      # message box
from tkinter import filedialog as fd # filechooser
from tkinter import messagebox as mb
from gramatica import analizador


class GUI:
 # Metodo que contiene la definicion de la interfaz grafica 
    
   
    def __init__(self):
        self.window = Tk()
        self.nameFile=""
        self.txtEntrada = Entry(self.window,width=10)
        self.txtConsola = Entry(self.window,width=10)
        self.txtrecorrido=Entry(self.window,width=10)
        self.txtTOKEN=Entry(self.window,width=10)
        # Propiedades de la ventana
        self.window.title("ANALIZADOR - JPR")
        self.window.geometry('1600x1000')
        self.window.configure(bg = 'gray90')
              

        # creacion del menu
        self.menu = Menu(self.window)
        #creacion de los submenu
        self.file_item = Menu(self.menu,tearoff=0)   #SUB MENU FUNCIONALIDADES 
        self.file_item.add_command(label='Crear archivo', command=self.nuevo_archivo)
        self.file_item.add_command(label='Abrir archivos', command=self.abrirFile)
        self.file_item.add_command(label='Guardar', command=self.guardar)
        self.file_item.add_command(label='Guardar como', command=self.guardarcomo)
 
        self.herramienta_item = Menu(self.menu,tearoff=0)    # SUB MENU HERRAMIENTAS
        self.herramienta_item.add_command(label='Interpretar',command=self.Analizar)
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
        self.txtEntrada = scrolledtext.ScrolledText(self.window,width=80,height=25)   # textArea Entrada
        self.txtEntrada.place(x=50, y = 50)
 
        self.txtConsola = scrolledtext.ScrolledText(self.window,width=70,height=25, background="black")   # textConsola area para la consola 
        self.txtConsola.place(x=750, y =50) 
        self.txtConsola.config(fg="green3",bg="gray20")      


        self.window.mainloop()


    def Analizar(self):
        self.txtEntrada.delete(0, 'end')
        
        entrada= self.txtEntrada.get("1.0",END) # FILA 1 COLUMNA 0
        scanner= analizador(entrada)
        self.txtConsola.insert("1.0",scanner)


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
start = GUI()