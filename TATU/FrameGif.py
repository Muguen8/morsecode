import os
import tkinter as tk
from time import sleep
import PIL
from PIL import Image, ImageTk
import itertools
import threading

class gif1(tk.Frame):
	def __init__(self, maestro, **kwargs):
		super().__init__(maestro)
		
		self.maestro = maestro
		self.bandera = False
		self.fondo = kwargs.get("bg",maestro.cget("bg"))
		self.intervalo = kwargs.get("intervalo", 50)
		self.ruta      = kwargs.get("ruta")
		self.ext       = kwargs.get("ext", ".png")
		self.texto = False
		self.resize =  kwargs.get("resize", False)
		self.px = 10
		self.py = 10
	
		
	def arrancar(self):
		x = threading.Thread(target=self.hiloLoading)
		x.daemon=True
		x.start()
	
	def loopear(self):
		try:
			self.maestro.winfo_toplevel().after(100, self.loopear)
		except:
			self.bandera=True
		self.cerrar()
	
	def hiloLoading(self):
		
		self.labels = []

		self.construir()
		self.crearLabels()		
		self.reloj()
		
		self.loopear()
		
		try:
			self.generalisimo.pack(expand = True, fill = tk.BOTH, side = tk.TOP)
		except Exception as e:
			print(e)
			
	def construir(self):
			
		self.generalisimo = tk.Frame(self, bg = self.fondo)
		self.generalisimo.rowconfigure(1, weight = 1)
		self.generalisimo.columnconfigure(0, weight = 1)
		
		
		self.f = tk.Frame(self.generalisimo, bg = self.fondo)
		
		self.IMAGEN = tk.Label(self.f, 
							   bg 	  = self.fondo,
							   anchor = tk.CENTER)
		self.IMAGEN.grid(row    = 0,
						 column = 0,)
		
		if self.texto:
			self.TEXTO = tk.Label(self.f, 
								  textvariable = self.texto,
								  bg     = self.fondo,
								  font 	 = ("System", 9),
								  anchor = tk.CENTER)
			self.TEXTO.grid(row    = 1,
							column = 0,
							padx   = self.px)


		self.f.grid(row 	= 0, 
					column  = 0, 
					sticky  = "")


	def actualizar_label(self, msj):
		self.texto.set(msj)


	def crearLabels(self):
		self.etiquetas = []
		for n in sorted(os.listdir(self.ruta), key = lambda x: x.split(".")[0]):
			ruta_imagen = self.ruta + f"/{n}"
			
			image = Image.open(ruta_imagen)
			if self.resize:
				x,y=self.resize
				image= image.resize((x,y), Image.ANTIALIAS)
			image = ImageTk.PhotoImage(image)
			label = tk.Label(self.f, 
							 image = image,
							 bg = self.fondo)
			label.image = image
			self.etiquetas.append(label)
		self.labels += self.etiquetas

	def cambiarImagen(self, label):
		self.IMAGEN.grid_forget()
		self.IMAGEN = label
		self.IMAGEN.grid(row = 0,
						 column = 0,
						 padx = self.px,
						 pady   = (3, 0))
	
	def loop(self):
		try:
			label = self.labels.pop(0)
		except IndexError:
			self.labels += self.etiquetas
			label =  self.labels.pop(0)
		finally:
			self.cambiarImagen(label)

	def reloj(self):
		self.loop()
		self.f.after(self.intervalo, self.reloj)
	
	def cerrar(self):
		if self.bandera:
			c = 0
			while c < 30:
				try:
					#ventana.deconify()
					#for n in self.winfo_children():
					#	n.destroy()
					self.destroy()
					c = 30
					print("LOADING DESTROY")
					break
				except:
					c += 1
					print("ERROR")
					
