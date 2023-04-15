#Notificaciones
import tkinter as tk
import PIL
from PIL import Image, ImageTk
import json
import os			
#import CajonDeVariablesGrales
#import requests

class BtnCheck(tk.Frame):
	
	def __init__(self, maestro, texto, variable, initial_val = True, boton = {}, label = {}, **kwargs):
		super().__init__(maestro, bg = kwargs.get("bg", maestro.cget("bg")))
		
		self.rowconfigure(0, weight = 1)
		#self.columnconfigure(0, weight = 1)
		simbolo_check  = "✔" #"✔"
		simbolo_empty  = " "
		self.estado_check = variable.get()
		
		print(self.estado_check)
		if self.estado_check :
			simbolo = simbolo_check
			variable.set(True)
		else:
			simbolo = simbolo_empty #"☐" #"✘"		
			variable.set(False)
		
		#self.estado_check  = not self.estado_check 
		
		color = self.cget("bg")

		borde = boton.get("borde", 6)

		font_1 = kwargs.get("font_1", ("Yu Gothic Medium", 12))
		font_2 = kwargs.get("font_2", ("Yu Gothic Medium", 12, "bold"))

		f_label = tk.Frame(self, bg = color)
		self.l_0 = tk.Label(f_label, 
					   padx   = 5, 
					   anchor = tk.CENTER,
					   bg     = color,  
					   text   = texto, 
					   fg     = label.get("color_letra", "#292929"), 
					   font   = label.get("fuente", font_1)
					   )
		self.l_0.grid(row = 0, column = 0, sticky = "ns", pady = (borde//2,0), padx = (5,3))

		f_contenido = tk.Frame(self, bg = color)

		normal_1 = boton.get("normal_1", "#FFFFFF")
		normal_letra = boton.get("normal_letra", "#2CDA91") #"#FFFFFF"
		normal_2 = boton.get("normal_2", "#BFBFBF")
		
		b_2 = tk.Label(f_contenido, 
					   width  = 2,
					   bg     = boton.get("fondo", normal_2),  
					   text   = simbolo, 
					   fg     = boton.get("color_letra", normal_letra), 
					   font   = boton.get("fuente", font_2)
					   )
					   
		b_1 = tk.Label(f_contenido, 
					   cursor = "hand2", 
					   width  = 2,
					   #height = boton.get("label_height", 2), 
					   bg     = boton.get("fondo", normal_1), 
					   fg     = boton.get("color_letra", normal_letra), 
					   text   = simbolo, 
					   font   = boton.get("fuente", font_2)
					   )
		
		b_2.grid(row = 0, column  =0, padx = (0, borde), pady = (borde, 0))
		b_1.grid(row = 0, column  =0)
		
		resaltar = boton.get("resaltar_1", "#E5E5E5")
		resaltar_letra = boton.get("resaltar_letra", "#2ABC7F")
		resaltar_2 = boton.get("resaltar_2", "#4D4D4D")
		#resaltar_letra_2 = boton.get("resaltar_letra_2", normal_1)
		
		def func_resaltar(estado):
			if estado:
				b_2.configure(bg = resaltar_2)
				b_1.configure(bg = resaltar, fg = resaltar_letra)
			else:
				b_2.configure(bg = normal_2)
				b_1.configure(bg = normal_1, fg = normal_letra)
			
			
		b_1.bind("<Enter>", lambda e: func_resaltar(True))
		b_1.bind("<Leave>", lambda e: func_resaltar(False))

		presionar       = boton.get("presionar", "#252525")
		presionar_letra = boton.get("presionar_letra", "#2E8661")
		
		ACCION = boton.get("accion", False)
		PARAM  = boton.get("param",  True)
		
		def func_presionar(estado):
			if estado:
				b_2.configure(bg = presionar, fg = presionar_letra)
				b_1.grid_forget() #configure(bg = presionar, fg = presionar_letra)
			else:
				b_2.configure(bg = normal_2)
				b_1.grid(row = 0, column  =0)#.configure(bg = normal_1, fg = normal_letra)
				if self.estado_check :
					simbolo = simbolo_empty #"✘"
					variable.set(False)
				else:
					simbolo = simbolo_check
					variable.set(True)
				self.estado_check  = not self.estado_check 
				b_2.configure(text = simbolo)
				b_1.configure(text = simbolo)
				if ACCION:
					ACCION(PARAM)
	
		b_1.bind("<ButtonPress>", lambda e: func_presionar(True))
		b_1.bind("<ButtonRelease>", lambda e: func_presionar(False))
	
		f_contenido.grid(row =0, column = 1, sticky = "nswe")
		f_label.grid(row =0, column = 0, sticky = "nswe")
	
	def set_falta_aceptar(self, color):
		self.l_0.configure(fg = color)


class BtnRetro(tk.Frame):
	
	def __init__(self, maestro, boton={}):
		super().__init__(maestro, bg = maestro.cget("bg"))
		
		self.rowconfigure(0, weight = 1)
		self.columnconfigure(0, weight = 1)

		borde = boton.get("borde", 8)
		borde_2 = boton.get("borde_2", 0)
		
		color = maestro.cget("bg")
		f_contenido = tk.Frame(self, bg = color)
		if borde_2:
			f_ext = tk.Frame(self, bg = "#828282",padx=1,pady=1)
			f_ext.grid(row =0,column=0,)
			f_contenido = tk.Frame(f_ext, bg = color)
		
		self.normal_1 = boton.get("normal_1", "#4D4D4D")
		self.normal_letra = boton.get("normal_letra", "#FFFFFF") #"#FFFFFF"
		self.normal_2 = boton.get("normal_2", "#FFFFFF")

		self.desactivado_1 = boton.get("desactivado_1", "#CACACA")
		self.desactivado_letra = boton.get("desactivado_letra", "#A0A0A0") #"#FFFFFF"
		self.desactivado_2 = boton.get("desactivado_2", "#DEDEDE")
		
		sep_px = boton.get("sep_px", 5)
		
		self.b_2 = tk.Label(f_contenido, 
					        padx   = sep_px, 
					        height = boton.get("label_height", 2), 
					        bg     = boton.get("fondo", self.normal_2),  
					        text   = boton.get("texto", "VACIO"), 
					        fg     = boton.get("fondo", self.normal_2), 
					        font   = boton.get("fuente", ("Fixedsys", 15, "bold")))
					   
		self.b_1 = tk.Label(f_contenido, 
							cursor = "hand2", 
							padx   = sep_px, 
							height = boton.get("label_height", 2), 
							bg     = boton.get("fondo", self.normal_1), 
							fg     = boton.get("color_letra", self.normal_letra), 
							text   = boton.get("texto", "VACIO"), 
							font   = boton.get("fuente", ("Fixedsys", 15, "bold")))
		
		self.b_2.grid(row = 0, column  =0, padx = (borde_2, borde), pady = (borde, borde_2))
		self.b_1.grid(row = 0, column  =0)
		
		self.resaltar = boton.get("resaltar_1", self.normal_2)
		self.resaltar_letra = boton.get("resaltar_letra", self.normal_1)
		self.resaltar_2 = boton.get("resaltar_2", self.normal_1)
		
		self.presionar       = boton.get("presionar", "#252525")
		self.presionar_letra = boton.get("presionar_letra", "#7F7F7F")
		
		self.ACCION = boton.get("accion", print)
		self.PARAM  = boton.get("param",  [])
		
		f_contenido.grid(row =0, column = 0, sticky = "nswe")
		self.vincular()
		#self.desvincular()			

	def vincular(self,):
		self.func_resaltar(False)
		self.b_1.bind("<Enter>", lambda e: self.func_resaltar(True))
		self.b_1.bind("<Leave>", lambda e: self.func_resaltar(False))
		self.b_1.bind("<ButtonPress>", lambda e:   self.func_presionar(True))
		self.b_1.bind("<ButtonRelease>", lambda e: self.func_presionar(False))
		self.b_1.config(state = "normal",cursor="hand2")
		
		
	def desvincular(self,):
		self.b_2.configure(bg = self.desactivado_2)
		self.b_1.configure(bg = self.desactivado_1, fg = self.desactivado_letra)
		self.b_1.unbind("<Enter>")
		self.b_1.unbind("<Leave>")
		self.b_1.unbind("<ButtonPress>")
		self.b_1.unbind("<ButtonRelease>")
		self.b_1.config(state = "disabled",cursor="arrow")
	
	def func_resaltar(self,estado):
		if estado:
			self.b_2.configure(bg = self.resaltar_2)
			self.b_1.configure(bg = self.resaltar, fg = self.resaltar_letra)
		else:
			self.b_2.configure(bg = self.normal_2)
			self.b_1.configure(bg = self.normal_1, fg = self.normal_letra)

	def func_presionar(self,estado):
		if estado:
			self.b_2.configure(bg = self.presionar, fg = self.presionar_letra)
			self.b_1.grid_forget() #configure(bg = presionar, fg = presionar_letra)
		else:
			self.b_2.configure(bg = self.normal_2)
			self.b_1.grid(row = 0, column  =0)#.configure(bg = normal_1, fg = normal_letra)
			if self.PARAM:
				self.ACCION(*self.PARAM)
			else:
				self.ACCION()
			
	def cambiar_texto(self, kwargs):
		self.b_1.configure(**kwargs)
		self.b_2.configure(**kwargs)

	def destacar(self, bg):
		self.b_1.configure(bg=bg)
	
	def cambiar_resaltar(self, color):
		self.resaltar = color
	
	def cambiar_command(self, **boton):
		self.ACCION = boton.get("command", print)
		self.PARAM  = boton.get("param",  self.PARAM)


class notificacionObligatoria(tk.Toplevel):
	
	
	def __init__(self, maestro, **kwargs):
		super().__init__(maestro, bg = kwargs["borde_color"])

		self.DIRECTORIO = os.path.abspath(os.path.dirname(__file__))
	
		self.attributes('-alpha', 0.0)
		self.maestro = maestro
		self.traerIconos()
	
		#self.link  = kwargs.get("link", {})
		self.ancho = kwargs.get("ancho", 100)
		self.alto  = kwargs.get("alto", 15)
		self.px = kwargs.get("px", 10)
		self.py = kwargs.get("py", 10)
		self.columnconfigure(0, weight =1)
		self.rowconfigure(0, weight =1)
		self.borde = kwargs.get("borde", 4)
		self.borde_2 = kwargs.get("borde_2", 1)
		
		self.var_consentimiento = tk.BooleanVar()
		self.pedir_consentimiento = kwargs.get("pedir_consentimiento", False)
		self.btn_cerrar = kwargs.get("btn_cerrar", {})
		self.accion_al_cierre = kwargs.get("accion_al_cierre", False)
		self.bind("<Return>", self.accion_al_cierre)
		self.layout(frame_1 = kwargs.get("frame_1", {}),
					marco   = kwargs.get("marco", {}),
					icono   = kwargs.get("icono", False),
					titulo  = kwargs.get("titulo", {}),
					contenido  = kwargs.get("contenido", {}),
					boton  = kwargs.get("boton", {}))
		self.wm_attributes("-topmost", 1)
		self.lift()
		self.wm_overrideredirect(True)
		self.protocol("WM_DELETE_WINDOW", self.protocoloCerrar)

	def traerIconos(self):
		global TRABA
		TRABA     = ImageTk.PhotoImage(Image.open(f'{self.DIRECTORIO}\\CODA\\Notificaciones\\iconos\\traba.png'))

	def protocoloCerrar(self, *args):
		self.unbind("<Return>")
		self.destroy()
		try:
			if self.accion_al_cierre:
				self.accion_al_cierre()
		except:
			pass
			
	def layout(self, frame_1, marco, icono, titulo, contenido, boton):
		frame_0 = tk.Frame(self, bg = self.cget("bg"))
		frame_0.columnconfigure(0, weight =1)
		frame_0.rowconfigure(0, weight =1)
		frame_0.rowconfigure(1, weight =1)

		marco_0 = tk.LabelFrame(self, bg = marco.get("bg", self.cget("bg")), bd = self.borde_2, relief = tk.FLAT)
		marco_0.columnconfigure(0, weight =1)
		marco_0.rowconfigure(0, weight =1)
		marco_0.rowconfigure(1, weight =1)
		marco_0.grid(row = 0, column = 0, sticky = "nswe", padx = (self.borde,0), pady = (0, self.borde))
		
		frame_1 = tk.Label(marco_0, **frame_1)
		frame_1.grid(row = 0, column = 0, sticky = "nswe") #, padx = (self.borde,0), pady = (0, self.borde)
		
		frame_1.rowconfigure(1,weight = 1)
		frame_1.columnconfigure(0,weight = 1)
		frame_1.columnconfigure(1,weight = 1)
		frame_1.columnconfigure(2,weight = 1)
		frame_1.columnconfigure(3,weight = 0)
		frame_1.columnconfigure(4,weight = 0)
		
		barra_horizontal = tk.Label(frame_1, image = TRABA, bg = frame_1.cget("bg"), width = self.ancho)
		barra_horizontal.grid(row = 0, column = 0, columnspan = 100, sticky = "we", padx = self.borde)

		barra_vertical = tk.Label(frame_1, image = TRABA, bg = frame_1.cget("bg"), height = self.alto)
		barra_vertical.grid(row = 0, column = 0, sticky = "ns", rowspan = 100, pady = self.borde)
		
		margen_dcho = 1
		if icono:
			l_icono = tk.Label(frame_1, bg = frame_1.cget("bg"), image = icono)
			l_icono.grid(row = 0, rowspan =100, column = 0, sticky = "w", padx = (self.px*2, self.px), pady = self.py,)
			margen_dcho = icono.width()

		imagen_margen_dcho = TRABA
		l_traba = tk.Label(frame_1, width = margen_dcho, bg = frame_1.cget("bg"), image = imagen_margen_dcho)
		l_traba.grid(row = 0, rowspan = 100, column = 3, sticky = "ns")

		f_titulo = self.agregar_titulo(frame_1, titulo)
		f_titulo.grid(row = 0, column = 0, columnspan = 4, sticky = "nwe", padx = (10,0), pady = (self.py*2, self.py//2))
		
		self.agregar_paquetes(frame_1, contenido, boton)
		
		if self.btn_cerrar:
			normal_1   = self.btn_cerrar.get("normal_1",    "#BD5A5A")
			normal_2   = self.btn_cerrar.get("normal_2",    "#FFFFFF")
			resaltar_1 = self.btn_cerrar.get("resaltar_1",  "#843D3D")   
			resaltar_2 = self.btn_cerrar.get("resaltar_2",  "#EAEAEA")
			resaltar_letra = self.btn_cerrar.get("resaltar_letra", resaltar_2)
			presionar  = self.btn_cerrar.get("presionar", resaltar_1)
			
			l_cerrar = BtnRetro(frame_1, boton = {"texto": "x", 
												  "label_height":   1, 
												  "fuente": 		("Fixedsys", 20, "bold"),
												  "normal_1" :      normal_1,
												  "normal_2" :      normal_2,
												  "resaltar_1":     resaltar_1,
												  "resaltar_2":     resaltar_2,
												  "resaltar_letra": resaltar_letra,
												  "presionar" :     presionar,
												  "accion":         self.protocoloCerrar,
												  })
			l_cerrar.grid(row = 0, rowspan = 100, column = 3, sticky = "ne", padx = self.px//2, pady = self.py//2)
		
		frame_0.grid(row = 0, column = 1, sticky = "nswe")
	
	def agregar_paquetes(self, frame_1, contenido, boton):
		f_contenido = self.agregar_contenido(frame_1, contenido)
		f_contenido.grid(row = 1, rowspan = 1, column = 1, padx = (0,self.px), pady = (0, self.py//2))

		f_boton = self.agregar_boton(frame_1, boton)
		f_boton.grid(row = 3, column = 0, columnspan = 4, padx = self.px + 10, pady = (0, self.py))
	
	def get_var_consentimiento(self):
		return self.var_consentimiento.get()
			
	def agregar_titulo(self, maestro, titulo):
		color = maestro.cget("bg")
		f_tit = tk.Frame(maestro, bg = color)

		f_tit.rowconfigure(0,weight = 1)
		f_tit.columnconfigure(0,weight = 1)
		
		l_1 = tk.Label(f_tit, anchor = tk.CENTER, text = titulo.get("texto", "TITULO"), bg = color, font = titulo.get("fuente", ("Fixedsys", 30)), fg = titulo.get("color_1", "#212121"))
			
		l_1.grid(row = 0, column = 0, sticky = "n")
		#l_2.grid(row = 0, column = 0, sticky = "n", padx = (0, 2), pady = (2, 0))
		return f_tit

	def agregar_contenido(self, maestro, contenido):
		color = maestro.cget("bg")
		f_contenido = tk.Frame(maestro, bg = color)
		f_contenido.rowconfigure(0,weight = 1)
		f_contenido.columnconfigure(0,weight = 1)
		txt = '''Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'''
		l_1 = tk.Label(f_contenido, 
					   wraplength = contenido.get("wraplenght",500), 
					   anchor = tk.CENTER, 
					   text   = contenido.get("texto", txt), bg = color, font =  contenido.get("fuente", ("Fixedsys", 16)), fg = contenido.get("color", "#212121"))
		l_1.grid(row = 0, column = 0, sticky = "n")
		return f_contenido
	
	def destruir(self,*args):
		self.destroy()
	
	def agregar_boton(self, maestro, boton):
		color = maestro.cget("bg")
		boton.update({"param":[True,self]})
		if not boton.get("accion",False):
			boton.update({"accion":self.protocoloCerrar})
		f_contenido = BtnRetro(maestro, boton)
		return f_contenido

class sendInfo(notificacionObligatoria):

	def agregar_paquetes(self, frame_1, contenido, boton):
		f_contenido = self.agregar_contenido(frame_1, contenido)
		f_contenido.grid(row = 1, rowspan = 1, column = 1, padx = self.px)

		f_contenido_2 = self.agregar_contenido(frame_1, contenido.get("contenido_2", {"texto": "", "color": "#AF0000","fuente" : ("Fixedsys", 12)}))
		f_contenido_2.grid(row = 2, rowspan = 1, column = 1, columnspan = 2, sticky = "nwe", padx = self.px, pady = (0, self.py//2))
		
		f_txt = self.agregarTexto(frame_1)
		f_txt.grid(row = 3, column = 1, columnspan = 2, padx = self.px + 10, pady = (0, self.py))

		f_boton = self.agregar_boton(frame_1, boton)
		f_boton.grid(row = 4, column = 1,padx = self.px + 10, pady = (0, self.py))

	def agregarTexto(self, maestro, *args):
			
			f_texto = tk.Frame(maestro, bg = maestro.cget("bg"))
			f_texto.rowconfigure(0, weight = 1)
			f_texto.columnconfigure(0, weight = 1)
			barra = tk.Scrollbar(f_texto)
			f_f_t = tk.LabelFrame(f_texto, relief = tk.FLAT, bd = 1, bg = "#A0A0A0")			
			texto_cita = tk.Text(f_f_t,
							 width  = 55,
							 height = 5, 
							 font   = ("Fixedsys", 14), 
							 padx   = 10,
							 pady   = 5,
							 wrap   = tk.WORD,
							 spacing1 = 5, 
							 spacing2 = 10, 
							 spacing3 = 10, 
							 tabs = 30, 
							 relief = tk.FLAT,
							 undo = 25,
							 autoseparators   = 20,
							 fg = "#1A1A1A",
							 selectbackground = "#FFFFFF",
							 yscrollcommand   = barra.set)
			color = f_f_t.cget("bg")
			f_f_t.bind("<Enter>", lambda e: e.widget.configure(bg = "#1F1F1F"))
			f_f_t.bind("<Leave>", lambda e: e.widget.configure(bg = "#A0A0A0"))
			texto_cita.grid(row = 0, column = 0, sticky = "nsew")		
			f_f_t.grid(row = 0, column = 0, sticky = "nsew")
			barra.grid(row = 0, column = 1, sticky = "ns")
			barra.config(command = texto_cita.yview )
			return f_texto

class preguntar(notificacionObligatoria): 
	
	def agregar_boton(self, maestro, boton):
		color = maestro.cget("bg")
		
		f_btnes = tk.Frame(maestro, bg = color)
		
		boton_2 = boton.get("boton_2", {})
		boton.update({"borde_2":2,"borde":2})
		boton.update({"param": [False,self]})
		boton_2.update({"borde_2":2,"borde":2})
		boton_2.update({"param": [True,self]})
		
		b_1 = BtnRetro(f_btnes, boton)
		b_2 = BtnRetro(f_btnes, boton_2)
		
		b_1.grid(row = 0, column = 0, padx = (3,20), pady = 2)
		b_2.grid(row = 0, column = 1, padx = (20,3), pady = 2)

		return f_btnes

	def agregarTexto(self, maestro, *args):
			
		f_texto = tk.Frame(maestro, bg = maestro.cget("bg"))
		f_texto.rowconfigure(0, weight = 1)
		f_texto.columnconfigure(0, weight = 1)
		barra = tk.Scrollbar(f_texto)
		f_f_t = tk.LabelFrame(f_texto, relief = tk.FLAT, bd = 1, bg = "#A0A0A0")			
		texto_cita = tk.Text(f_f_t,
						 width  = 55,
						 height = 5, 
						 font   = ("Fixedsys", 20), 
						 padx   = 10,
						 pady   = 5,
						 wrap   = tk.WORD,
						 spacing1 = 5, 
						 spacing2 = 10, 
						 spacing3 = 10, 
						 tabs = 30, 
						 relief = tk.FLAT,
						 undo = 25,
						 autoseparators   = 20,
						 fg = "#1A1A1A",
						 selectbackground = "#FFFFFF",
						 yscrollcommand   = barra.set)
		color = f_f_t.cget("bg")
		f_f_t.bind("<Enter>", lambda e: e.widget.configure(bg = "#1F1F1F"))
		f_f_t.bind("<Leave>", lambda e: e.widget.configure(bg = "#A0A0A0"))
		texto_cita.grid(row = 0, column = 0, sticky = "nsew")		
		f_f_t.grid(row = 0, column = 0, sticky = "nsew")
		barra.grid(row = 0, column = 1, sticky = "ns")
		barra.config(command = texto_cita.yview )
		return f_texto

class condiciones(notificacionObligatoria):

	def protocoloCerrar(self, *args):
		self.destroy()
		if self.accion_al_cierre:
			self.accion_al_cierre(False)
		
	def accion(self, *args):
		if self.var_condiciones.get():
			self.destroy()
			if self.accion_al_cierre:
				self.accion_al_cierre(True)
		else:
			self.ch_aceptar.set_falta_aceptar("red")

	def agregar_paquetes(self, frame_1, contenido, boton):
		
		f_contenido = self.agregar_contenido(frame_1, contenido)
		f_contenido.grid(row = 1, rowspan = 1, column = 0, columnspan = 4, padx = self.px)

		txt = '''Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'''
		self.contenido_txt = contenido.get("contenido_txt", txt)
		
		f_txt = self.agregarTexto(frame_1)
		f_txt.grid(row = 2, column = 1, columnspan = 2, padx = self.px + 10, pady = (self.py*2, 0))

		f_contenido_2 = self.agregar_contenido(frame_1, contenido.get("contenido_2", {"texto": "", "color": "#AF0000","fuente" : ("Fixedsys", 12)}))
		f_contenido_2.grid(row = 3, rowspan = 1, column = 1, columnspan = 2, sticky = "nwe", padx = self.px)

		self.var_condiciones = tk.BooleanVar()
		self.var_condiciones.set(False)
		self.ch_aceptar = BtnCheck(frame_1, 
							       contenido.get("texto_check", "Aceptar terminos y condiciones"), 
							       variable = self.var_condiciones)
		self.ch_aceptar.grid(row = 4, column = 0,columnspan = 4, padx = (self.px, self.px))
		
		boton["accion"] = self.accion
		boton["param"]  = [self,]
		
		self.f_boton = self.agregar_boton(frame_1, boton)
		self.f_boton.grid(row = 5, column = 0, columnspan = 4, padx = self.px, pady = self.py)

	def agregarTexto(self, maestro):
		
		f_texto = tk.Frame(maestro, bg = maestro.cget("bg"))
		f_texto.rowconfigure(0, weight = 1)
		f_texto.columnconfigure(0, weight = 1)
		barra = tk.Scrollbar(f_texto)
		f_f_t = tk.LabelFrame(f_texto, relief = tk.FLAT, bd = 1, bg = "#A0A0A0")			
		texto_cita = tk.Text(f_f_t,
						 width  = 62,
						 height = 6, 
						 font   = ("Fixedsys", 14), 
						 padx   = 10,
						 pady   = 5,
						 wrap   = tk.WORD,
						 spacing1 = 5, 
						 spacing2 = 10, 
						 spacing3 = 10, 
						 tabs = 30, 
						 relief = tk.FLAT,
						 undo = 25,
						 autoseparators   = 20,
						 fg = "#1A1A1A",
						 #highlightcolor="#4D4D4D",
						 selectbackground="#BED0FF",
						 yscrollcommand   = barra.set)
		texto_cita.insert(1.0, self.contenido_txt)
		color = f_f_t.cget("bg")
		#f_f_t.bind("<Enter>", lambda e: e.widget.configure(bg = "#1F1F1F"))
		#f_f_t.bind("<Leave>", lambda e: e.widget.configure(bg = "#A0A0A0"))
		texto_cita.grid(row = 0, column = 0, sticky = "nsew")		
		f_f_t.grid(row = 0, column = 0, sticky = "nsew")
		barra.grid(row = 0, column = 1, sticky = "ns")
		barra.config(command = texto_cita.yview )
		texto_cita.configure(state = "disabled")
		return f_texto
	
class lista_preguntas(notificacionObligatoria): 
	
	def agregar_boton(self, maestro, boton):
		color = maestro.cget("bg")
		
		f_btnes = tk.Frame(maestro, bg = color)
	
		r=0
		for btn in boton:
			boton[btn]["param"].append(self)
			b_1 = BtnRetro(f_btnes, boton[btn])
			b_1.grid(row = r, column = 0, padx = 10, pady = 3)
			r+=1

		return f_btnes

def centrar(root, ventana):
	"Centra el TopLevel en la pantalla"
	ventana.update_idletasks()
	ancho = ventana.winfo_width()
	alto  = ventana.winfo_height()
	tam_x = root.winfo_screenwidth()
	tam_y = root.winfo_screenheight()
	x     = (tam_x//2) - (ancho //2)
	y     = (tam_y//2) - (alto //2)
	ventana.geometry('{}x{}+{}+{}'.format(ancho, alto, x, y))





def warning(root,**kwargs):
	DISPLAY_NOTIFICACION = True
	DIRECTORIO = os.path.abspath(os.path.dirname(__file__))

	alto   = kwargs.get("alto",200)
	ancho  = kwargs.get("ancho",400)
	titulo = kwargs.get("titulo","titulo")
	
	rta_icono=kwargs.get("rta_ico",f'{DIRECTORIO}\\CODA\\Notificaciones\\iconos\\!_1.png')
	global ICONO
	ICONO = ImageTk.PhotoImage(Image.open(rta_icono))	
	
	frame_1 = {"bg": kwargs.get("fondo","#F8F82C")}
	btn_cerrar = {"activo":kwargs.get("btn_cerrar",1)}
	borde_color = kwargs.get("borde_color","#4D4D4D")
	boton = {"texto": kwargs.get("texto","TEXTO"), "accion":  kwargs.get("accion",False), "fuente": kwargs.get("fuente_btn",("Fixedsys", 16, "bold"))}
	marco = {"bg" : kwargs.get("bg_marco","#1A1A1A")}
	
	d_contenido = {"texto": kwargs.get("texto_contenido","Ipso Lore Cuthulu"), "fuente" : kwargs.get("fuente_contenido",("Small Fonts", 17))}

	o = notificacionObligatoria(root, 
								borde_color = borde_color, 
								frame_1 = frame_1,
								ancho = ancho,
								alto  = alto,
								icono = ICONO,
								btn_cerrar = btn_cerrar,
								contenido  = d_contenido,
								accion_al_cierre = kwargs.get("accion_al_cierre",print),
								boton  = boton,
								marco  = marco,
								titulo = {"texto": titulo})
	centrar(root, o) 
	o.attributes('-alpha', 1.0)


def pregunta(root,**kwargs):

	DISPLAY_NOTIFICACION = True
	DIRECTORIO = os.path.abspath(os.path.dirname(__file__))

	alto   = kwargs.get("alto",200)
	ancho  = kwargs.get("ancho",400)
	titulo = kwargs.get("titulo","titulo")
	
	if kwargs.get("ruta_icono",False):#=="warning":
		rta_icono   =  kwargs.get("ruta_icono")
	else:
		rta_icono   = f'{DIRECTORIO}\\CODA\\Notificaciones\\iconos\\preguntar.png'
	print(rta_icono)
	global ICONO
	ICONO = ImageTk.PhotoImage(Image.open(rta_icono))	

	frame_1 = {"bg": kwargs.get("fondo","#FFFFFF")}
	btn_cerrar  = {"resaltar_letra" : kwargs.get("resaltar_letra","#AFAFAF"), "normal_2": kwargs.get("normal_2","#A2A2A2"), "resaltar_2" :kwargs.get("resaltar_2","#4D4D4D")}
	borde_color = kwargs.get("borde_color","#717171")
	boton = kwargs.get("boton",{"texto": "NO", "normal_2" :"#A2A2A2", "resaltar_2" :"#4D4D4D", "boton_2": {"texto": "SI", "normal_2" :"#A2A2A2", "resaltar_2" :"#4D4D4D"}})
	marco = {"bg" : "#1A1A1A"}
	d_contenido = {"texto": kwargs.get("pregunta","¿PREGUNTAR?"), "fuente" : kwargs.get("fuente_pregunta",("Fixedsys", 16))}
	o = preguntar(root, 
				  borde_color = borde_color, 
				  frame_1 = frame_1,
				  ancho   = ancho,
				  alto    = alto,
				  icono   = ICONO,
				  btn_cerrar  = btn_cerrar,
				  contenido = d_contenido,
				  accion_al_cierre = kwargs.get("accion_al_cierre",print),
				  boton = boton,
				  marco = marco,
				  titulo = {"texto": titulo})
	centrar(root, o) 
	o.attributes('-alpha', 1.0)
	o.focus_set()
	return o

def opciones(root,**kwargs):

	DISPLAY_NOTIFICACION = True
	DIRECTORIO = os.path.abspath(os.path.dirname(__file__))

	alto   = kwargs.get("alto",250)
	ancho  = kwargs.get("ancho",400)
	titulo = kwargs.get("titulo","titulo")
	
	rta_icono   = f'{DIRECTORIO}\\CODA\\Notificaciones\\iconos\\preguntar.png'
	global ICONO
	ICONO = ImageTk.PhotoImage(Image.open(rta_icono))	

	frame_1 = {"bg": kwargs.get("fondo","#FFFFFF")}
	btn_cerrar  = {"resaltar_letra" : kwargs.get("resaltar_letra","#AFAFAF"), "normal_2": kwargs.get("normal_2","#A2A2A2"), "resaltar_2" :kwargs.get("resaltar_2","#4D4D4D")}
	borde_color = kwargs.get("borde_color","#717171")
	boton = {"boton" : {"texto": "ESTA ES LA PRIMERA OPC", "normal_2" :"#A2A2A2", "resaltar_2" :"#4D4D4D","label_height":1,  "accion":print,"param":[1,]},
			 "boton2": {"texto": "ESTA ES LA PRIMERA OPC 2", "normal_2" :"#A2A2A2", "resaltar_2" :"#4D4D4D","label_height":1,"accion":print,"param":[2,]},
			 "boton3": {"texto": "ESTA ES LA PRIMERA OPC 3", "normal_2" :"#A2A2A2", "resaltar_2" :"#4D4D4D","label_height":1,"accion":print,"param":[3,]}}
			 
	marco = {"bg" : "#1A1A1A"}
	d_contenido = {"texto": kwargs.get("pregunta","¿CUAL DE LAS OPCIONES QUERES?"), "fuente" : kwargs.get("fuente_pregunta",("Fixedsys", 16))}
	o = lista_preguntas(root, 
						borde_color = borde_color, 
						frame_1 = frame_1,
						ancho   = ancho,
						alto    = alto,
						icono   = ICONO,
						btn_cerrar  = btn_cerrar,
						contenido = d_contenido,
						accion_al_cierre = print,
						boton = boton,
						marco = marco,
						titulo = {"texto": titulo})
	centrar(root, o) 
	o.attributes('-alpha', 1.0)


def condicion(root,**kwargs):
	DISPLAY_NOTIFICACION = True
	DIRECTORIO = os.path.abspath(os.path.dirname(__file__))

	alto   = kwargs.get("alto",200)
	ancho  = kwargs.get("ancho",400)
	titulo = kwargs.get("titulo","titulo")
	
	rta_icono=kwargs.get("rta_ico",f'{DIRECTORIO}\\CODA\\Notificaciones\\iconos\\condiciones.png')
	global ICONO
	ICONO = ImageTk.PhotoImage(Image.open(rta_icono))	

	frame_1 = {"bg": kwargs.get("fondo","#9DCFFF")}
	btn_cerrar = {"resaltar_letra" :"#AFAFAF", "normal_2" :"#A2A2A2", "resaltar_2" :"#4D4D4D"}
	borde_color = "#717171"
	boton  = {"texto":  kwargs.get("texto_btn","ACEPTAR"), "normal_2" :"#A2A2A2", "resaltar_2" :"#4D4D4D"}
	marco  = {"bg" : "#1A1A1A"}
	d_contenido = {"texto": kwargs.get("texto_contenido","Estos son los terminos y condiciones "),"texto_check":"Aceptar Terminos y Condiciones",
					"contenido_txt":kwargs.get("contenido_txt","VACIO"), 
					"fuente" : kwargs.get("fuente_contenido",("Small Fonts", 17))}
	o = condiciones(root, 
				    borde_color = borde_color, 
				    frame_1 = frame_1,
				    ancho = ancho,
				    alto  = alto,
				    icono = ICONO,
				    btn_cerrar = btn_cerrar,
				    contenido  = d_contenido,
				    accion_al_cierre = kwargs["accion_al_cierre"],#.get("accion_al_cierre",print),
				    boton  = boton,
				    marco  = marco,
				    titulo = {"texto": titulo})
	centrar(root, o) 
	o.attributes('-alpha', 1.0)
	return o


def error(root,**kwargs):
	DISPLAY_NOTIFICACION = True
	DIRECTORIO = os.path.abspath(os.path.dirname(__file__))

	alto   = kwargs.get("alto",200)
	ancho  = kwargs.get("ancho",400)
	titulo = kwargs.get("titulo","titulo")
	
	rta_icono=kwargs.get("rta_ico",f'{DIRECTORIO}\\CODA\\Notificaciones\\iconos\\error.png')
	global ICONO
	ICONO = ImageTk.PhotoImage(Image.open(rta_icono))	

	frame_1 = {"bg": "#E49B9B"}
	btn_cerrar = {"resaltar_letra" :"#AFAFAF", "normal_2" :"#A2A2A2", "resaltar_2" :"#4D4D4D"}
	borde_color = "#A65555"
	boton = {"texto":"ACEPTAR","normal_2" :"#A2A2A2", "resaltar_2" :"#4D4D4D","accion":kwargs.get("accion_al_cierre",print),}
	marco = {"bg" : "#1A1A1A"}
	contenido = {"texto": kwargs.get("texto","EL CONTENIDO ESTA VACIO"), "fuente" : kwargs.get("fuente",("Fixedsys", 17)), "color" :kwargs.get("color","#FFFFFF")}

	o = notificacionObligatoria(root, 
								borde_color = borde_color, 
								frame_1 = frame_1,
								ancho = ancho,
								alto  = alto,
								icono = ICONO,
								btn_cerrar = btn_cerrar,
								contenido  = contenido,
								accion_al_cierre = kwargs.get("accion_al_cierre",print),
								boton  = boton,
								marco  = marco,
								titulo = {"texto": titulo})
	centrar(root, o) 
	o.attributes('-alpha', 1.0)


def info(root,**kwargs):
	DISPLAY_NOTIFICACION = True
	DIRECTORIO = os.path.abspath(os.path.dirname(__file__))

	alto   = kwargs.get("alto",200)
	ancho  = kwargs.get("ancho",400)
	titulo = kwargs.get("titulo","titulo")
	
	rta_icono=kwargs.get("rta_ico",f'{DIRECTORIO}\\CODA\\Notificaciones\\iconos\\info_1.png')
	global ICONO
	ICONO = ImageTk.PhotoImage(Image.open(rta_icono))	

	frame_1 = {"bg": "#ADD8E6"}
	btn_cerrar = {"resaltar_2" :"#638BB1"}
	borde_color = "#66A1B4"
	boton = {}
	marco = {"bg" : "#1A1A1A"}
	d_contenido = {"texto": "texto_contenido", "fuente" : ("Small Fonts", 17)}

	o = notificacionObligatoria(root, 
								borde_color = borde_color, 
								frame_1 = frame_1,
								ancho = ancho,
								alto  = alto,
								icono = ICONO,
								btn_cerrar = btn_cerrar,
								contenido  = d_contenido,
								accion_al_cierre = kwargs.get("accion_al_cierre",print),
								boton  = boton,
								marco  = marco,
								titulo = {"texto": titulo})
	centrar(root, o) 
	o.attributes('-alpha', 1.0)



def nuevo_record(root,**kwargs):
	DISPLAY_NOTIFICACION = True
	DIRECTORIO = os.path.abspath(os.path.dirname(__file__))

	alto   = kwargs.get("alto",200)
	ancho  = kwargs.get("ancho",400)
	titulo = kwargs.get("titulo","titulo")
	
	rta_icono=kwargs.get("rta_ico",f'{DIRECTORIO}\\CODA\\Notificaciones\\iconos\\copa.png')
	global ICONO
	ICONO = ImageTk.PhotoImage(Image.open(rta_icono))	

	frame_1 = {"bg": "gold"}
	btn_cerrar = {"resaltar_2" :"#638BB1"}
	borde_color = "#664200"
	boton = {"texto":"OKI DOKI","fuente" : ("Fixedsys", 17), "accion":kwargs.get("accion_al_cierre",False)}
	marco = {"bg" : "#1A1A1A"}
	d_contenido = {"texto": kwargs.get("texto_contenido"), "fuente" : ("Small Fonts", 17)}

	o = notificacionObligatoria(root, 
								borde_color = borde_color, 
								frame_1 = frame_1,
								ancho = ancho,
								alto  = alto,
								icono = ICONO,
								btn_cerrar = btn_cerrar,
								contenido  = d_contenido,
								accion_al_cierre = kwargs.get("accion_al_cierre",print),
								boton  = boton,
								marco  = marco,
								titulo = {"texto": titulo})
	centrar(root, o) 
	o.attributes('-alpha', 1.0)


def consejo(root,**kwargs):
	DISPLAY_NOTIFICACION = True
	DIRECTORIO = os.path.abspath(os.path.dirname(__file__))

	alto   = kwargs.get("alto",200)
	ancho  = kwargs.get("ancho",400)
	titulo = kwargs.get("titulo","titulo")
	
	rta_icono=kwargs.get("rta_ico",f'{DIRECTORIO}\\CODA\\Notificaciones\\iconos\\consejo_1.png')
	global ICONO
	ICONO = ImageTk.PhotoImage(Image.open(rta_icono))	
	
	frame_1 = {"bg": "#FFFFFF"}
	btn_cerrar = {"resaltar_letra" :"#AFAFAF", "normal_2" :"#A2A2A2", "resaltar_2" :"#4D4D4D"}
	borde_color = "#717171"
	boton = {"normal_2" :"#A2A2A2", "resaltar_2" :"#4D4D4D"}
	marco = {"bg" : "#1A1A1A"}
	d_contenido = {"texto": "texto_contenido", "fuente" : ("Small Fonts", 17)}

	o = notificacionObligatoria(root, 
								borde_color = borde_color, 
								frame_1 = frame_1,
								ancho = ancho,
								alto  = alto,
								icono = ICONO,
								btn_cerrar = btn_cerrar,
								contenido  = d_contenido,
								accion_al_cierre = kwargs.get("accion_al_cierre",print),
								boton  = boton,
								marco  = marco,
								titulo = {"texto": titulo})
	centrar(root, o) 
	o.attributes('-alpha', 1.0)


def mensajear(root,**kwargs):
	DISPLAY_NOTIFICACION = True
	DIRECTORIO = os.path.abspath(os.path.dirname(__file__))

	alto   = kwargs.get("alto",200)
	ancho  = kwargs.get("ancho",400)
	titulo = kwargs.get("titulo","titulo")
	
	rta_icono=kwargs.get("rta_ico",f'{DIRECTORIO}\\CODA\\Notificaciones\\iconos\\informar_error.png')
	global ICONO
	ICONO = ImageTk.PhotoImage(Image.open(rta_icono))	

	frame_1 = {"bg": "#FFFFFF"}
	btn_cerrar = {"resaltar_letra" :"#AFAFAF", "normal_2" :"#A2A2A2", "resaltar_2" :"#4D4D4D"}
	borde_color = "#717171"
	boton = {"texto": "ENVIAR", "normal_2" :"#A2A2A2", "resaltar_2" :"#4D4D4D"}
	marco  = {"bg" : "#1A1A1A"}
	d_contenido = {"texto": "Envianos un mensaje ! 20% seguro que lo recibimos...", "fuente" : ("Fixedsys", 16), "contenido_2": {"texto": "Al enviar el mensaje se adjunta la bitacora con los errores recolectados por el programa.", "color": "#AF0000","fuente" : ("Fixedsys", 12)}}
	o = sendInfo(root, 
				borde_color = borde_color, 
				frame_1 = frame_1,
				ancho = ancho,
				alto  = alto,
				icono   = ICONO,
				btn_cerrar  = btn_cerrar,
				contenido = d_contenido,
				accion_al_cierre = print,
				boton = boton,
				marco = marco,
				titulo = {"texto": titulo})
	centrar(root, o) 
	o.attributes('-alpha', 1.0)


def aceptar_terminos(acepto):
	print("-->>",acepto)
	if acepto:
		print(".........................")
		CajonDeVariablesGrales.FUNC_MINIZAR(False)
		CajonDeVariablesGrales.FUNC_DESACTIVAR()
		DIRECTORIO = os.path.abspath(os.path.dirname(__file__))
		ruta_base =  DIRECTORIO+ "\\CODA\\Notificaciones\\"
		ruta= "config_inicial"
		with open(ruta_base+ruta, "r", encoding="utf-8") as archivo:
			config=json.load(archivo)
			config["acepta_terminos_y_condiciones"]=True
		with open(ruta_base+ruta, "w", encoding="utf-8") as archivo:
			nuevo=json.dumps(config)
			archivo.write(nuevo)
		print("Se aceptaron los terminos y condiciones")
	else:
		CajonDeVariablesGrales.root.destroy()
		

def display_condiciones(root):
	DIRECTORIO = os.path.abspath(os.path.dirname(__file__))
	ruta_base =  DIRECTORIO+ "\\CODA\\Notificaciones\\"
	ruta= "config_inicial"
	with open(ruta_base+ruta, "r", encoding="utf-8") as archivo:
		archivo=json.load(archivo)
	aceptacion = archivo["acepta_terminos_y_condiciones"]		
	print("ACEPTACION = ", aceptacion)
	if not aceptacion:
		CajonDeVariablesGrales.FUNC_MINIZAR(True)
		CajonDeVariablesGrales.FUNC_DESACTIVAR()
		DIRECTORIO = os.path.abspath(os.path.dirname(__file__))
		ruta= DIRECTORIO+ "\\CODA\\_terminos_y_condiciones.txt"
		with open(ruta, "r", encoding="utf-8") as archivo:
			terminos_y_condiciones=archivo.read()		
		condicion(root,contenido_txt=terminos_y_condiciones,accion_al_cierre=aceptar_terminos)	

def chequearPrimeraVez(root):
	display_condiciones(root)
	return True


if __name__ == "__main__":

	#marco = {"bg" : "#1A1A1A"}
	def a(*args):
		print("..............",args)
	root = tk.Tk()
	var = tk.BooleanVar()
	btn=tk.Button(root,)
	boton = {"fuente":("Fixedsys", 20),"accion":a,"texto": "NO", "normal_2" :"#A2A2A2", "resaltar_2" :"#4D4D4D", "boton_2": {"texto": "SI", "normal_2" :"#A2A2A2", "resaltar_2" :"#4D4D4D"}}
	#nuevo_record(root, pregunta="¿QUERES BORRAR TODO?", titulo="BORRAR", boton= boton)
	#BtnCheck(root, "Aceptar condiciones", 
	#		 variable = var).grid(row =0, column = 0)
	#BtnCheck(root, "DOS", variable = var, onvalue = "DOS", offvalue = "NOP_DOS").grid(row =1, column = 0)
	def p():
		print("aaaaaaaaaaaaaaaaaaaaaaaaaa")

	r= 5
	d= 1
	n= 1

	old_r=2
	old_d=2
	old_n=2
	
	bandera = False
	new_record = ""
	if r>old_r:
		new_record+=f"\n♡ RECOMPENSA MAXIMA: {r} ♡\n"
		bandera = True
	if d>old_d:
		new_record+=f"\n♡ ENEMIGOS DERROTADOS: {d} ♡\n"
		bandera = True
	if n>old_n:
		new_record+=f"\n♡ NIVEL ALCANZADO: {n} ♡\n"
		bandera = True
		
	if bandera:
		nuevo_record(root, titulo="¡NUEVO RECORD!", texto_contenido = new_record,accion_al_cierre=p)
			
	root.mainloop()
		#chequearNotificaciones()
	#
	#from tkinter import *
	#from tkinter import font
	#
	#root = Tk()
	#root.title('Font Families')
	#fonts=list(font.families())
	#fonts.sort()
	#
	#def populate(frame):
	#	'''Put in the fonts'''
	#	listnumber = 1
	#	for item in fonts:
	#		label = "listlabel" + str(listnumber)
	#		label = Label(frame,text=item + "  " + "✔, ✓",font=(item, 12)).pack()
	#		listnumber += 1
	#
	#def onFrameConfigure(canvas):
	#	'''Reset the scroll region to encompass the inner frame'''
	#	canvas.configure(scrollregion=canvas.bbox("all"))
	#
	#canvas = Canvas(root, borderwidth=0, background="#ffffff")
	#frame = Frame(canvas, background="#ffffff")
	#vsb = Scrollbar(root, orient="vertical", command=canvas.yview)
	#canvas.configure(yscrollcommand=vsb.set)
	#
	#vsb.pack(side="right", fill="y")
	#canvas.pack(side="left", fill="both", expand=True)
	#canvas.create_window((4,4), window=frame, anchor="nw")
	#
	#frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))
	#
	#populate(frame)
	#
	#root.mainloop()
	
	"Century Gothic"
	"Fixedsys"
	"Segoe UI Semibold"
	"Segoe UI Light"
	"Small Fonts"
	"Yu Gothic Medium"
