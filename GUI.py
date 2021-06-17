
from tkinter import *            # ventana
from tkinter import Menu            # barra de tareas
from tkinter import scrolledtext    # textarea
from tkinter import messagebox      # message box
from tkinter import filedialog as fd # filechooser
from tkinter import messagebox as mb
from tkinter import Canvas,Frame
import tkinter as tk
import webbrowser


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
              
        # self.lbl = Label(self.window, text="Proyecto 1 - JPR", font=("Arial Bold", 15), bg='#24C14A')
        # self.lbl.pack(fill=X)  # Label estirado por el eje X en su posicion
                
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
        self.report_item.add_command(label='Reporte de Errores',command=self.reporte1)
        self.report_item.add_command(label='Arbol AST')
        self.report_item.add_command(label='Tabla de Simbolos')


        self.menu.add_cascade(label='Archivo', menu=self.file_item)
        self.menu.add_cascade(label='herramientas', menu=self.herramienta_item)
        self.menu.add_cascade(label='Reportes', menu=self.report_item) 
        self.window.config(menu=self.menu)


        # propiedades del textarea
       # self.txtEntrada = scrolledtext.ScrolledText(self.window,width=80,height=25)   # textArea Entrada
        self.txtEntrada= ScrollTextUwU(self.txtEntrada)
        self.txtEntrada.place(x=50, y = 50)
 
        self.txtConsola = scrolledtext.ScrolledText(self.window,width=70,height=25, background="black")   # textConsola area para la consola 
        self.txtConsola.place(x=750, y =50) 
        self.txtConsola.config(fg="green3",bg="gray20")      


        self.posicion = Label(self.window,text=f" Linea: 0      Columa: 0", font=("Times New Roman", 13), bg='deep sky blue')
        self.posicion.pack(side = BOTTOM, fill= X)

        self.txtEntrada.text.bind("<Button-1>", self.getInfo) # Clik derecho 
        self.txtEntrada.text.bind("<Button-2>", self.getInfo) # Click izquierdo
        self.txtEntrada.text.bind("<Button-3>", self.getInfo) # ruedita  


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
                <h4 class ="bg-warning">Errores lexicos <h4>
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
                    <tr>
                    <th scope="row">1</th>
                    <td>Mark</td>
                    <td>Otto</td>
                    <td>@mdo</td>
                    </tr>
                    <tr>
                    <th scope="row">2</th>
                    <td>Jacob</td>
                    <td>Thornton</td>
                    <td>@fat</td>
                    </tr>


                    <tr>
                    <th scope="row">3</th>
                    <td>Larry</td>
                    <td>the Bird</td>
                    <td>@twitter</td>
                    </tr>
        """
        datos="<tr>"
        lista = ["hola","jaunito","jojo"]
        for x in lista:
            datos+="\n<th scope=\"row\">" +str(contador)+"</th>\n<td>"+x+"</td></tr>"
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



    def getInfo(self, event):
        self.txtEntrada.text.bind("<Button-1>", self.getInfo) # Clik derecho 
        self.txtEntrada.text.bind("<Button-2>", self.getInfo) # Click izquierdo
        self.txtEntrada.text.bind("<Button-3>", self.getInfo) # ruedita 



        
        string = self.txtEntrada.text.index(INSERT).split(".")
        fila= string[0]
        columna= string[1]

        self.posicion.config(text=f" Linea: "+fila+"      Columa:  "+columna)

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


        self.scrollbar.bind("<Motion>", self.onScrollRelease)
        self.text.bind("<Motion>", self.numero_lineas.redraw)
        self.text.bind("<Key>", self.onPressDelay)
        self.text.bind("<Button-1>", self.numero_lineas.redraw)
        self.scrollbar.bind("<Button-1>", self.onScrollPress)
        self.scrollbar.bind("<Motion>", self.numero_lineas.redraw)
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