class gif(tk.Frame):
	def __init__(self, maestro, **kwargs):
		super().__init__(maestro,bg=kwargs.get("bg",maestro.cget("bg")))
		
		self.maestro = maestro
		self.bandera = False
		self.c_loops = 100
		self.fondo = kwargs.get("bg",maestro.cget("bg"))
		self.intervalo = kwargs.get("intervalo", 50)
		self.ruta      = kwargs.get("ruta")
		self.ext       = kwargs.get("ext", ".png")
		self.texto = False
		self.resize =  kwargs.get("resize", False)
		
		
	def arrancar(self, c_loops=False):
		self.c_loops = c_loops
		x = threading.Thread(target=self.hiloLoading)
		x.daemon=True
		x.start()
	
	def actualizar_c_loops(self,cant):
		self.c_loops=cant
		self.loop()
		
	def loopear(self):
		self.maestro.winfo_toplevel().after(40, self.loopear)
		self.cerrar()
	
	def hiloLoading(self):
		
		self.labels = []

		self.construir()
		self.crearLabels()		
		self.reloj()
		
		self.loopear()
		
		try:
			self.generalisimo.pack(expand = True, fill = tk.BOTH, side = tk.TOP)
		except Exception as e:
			print(e)
			
	def construir(self):
			
		self.generalisimo = tk.Frame(self, bg = self.fondo)
		self.generalisimo.rowconfigure(1, weight = 1)
		self.generalisimo.columnconfigure(0, weight = 1)
		
		
		self.f = tk.Frame(self.generalisimo, bg = self.fondo)
		
		self.IMAGEN = tk.Label(self.f, 
							   #bg 	  = "green",#self.fondo,
							   anchor = tk.CENTER)
		self.IMAGEN.grid(row    = 0,
						 column = 0,)
		
		if self.texto:
			self.TEXTO = tk.Label(self.f, 
								  textvariable = self.texto,
								  bg     = self.fondo,
								  font 	 = ("System", 9),
								  anchor = tk.CENTER)
			self.TEXTO.grid(row    = 1,
							column = 0)


		self.f.grid(row 	= 0, 
					column  = 0,)


	def actualizar_label(self, msj):
		self.texto.set(msj)


	def crearLabels(self):
		self.etiquetas = []
		def limpiar(x):
			o = x.split(".")[0]
			x = o 
			x = x.strip().replace("(","")
			x = x.replace(")","")
			try:
				return int(x)
			except:
				return o 
		for n in sorted(os.listdir(self.ruta), key = lambda x: limpiar(x)):
			ruta_imagen = self.ruta + f"/{n}"
			image = Image.open(ruta_imagen)
			if self.resize:
				x,y=self.resize
				image= image.resize((x,y))
			image = ImageTk.PhotoImage(image)
			#image = Image.open(ruta_imagen)
			#image = ImageTk.PhotoImage(image)
			label = tk.Label(self.f,)#bg = "red")#self.fondo)		
			label.IMAGEN = image
			label.config(image=label.IMAGEN)
			self.etiquetas.append(label)
		self.labels += self.etiquetas

	def cambiarImagen(self, label):
		self.IMAGEN.grid_forget()
		self.IMAGEN = label
		self.IMAGEN.config(bg=self.fondo)
		self.IMAGEN.grid(row = 0,
						 column = 0)
	
	def loop(self):
		if self.c_loops>0 or self.c_loops=="inf":
			try:
				label = self.labels.pop(0)
			except IndexError:
				self.labels += self.etiquetas
				label =  self.labels.pop(0)
				self.c_loops-=1
			finally:
				self.cambiarImagen(label)
		else:
			self.maestro.grid_forget()
			self.grid_forget()

	def reloj(self):
		self.loop()
		self.f.after(self.intervalo, self.reloj)
	
	def cerrar(self):
		if self.bandera:
			c = 0
			while c < 30:
				try:
					#ventana.deconify()
					#for n in self.winfo_children():
					#	n.destroy()
					self.destroy()
					c = 30
					print("LOADING DESTROY")
					break
				except:
					c += 1
					print("ERROR")
			
if __name__ == "__main__":

	raiz = tk.Tk()
	raiz.state("zoomed")
	directorio = os.path.abspath(os.path.dirname(__file__))	
	r = f'{directorio}/iconos/loop_loading/'
	o = gif(raiz, ruta = r, resize = (210, 100), intervalo = 200, label_frame = True)	
	o.pack()
	o.arrancar()	
	
	raiz.mainloop()
