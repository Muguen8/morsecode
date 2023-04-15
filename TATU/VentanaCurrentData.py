# Ventana Current Data
import tkinter as tk
from tkinter import ttk
import PIL
from PIL import Image, ImageTk
import threading
import serial
import random
import buscandoPort
import FrameGif
import os
import Notificaciones
import CajonGeneral
#import winsound
from ScrollFrame import ScrollableFrame
import time
from winsound import *
import json


class ventanaDataActual(tk.Frame):
	
	def __init__(self, maestro, **kwargs):
		super().__init__(maestro, **kwargs)

		self.maestro = maestro
		self.maestro.protocol("WM_DELETE_WINDOW", self.protocolo_cerrar_ventana)
		self.FONDO   = kwargs.get("bg", "#222323")
		self.FONDO_1 = "#fe6c90"#kwargs.get("bg", "#FFFFFF")
		self.FONDO_2 = "#EFEFEF"#kwargs.get("bg", "#FFFFFF")
		self.traerIconos()

		self.CONTRASEÑA_TATU = ["tatu","tapita"]
		self.CONTRASEÑA_MILO = ["milo","pochoclo"]

		self.hilo_activo    = False
		self.estado_conn    = False
		self.sv_estado_conn = tk.StringVar()
		self.sv_estado_conn.set("■")
		self.puerto_sel 	= tk.StringVar()
		self.puerto_sel.set("Buscar puerto")
		
		self.directorio = os.path.abspath(os.path.dirname(__file__))	
		self.ruta_base = f'{self.directorio}/iconos/GIF/'
		self.lista_gif = os.listdir(self.ruta_base)
		
		self.poblarVentana()
		

	def traerIconos(self):
		"Cargamos los ico que vamos a utilizar en el menu"
		#global ARDUINO_CONN_OK
		#global MICRO_B
		#global MICRO_R
		#global MICRO_V
		global TOP_SECRET
		global ESPIA_H
		global ESPIA_M
		global ESPIA_M_P

	
		#ARDUINO_CONN_OK = ImageTk.PhotoImage(Image.open('iconos\\app_icon.png'))	
		TOP_SECRET = ImageTk.PhotoImage(Image.open('iconos\\top_secret_2.png'))	
		ESPIA_M = ImageTk.PhotoImage(Image.open('iconos\\espia.png'))	
		ESPIA_M_P = ImageTk.PhotoImage(Image.open('iconos\\espia_p.png'))	
		ESPIA_H = ImageTk.PhotoImage(Image.open('iconos\\espia_h.png'))	
		#MICRO_B = ImageTk.PhotoImage(Image.open('iconos\\micro_black.png'))
		#MICRO_V = ImageTk.PhotoImage(Image.open('iconos\\micro_conectado.png'))
		#MICRO_R = ImageTk.PhotoImage(Image.open('iconos\\micro_desconectado.png'))


	def frameValorActual(self, padre):
		f_val_actual = tk.Frame(padre, bg = "#FFFFFF")
		return f_val_actual
	

	def frameEstadoConn(self, padre):
				
		f_a = tk.Frame(padre, bg = "#FFB6FB", relief=tk.FLAT,padx=2,pady=2)
		f_estado_conn = tk.Frame(f_a, bg = self.FONDO_1, relief=tk.FLAT)

		self.display_estado_conn = tk.Label(f_estado_conn, 
											textvariable = self.sv_estado_conn, 
											font = ("Fixedsys", 20),
											fg   = "#7E2222",
											bg   = self.FONDO_1)
		self.display_estado_conn.grid(row 	= 0, 
								      column = 1, 
								      padx   = 5, 
								      pady   = 10)

		
		valores = ["Buscar puerto",] + [n.device for n in buscandoPort.lista_puertos()]
		
		self.cb_puerto = ttk.Combobox(f_estado_conn, 
									  #justify     = tk.CENTER,
									  width   	   = 15,
									  #relief 	   = tk.FLAT,
									  textvariable = self.puerto_sel,
									  values       = valores,
									  state        = "readonly",
									  font = ("Fixedsys", 20),)

		self.cb_puerto.grid(row 	= 0, 
							 column = 3, 
							 padx   = (0, 10), 
							 pady   = 10)
		
		self.cb_puerto.bind("<<ComboboxSelected>>", lambda x: self.focus_set())

		self.ico_arduino = tk.Button(f_estado_conn, 
									 image    = MICRO_B,
									 text     = "ABIR CONN.  ",
									 compound = tk.LEFT,
									 cursor  = "hand2",
									 bg      = self.FONDO_1,
									 font    = ("Fixedsys", 20),
									 relief  = tk.FLAT,
									 command = self.abrirConexion)
		self.ico_arduino.grid(row 	= 0, 
						 column = 4, 
						 sticky = "nw", 
						 padx   = (0,10), 
						 pady   = 10)
						 
		self.ico_arduino.bind("<Enter>", lambda x: x.widget.configure(bg = "#FFD2EF"))
		self.ico_arduino.bind("<Leave>", lambda x: x.widget.configure(bg = self.FONDO_1))
			
		f_estado_conn.pack(expand=True,fill=tk.BOTH)
		
		return f_a


	def desplegar_frame(self,boton_secreto,f_estado_conn):
		if boton_secreto.estado:
			cerrar=boton_secreto
			abrir=f_estado_conn
			self.cb_puerto.focus_set()
		else:
			cerrar=f_estado_conn
			abrir=boton_secreto
		
		cerrar.grid_forget()
		abrir.grid(row = 0, 
					column = 0, 
					sticky = "nw", 
					padx = 20, 
					pady = (40, 30))
					
		boton_secreto.estado=not boton_secreto.estado


	def plegar_frame(self,f_estado_conn):
		f_estado_conn.grid_forget()

	
	def poblarVentana(self):
		
		f_contenedor = self
		
		self.rowconfigure(0, weight = 0)
		self.rowconfigure(1, weight = 1)
		self.columnconfigure(0, weight = 1)
		self.columnconfigure(1, weight = 0)

		self.f_panel = tk.Frame(f_contenedor,bg=self.FONDO)
		self.f_gif = self.panel_gif(self.f_panel)

		f_estado_conn = self.frameContrasenia(f_contenedor)
		
		boton_secreto = tk.Button(f_contenedor, 
								  cursor="hand2", 
								  bg=self.FONDO,
								  text=".- -... .-. .. .-.",
								  image=  ESPIA_M,
					              compound=tk.LEFT, 
								  font=("Fixedsys", 20),
								  relief=tk.FLAT,fg="#FFFFFF",
								  command = lambda:self.desplegar_frame(boton_secreto,f_estado_conn))
		boton_secreto.estado = True
		boton_secreto.bind("<Enter>",lambda e: e.widget.config(fg="#FFC0CB",image=ESPIA_M_P))
		boton_secreto.bind("<Leave>",lambda e: e.widget.config(fg="#FFFFFF",image=ESPIA_M))
		boton_secreto.grid(row = 0, 
						   column = 0, 
						   sticky = "nw", 
						   padx = 5, 
						   pady = (20, 10))
		
		self.f_tit = self.frameTitulo(f_contenedor)
		
		ts= tk.Label(self.f_panel, 
					 image   = TOP_SECRET,
					 bg      = self.FONDO,)
		
						  
		ts.grid(row = 0, 
				column = 0, 
				sticky = "n",
				pady   = (3, 20))

		self.f_tit.grid(row = 0, 
						column = 1, 
						sticky = "n",
						padx = 5, 
						pady = (30,0))

		self.f_gif.grid(row = 1, 
						column = 0, 
						sticky = "n",
						pady   = 45)

		self.f_panel.grid(row = 1, 
						  column = 0, 
						  columnspan = 2, 
						  sticky = "n",
						  padx = 5, 
						  pady = (20, 0))

	def frameContrasenia(self,padre):
		
		f_a = tk.Frame(padre, bg = "#FB748C", relief=tk.FLAT,padx=2,pady=2)
		f_estado_conn = tk.Frame(f_a, bg = self.FONDO_2, relief=tk.FLAT)


		label_puertp = tk.Label(f_estado_conn, 
								text = "CONTRASEÑA ", 
								font = ("Fixedsys", 20),
								bg   = self.FONDO_2,
								anchor = "e")
		label_puertp.grid(row 	= 0, 
						  column = 2, 
						  pady   = 5)
		v_contrasenia=tk.StringVar()
		def to_upper():
			pass
		v_contrasenia.trace_add('write', lambda *args:v_contrasenia.set(v_contrasenia.get().upper()))
		
		self.cb_puerto = ttk.Entry(f_estado_conn, 
								  justify     = tk.CENTER,
								  textvariable = v_contrasenia,
								  #values       = valores,
								  #state        = "readonly",
								  font = ("Fixedsys", 20),)

		self.cb_puerto.grid(row 	= 0, 
							 column = 3, 
							 padx   = (0, 10), 
							 pady   = 5)
		self.cb_puerto.bind("<Return>", lambda evento:self.probar_contrasenia(v_contrasenia.get().strip().lower()))
		
		ico_arduino = tk.Button(f_estado_conn, 
									 #image    = MICRO_B,
									 text     = "ENTRAR",
									 #compound = tk.LEFT,
									 cursor  = "hand2",
									 bg      = self.FONDO_2,
									 font    = ("Fixedsys", 20),
									 relief  = tk.FLAT,
									 command = lambda :self.probar_contrasenia(v_contrasenia.get().strip().lower()))
		ico_arduino.grid(row 	= 0, 
						 column = 4, 
						 sticky = "nw", 
						 padx   = (0,10), 
						 pady   = 5)
						 
		ico_arduino.bind("<Enter>", lambda x: x.widget.configure(bg = "#FA95A7"))
		ico_arduino.bind("<Leave>", lambda x: x.widget.configure(bg = self.FONDO_2))
			
		f_estado_conn.pack(expand=True,fill=tk.BOTH)
		
		return f_a


	def probar_contrasenia(self, contrasenia):
		if contrasenia == "admin":
			CajonGeneral.FUNC_CAMBIAR_VENTANA("administrador")			
		if contrasenia in CajonGeneral.DATA_CONFIG.keys():
			CajonGeneral.USUARIO = contrasenia
			CajonGeneral.FUNC_CAMBIAR_VENTANA("panel_principal")
		else:
			self.impostor() 


	def impostor(self):
		pass


	def terminar_gif(self):
		for n in self.gif_activos:
			n.bandera=True
			n.destroy()
	
	
	def panel_gif(self,maestro):
		
		self.gif_activos=[]
		f_gif = tk.Frame(maestro, bg = self.FONDO)

		c_max = 2
		r_max = 1
		c=0
		r=0
		lista_copia =random.sample(self.lista_gif[0:],len(self.lista_gif))

		paleta = random.sample(CajonGeneral.paleta_neon,len(CajonGeneral.paleta_neon))
		for n in range(0,c_max+1*r_max+1):
			try:
				rta=lista_copia.pop()
			except IndexError:
				lista_copia =random.sample(self.lista_gif[0:],len(self.lista_gif))
				rta=lista_copia.pop()
			
			f = tk.Frame(f_gif, bg = paleta.pop(),pady=2)
			g=self.frameGif(f,self.ruta_base +"/"+ rta)
			g.pack()
			self.gif_activos.append(f)
			f.grid(column=c,row=r, padx=35)
			if c==c_max:
				c=0
				r+=1
			else:
				c+=1
			if r==r_max:
				break
		return f_gif


	def frameGif(self,padre,ruta, intervalo = 48):
		#r = random.choice(self.lista_gif)
		#r = self.ruta_base +"/"+ r
		o = FrameGif.gif1(padre, ruta = ruta, intervalo = intervalo) #resize=(400,400)	
		o.arrancar()
		
		return o
		

	def frameTitulo(self,padre):
		f_titulo = tk.Frame(padre, bg = self.FONDO)
		T = tk.Label(f_titulo, 
					 text = "PROGRAMA ESPECIAL DE ESPIAS", 
					 #image=  ESPIA_H,
					 #compound=tk.RIGHT,
					 font = ("Fixedsys", 20),
					 fg   = "#F5F5F5",
					 bg   = self.FONDO)
		T.grid(row 	= 0, 
			     column = 1, 
			     padx   = 20, 
			     pady   = (30,10),
			     sticky="ne")
		
		return f_titulo
		

	def abrirConexion(self):
		#self.terminar_gif()
		#self.f_gif.destroy()
		#return 
		if self.estado_conn:
			self.cerrar_hilo()
			self.cerrar_conn()
		else:
			p_sel = self.puerto_sel.get() 
			if p_sel == "Buscar puerto":
				puerto = buscandoPort.buscar()
				self.conn_arduino = buscandoPort.conectar(puerto)
			else:
				conn_arduino = buscandoPort.conectar(p_sel)
				if conn_arduino:
					puerto = p_sel
					self.conn_arduino = conn_arduino
				else:
					#Notificaciones.error(self.maestro.winfo_toplevel(), contenido="Una vez analizado, el texto de la norma no puede modificarse. ¿Estas seguro de continuar?", titulo="¿Analizar?")
					self.conn_arduino = False
					return
			bandera = buscandoPort.enviar_handshake(self.conn_arduino)
			if bandera:
				print("CONEXION ESTABLECIDA : ", self.conn_arduino)
				self.estado_conn = True
				self.displayEstadoConn(puerto)
				CajonGeneral.CONN_ARDUINO = self.conn_arduino
				self.leer_data_entrante()
				#self.inicializar_animacion()
				#self.abrir_hilo()
			else:
				CajonGeneral.CONN_ARDUINO = False
				self.conn_arduino = False
				self.estado_conn = False
				Notificaciones.error(self.maestro.winfo_toplevel(), texto="NO PUDIMOS CONECTARNOS A LA MAQUINA MORSE. ¿ESTAS SEGURA QUE ESTA CONECTADA? (TIENE QUE ESTAR PRENDIDA LA LUZ)", titulo="UPS..HUBO UN PROBLEMA")

	
	def leer_data_entrante(self):
		if not CajonGeneral.HILO_LECTURA: # = True
			CajonGeneral.HILO_LECTURA = True
			CajonGeneral.RECOLECTAR_DATA = True
			CajonGeneral.BUFFER = """"""
			self.t1 = threading.Thread(target = buscandoPort.recolectar_data_entrante)
			self.t1.deamon=True
			self.t1.start()	
	
	def inicializar_animacion(self):
		for objeto_graf in self.lista_o_graf:
			objeto_graf.inicializar_animacion()


	def abrir_hilo(self):
		self.hilo_activo = True		
		self.t1 = threading.Thread(target = self.readCurrentData)
		self.t1.deamon=True
		self.t1.start()


	def displayEstadoConn(self, puerto = None):
		if self.estado_conn:
			self.puerto_sel.set(puerto)
			self.ico_arduino.configure(image = MICRO_V)
			self.ico_arduino.configure(text  = "DESCONECTAR")
			self.sv_estado_conn.set("■")
			self.display_estado_conn.config(fg = "#399439")
			self.cb_puerto.configure(state = "disabled")
		else:
			self.ico_arduino.configure(image = MICRO_R)
			self.ico_arduino.configure(text  = "CONECTAR ")
			self.sv_estado_conn.set("■")
			self.display_estado_conn.config(fg = "#DD2E2E")
			self.cb_puerto.configure(state = "readonly")


	def cerrar_hilo(self,):
		#self.cerrarAnimacion()
		if self.hilo_activo:
			print('Cerrar hilo')
			self.hilo_activo = False
			print('Wait until Thread is terminating')
			self.t1.join()
			print("EXIT")


	def cerrar_conn(self):
		if self.estado_conn:
			buscandoPort.cerrar_conn(self.conn_arduino)#self.conn_arduino.close()
			self.estado_conn  = False
			self.displayEstadoConn()
			print("CONN CERRADA")


	def protocolo_cerrar_ventana(self):
		self.terminar_gif()
		if self.estado_conn:
			self.cerrar_conn()
		self.cerrar_hilo()
		self.maestro.destroy()
	



class panelPrincipal(ventanaDataActual):

	def traerIconos(self):
		"Cargamos los ico que vamos a utilizar en el menu"
		global ARDUINO_CONN_OK
		global MICRO_B
		global MICRO_R
		global MICRO_V
		global MORSE
		global AGENDA
		global JUEGO
		global CUENTO
		
		global COFRE_0
		global NIVEL_0
		global ZOMBI_0
		global RUBIES_0
		
		global REFRESH
				
		ARDUINO_CONN_OK = ImageTk.PhotoImage(Image.open('iconos\\app_icon.png'))	
		CUENTO   = ImageTk.PhotoImage(Image.open('iconos\\cuento.png'))
		MORSE   = ImageTk.PhotoImage(Image.open('iconos\\morse.png'))
		AGENDA   = ImageTk.PhotoImage(Image.open('iconos\\agenda.png'))
		
		MICRO_B = ImageTk.PhotoImage(Image.open('iconos\\micro_black.png'))
		MICRO_V = ImageTk.PhotoImage(Image.open('iconos\\micro_conectado.png'))
		MICRO_R = ImageTk.PhotoImage(Image.open('iconos\\micro_desconectado.png'))
		JUEGO = ImageTk.PhotoImage(Image.open('iconos\\juego.png'))	

		COFRE_0 = ImageTk.PhotoImage(Image.open('iconos\\cofre.png'))	
		NIVEL_0 = ImageTk.PhotoImage(Image.open('iconos\\medalla.png'))	
		ZOMBI_0 = ImageTk.PhotoImage(Image.open('iconos\\zombi.png'))
		RUBIES_0 = ImageTk.PhotoImage(Image.open('iconos\\rubi_chico.png'))

		REFRESH = ImageTk.PhotoImage(Image.open('iconos\\refresh.png'))
		
		
	def poblarVentana(self):
		
		clave = CajonGeneral.USUARIO
		f_contenedor =  tk.Frame(self, bg =self.FONDO,padx=2,pady=2)
		self.gif_activos = [] 
		
		
		self.rowconfigure(0, weight = 0)
		self.rowconfigure(1, weight = 0)
		#self.rowconfigure(2, weight = 0)
		self.columnconfigure(0, weight = 0)
		self.columnconfigure(1, weight = 0)
		#self.columnconfigure(2, weight = 0)

		msj = f"BIENVENIDA AGENTE: {CajonGeneral.USUARIO.upper()}"
			
		self.AMARILLO = "#F8F859"
		tit_bienvenida = tk.Label(f_contenedor, 
								  bg=self.FONDO,
								  text=msj,
								  font=("Fixedsys", 28),
								  relief=tk.FLAT,
								  fg=self.AMARILLO,)
		#boton_secreto.bind("<Enter>",lambda e: e.widget.config(fg="#B55AFC"))
		#boton_secreto.bind("<Leave>",lambda e: e.widget.config(fg="#FFFFFF"))
		tit_bienvenida.grid(row = 0, 
						   column = 0, 
						   sticky = "nw",  columnspan=2, 
						   padx = 5, 
						   pady = (20, 0))
		
		f_info = self.panel_info_agente(f_contenedor, clave=clave)
		f_info.grid(row = 1, 
				    column = 0, 
				    sticky = "n",
				    columnspan=2, 
				    padx = 5, 
				    pady = (20, 0))


		f_estado_conn = self.frameEstadoConn(f_contenedor)
		f_estado_conn.grid(row = 2, 
						   column = 0, 
						   sticky = "nw", 
						   padx = 5, 
						   pady = (20,0))
		
		f_menu = self.panel_menu_botones(f_contenedor)
		f_menu.grid(row = 3, 
				    column = 0, 
				    sticky = "nw", 
				    padx = 5, 
				    pady = (0,10))
	
		f_retrato = self.panel_retrato(f_contenedor, clave=clave)
		f_retrato.grid(row = 2, 
					  column = 1, 
					  sticky = "ne", 
					  rowspan=2,
					  padx = 5, 
					  pady = (20,5))

		f_score = self.panel_score(f_contenedor, clave=clave)
		f_score.grid(row = 4, 
					 column = 0,
					 columnspan=2, 
					 sticky = "n", 
					 rowspan=2,
					 padx = 5, 
					 pady = (15,20))
		
		
		f_contenedor.pack(anchor="n")
		
		
	def panel_info_agente(self,padre,clave):
		BORDE=self.AMARILLO
		f_panel = tk.Frame(padre, bg =BORDE,padx=2,pady=2)
		f_contenedor = tk.Frame(f_panel, bg = self.FONDO)
		self.info=CajonGeneral.DATA_CONFIG[clave]["info_usuario"]
		
		f_info=tk.Frame(f_contenedor, bg = self.FONDO)
		c=0
		r=0
		c_max=2
		ancho = 15 #max(self.info[clave],key=lambda x: len(x))
		for n in self.info:
			f=tk.Frame(f_info, bg = self.FONDO)
			tk.Label(f,text=n.upper() + " : ",anchor="e", width=ancho,bg = self.FONDO,font=("Fixedsys", 20),fg="#f0f6f0").pack(side=tk.LEFT, padx=(5,0),anchor="w")
			tk.Label(f,text=self.info[n].upper(),bg = self.FONDO,font=("Fixedsys", 17),fg="#f0f6f0").pack(side=tk.LEFT, padx=(0,15))
			f.grid(row=r,column=c,sticky="nw")
			c+=1
			if c==c_max:
				r+=1
				c=0
		f_info.pack(side=tk.LEFT,anchor="w")		
		f_contenedor.pack(anchor="nw")
		return f_panel


	def panel_retrato(self,padre,clave):
		BORDE="#F8F859"
		f_panel = tk.Frame(padre, bg =BORDE,padx=2,pady=2)
		f_contenedor = tk.Frame(f_panel, bg = self.FONDO,pady=6)
		
		#self.info={"tatu":"/misc_1/","milo":"/misc_1/"}
		rta = CajonGeneral.DATA_CONFIG[clave]["retrato"]
		if rta:
			rta = self.directorio +"/perfil/"+ rta
		else:
			rta = self.directorio +"/perfil/"+"/misc_1/"
		if rta[-1]=="/":
			f=self.frameGif(f_contenedor,rta, intervalo=200)
			self.gif_activos.append(f)
		else:
			self.PERFIL = ImageTk.PhotoImage(Image.open(rta))
			f=tk.Label(f_contenedor, 
					 bg=self.FONDO,
					 image = self.PERFIL)
									
		f.pack(side=tk.LEFT,anchor="nw")		
		f_contenedor.pack(anchor="nw")
		return f_panel

	def panel_score(self,padre, clave):
		BORDE=self.FONDO
		f_panel = tk.Frame(padre, bg =BORDE,padx=2,pady=2)
		f_contenedor = tk.Frame(f_panel, bg = self.FONDO)
				
		self.v_recompensa = tk.IntVar()
		self.v_derrotados = tk.IntVar()
		self.v_nivel      = tk.IntVar()
		self.v_rubies     = tk.IntVar()

		CajonGeneral.SCORE_recompensa =self.v_recompensa
		CajonGeneral.SCORE_derrotados =self.v_derrotados
		CajonGeneral.SCORE_nivel      =self.v_nivel
		CajonGeneral.SCORE_rubies     =self.v_rubies
		
		recompensa = CajonGeneral.DATA_CONFIG[clave]["score"].get("recompensa",0)
		derrotados = CajonGeneral.DATA_CONFIG[clave]["score"].get("derrotados",0)
		nivel = CajonGeneral.DATA_CONFIG[clave]["score"].get("nivel",1)
		rubies = CajonGeneral.DATA_CONFIG[clave]["score"].get("rubies",0)

		self.v_recompensa.set(recompensa)
		self.v_derrotados.set(derrotados)
		self.v_nivel.set(nivel)
		self.v_rubies.set(rubies)

		score_rank = tk.Label(f_contenedor, 
									bg=self.FONDO,
									#image = COFRE_0,
									padx = 20,
									#compound=tk.LEFT,
									text="LOGROS MAXIMOS",
									font=("Fixedsys", 20, "underline"),
									relief=tk.FLAT,
									fg="#FC8DC0",)
		TAMAÑO_SCORE= 20
		score_recompensa = tk.Label(f_contenedor, 
							  bg=self.FONDO,
							  image = COFRE_0,
							  padx = 20,
							  compound=tk.LEFT,
							  textvariable=self.v_recompensa,
							  font=("Fixedsys", TAMAÑO_SCORE),
							  relief=tk.FLAT,
							  fg="gold",)

		score_recompensa = tk.Label(f_contenedor, 
							  bg=self.FONDO,
							  image = COFRE_0,
							  padx = 20,
							  compound=tk.LEFT,
							  textvariable=self.v_recompensa,
							  font=("Fixedsys", TAMAÑO_SCORE),
							  relief=tk.FLAT,
							  fg="gold",)
		score_derrotados= tk.Label(f_contenedor, 
							  bg=self.FONDO,
							  image = ZOMBI_0,
							  padx = 20,
							  compound=tk.LEFT,
							  textvariable=self.v_derrotados,
							  font=("Fixedsys", TAMAÑO_SCORE),
							  relief=tk.FLAT,
							  fg="#9CC99C",)							  
		score_nivel= tk.Label(f_contenedor, 
							  bg=self.FONDO,
							  image = NIVEL_0,
							  padx = 20,
							  compound=tk.LEFT,
							  textvariable=self.v_nivel,
							  font=("Fixedsys", 30),
							  relief=tk.FLAT,
							  fg="#A7CCD8",)

		score_rubies= tk.Label(f_contenedor, 
							  bg=self.FONDO,
							  image = RUBIES_0,
							  padx = 20,
							  compound=tk.LEFT,
							  textvariable=self.v_rubies,
							  font=("Fixedsys", 30),
							  relief=tk.FLAT,
							  fg="#FF96BE",)
		
		score_rank.grid(row = 0, 
						  column = 0, 
						  columnspan=3,
						  sticky = "n",
						  padx = 5, 
						  pady = 10)
						  
		score_recompensa.grid(row = 1, 
						  column = 0, 
						  sticky = "nw",
						  padx = 5, 
						  pady = 5)
		score_derrotados.grid(row = 1, 
						  column = 2, 
						  sticky = "nw",
						  padx = 5, 
						  pady = 5)
		score_nivel.grid(row = 1, 
						  column = 1, 
						  sticky = "nw",
						  padx = 5, 
						  pady = 5)
		score_rubies.grid(row = 1, 
						  column = 3, 
						  sticky = "nw",
						  padx = 5, 
						  pady = 5)

		
		f_contenedor.pack(anchor="nw")
		return f_panel
		
		
	def agregar_boton(self,maestro,imagen,param):
		fb= tk.LabelFrame(maestro,bg="#F0CED4",relief=tk.FLAT,bd=4)
		b=tk.Button(fb,image=imagen,bg=self.FONDO,cursor="hand2",relief=tk.FLAT, command=lambda:self.abrir_ventana(param))
		b.pack()
		b.bind("<Enter>", lambda x: x.widget.configure(bg = "#F0CED4"))
		b.bind("<Leave>", lambda x: x.widget.configure(bg = self.FONDO))
		
		fb.pack(side=tk.TOP, padx=5, pady=(5,0))


	def panel_menu_botones(self,padre):
		BORDE="#F8F859"
		#f_panel = tk.Frame(padre, bg =BORDE,padx=2,pady=2)
		f_contenedor = tk.Frame(padre, bg = self.FONDO)
		
		btnes=[["MAQUINA",MORSE,"maquina"],["TRADUCIR",AGENDA,"traductor"],["MISION",JUEGO,"juego"],["CUENTO",CUENTO,"cuento"]]
	
		f_info=tk.Frame(f_contenedor, bg = self.FONDO)
		c=0
		r=0
		c_max=4
		ancho = 15 #max(self.info[clave],key=lambda x: len(x))
		for n in btnes:
			titulo,imagen,param=n
			f0 = tk.Frame(f_info, bg =BORDE,padx=2,pady=2)
			f=tk.Frame(f0, bg = self.FONDO,padx=5,pady=5)
			self.agregar_boton(f,imagen,param)
			tk.Label(f,text=titulo,bg = self.FONDO,font=("Fixedsys", 17),fg="#f0f6f0").pack(side=tk.TOP, padx=5)
			f.pack()
			f0.grid(row=r,column=c,sticky="nw",padx=(0,15), pady=5)
			c+=1
			if c==c_max:
				r+=1
				c=0
		f_info.pack(side=tk.LEFT,anchor="w")	
		#f_contenedor.pack(anchor="nw")
		return f_contenedor


	def frameEstadoConn(self, padre):
				
		f_a = tk.Frame(padre, bg = self.AMARILLO, relief=tk.FLAT,padx=2,pady=2)
		f_estado_conn = tk.Frame(f_a, bg = self.FONDO_1, relief=tk.FLAT)

		self.display_estado_conn = tk.Label(f_estado_conn, 
											textvariable = self.sv_estado_conn, 
											font = ("Fixedsys", 20),
											fg   = "#7E2222",
											bg   = self.FONDO_1)
		self.display_estado_conn.grid(row 	= 0, 
								      column = 1, 
								      padx   = 5, 
								      pady   = 10)

		#label_puertp = tk.Label(f_estado_conn, 
		#						text = "Puerto ", 
		#						font = ("Fixedsys", 20),
		#						bg   = self.FONDO_1,
		#						anchor = "e")
		#label_puertp.grid(row 	= 0, 
		#				  column = 2, 
		#				  pady   = 10)
		def buscar_puertos():
			puertos = ["Buscar puerto",] + [n.device for n in buscandoPort.lista_puertos()]
			return puertos
		
		valores = buscar_puertos()
		
		self.cb_puerto = ttk.Combobox(f_estado_conn, 
									  #justify     = tk.CENTER,
									  width   	   = 15,
									  #relief 	   = tk.FLAT,
									  textvariable = self.puerto_sel,
									  values       = valores,
									  state        = "readonly",
									  font = ("Fixedsys", 20),)

		self.cb_puerto.grid(row 	= 0, 
							 column = 3, 
							 padx   = (0, 10), 
							 pady   = 10)
		
		self.cb_puerto.bind("<<ComboboxSelected>>", lambda x: self.focus_set())

		refresh = tk.Button(f_estado_conn, 
									 image    = REFRESH,
									 cursor  = "hand2",
									 bg      = self.FONDO_1,
									 font    = ("Fixedsys", 20),
									 relief  = tk.FLAT,
									 command = lambda:self.cb_puerto.config(values=buscar_puertos()))
		refresh.grid(row 	= 0, 
					 column = 4, 
					 sticky = "w", 
					 padx   = (0,3), 
					 pady   = 10)

		refresh.bind("<Enter>", lambda x: x.widget.configure(bg = "#FFD2EF"))
		refresh.bind("<Leave>", lambda x: x.widget.configure(bg = self.FONDO_1))

		self.ico_arduino = tk.Button(f_estado_conn, 
									 image    = MICRO_B,
									 text     = " ABIR CONN. ",
									 compound = tk.LEFT,
									 cursor  = "hand2",
									 bg      = self.FONDO_1,
									 font    = ("Fixedsys", 20),
									 relief  = tk.FLAT,
									 command = self.abrirConexion)
		self.ico_arduino.grid(row 	= 0, 
						 column = 5, 
						 sticky = "nw", 
						 padx   = (0,10), 
						 pady   = 10)
						 
		self.ico_arduino.bind("<Enter>", lambda x: x.widget.configure(bg = "#FFD2EF"))
		self.ico_arduino.bind("<Leave>", lambda x: x.widget.configure(bg = self.FONDO_1))
			
		f_estado_conn.pack(expand=True,fill=tk.BOTH)
		
		return f_a


	def abrir_ventana(self,param):
		CajonGeneral.FUNC_CAMBIAR_VENTANA(param)



class maquinaMorse(ScrollableFrame):
	
	def __init__(self, maestro, **kwargs):
		super().__init__(maestro, **kwargs)

		self.maestro = maestro
		self.CONN  = kwargs.get("CONN", False)
		
		self.FONDO   = kwargs.get("bg", "#222323")
		self.FONDO_1 = "#fe6c90"#kwargs.get("bg", "#FFFFFF")
		self.FONDO_2 = "#FBFBFB"#kwargs.get("bg", "#FFFFFF")
		self.TXT_ANCHO = 60
		self.TXT_ALTO  = 8
		self.FONDO_LECTOR = "#444444"
		self.COLOR_TXT="#F9F9F9"
		self.COLOR_BLINK="#FFC0CB"
		self.COLOR_RESALTADO="#FF607C"
		self.TITULO = " MENSAJE ENTRANTE: "
		self.RECOLECTAR_BUFFER = False
		
		self.DURACION_PUNTO =  200
		self.DURACION_LINEA =  self.DURACION_PUNTO*3


		global ICONO_2
		ICONO_2   = ImageTk.PhotoImage(Image.open('iconos\\morse.png'))
		
		"""
		
		La duración del punto es la mínima posible. 
		Una raya tiene una duración de aproximadamente tres veces la del punto. 
		Entre cada par de símbolos de una misma letra existe una ausencia de señal con duración aproximada a la de un punto. 
		Entre las letras de una misma palabra, la ausencia es de aproximadamente tres puntos. 
		Para la separación de palabras transmitidas el tiempo es de aproximadamente tres veces el de la raya.
		
		
		"""
		self.hilo_activo    = False
		self.estado_conn    = False

		##self.sv_estado_conn = tk.StringVar()
		##self.sv_estado_conn.set("■")
		##self.puerto_sel 	= tk.StringVar()
		
		self.directorio = os.path.abspath(os.path.dirname(__file__))	
		self.ruta_base = f'{self.directorio}/iconos/GIF/'
		self.lista_gif = os.listdir(self.ruta_base)
		self.ruta_sonido = f'{self.directorio}/sonido'
		
		self.poblarVentana()
		
		if CajonGeneral.CONN_ARDUINO:
			self.recolectar_data_entrante()

	def beep(self,**kwargs):
		for n in kwargs["codigo"]:
			frequency = 500  
			if n==".":
				duracion=self.DURACION_PUNTO
			elif n == "-":
				duracion=self.DURACION_LINEA
			elif len(n.strip()) == 0:
				PlaySound(self.ruta_sonido + "/silencio.wav", SND_FILENAME)
				duracion=False
			else:
				duracion = False
			if duracion:
				#frequency = 500  
				Beep(frequency, duracion)
		self.hilo_activo = False

	def poblarVentana(self):
		self.rowconfigure(0, weight = 1)
		self.columnconfigure(0, weight = 1)
		
		f_contenedor =  tk.Frame(self.scrollable_frame, bg =self.FONDO,padx=2,pady=2)

		self.scrollable_frame.rowconfigure(0, weight = 1)
		self.scrollable_frame.columnconfigure(0, weight = 1)
		
		f_contenedor.rowconfigure(0, weight = 1)
		f_contenedor.columnconfigure(0, weight = 1)
				
		f_uno = self.fila_uno(f_contenedor)
		f_uno.grid(row=0,column=0,sticky="nw",padx=100)
		
		fila_dos = self.fila_dos(f_contenedor)
		fila_dos.grid(row=1,column=0,sticky="n",padx=100)

		fila_tres = self.fila_tres(f_contenedor)
		fila_tres.grid(row=2,column=0,sticky="n",pady=50,padx=(20,60))
		
		f_contenedor.pack(expand=True,fill=tk.X,anchor="n")
		#f_estado_conn = self.frameContrasenia(f_conitenedor)


	def traducir(self,letra):
		try:
			msj = CajonGeneral.diccionario_morse[letra.upper()]
		except KeyError:
			msj= "?"
		return msj
		
	def insertar_en_txt(self,data):
		self.texto_cita.config(state="normal")
		try:
			self.texto_cita.insert(tk.END, data)
		except IndexError:
			pass
		self.texto_cita.config(state="disabled")

	def leer_data_entrante(self):
		if len(CajonGeneral.BUFFER)>0:
			data = CajonGeneral.BUFFER[:]
			self.insertar_en_txt(data)
			self.last_char.set(data[-1].upper())
			codigo= self.traducir(data[-1].upper())
			self.last_char_code.set(r'{}'.format(codigo))
			CajonGeneral.BUFFER = r""""""
		
	def recolectar_data_entrante(self):
		if self.RECOLECTAR_BUFFER:
			self.leer_data_entrante()
			self.after(20,self.recolectar_data_entrante)
		
	def fila_uno(self,padre):
		f_panel = tk.Frame(padre, bg =self.FONDO,padx=2,pady=2)
		f_panel.rowconfigure(0, weight = 1)
		f_panel.columnconfigure(0, weight = 1)

		self.last_char = tk.StringVar()
		self.last_char_code = tk.StringVar()
		
		normal_1   = "#FFC0CB"
		normal_2   = "#292929"
		resaltar_1 = "#FFFFFF"
		resaltar_2 ="#868686"
		resaltar_letra = "#444444"
		presionar  = resaltar_1
		fuente = ("Fixedsys", 17)
		boton_volver = Notificaciones.BtnRetro(f_panel, boton = {"texto":  "VOLVER", 
																 "label_height":   1, 
																 "fuente": 		  fuente,
																 "normal_1" :      normal_1,
																 "normal_2" :      normal_2,
																 "resaltar_1":     resaltar_1,
																 "resaltar_2":     resaltar_2,
																 "resaltar_letra": resaltar_letra,
																 "presionar" :     presionar,
																 "param"     :     False, 
																 "accion":         self.salir,
																 "borde" : 4
																 })
		boton_volver.grid(row = 0, 
						   column = 0, 
						   sticky = "nw",
						   padx = 5, 
						   pady = (20, 0))

		
		f_incoming = tk.Frame(f_panel, bg ="#ffffff",padx=2,pady=2)
		tk.Label(f_incoming,width=3,bg=self.FONDO,textvariable=self.last_char,font=("Fixedsys", 20),fg="#FFFFFF").pack(side=tk.LEFT)
		tk.Label(f_incoming,width=6,bg=self.FONDO,textvariable=self.last_char_code,font=("Fixedsys", 20),fg="#FFFFFF").pack(side=tk.LEFT)


		estado_con = tk.Label(f_panel, 
								  cursor="hand2", 
								  bg=self.FONDO,
								  text="", 
								  font=("Fixedsys", 20),
								  relief=tk.FLAT,fg="#FFFFFF")
								  #command = lambda:self.desplegar_frame(boton_secreto,f_estado_conn))
		
		estado_con.bind("<Enter>",lambda e: e.widget.config(fg="#B55AFC"))
		estado_con.bind("<Leave>",lambda e: e.widget.config(fg="#FFFFFF"))

		self.AMARILLO = "#F8F859"
		tit_bienvenida = tk.Label(f_panel, 
								  image=ICONO_2,
								  compound=tk.LEFT,
								  bg=self.FONDO,
								  text= self.TITULO,
								  font=("Fixedsys", 25),
								  relief=tk.FLAT,
								  fg=self.AMARILLO,)
						   		
		boton_volver.grid(row = 0, 
						   column = 0, 
						   sticky = "nw", 
						   padx = 5, 
						   pady = (20, 10))

		tit_bienvenida.grid(row = 1, 
					    column = 1, 
					    sticky = "nw", 
					    padx = (5,0), 
					    pady = (20, 10))	
					    	
		f_incoming.grid(row = 1, 
					    column = 2, 
					    sticky = "w", 
					    padx = (0,15), 
					    pady = (20, 10))
		
		estado_con.grid(row = 0, 
						column = 3, 
						sticky = "ne", 
						padx = 5, 
						pady = (20, 10))


		return f_panel

	def fila_dos(self,padre):
		
		f_panel = tk.Frame(padre, bg =self.FONDO,padx=2,pady=2)
		#f_panel.rowconfigure(0, weight = 1)
		#f_panel.columnconfigure(0, weight = 1)
		#f_panel.columnconfigure(1, weight = 1)

		
		def clear_last():
			self.texto_cita.config(state="normal")
			txt=self.texto_cita.get(1.0,tk.END)
			if len(txt)>1:
				txt=txt[:-1]
			self.texto_cita.delete(1.0,tk.END)
			self.texto_cita.insert(1.0, r'{}'.format(txt[:-1]))
			self.texto_cita.config(state="disabled")
		
		def func_clear_all(*args):
			estado,widget = args
			widget.destroy()
			if estado:
				self.texto_cita.config(state="normal")
				self.texto_cita.delete(1.0,tk.END)
				self.texto_cita.config(state="disabled")
			
		
		def preguntar_si_borrar_todo():
			boton = {"fuente":("Fixedsys", 17),"texto": " NO ","accion":print, "normal_2" :"#A2A2A2", "resaltar_2" :"#4D4D4D", "boton_2": {"texto": " SI ","fuente":("Fixedsys", 17), "accion":func_clear_all,"normal_2" :"#A2A2A2", "resaltar_2" :"#4D4D4D"}}
			Notificaciones.pregunta(self.winfo_toplevel(), pregunta="¿QUERES BORRAR TODO?", titulo="BORRAR", boton= boton)

			
		BORDE=self.COLOR_TXT
		f_marco_btn = tk.Frame(f_panel, bg =BORDE,padx=2,pady=2)
		f_btnes = tk.Frame(f_marco_btn, bg = self.FONDO)

		#clear_agregar = tk.Button(f_btnes, 
		#					   cursor="hand2", 
		#					   bg=self.FONDO,
		#					   text="+", 
		#					   font=("Fixedsys", 20),
		#					   relief=tk.FLAT,fg="#FFFFFF",
		#					   command = agregar_txt)
		#
		#clear_agregar.bind("<Enter>",lambda e: e.widget.config(fg="#B55AFC"))
		#clear_agregar.bind("<Leave>",lambda e: e.widget.config(fg="#FFFFFF"))

		clear_last = tk.Button(f_btnes, 
							   cursor="hand2", 
							   bg=self.FONDO,
							   text="<", 
							   font=("Fixedsys", 20),
							   relief=tk.FLAT,fg="#FFFFFF",
							   command = clear_last)
		
		clear_last.bind("<Enter>",lambda e: e.widget.config(fg="#B55AFC"))
		clear_last.bind("<Leave>",lambda e: e.widget.config(fg="#FFFFFF"))

		
		f_marco = tk.Frame(f_panel, bg =self.FONDO_1,padx=2,pady=2)
		f_texto, self.texto_cita = self.agregarTexto(f_marco)

		clear_all = tk.Button(f_btnes, 
							   cursor="hand2", 
							   bg=self.FONDO,
							   text="x", 
							   font=("Fixedsys", 20),
							   relief=tk.FLAT,fg="#FFFFFF",command=preguntar_si_borrar_todo)
							   #command = lambda:self.desplegar_frame(boton_secreto,f_estado_conn))
		
		clear_all.bind("<Enter>",lambda e: e.widget.config(fg="#B55AFC"))
		clear_all.bind("<Leave>",lambda e: e.widget.config(fg="#FFFFFF"))

		f_btnes.pack(expand=True, fill=tk.BOTH)

		clear_last.grid(row = 0, 
						column = 0, 
						sticky = "nw", 
						padx = 5, 
						pady = (20, 10))
		
		clear_all.grid(row = 1, 
					   column = 0, 
					   sticky = "nw", 
					   padx = 5, 
					   pady = (20, 10))

		#clear_agregar.grid(row = 2, 
		#				   column = 0, 
		#				   sticky = "nw", 
		#				   padx = 5, 
		#				   pady = (20, 10))
		
		f_marco_btn.grid(row = 0, 
					  column = 1, 
					  sticky = "nw", 
					  padx = 5, 
					  pady = (20, 10))

		f_texto.grid(row = 0, 
					 column = 0)
					  
		f_marco.grid(row = 0, 
					 column = 0, 
					 sticky = "n", 
					 padx = 5, 
					 pady = (20, 10))

		return f_panel
	
	def agregar_boton(self,padre,letra,codigo):
		CLR_TEXTO= "#FFFFFF"
		CLR_TEXTO_R= "#220023"
		BORDE = "#F0CED4"
		fb= tk.LabelFrame(padre,bg=BORDE,relief=tk.FLAT,bd=2)
		
		b=tk.Button(fb,text=f"{letra} ( {codigo} )", fg = CLR_TEXTO, bg=self.FONDO,font=("Fixedsys", 17),cursor="hand2",relief=tk.FLAT, command=lambda:self.beep(codigo=codigo))
		b.pack()
						 
		b.bind("<Enter>", lambda x: x.widget.configure(bg = "#F0CED4",fg=CLR_TEXTO_R))
		b.bind("<Leave>", lambda x: x.widget.configure(bg = self.FONDO,fg=CLR_TEXTO))
		
		fb.pack(side=tk.TOP, padx=5, pady=(5,0))
		
		return b
		
	def fila_tres(self,padre):
		BORDE="#F8F859"
		f_panel = tk.Frame(padre, bg =BORDE,padx=2,pady=2)
		f_contenedor = tk.Frame(f_panel, bg = self.FONDO)
		
		f_info=tk.Frame(f_contenedor, bg = self.FONDO,padx=20,pady=20)
		c=0
		r=0
		c_max=4
		ancho = 15 #max(self.info[clave],key=lambda x: len(x))
		for n in CajonGeneral.diccionario_morse:
			letra= n.upper()
			codigo=CajonGeneral.diccionario_morse[n]
			#f0 = tk.Frame(f_info, bg =BORDE,padx=2,pady=2)
			f=tk.Frame(f_info, bg = self.FONDO,padx=5,pady=5)
			self.agregar_boton(f,letra,codigo)
			#tk.Label(f,text=titulo,bg = self.FONDO,font=("Fixedsys", 17),fg="#f0f6f0").pack(side=tk.TOP, padx=5)
			#f.pack()
			f.grid(row=r,column=c,sticky="nw",padx=(0,15))
			c+=1
			if c==c_max:
				r+=1
				c=0
		f_info.pack(side=tk.LEFT,anchor="w")	
		f_contenedor.pack(anchor="nw")
		return f_panel
	
	def agregarTexto(self,maestro):
		
		f_texto = tk.Frame(maestro, bg =  self.FONDO)						
		
		f_texto.columnconfigure(0, weight = 1)
		f_texto.rowconfigure(0, weight = 1)
		
		barra   = ttk.Scrollbar(maestro) 
		texto_cita = tk.Text(f_texto,
							 width = self.TXT_ANCHO,#60,
							 height= self.TXT_ALTO,#8, 
							 padx     		   = 40,
							 pady     		   = 20,
							 wrap     		   = tk.WORD,
							 spacing2 		   = 10, 
							 tabs   		   = 30, 
							 undo   		   = 25,
							 autoseparators    = 20,
							 bg     		   = self.FONDO_LECTOR,
							 fg                = self.COLOR_TXT,
							 insertbackground  = self.COLOR_BLINK,
							 insertwidth       = 3,
							 insertofftime     = 400,
							 insertontime      = 600,
							 selectbackground  = self.COLOR_RESALTADO,
							 state = "disabled",
							 cursor = "arrow",
							 font              = ("Fixedsys", 24),
							 yscrollcommand    = barra.set,
							 relief 		   = tk.FLAT,)
		#texto_cita.bind("<FocusIn>",  self.vincular_texto)
		#texto_cita.bind("<FocusOut>", self.desvincular_texto)
		#texto_cita.bind("<Leave>",    self.desvincular_texto)
		
		barra.config(command = texto_cita.yview )

		texto_cita.grid(row    = 0,
					    column = 0,
					    sticky = "nsew")
		
		barra.grid(row       = 0, 
				   column    = 1,
				   sticky    = "nse")

		return f_texto,texto_cita

	def salir(self,*args):
		self.unbind("<Enter>")
		self.unbind("<Leave>")
		self.unbind_all("<MouseWheel>")
		
		CajonGeneral.FUNC_CAMBIAR_VENTANA("panel_principal")
		


class traductor(maquinaMorse):
	
	def poblarVentana(self):
		#self.rowconfigure(0, weight = 1)
		#self.columnconfigure(0, weight = 1)
		
		f_contenedor =  tk.Frame(self.scrollable_frame, bg =self.FONDO,padx=2,pady=2)

		#self.scrollable_frame.rowconfigure(0, weight = 1)
		#self.scrollable_frame.columnconfigure(0, weight = 1)
		
		#f_contenedor.rowconfigure(0, weight = 1)
		#f_contenedor.columnconfigure(0, weight = 1)

		normal_1   = "#FFC0CB"
		normal_2   = "#292929"
		resaltar_1 = "#FFFFFF"
		resaltar_2 ="#868686"
		resaltar_letra = "#444444"
		presionar  = resaltar_1
		fuente = ("Fixedsys", 17)
		b3 = Notificaciones.BtnRetro(f_contenedor, boton = {"texto":  "VOLVER", 
																 "label_height":   1, 
																 "fuente": 		  fuente,
																 "normal_1" :      normal_1,
																 "normal_2" :      normal_2,
																 "resaltar_1":     resaltar_1,
																 "resaltar_2":     resaltar_2,
																 "resaltar_letra": resaltar_letra,
																 "presionar" :     presionar,
																 "param"     :     False, 
																 "accion":         self.salir,
																 "borde" : 4
																 })
		b3.grid(row = 0, 
						   column = 0, 
						   sticky = "nw",
						   padx = (100,10), 
						   pady = (20, 0))
		



		global AGENDA_2
		AGENDA_2   = ImageTk.PhotoImage(Image.open('iconos\\agenda.png'))

		self.AMARILLO = "#F8F859"
		tit_bienvenida = tk.Label(f_contenedor, 
								  image=AGENDA_2,
								  compound=tk.LEFT,
								  bg=self.FONDO,
								  text=" TRADUCTOR (SUPER SECRETO)",
								  font=("Fixedsys", 28),
								  relief=tk.FLAT,
								  fg=self.AMARILLO,)
		tit_bienvenida.grid(row = 1, 
						   column = 0, 
						   sticky = "n",  columnspan=2, 
						   padx = 5, 
						   pady = (0, 0))
		#f_uno = self.fila_uno(f_contenedor)
		#f_uno.grid(row=0,column=0,sticky="nwe",padx=100)
		#
		fila_dos = self.traductor(f_contenedor)
		fila_dos.grid(row=2,column=0,padx=100,pady=(50,0))

		#fila_tres = self.fila_tres(f_contenedor)
		#fila_tres.grid(row=3,column=0,sticky="n",pady=50,padx=100)
		#
		f_contenedor.pack(expand=True,fill=tk.X,anchor="n")
		#f_estado_conn = self.frameContrasenia(f_contenedor)
	
	
	
	def traductor(self,padre):
		BORDE="#FF879C"
		f_panel = tk.Frame(padre, bg =BORDE,padx=2,pady=2)
		f_contenedor = tk.Frame(f_panel, bg = self.FONDO)

		global INTERCAMBIAR
		global INTERCAMBIAR_R
		global INTERCAMBIAR_P	
		INTERCAMBIAR = ImageTk.PhotoImage(Image.open('iconos\\intercambiar.png'))	
		INTERCAMBIAR_R = ImageTk.PhotoImage(Image.open('iconos\\intercambiar_r.png'))	
		INTERCAMBIAR_P = ImageTk.PhotoImage(Image.open('iconos\\intercambiar_p.png'))	

		global SONAR	
		global SONAR_R	
		global SONAR_P	
		SONAR = ImageTk.PhotoImage(Image.open('iconos\\sonar.png'))	
		SONAR_R = ImageTk.PhotoImage(Image.open('iconos\\sonar_r.png'))	
		SONAR_P = ImageTk.PhotoImage(Image.open('iconos\\sonar_p.png'))	

		d_tradu = {"to_palabras":CajonGeneral.diccionario_to_morse,"to_code":CajonGeneral.diccionario_morse}  
		
		def hacer_sonar(*args):
			codigo = self.v_salida.get().strip()
			if len(codigo)<0 or len(codigo) > 50:
				return
			if self.hilo_activo:
				return
			else:
				print("abriendo hilo")
				self.hilo_activo = True		
				self.t1 = threading.Thread(target = self.beep, kwargs = {"codigo":codigo})
				self.t1.deamon=True
				self.t1.start()		
			
		def intercambiar(evento):
			evento.widget.configure(image = INTERCAMBIAR_R)
			self.v_entrada.set("")
			self.v_salida.set("")
			
			if self.clave_traduccion == "to_code":
				self.v_tit_entrada.set("CODIGO")
				self.v_tit_salida.set("PALABRAS")
				self.clave_traduccion = "to_palabras"
				self.bs.configure(image = SONAR_P, cursor="arrow")
				self.bs.unbind("<Enter>")# lambda x: x.widget.configure(image = SONAR_R))
				self.bs.unbind("<Leave>")# lambda x: x.widget.configure(image = SONAR))
				self.bs.unbind("<Button-1>")#, lambda x: x.widget.configure(image = SONAR_P))		
				self.bs.unbind('<ButtonRelease-1>')#, intercambiar)
			else:
				self.v_tit_entrada.set("PALABRAS")
				self.v_tit_salida.set("CODIGO")
				self.clave_traduccion = "to_code"
				self.bs.configure(image = SONAR, cursor="hand2")
				self.bs.bind("<Enter>", lambda x: x.widget.configure(image = SONAR_R))
				self.bs.bind("<Leave>", lambda x: x.widget.configure(image = SONAR))
				self.bs.bind("<Button-1>", lambda x: x.widget.configure(image = SONAR_P))
				self.bs.bind('<ButtonRelease-1>', hacer_sonar)
					
		def traducir(*args):
			txt= self.v_entrada.get()
			self.v_entrada.set(txt.upper())
			tra=""
			if self.clave_traduccion == "to_palabras":
				txt = txt.split(" ")
			d = d_tradu[self.clave_traduccion]
			for n in txt:
				if n.strip():
					try:
						t=d[n.upper()] 
						if self.clave_traduccion == "to_code":
							tra+=t+" "
						else:
							tra+=t
					except KeyError:
						tra+="?"					
				else:
					tra+="  "
			self.v_salida.set(tra)
		
		self.clave_traduccion = "to_code"
		self.v_tit_entrada = tk.StringVar()
		self.v_entrada = tk.StringVar()
		self.v_tit_salida  = tk.StringVar()
		self.v_salida  = tk.StringVar()

		self.v_entrada.trace_add('write', traducir)

		self.v_tit_entrada.set("PALABRAS")
		self.v_tit_salida.set("CODIGO")
		
		f_entrada = tk.Frame(f_contenedor,bg=BORDE,padx=2,pady=2)		
		entrada = tk.Entry(f_entrada,width=40,justify=tk.CENTER,textvariable=self.v_entrada,font=("Fixedsys", 17),state="normal").pack(side=tk.LEFT,expand=True,fill=tk.X )
		f_entrada.grid(row=0,column=1,  padx=(0,15), pady=(15,5),sticky="we")
		tk.Label(f_contenedor,fg="#FFFFFF", bg=self.FONDO,width=15,textvariable=self.v_tit_entrada,font=("Fixedsys", 17),state="normal").grid(row=0,column=0, padx = 5, pady=5)
		
		f_salida = tk.Frame(f_contenedor,bg=BORDE,padx=2,pady=2)
		salida  = tk.Label(f_salida,justify=tk.CENTER,relief=tk.FLAT,width=38,cursor="arrow",textvariable=self.v_salida,font=("Small Fonts", 20,"bold"),state="normal",wrap=550).pack(side=tk.LEFT,anchor="nw")
		
		tk.Label(f_contenedor,fg="#FFC0CB", bg=self.FONDO,width=15,textvariable=self.v_tit_salida,font=("Fixedsys", 17),state="normal").grid(row=1,column=0, padx = 5, pady=5,sticky="nw")
		f_salida.grid(row=1,column=1,  padx=(0,15), pady=(5,15))


		bb = tk.Label(f_contenedor, 
				       image    = INTERCAMBIAR,
				       cursor  = "hand2",
				       bg      = self.FONDO,
				       relief  = tk.FLAT)
		bb.grid(row=0,column=2,rowspan=2, padx=10, pady=15)
			    
		bb.bind("<Enter>", lambda x: x.widget.configure(image = INTERCAMBIAR_R))
		bb.bind("<Leave>", lambda x: x.widget.configure(image = INTERCAMBIAR))
		bb.bind("<Button-1>", lambda x: x.widget.configure(image = INTERCAMBIAR_P))
		bb.bind('<ButtonRelease-1>', intercambiar)
		

		self.bs = tk.Label(f_contenedor, 
				       image    = SONAR,
				       cursor  = "hand2",
				       bg      = self.FONDO,
				       relief  = tk.FLAT)
		self.bs.grid(row=0,column=3,rowspan=2, padx=(0,10), pady=15)    
		self.bs.bind("<Enter>", lambda x: x.widget.configure(image = SONAR_R))
		self.bs.bind("<Leave>", lambda x: x.widget.configure(image = SONAR))
		self.bs.bind("<Button-1>", lambda x: x.widget.configure(image = SONAR_P))
		self.bs.bind('<ButtonRelease-1>', hacer_sonar)
		
		
		f_contenedor.pack(anchor="nw")
		return f_panel
	


class tipear(maquinaMorse):
	
	def resetear(self,*args):
		self.mensaje_pregunta.destroy()
		for n in self.scrollable_frame.winfo_children():
			n.destroy()
		self.poblarVentana()
	
	def preguntar_resetear(self):
		def cerrar(*args):
			self.mensaje_pregunta.destroy()
			
		boton = {"fuente":("Fixedsys", 17),"texto": " NO ","accion":cerrar, "normal_2" :"#A2A2A2", "resaltar_2" :"#4D4D4D", "boton_2": {"texto": " SI ","fuente":("Fixedsys", 17), "accion":self.resetear,"normal_2" :"#A2A2A2", "resaltar_2" :"#4D4D4D"}}
		self.mensaje_pregunta = Notificaciones.pregunta(self.winfo_toplevel(), pregunta="¿QUERES VOLVER A COMENZAR?", titulo="RESETAR", boton= boton)
	
	def poblarVentana(self):
		
		self.rowconfigure(0, weight = 1)
		self.columnconfigure(0, weight = 1)
		self.bind_all("<Key>", lambda e: self.chequear_si_coincide(e.char.upper()))
		f_contenedor =  tk.Frame(self.scrollable_frame, bg =self.FONDO,padx=2,pady=2)

		self.ver_cod = tk.BooleanVar()
		self.ver_cod.set(True)
		self.auto_space = tk.BooleanVar()
		self.auto_space.set(True)
		
		self.v_valor = tk.StringVar()
		self.valor_base = 1
		self.valor = self.valor_base
		self.v_valor.set(f"(+{self.valor})")
		
		self.v_cont_rubies = tk.IntVar()
		self.v_cont_rubies.set(0)
		
		self.scrollable_frame.rowconfigure(0, weight = 1)
		self.scrollable_frame.columnconfigure(0, weight = 1)
		
		f_contenedor.rowconfigure(0, weight = 1)
		f_contenedor.columnconfigure(0, weight = 1)
				
		f_uno = self.fila_uno(f_contenedor)
		f_uno.grid(row=0,column=0,columnspan=2,sticky="nwe")
		
		f_rubies = self.contador_rubies(f_uno)
		f_rubies.grid(row=1,column=3)
		
		cadena = random.choice(list(CajonGeneral.cuentos.values())).strip()
		fila_dos = self.frame_show_word(f_contenedor, cadena)
		fila_dos.grid(row=1,column=0,sticky="n",padx=50)
		
		fila_tres = self.panel_botones(f_contenedor)
		fila_tres.grid(row=2,column=0,sticky="n",pady=(20,50),padx=50)
		
		f_contenedor.pack(expand=True,fill=tk.X,anchor="n", padx = 50)

	def agregar_boton(self,padre,letra,codigo, borde):
		CLR_TEXTO= "#FFFFFF"
		CLR_TEXTO_R= "#220023"
		BORDE = borde
		fb= tk.LabelFrame(padre,bg=BORDE,relief=tk.FLAT,bd=2)
		fb.BORDE = BORDE
		
		fb.columnconfigure(0,weight=1) 
		fb.rowconfigure(0,weight=1)		
		
		
		l_1=tk.Label(fb,text=f"{letra}", width= 3,fg = CLR_TEXTO, bg=self.FONDO,font=("Fixedsys", 17),relief=tk.FLAT)
		l_1.grid(row=0,column=0,sticky="nswe")

		if codigo:
			b=tk.Button(fb,text=codigo, fg = CLR_TEXTO, bg=self.FONDO,font=("Fixedsys", 6),cursor="hand2",relief=tk.FLAT, command=lambda:self.beep(codigo=codigo))
			b.grid(row=1,column=0,sticky="nswe")					 
			b.bind("<Enter>", lambda x: x.widget.configure(bg = "#F0CED4",fg=CLR_TEXTO_R))
			b.bind("<Leave>", lambda x: x.widget.configure(bg = self.FONDO,fg=CLR_TEXTO))
		else:
			b=tk.Label(fb,text="", fg = CLR_TEXTO, bg=self.FONDO,font=("Fixedsys", 6),cursor="hand2",relief=tk.FLAT, )
			b.grid(row=1,column=0,sticky="nswe")					 
		
		if self.ver_cod.get():
			b.TEXTO = codigo
		else:
			b.TEXTO = " "
		
		fb.pack(expand = True,fill=tk.BOTH,side=tk.TOP)
		
		return fb,l_1,b
	
	def esconder_codigo(self,*args):
		if not self.ver_cod.get():
			for n in self.palabra_en_display:
				l,fb,l_1,b,f= n
				b.config(text=" "*(len(b.TEXTO)))
		else:
			if self.v_cont_rubies.get() > 0:
				self.reproducir_sonido(self.ruta_sonido + "/ouch.wav")
				self.v_cont_rubies.set(max(0,self.v_cont_rubies.get()-5))
			for n in self.palabra_en_display:
				l,fb,l_1,b,f = n
				b.config(text=b.TEXTO)
		self.actulizar_valor()
			
	
	def frame_show_word(self, padre, cadena):
		BORDE="#F8F859"
		f_panel = tk.Frame(padre, bg =BORDE,padx=2,pady=2)
		f_contenedor = tk.Frame(f_panel, bg = self.FONDO)
		
		self.contador_correcta = 0
		self.base_cursor = 0
		self.cursor = 0
		self.palabra_en_display = []
		self.MAX_LINEAS = 4
		self.CANT_MAX_LETRAS =  12
		self.CADENA = cadena
		
		self.FRAME_LETRAS=tk.Frame(f_contenedor, bg = self.FONDO,padx=20,pady=20)

		
		for letra in self.CADENA:
			f=tk.Frame(self.FRAME_LETRAS, bg = self.FONDO,padx=5,pady=5)
			letra= letra.upper()
			try:
				f_borde = "#F0CED4"
				codigo=CajonGeneral.diccionario_morse[letra]
			except KeyError:
				f_borde = "#696969"
				codigo= ""
			fb,l_1,b = self.agregar_boton(f,letra,codigo,f_borde)
			self.palabra_en_display.append([letra,fb,l_1,b,f])

		c=0
		r=0
		for letra in self.palabra_en_display:
			l,fb,l_1,b,f = letra
			f.grid(row=r,column=c,sticky="we")
			c+=1
			if c==self.CANT_MAX_LETRAS:
				r+=1
				c=0
				if r == self.MAX_LINEAS:
					break		
		self.FRAME_LETRAS.pack(expand = True, fill=tk.BOTH,side=tk.LEFT,anchor="w")
		f_contenedor.pack(expand = True, fill=tk.BOTH,side=tk.LEFT,anchor="w")	
		
		return f_panel		


	def ver_adelante_si_espacio(self,pod):
		try:
			if self.auto_space.get():
				l = self.palabra_en_display[self.contador_correcta][0]
				if l.isspace():
					return True
				else:
					return False
			else:
				return False
		except IndexError:
			return False


	def marcar_correcta(self, pos):
		CORRECTA = "#90EE90"
		CORRECTA_R = "#B3D7B3"
		PROX = "#F4C36A"

		borde = self.palabra_en_display[pos][1].BORDE
		self.palabra_en_display[pos][1].config(bg=borde)
		self.palabra_en_display[pos][2].config(bg=CORRECTA)
		
		b = self.palabra_en_display[pos][3]
		b.config(bg=CORRECTA)
		b.bind("<Enter>", lambda x: x.widget.configure(bg = CORRECTA_R))
		b.bind("<Leave>", lambda x: x.widget.configure(bg = CORRECTA))

		self.palabra_en_display[pos+1][1].config(bg=PROX)			

	def chequear_si_coincide(self,letra):
		#letra = evento.char.upper()
		
		CORRECTA = "#90EE90"
		CORRECTA_R = "#B3D7B3"
		INCORRECTA = "#FF9999"
		PROX = "#F4C36A"
		ruta_match =self.ruta_sonido + "/correcto_1.wav"
		ruta_error =self.ruta_sonido + "/inco.wav"
		

		if self.palabra_en_display[self.contador_correcta][0] ==letra:
			if not self.palabra_en_display[self.contador_correcta][0].isspace():
				t=len(str(self.v_cont_rubies.get()+self.valor))
				if t>2:
					self.label_contador_rubies.config(width=t)
				self.v_cont_rubies.set(self.v_cont_rubies.get()+self.valor)
				self.reproducir_sonido(ruta_match)
			self.marcar_correcta(self.contador_correcta)	
			self.contador_correcta+=1
			#self.cursor+=1	
			if self.ver_adelante_si_espacio(self.contador_correcta):
				self.marcar_correcta(self.contador_correcta)
				self.contador_correcta+=1
				#self.cursor+=1	
			if self.contador_correcta >self.CANT_MAX_LETRAS: 
				self.scrollear()
		else:
			self.v_cont_rubies.set(max(0,self.v_cont_rubies.get()-1))
			self.reproducir_sonido(ruta_error)
			borde = self.palabra_en_display[self.contador_correcta][1].BORDE
			self.palabra_en_display[self.contador_correcta][1].config(bg=borde)
			self.palabra_en_display[self.contador_correcta][2].config(bg=INCORRECTA)
			self.palabra_en_display[self.contador_correcta][3].config(bg=INCORRECTA)

	def contador_rubies(self, padre):
		global RUBI
		RUBI   = ImageTk.PhotoImage(Image.open('iconos\\rubi.png'))
		f_incoming = tk.Frame(padre, bg =self.FONDO,padx=2,pady=2)
		tk.Label(f_incoming,bg=self.FONDO,image=RUBI,font=("Fixedsys", 20),fg="#FFFFFF").pack(side=tk.LEFT)
		self.label_contador_rubies=tk.Label(f_incoming,bg=self.FONDO,width=2,textvariable=self.v_cont_rubies,font=("Fixedsys", 40),fg="#FF4666")
		self.label_contador_rubies.pack(side=tk.LEFT)
		tk.Label(f_incoming,bg=self.FONDO,textvariable=self.v_valor,font=("Fixedsys", 20),fg="#99D6A8").pack(side=tk.LEFT, padx=(0,100))

		return f_incoming

	def leer_data_entrante(self):
		print("... leer")
		if len(CajonGeneral.BUFFER)>0:
			data = CajonGeneral.BUFFER[:]
			data = data[-1].upper()
			self.last_char.set(data[-1].upper())
			codigo= self.traducir(data[-1].upper())
			self.last_char_code.set(r'{}'.format(codigo))
			self.chequear_si_coincide(data)
			CajonGeneral.BUFFER = r""""""
		
	def reproducir_sonido(self,ruta):
		#PlaySound(ruta, SND_FILENAME)
		x = threading.Thread(target=lambda:PlaySound(ruta, SND_FILENAME))
		x.daemon=True
		x.start()
	
	def panel_botones(self, padre):
		"REFRESH"
		"TOGGLE COD"
		"TOGGLE SPACE"
		f_panel = tk.Frame(padre, bg =self.FONDO,padx=2,pady=2)

		normal_1   = "#D89BDB"
		normal_2   = "#CECECE"
		resaltar_1 = "#FFFFFF"
		resaltar_2 ="#868686"
		resaltar_letra = "#444444"
		presionar  = resaltar_1
		fuente = ("Fixedsys", 20)
		br = Notificaciones.BtnRetro(f_panel, boton = {"texto":  "RESETEAR", 
																 "label_height":   1, 
																 "fuente": 		  fuente,
																 "normal_1" :      normal_1,
																 "normal_2" :      normal_2,
																 "resaltar_1":     resaltar_1,
																 "resaltar_2":     resaltar_2,
																 "resaltar_letra": resaltar_letra,
																 "presionar" :     presionar,
																 "param"     :     False, 
																 "accion":         self.preguntar_resetear,
																 "borde" : 4
																 })
		
		bc= tk.Frame(f_panel,bg=self.FONDO,)
		ver_cod = Notificaciones.BtnCheck(bc, 
								 "VER CODIGO", 
								 variable = self.ver_cod,
								 font_1 = ("Fixedsys", 20),
								 font_2 = ("Fixedsys", 20,"bold"),
								 label  = {"color_letra":"#FFECEF"},
								 boton  = {"accion":self.esconder_codigo})
		ver_cod.grid(row =0, column = 0, padx = (0,10), pady=(10,0),sticky = "nw")
		
		
		be= tk.Frame(f_panel,bg=self.FONDO,)
		auto_space = Notificaciones.BtnCheck(be, 
								 "AUTO-ESPACIADO", 
								 variable = self.auto_space,
								 font_1 = ("Fixedsys", 20),
								 font_2 = ("Fixedsys", 20,"bold"),
								 label  = {"color_letra":"#FFECEF"},
								 boton  = {"accion":self.toggle_auto_espaciado})
		auto_space.grid(row =0, column = 0, padx = (0,10), pady=(10,0),sticky = "nw")


		br.pack(side=tk.RIGHT, anchor="s", padx=10)
		bc.pack(side=tk.LEFT)#.grid(row=0,column=1,sticky="w")
		be.pack(side=tk.LEFT, padx=10)#.grid(row=0,column=0,sticky="w")
		
		return f_panel

	def actulizar_valor(self,*args):
		v = self.valor_base
		if not self.ver_cod.get():
			v+=2
		if not self.auto_space.get():
			v+=2
		self.v_valor.set(f"(+{v})")
		self.valor = v

	def toggle_auto_espaciado(self,*args):
		if self.ver_adelante_si_espacio(self.contador_correcta):
			self.marcar_correcta(self.contador_correcta)
			self.contador_correcta+=1
		self.actulizar_valor()

	def scrollear(self):
		c=0
		for letra in self.palabra_en_display:
			l,fb,l_1,b,f = letra
			f.grid_forget() #row=r,column=c,sticky="we")
			c+=1
			if c==self.CANT_MAX_LETRAS:
				break
		self.contador_correcta = self.contador_correcta- self.CANT_MAX_LETRAS
		self.palabra_en_display=self.palabra_en_display[c:]
		
		c=0
		r=0
		for letra in self.palabra_en_display:
			l,fb,l_1,b,f = letra
			f.grid(row=r,column=c,sticky="we")
			c+=1
			if c==self.CANT_MAX_LETRAS:
				r+=1
				c=0
				if r == self.MAX_LINEAS:
					break	


	def ejecutar_salir(self,*args):			
		try:
			self.ventana_mensaje.destroy()
		except:
			pass	
		try:
			self.destroy()
		except:
			pass	
		#self.ventana_mensaje = Notificaciones.nuevo_record(self.winfo_toplevel(), titulo="   ¡NUEVO RECORD!   ", texto_contenido = new_record)
		CajonGeneral.FUNC_CAMBIAR_VENTANA("panel_principal")
		#self.ventana_mensaje
			
	def guardar_juego(self):
		print("GUARDAR JUEGO .......... ")
		try:
			self.ventana_mensaje.destroy()
		except:
			pass
		r= self.v_cont_rubies.get()
	     		
		DATA_CONFIG = CajonGeneral.DATA_CONFIG
		SCORE = CajonGeneral.DATA_CONFIG[CajonGeneral.USUARIO]["score"]
		
		old_r=CajonGeneral.SCORE_rubies.get()
		
		bandera = False
		new_record = ""
		if r>old_r:
			new_record+=f"\n♡ RUBIES: {r} ♡\n"
			DATA_CONFIG[CajonGeneral.USUARIO]["score"]["rubies"] = r
			CajonGeneral.SCORE_rubies.set(r)
			bandera = True

		if bandera:
			with open(CajonGeneral.ruta_save_data,"w") as archivo:
				data = json.dumps(DATA_CONFIG, indent=3)
				archivo.write(data)
				print("archivo guardado")
			CajonGeneral.DATA_CONFIG = DATA_CONFIG
		else:
			self.ejecutar_salir()
		"abrir guardado de score"
		"cheuqear si el score es mayor"
		"actualizar"
		"guardar"
		"entregar medallas ? "
		"volver a pantalla principal"
		pass


	def salir(self,*args):
		self.unbind("<Enter>")
		self.unbind("<Leave>")
		self.unbind_all("<MouseWheel>")
		
		self.guardar_juego()
		CajonGeneral.FUNC_CAMBIAR_VENTANA("panel_principal")
		

class Enemigo(tk.Frame):
	
	
	def __init__(self, maestro, nivel, atacar, **kwargs):
		super().__init__(maestro, **kwargs)
		
		self.seed_vida =   3#CajonGeneral.DATA_CONFIG[CajonGeneral.USUARIO]["dificultad"]["seed_vida"]
		self.seed_ataque = 2#CajonGeneral.DATA_CONFIG[CajonGeneral.USUARIO]["dificultad"]["seed_ataque"]
		
		self.atacar = atacar
		self.nivel= nivel
		self.plus = 0
		
		self.ataque= False
		self.recompensa= False
		
		self.v_nombre=tk.StringVar()
		self.v_recompensa=tk.IntVar()
		self.v_ataque =tk.IntVar() 
		self.v_vida = tk.IntVar()
		
		self.imagen= False
		self.nombre= False
		
		#self.last_danio=tk.StringVar()
		#self.last_danio.set(f'BOOM!')
		
		self.resize = False#(300,300)

		self.animacion_de_atacar= False
		self.sonido_de_atacar= False
		self.animacion_de_danio = False
		self.sonido_de_danio = False
		
		self.FONDO   = kwargs.get("bg", "#222323")
		self.FONDO_1 = "#fe6c90"#kwargs.get("bg", "#FFFFFF")
		self.FONDO_2 = "#EFEFEF"#kwargs.get("bg", "#FFFFFF")
		
		self.estado_animacion_de_atacar = False
		self.estado_animacion_de_danio   = False
	
		self.directorio = os.path.abspath(os.path.dirname(__file__))	
		self.ruta_base = f'{self.directorio}/iconos/enemigos/'
		self.ruta_animacion = f'{self.ruta_base}/animacion/'
		self.ruta_imagen = f'{self.ruta_base}/imagen/'
		self.ruta_sonido = f'{self.directorio}/sonido'
		self.generar_stats(nivel)
		self.seleccionar_personaje()
		#self.seleccionar_animacion()
		self.generar_recompensa()
		
		self.traerIconos()
		
		self.poblarVentana()

	def traerIconos(self):
		"Cargamos los ico que vamos a utilizar en el menu"
		#global MALO
		global ESPADA
		global CORAZON_2
		global COINS
		global GOLPE
		
		#MALO = ImageTk.PhotoImage(Image.open('iconos\\malo.png'))	
		ESPADA = ImageTk.PhotoImage(Image.open('iconos\\espada.png'))	
		CORAZON_2   = ImageTk.PhotoImage(Image.open('iconos\\corazon.png'))
		COINS   = ImageTk.PhotoImage(Image.open('iconos\\coins.png'))
		GOLPE   = ImageTk.PhotoImage(Image.open('iconos\\golpe.png'))

	def reset_enemigo(self, prox_nivel):
		#def resetear():
		#	self.imagen.destroy()
		#	for n in self.winfo_children():
		#		n.destroy()
		#	self.poblarVentana()
		#self.last_danio.set(f'BOOM!')
		print("PROXIMO NIVEL : ", prox_nivel)
		self.plus = 0
		self.nivel = prox_nivel
		self.generar_stats(prox_nivel)
		self.seleccionar_personaje()
		self.imagen_retrato.config(image=self.imagen)
		self.generar_recompensa()
		#self.after(500,resetear)
	
	def seleccionar_personaje(self):
		lista_personajes = os.listdir(self.ruta_imagen)
		nombre = random.choice(lista_personajes)
		self.nombre = nombre.replace("_"," ").upper().split(".")[0]
		self.v_nombre.set(self.nombre)

		image = Image.open(f"{self.ruta_imagen}/{nombre}")
		print (image.mode)
		if self.resize:
			x,y=self.resize
			image= image.resize((x,y))
		image = ImageTk.PhotoImage(image)
		self.imagen = image #ImageTk.PhotoImage(Image.open(f"{self.ruta_imagen}/{nombre}"))	


	def generar_stats(self,nivel):
		print("\n"*3)
		print("SEED V",self.seed_vida)
		print("SEED A",self.seed_ataque)
		print("NIVEL",nivel)
		max_vida = self.seed_vida*nivel+self.seed_vida
		min_vida = self.seed_vida#+nivel
				
		vida = random.randint(min_vida,max_vida)
	
		print("VIDA MAX: ", max_vida)
		print("VIDA MIN: ", min_vida)		
		print("VIDA : ", vida)

		self.v_vida.set(vida)
		if (abs(vida-max_vida)) < (abs(vida-min_vida)):
			media = max_vida - min_vida
			self.plus += max(0,(vida - media))
			print("MEDIA : ", media)
			print("\t|____PLUS RECOMPENSA POR vida : +", abs(vida - media))
		
								  
		print("\n")
		max_att = self.seed_ataque*nivel+self.seed_ataque
		min_att = self.seed_ataque#+nivel

		self.ataque = random.randint(min_att,max_att)
		self.ataque = max_att

		self.v_ataque.set(self.ataque)

		print("ATAQUE MAX: ", max_att)
		print("ATAQUE MIN: ", min_att)
		print("ATAQUE : ", self.ataque)

		if (abs(self.ataque-max_att)) < (abs(self.ataque-min_att)):
			media = max_att - min_att
			self.plus += max(0,(self.ataque - media))
			print("MEDIA : ", media)
			print("\t|____PLUS RECOMPENSA POR ataque : +", self.ataque - media)
		print("\n")

	def generar_recompensa(self):
		self.recompensa = self.nivel + self.plus #self.v_vida.get()+self.ataque+self.plus
		self.v_recompensa.set(self.recompensa)
		print("::::::::::: RECOMPENSA :: ",self.recompensa, "(",self.nivel,",",self.plus,")")
		

	def reproducir_animacion_ataque(self,danio):
		if danio==5:
			bg="#EAD944"
		elif danio == 10:
			bg="#E59667"
		else:
			bg="#D44A56"
		self.reproducir_sonido("/golpe.wav")
		self.label_danio.config(text=f"¡PUM!\nx{danio}")
		self.label_danio.grid(row=0,column=0,sticky="nswe")
		self.after(2000,lambda:self.label_danio.grid_forget())
		
	def reproducir_sonido(self,ruta):
		x = threading.Thread(target=lambda:PlaySound(self.ruta_sonido + ruta, SND_FILENAME))
		x.daemon=True
		x.start()
	
	def recibir_danio(self, danio):
		self.reproducir_animacion_ataque(danio)
		
		tam_letra = max(20,50 - (len(str(self.v_vida.get()))*10-10))
		self.tit_vida.config(font=("Fixedsys", tam_letra))
		self.v_vida.set(max(self.v_vida.get()-danio,0))

		if self.v_vida.get()<=0:
			print("ENEMIGO DERROTADO")
			return True
		else:
			return False
			
	def poblarVentana(self):
		self.rowconfigure(0, weight = 1)
		self.columnconfigure(0, weight = 1)

		self.AMARILLO = "#F8F859"
		self.ROJO = "#FF4B4B"
		self.AZUL = "#5E7E9C"
		
		BORDE = "#9CC99C"
		self.gif_activos = [] 		
		
		f_borde_general = tk.Frame(self, bg =BORDE,padx=2,pady=2)
		f_borde_general.rowconfigure(0, weight = 1)
		f_borde_general.columnconfigure(0, weight = 1)

		f_contenedor = tk.Frame(f_borde_general, bg = self.FONDO)
						
		tit_nombre = tk.Label(f_contenedor, 
							  bg=self.FONDO,
							  textvariable=self.v_nombre,
							  width = 25, 
							  font=("Fixedsys", 28),
							  relief=tk.FLAT,
							  fg="#C6F9C6",)
		
		tam_letra = max(10,50 - (len(str(self.recompensa))*10-10))
	
		tit_coins = tk.Label(f_contenedor, 
								  bg=self.FONDO,
								  image = COINS,
							      compound=tk.LEFT,
								  textvariable=self.v_recompensa,
								  font=("Fixedsys", tam_letra),
								  relief=tk.FLAT,
								  fg=self.AMARILLO,)
		tam_letra = max(10,50 - (len(str(self.ataque))*10-10))
		tit_ataque = tk.Label(f_contenedor, 
							  bg=self.FONDO,
							  image = ESPADA,
							  compound=tk.LEFT,
							  textvariable=self.v_ataque,
							   font=("Fixedsys", tam_letra),
							  relief=tk.FLAT,
							  fg=self.AZUL,)
		tam_letra = max(10,50 - (len(str(self.v_vida.get()))*10-10))
		self.tit_vida = tk.Label(f_contenedor, 
						    bg=self.FONDO,
							image = CORAZON_2,
							compound=tk.LEFT,
						    textvariable=self.v_vida,
						    font=("Fixedsys", tam_letra),
						    relief=tk.FLAT,
						    fg= self.ROJO,)
		#b = tk.Button(f_contenedor, text = "BOOM", command = lambda:self.recibir_danio(1))
		
		f_retrato = self.panel_retrato(f_contenedor)
		
		tit_nombre.grid(row=0,column=0,sticky="n",columnspan=2)
		tit_coins.grid(row=1,column=0,sticky="nw")
		tit_ataque.grid(row=2,column=0,sticky="nw")
		self.tit_vida.grid(row=3,column=0,sticky="nw")
		#b.grid(row=4,column=0,sticky="nw")
		
		f_retrato.grid(row=1,column=1,rowspan=3,sticky="n",padx = 20, pady=20)
		
		f_contenedor.grid(row=0,column=0,sticky="nswe")
		f_borde_general.grid(row=0,column=0,sticky="nswe")
			
	def panel_retrato(self,padre):
		BORDE="#F1F1F1"
		f_panel = tk.Frame(padre, bg =BORDE,padx=2,pady=2)
		f_contenedor = tk.Frame(f_panel, bg = self.FONDO)
		f_contenedor.columnconfigure(0,weight=1)
		c=CajonGeneral.paleta
		
		self.imagen_retrato = tk.Label(f_contenedor,height= 350,width=310,anchor="n",image = self.imagen,bg=random.choice(c))
		self.imagen_retrato.grid(row=0,column=0)

		self.label_danio = tk.Label(f_contenedor,image=GOLPE,compound=tk.BOTTOM,text="",font=("Fixedsys", 30),fg="#FFFFFF",bg="#ba2c38")	
				
		f_contenedor.pack(anchor="nw")
		return f_panel
	
	
class Ataques(tk.Frame):
	
	
	def __init__(self,maestro,victoria,fail,**kwargs):
		super().__init__(maestro, **kwargs)
			
		"TIEMPO INICIAL"
		"TIMER"
		"FRAME CON 3 BTNES"
		"BTN SIMPLE"
		"BTN MEDIO"
		"BTN HARD"
		
		self.tiempo = tk.IntVar()
		self.tiempo_base= CajonGeneral.DATA_CONFIG[CajonGeneral.USUARIO]["dificultad"]["tiempo"]
		self.tiempo.set(self.tiempo_base)
		
		self.FREEZE = False
		
		self.opciones = {}
	
		self.victoria = victoria
		self.fail = fail
		
		self.activado = False
		
		self.PUNTAJE_FACIL = CajonGeneral.DATA_CONFIG[CajonGeneral.USUARIO]["dificultad"]["puntaje_facil"]
		self.PUNTAJE_MEDIO = CajonGeneral.DATA_CONFIG[CajonGeneral.USUARIO]["dificultad"]["puntaje_medio"]
		self.PUNTAJE_DIFICIL = 0
		
		self.v_facil = tk.StringVar()
		self.v_facil_letra =  tk.StringVar()
		self.v_medio = tk.StringVar()
		self.v_dificil = tk.StringVar()
		
		self.COLORES = ["#FFF874","#FFC67F","#F7716D"]
		
		self.maestro = maestro
		self.FONDO   = kwargs.get("bg", "#222323")
		self.FONDO_1 = "#fe6c90"
		self.FONDO_2 = "#EFEFEF"
		self.traerIconos()

		self.directorio = os.path.abspath(os.path.dirname(__file__))	
		self.ruta_base = f'{self.directorio}/iconos/GIF/'
		self.lista_gif = os.listdir(self.ruta_base)
		self.ruta_sonido = f'{self.directorio}/sonido'
		
		self.generar_opciones()
		self.poblarVentana()
		self.activar_reloj()
		
	def resetear(self):
		CLR = "#E5E5E5"
		#self.tit_reloj.config(fg=CLR)	
		self.stop_clock()
		self.tiempo.set(self.tiempo_base)
		self.generar_opciones()
		labels   = [self.l_facil,self.l_medio,self.l_dificil]
		for nro,n in enumerate(labels):
			n.config(bg=self.COLORES[nro])
		#nuevo = self.panel_opc(self.f_contenedor)
		#nuevo.grid(row=0,column=0,padx = 5, pady = 5,sticky="nw")
		#self.f_panel_opc.destroy()
		#self.f_panel_opc = nuevo
		
		self.start_clock()
	
	def start_clock(self):
		if not self.activado:
			self.activado = True
			
	def stop_clock(self):
		self.activado = False
	
	def chequear_si_coincide(self,cadena):
		opciones = [self.v_facil_letra.get(),self.v_medio.get(),self.v_dificil.get()]
		labels   = [self.l_facil,self.l_medio,self.l_dificil]
		puntaje  = [self.PUNTAJE_FACIL,self.PUNTAJE_MEDIO,self.PUNTAJE_DIFICIL,]
		correcta = False
		danio = 0
		for nro,opc in enumerate(opciones):
			if opc.strip() == cadena.upper().strip():
				correcta = opc
				danio = puntaje[nro]
				#self.reproducir_sonido("/error.wav")
				#PlaySound(self.ruta_sonido + "/coin.wav", SND_FILENAME)
				break
		if correcta:
			for nro,opc in enumerate(opciones):
				label = labels[nro]
				if opc != correcta:
					label.config(bg="#BFBFBF")
				else:
					label.config(bg="#8EF28E")
			self.victoria(danio)
		
		
		parcial_match = False
		if len(cadena.upper().strip()) > 1:
			parcial_match = True
		else:
			for opc in opciones:
				s = cadena.upper().strip()
				tam = len(s)
				if s == opc[:tam]:
					parcial_match = True
				
					
		return parcial_match
		
	def reproducir_sonido(self,ruta):
		x = threading.Thread(target=lambda:PlaySound(self.ruta_sonido + ruta, SND_FILENAME))
		x.daemon=True
		x.start()
		
	def desactivar(self):
		opciones = [self.v_facil_letra.get(),self.v_medio.get(),self.v_dificil.get()]
		labels  = [self.l_facil,self.l_medio,self.l_dificil]
		for nro,opc in enumerate(opciones):
			label = labels[nro]
			label.config(bg="#BFBFBF")

	def activar_reloj(self):
		if self.tiempo.get() > 0 and self.activado:
			t = self.tiempo.get()
			if t in (self.tiempo_base,11,4,3,2,1):
				Beep(150*t, 100)
			if t < 8:
				CLR = self.ROJO
				self.tit_reloj.config(fg=CLR)
			elif t < 13:
				CLR = self.NARANJA
				self.tit_reloj.config(fg=CLR)
			else:
				CLR = "#E5E5E5"
				self.tit_reloj.config(fg=CLR)				
			self.tiempo.set(self.tiempo.get()-1)
		elif self.activado:
			self.activado = False
			#self.reproducir_sonido("/error.wav")
			self.fail()
		
		self.after(1000,self.activar_reloj)

	def generar_opciones(self):
		"opcion facil = letra + codigo"
		
		abecedario = CajonGeneral.abecedario[::]#['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N','Ñ', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z','0','1','2','3','4','5','6','7','8','9']

		"opcion dificil = palabra corta"
		opc_dificil = random.choice(CajonGeneral.palabras).upper()
		borrar = []
		for n in opc_dificil:
			borrar.append(n.upper())
		for n in  list(set(borrar)):
			try:
				abecedario.remove(n)
			except:
				pass
				
		self.PUNTAJE_DIFICIL=self.PUNTAJE_MEDIO*len(opc_dificil)
		
		letra_facil = random.choice(abecedario)
		opc_facil = f'{letra_facil} {CajonGeneral.diccionario_morse[letra_facil]}'
		try:
			abecedario.remove(letra_facil)
		except:
			pass
			
		"opcion media = solo letra"		
		opc_media = random.choice(abecedario)
		self.RESPUESTA = opc_dificil

		self.v_facil.set(opc_facil) 		
		self.v_facil_letra.set(letra_facil)
		self.v_medio.set(opc_media)    
		self.v_dificil.set(opc_dificil)  
		
		
		#self.opciones = {opc_facil:[letra_facil,self.PUNTAJE_FACIL],opc_media:[opc_media,self.PUNTAJE_MEDIO],opc_dificil:[opc_dificil,self.PUNTAJE_DIFICIL]}
		
	def traerIconos(self):
		"Cargamos los ico que vamos a utilizar en el menu"
		pass
	
	def poblarVentana(self):
		self.rowconfigure(0, weight = 1)
		self.columnconfigure(0, weight = 1)

		self.AMARILLO = "#F8F859"
		self.AZUL = "#5E7E9C"

		self.VERDE = "#35926e"
		self.NARANJA = "#FFAB62"
		self.ROJO = "#FF4B4B"
		
		BORDE = "#FFFFFF"
		self.gif_activos = [] 		
		
		f_borde_general = tk.Frame(self, bg=self.FONDO)
		f_borde_general.rowconfigure(0, weight = 1)
		f_borde_general.columnconfigure(0, weight = 1)

		self.f_contenedor = tk.Frame(f_borde_general, bg = self.FONDO)
		
		global RELOJ
		RELOJ = ImageTk.PhotoImage(Image.open('iconos\\reloj.png'))					
		
		self.tit_reloj = tk.Label(self.f_contenedor, 
									bg=self.FONDO,
									#width = 200,
									anchor = "w",
									image = RELOJ,
									compound=tk.TOP,
									textvariable=self.tiempo,
									font=("Fixedsys", 50),
									relief=tk.FLAT,
									fg= "#E5E5E5",)

		self.f_panel_opc = self.panel_opc(self.f_contenedor)
		self.tit_reloj.grid(row=0,column=1,padx = 5, pady = 5,sticky="ne")
		self.f_panel_opc.grid(row=0,column=0,padx = 5, pady = 5,sticky="nw")
	
		self.f_contenedor.grid(row=0,column=0,sticky="nswe")
		f_borde_general.grid(row=0,column=0,sticky="nswe")

	def panel_opc(self,padre):
		BORDE="#F859BF"
		f_panel = tk.Frame(padre, bg =BORDE,padx=2,pady=2)
		f_contenedor = tk.Frame(f_panel, bg = self.FONDO)
		
		
		self.l_facil = tk.Label(f_contenedor, textvariable = self.v_facil, width = max(len(self.v_facil.get()),8),bg=self.COLORES[0], font=("Fixedsys", 25))
		self.l_facil.grid(row=0,column=0,padx = 5,pady = 5)#pack(side=tk.LEFT,padx = 5,pady = 5)
		#self.opciones[n].append(l)
		#self.label_opciones.append(l)

		self.l_medio = tk.Label(f_contenedor, textvariable = self.v_medio, width = max(len(self.v_medio.get()),3),bg=self.COLORES[1], font=("Fixedsys", 25))
		self.l_medio.grid(row=0,column=1,padx = 5,pady = 5)#pack(side=tk.LEFT,padx = 5,pady = 5)
		#self.opciones[n].append(l)
		#self.label_opciones.append(l)

		self.l_dificil = tk.Label(f_contenedor, textvariable = self.v_dificil, width = max(len(self.v_dificil.get()),6),bg=self.COLORES[2], font=("Fixedsys", 25))
		self.l_dificil.grid(row=0,column=2,padx = 5,pady = 5)#pack(side=tk.LEFT,padx = 5,pady = 5)
		#self.opciones[n].append(l)
		#self.label_opciones.append(l)


		ptos = [self.PUNTAJE_FACIL,self.PUNTAJE_MEDIO,self.PUNTAJE_DIFICIL]
		for nro,n in enumerate(ptos):
			l = tk.Label(f_contenedor, text = f"x{n}", bg = self.FONDO,font=("Fixedsys", 20),fg="#ffffff")
			l.grid(row=1,column=nro,padx = 5,pady = 5)#pack(side=tk.LEFT,padx = 5,pady = 5)
			
			
		f_contenedor.pack(anchor="nw")
		return f_panel



class Jugador(tk.Frame):
	
	def __init__(self, maestro, victoria, derrota, enemigo, **kwargs):
		super().__init__(maestro, **kwargs)
		
		self.LEER_DATA = True
		#self.RECOLECTAR_BUFFER = CajonGeneral.RECOLECTAR_BUFFER
		self.vida = tk.IntVar()
		self.vida_base = CajonGeneral.DATA_CONFIG[CajonGeneral.USUARIO]["dificultad"]["vida"]
		self.vida.set(2) #self.vida_base
		self.v_entrada = tk.StringVar()
		self.v_entrada.set("")
		
		self.inmunidad = False

		self.last_danio=tk.StringVar()
		self.last_danio.set('')
				
		self.victoria = victoria
		self.derrota = derrota
		self.enemigo=enemigo
		
		self.maestro = maestro
		self.FONDO   = kwargs.get("bg", "#222323")
		self.FONDO_1 = "#fe6c90"#kwargs.get("bg", "#FFFFFF")
		self.FONDO_2 = "#EFEFEF"#kwargs.get("bg", "#FFFFFF")
		self.traerIconos()

		self.directorio = os.path.abspath(os.path.dirname(__file__))	
		self.ruta_base = f'{self.directorio}/iconos/enemigos/'
		self.ruta_animacion = f'{self.ruta_base}/animacion/'
		self.ruta_imagen = f'{self.ruta_base}/imagen/'
		self.ruta_sonido = f'{self.directorio}/sonido'
		
		self.poblarVentana()
		if CajonGeneral.CONN_ARDUINO:
			self.recolectar_data_entrante()
			
	def traerIconos(self):
		"Cargamos los ico que vamos a utilizar en el menu"
		global CORAZON
		global HAND
		CORAZON   = ImageTk.PhotoImage(Image.open('iconos\\corazon.png'))
		HAND   = ImageTk.PhotoImage(Image.open('iconos\\zombi_hand.png'))

	def recibir_danio(self,danio):
		self.resetear_ataque()
		self.objeto_ataques.stop_clock()
		v = self.vida.get() - danio
		self.vida.set(max(v,0))
		self.reproducir_animacion_ataque(danio)
		if v > 0:
			if v < 6:
				CLR = self.NARANJA
			if v < 4:
				CLR = self.ROJO
			if v > 15:
				CLR = self.VERDE
			try:
				self.tit_vida.config(fg=CLR)
				self.after(300,self.objeto_ataques.start_clock())
			except:
				pass
		else:
			self.after(1000,self.muerto)
		
	def revivir(self):
		self.f_contenedor.config(bg=self.FONDO)
		self.vida.set(self.vida_base)
		self.LEER_DATA=True
		self.tit_vida.config(state="normal", fg = self.VERDE)
		self.retrato.config(state="normal")
		self.last_danio.set('')
			
	def muerto(self):
		self.last_danio.set('¡NOOO!')
		self.LEER_DATA=False
		self.tit_vida.config(state="disabled", fg = "#BFBFBF")
		self.retrato.config(state="disabled")
		self.derrota()
		
	def poblarVentana(self):
		self.rowconfigure(0, weight = 1)
		self.columnconfigure(0, weight = 1)

		self.AMARILLO = "#F8F859"
		self.AZUL = "#5E7E9C"

		self.VERDE = "#35926e"
		self.NARANJA = "#FFAB62"
		self.ROJO = "#FF4B4B"
		
		BORDE = "#F1F1F1"
		self.gif_activos = [] 		
		
		f_borde_general = tk.Frame(self, bg=BORDE,padx=2,pady=2)
		f_borde_general.rowconfigure(0, weight = 1)
		f_borde_general.columnconfigure(0, weight = 1)

		self.f_contenedor = tk.Frame(f_borde_general, bg = self.FONDO)
		self.f_contenedor.rowconfigure(2, weight = 1)
		self.f_contenedor.columnconfigure(0, weight = 1)
		self.f_contenedor.columnconfigure(1, weight = 1)

						
		self.tit_vida = tk.Button(self.f_contenedor, 
						        bg=self.FONDO,
							    #width = 200,
							    padx = 20,
							    anchor = "w",
							    image = CORAZON,
							    compound=tk.RIGHT,
						        textvariable=self.vida,
						        font=("Fixedsys", 50),
						        relief=tk.FLAT,
						        fg= self.VERDE,
								command = lambda: self.objeto_ataques.chequear_si_coincide(self.objeto_ataques.RESPUESTA),
								)
		panel_retrato = self.panel_retrato(self.f_contenedor)
	
		self.objeto_ataques = Ataques(self.f_contenedor, victoria=self.ejecutar_ataque,fail=self.fail_attaque)
	
		panel_entrada = self.panel_entrada(self.f_contenedor)
	
		self.tit_vida.grid(row=2,column=1,padx = (20,5), pady = 20,sticky="se")
		panel_retrato.grid(row=2,column=0,padx = (20,5), pady = 20,sticky="sw")
		
		self.objeto_ataques.grid(row=0,column=0,columnspan=2,padx = 20, pady = (20,0),sticky="n")
		panel_entrada.grid(row=1,column=0,columnspan=2,padx = 5, pady = (5,5),sticky="n")
		
		self.f_contenedor.grid(row=0,column=0,sticky="nswe")
		f_borde_general.grid(row=0,column=0,sticky="nswe")
	
			
	def traducir(self,letra):
		try:
			msj = CajonGeneral.diccionario_morse[letra.upper()]
		except KeyError:
			msj= "?"
		return msj
		
	def panel_entrada(self,padre):
		BORDE="#FF879C"
		f_contenedor = tk.Frame(padre, bg = self.FONDO)
		
		self.label_danio = tk.Label(padre,image = HAND,padx=10,compound=tk.LEFT,textvariable=self.last_danio,font=("Fixedsys", 30),bg="#ba2c38",fg="#FFFFFF")

		def clear_last():
			v= self.v_entrada.get()
			if len(v)>0:
				self.v_entrada.set(v[:-1])

		f_tit = tk.Frame(f_contenedor, bg = self.FONDO)
		tit = tk.Label(f_tit, 
					  #image=MORSE_3,
					  #compound=tk.LEFT,
					  bg=self.FONDO,
					  text=" LETRA: ",
					  font=("Fixedsys", 20),
					  relief=tk.FLAT,
					  fg="#FFFFFF",)
		
		self.last_char=tk.StringVar()
		self.last_char_code=tk.StringVar()
		
		self.last_char.set("")
		self.last_char_code.set("")
		
		f_incoming = tk.Frame(f_tit, bg ="#ffffff",padx=2,pady=2)
		tk.Label(f_incoming,width=3,bg=self.FONDO,textvariable=self.last_char,font=("Fixedsys", 20),fg="#FFFFFF").pack(side=tk.LEFT)
		tk.Label(f_incoming,width=6,bg=self.FONDO,textvariable=self.last_char_code,font=("Fixedsys", 20),fg="#FFFFFF").pack(side=tk.LEFT)
	  
		tit.pack(side=tk.LEFT, pady=5)
		f_incoming.pack(side=tk.LEFT, pady=5)
		f_tit.grid(row=0,column=0, pady=5)
		
		f_salida = tk.Frame(f_contenedor,bg=BORDE,padx=2,pady=2)
		salida  = tk.Label(f_salida,justify=tk.CENTER,relief=tk.FLAT,width=16,cursor="arrow",textvariable=self.v_entrada,font=("Small Fonts", 20,"bold"),state="normal",wrap=600).pack(side=tk.LEFT,anchor="nw")
		
		f_salida.grid(row=1,column=0,padx = (15,0), pady=(0,10))

		clear_last = tk.Button(f_contenedor, 
							   cursor="hand2", 
							   bg=self.FONDO,
							   text="<", 
							   font=("Small Fonts", 14,"bold"),
							   relief=tk.FLAT,fg="#FFFFFF",
							   command = clear_last)
		
		clear_last.bind("<Enter>",lambda e: e.widget.config(fg="#B55AFC",bg=BORDE))
		clear_last.bind("<Leave>",lambda e: e.widget.config(fg="#FFFFFF",bg=self.FONDO))
		clear_last.grid(row=1,column=1,padx = 5, pady=(0,10))
		

		#f_contenedor.pack(anchor="nw")
		return f_contenedor
	
	def panel_retrato(self,padre):
		BORDE="#FF879C"
		f_panel = tk.Frame(padre, bg =BORDE,padx=2,pady=2)
		f_contenedor = tk.Frame(f_panel, bg = self.FONDO)
		f_contenedor.columnconfigure(0,weight=1)
		image = Image.open('iconos\\espia.png')
		image = ImageTk.PhotoImage(image)
		self.JUGADOR = image #ImageTk.PhotoImage(Image.open(f"{self.ruta_imagen}/{nombre}"))	
		self.retrato = tk.Label(f_contenedor,image=self.JUGADOR,bg = self.FONDO,width=120,height=120)
		self.retrato.grid(row=0,column=0)
		
		f_contenedor.pack()
		
		return f_panel
	
	def reproducir_animacion_ataque(self,danio):
		if danio==5:
			bg="#EAD944"
		elif danio == 10:
			bg="#E59667"
		else:
			bg="#D44A56"
		self.last_danio.set(f"¡AGRR!\nx{danio}")
		ruta = f'/ataque ({random.randint(1,5)}).wav'
		self.after(2,lambda:self.reproducir_sonido(ruta))
		self.label_danio.grid(row=0,column=0,columnspan=2,sticky="nwe")
		self.after(1500,lambda:self.label_danio.grid_forget())
		
	def reproducir_sonido(self,ruta):
		x = threading.Thread(target=lambda:PlaySound(self.ruta_sonido + ruta, SND_FILENAME))
		x.daemon=True
		x.start()
	
	def ejecutar_ataque(self,danio):
		def actualizar():
			if self.derrotado:
				self.inmunidad = True
				self.victoria()
				self.objeto_ataques.stop_clock()
			else:
				self.inmunidad = False
				self.after(2500,lambda:self.recibir_danio(self.enemigo.ataque))
			self.LEER_DATA = True
		self.objeto_ataques.stop_clock()
		CajonGeneral.BUFFER=""
		self.LEER_DATA = False
		self.derrotado = self.enemigo.recibir_danio(danio)
		self.v_entrada.set("")
		actualizar()
				
	def leer_data_entrante(self):
		if len(CajonGeneral.BUFFER.strip())>0 and self.LEER_DATA: # ------------------------- NO ACEPTA CADENA EN BLANCO -- NO RECIBE LOS ESPACIOS - NO SE NECE PARA EL JUEGO"
			data = CajonGeneral.BUFFER[:]
			data = "".join(data.split()).upper()
			self.last_char.set(data[-1].upper())
			codigo= self.traducir(data[-1].upper())
			self.last_char_code.set(r'{}'.format(codigo))
			self.v_entrada.set(r"{}".format(self.v_entrada.get()+data))
			parcial_match = self.objeto_ataques.chequear_si_coincide(self.v_entrada.get())
			if not parcial_match:
				self.v_entrada.set(r"{}".format(""))
				
			CajonGeneral.BUFFER = r""""""
		
	def recolectar_data_entrante(self):
		self.leer_data_entrante()
		self.after(20,self.recolectar_data_entrante)
		
	def resetear_ataque(self):
		self.v_entrada.set("")
		self.objeto_ataques.resetear()
		CLR = self.VERDE
		self.tit_vida.config(fg=CLR)
	
	def fail_attaque(self):
		self.recibir_danio(self.enemigo.ataque)
		


class ventanaJuego(ScrollableFrame):
	
	def __init__(self, maestro, **kwargs):
		super().__init__(maestro, **kwargs)
		
		"DIFICULTAD"
		""
		self.dificultad = 1
		self.prox_dificultad = CajonGeneral.DATA_CONFIG[CajonGeneral.USUARIO]["dificultad"]["prox_dificultad"]
		self.contador_dificultad = 0
		
		self.recompensa = tk.IntVar()
		self.derrotados = tk.IntVar()
		self.nivel = tk.IntVar()
		self.maestro = maestro
		self.FONDO   = kwargs.get("bg", "#222323")
		maestro.config(bg=self.FONDO)
		self.FONDO_KO = "#D4A2A2" 
		self.FONDO_1 = "#fe6c90"#kwargs.get("bg", "#FFFFFF")
		self.FONDO_2 = "#EFEFEF"#kwargs.get("bg", "#FFFFFF")
		self.traerIconos()

		self.directorio = os.path.abspath(os.path.dirname(__file__))	
		self.ruta_base = f'{self.directorio}/iconos/GIF/'
		self.lista_gif = os.listdir(self.ruta_base)
		self.ruta_sonido = f'{self.directorio}/sonido'
		
		self.ruta_musica_base = f'{self.directorio}/sonido' + "/aventura.wav"
		self.start_musica()
		
		self.rowconfigure(1, weight = 1)
		self.columnconfigure(0, weight = 1)
		self.ventana_de_inicio()

	def traerIconos(self):
		"Cargamos los ico que vamos a utilizar en el menu"
		global COFRE
		global ESPIA_H_2
		global ZOMBI_FACE
		global ZOMBI
		global NIVEL
		
		COFRE = ImageTk.PhotoImage(Image.open('iconos\\cofre.png'))	
		ZOMBI_FACE = ImageTk.PhotoImage(Image.open('iconos\\zombi_face.png'))	
		ESPIA_H_2 = ImageTk.PhotoImage(Image.open('iconos\\espia_h.png'))	
		ZOMBI = ImageTk.PhotoImage(Image.open('iconos\\zombi.png'))	
		NIVEL = ImageTk.PhotoImage(Image.open('iconos\\medalla.png'))	


	def start_musica(self,*args):
		print("###########################  STAR MUSIC  ########################")
		self.stop_musica()
		PlaySound(self.ruta_musica_base, SND_FILENAME | SND_ASYNC)

	def stop_musica(self):
		print("-----------------------------  STOP MUSIC  -----------------------------")
		PlaySound(None, SND_ASYNC)
				
	def resetear_juego(self,*args):		
		self.stop_musica()
		try:
			self.ventana_mensaje.destroy()
		except:
			pass
		self.f_borde_general.destroy()	
		self.reset_valores()
		self.poblarVentana()
		self.objeto_jugador.objeto_ataques.start_clock()
		self.objeto_jugador.revivir()
	
	def reset_valores(self):
		try:
			self.pintar(clr=self.FONDO)
			self.f_sup.config(bg = self.FONDO)
			for n in self.botones_score:
				n.config(bg = self.FONDO)			
			self.f_contenedor.config(bg=self.FONDO)
			self.f_borde_general.config(background=self.FONDO)
		except:
			pass
		self.dificultad = 1
		self.prox_dificultad = 3
		self.contador_dificultad = 0
		self.recompensa.set(0)
		self.derrotados.set(0)
		self.nivel.set(1)

	def actualizar_score(self):
		CajonGeneral.SCORE_recompensa
		CajonGeneral.SCORE_derrotados
		CajonGeneral.SCORE_nivel     
	
	def guardar_juego(self):
		print("GUARDAR JUEGO .......... ")
		try:
			self.ventana_mensaje.destroy()
		except:
			pass
		r= self.recompensa.get()
		d= self.derrotados.get()
		n= self.nivel.get()
	     		
		DATA_CONFIG = CajonGeneral.DATA_CONFIG
		SCORE = CajonGeneral.DATA_CONFIG[CajonGeneral.USUARIO]["score"]
		
		old_r=CajonGeneral.SCORE_recompensa.get()
		old_d=CajonGeneral.SCORE_derrotados.get()
		old_n=CajonGeneral.SCORE_nivel.get()
		
		bandera = False
		new_record = ""
		if r>old_r:
			new_record+=f"\n♡ RECOMPENSA MAXIMA: {r} ♡\n"
			DATA_CONFIG[CajonGeneral.USUARIO]["score"]["recompensa"] = r
			CajonGeneral.SCORE_recompensa.set(r)
			bandera = True
		if d>old_d:
			new_record+=f"\n♡ ENEMIGOS DERROTADOS: {d} ♡\n"
			DATA_CONFIG[CajonGeneral.USUARIO]["score"]["derrotados"] = d
			CajonGeneral.SCORE_derrotados.set(d)
			bandera = True
		if n>old_n:
			new_record+=f"\n♡ NIVEL ALCANZADO: {n} ♡\n"
			DATA_CONFIG[CajonGeneral.USUARIO]["score"]["nivel"] = n
			CajonGeneral.SCORE_nivel.set(n)
			bandera = True
			
		print(new_record)
		if bandera:
			with open(CajonGeneral.ruta_save_data,"w") as archivo:
				data = json.dumps(DATA_CONFIG, indent=3)
				archivo.write(data)
				print("archivo guardado")
			CajonGeneral.DATA_CONFIG = DATA_CONFIG
			self.ventana_mensaje = Notificaciones.nuevo_record(self.winfo_toplevel(), titulo="¡NUEVO RECORD!", texto_contenido = new_record, accion_al_cierre =self.ejecutar_salir)
		else:
			self.ejecutar_salir()
		"abrir guardado de score"
		"cheuqear si el score es mayor"
		"actualizar"
		"guardar"
		"entregar medallas ? "
		"volver a pantalla principal"
		pass

	def salir(self,*args):
		self.guardar_juego()
	
	def ejecutar_salir(self,*args):			
		for n in self.scrollable_frame.winfo_children():
			n.destroy()
		self.f_borde_general.destroy()	
		self.reset_valores()
		
		self.reproducir_musica = False
		self.stop_musica()
					
		CajonGeneral.FUNC_CAMBIAR_VENTANA("panel_principal")
		try:
			self.ventana_mensaje.destroy()
		except:
			pass		
	
	def display_game_over(self):
		ruta = f'/lose.wav'
		self.reproducir_sonido(ruta)

		self.f_sup.config(bg = self.FONDO_KO)
		for n in self.botones_score:
			n.config(bg = self.FONDO_KO)			
		self.pintar(clr=self.FONDO_KO)
		self.f_contenedor.config(bg=self.FONDO_KO)
		self.f_borde_general.config(background=self.FONDO_KO)
		
		boton = {"fuente":("Fixedsys", 17),"texto": " NO ","accion":self.salir, "normal_2" :"#A2A2A2", "resaltar_2" :"#4D4D4D", "boton_2": {"texto": " SI ","fuente":("Fixedsys", 17), "accion":self.resetear_juego,"normal_2" :"#6EED9A", "resaltar_2" :"#4D4D4D"}}
		self.ventana_mensaje = Notificaciones.pregunta(self.winfo_toplevel(),fuente_pregunta=("Fixedsys", 17),ruta_icono='iconos\\game_over.png', fondo="#FF8888", pregunta="¡HEMOS SIDO DERROTADOS!\n¿VOLVEMOS A INTENTARLO?", titulo="¡DERROTA!", boton= boton)	
	
	def game_over(self):
		self.after(2000,self.display_game_over)
	
	
	def ventana_de_inicio(self):
		self.f_borde_general = tk.Frame(self.scrollable_frame, bg=self.FONDO,padx=2,pady=2)
		self.f_borde_general.rowconfigure(0, weight = 1)
		self.f_borde_general.columnconfigure(0, weight = 1)

		normal_1   = "#FFC0CB"
		normal_2   = "#292929"
		resaltar_1 = "#FFFFFF"
		resaltar_2 ="#868686"
		resaltar_letra = "#444444"
		presionar  = resaltar_1
		fuente = ("Fixedsys", 17)
		boton_volver = Notificaciones.BtnRetro(self.f_borde_general, boton = {"texto":  "VOLVER", 
																			 "label_height":   1, 
																			 "fuente": 		  fuente,
																			 "normal_1" :      normal_1,
																			 "normal_2" :      normal_2,
																			 "resaltar_1":     resaltar_1,
																			 "resaltar_2":     resaltar_2,
																			 "resaltar_letra": resaltar_letra,
																			 "presionar" :     presionar,
																			 "param"     :     False, 
																			 "accion":         self.salir,
																			 "borde" : 4
																			 })

		f_tit = tk.Frame(self.f_borde_general, bg=self.FONDO,padx=2,pady=2)
		agente = CajonGeneral.DATA_CONFIG[CajonGeneral.USUARIO]["info_usuario"]["nombre clave"].upper()
		texto = ["AGENTE ESPECIAL:",f"{agente}"," ¡EL MUNDO TE NECESITA!", "UNA INFECCION DE ZOMBIES AMENEZA LA PAZ","¡¿TE ANIMAS A ENFRENTARTE A ELLOS?!"]

		color=["#FE5173",
			   "#FEA4E1",
			   "#FE5173",
			   "#ff8142",
			   "#ffda45",
			   "#3368dc",] 

		sticker = tk.Label(self.f_borde_general, 
							   bg=self.FONDO,
							   image=ZOMBI_FACE)
		#sticker.pack(side=tk.TOP,pady = (5,0))
		#color = ["#F4F036","#ff4f69","#F4F036","#FE5173","#FEA4E1"]
		tamanio = [30,40,30,30,40]
		for nro,n in enumerate(texto):
			tit_nombre = tk.Label(f_tit, 
								   bg=self.FONDO,
								   text=n,
								   font=("Fixedsys", tamanio[nro]),
								   relief=tk.FLAT,
								   fg=color[nro],)
								  
			tit_nombre.pack(side=tk.TOP,pady = (5,0))
			
		boton_volver.grid(row = 0, 
						  column = 0, 
						  sticky = "nw",
						  padx = 5, 
						  pady = (20, 0))

		sticker.grid(row = 0, 
					 column = 0, 
					 sticky = "n",
					 padx = 5, 
					 pady = (10, 0))

		bton = tk.Button(self.f_borde_general, 
						bg="#90EE90",
						padx = 20,
						anchor = "w",
						cursor = "hand2",
						image = ESPIA_H_2,
						compound=tk.RIGHT,
						text="ACEPTAR LA MISION",
						font=("Fixedsys", 20),
						relief=tk.FLAT,
						fg= "#4D4D4D",
						command = self.resetear_juego)
		bton.bind("<Enter>", lambda x: x.widget.configure(bg = "#91FA6B",fg="#2F2F2F"))
		bton.bind("<Leave>", lambda x: x.widget.configure(bg="#90EE90",fg="#4D4D4D"))
		
		f_tit.grid(row=1,column=0,sticky="nswe")
		bton.grid(row=2,column=0,sticky="n", pady = 50)		
		self.f_borde_general.grid(row=0,column=0,padx = 100)
		
	def poblarVentana(self):
		

		self.AMARILLO = "#F8F859"
		self.AZUL = "#5E7E9C"

		self.VERDE = "#35926e"
		self.NARANJA = "#FFAB62"
		self.ROJO = "#FF4B4B"
		
		BORDE = "#FFFFFF"

		self.scrollable_frame.rowconfigure(0, weight = 1)
		self.scrollable_frame.columnconfigure(0, weight = 1)
		
		self.f_borde_general = tk.Frame(self.scrollable_frame, bg=self.FONDO)
	
		self.f_borde_general.rowconfigure(0, weight = 1)
		self.f_borde_general.columnconfigure(0, weight = 1)

		self.f_sup = tk.Frame(self.f_borde_general,bg=self.FONDO)
		
		normal_1   = "#FFC0CB"
		normal_2   = "#292929"
		resaltar_1 = "#FFFFFF"
		resaltar_2 ="#868686"
		resaltar_letra = "#444444"
		presionar  = resaltar_1
		fuente = ("Fixedsys", 17)
		boton_volver = Notificaciones.BtnRetro(self.f_sup, boton = {"texto":  "VOLVER", 
																	 "label_height":   1, 
																	 "fuente": 		  fuente,
																	 "normal_1" :      normal_1,
																	 "normal_2" :      normal_2,
																	 "resaltar_1":     resaltar_1,
																	 "resaltar_2":     resaltar_2,
																	 "resaltar_letra": resaltar_letra,
																	 "presionar" :     presionar,
																	 "param"     :     False, 
																	 "accion":         self.salir,
																	 "borde" : 4
																	 })		
		TAMAÑO_SCORE = 30
		score_recompensa = tk.Label(self.f_sup, 
							  bg=self.FONDO,
							  image = COFRE,
							  padx = 20,
							  compound=tk.LEFT,
							  textvariable=self.recompensa,
							  font=("Fixedsys", TAMAÑO_SCORE),
							  relief=tk.FLAT,
							  fg="gold",)
		score_derrotados= tk.Label(self.f_sup, 
							  bg=self.FONDO,
							  image = ZOMBI,
							  padx = 20,
							  compound=tk.LEFT,
							  textvariable=self.derrotados,
							  font=("Fixedsys", TAMAÑO_SCORE),
							  relief=tk.FLAT,
							  fg="#9CC99C",)							  
		score_nivel= tk.Label(self.f_sup, 
							  bg=self.FONDO,
							  image = NIVEL,
							  padx = 20,
							  compound=tk.LEFT,
							  textvariable=self.nivel,
							  font=("Fixedsys", 30),
							  relief=tk.FLAT,
							  fg="#A7CCD8",)		
		
		self.botones_score = [score_recompensa,score_derrotados,score_nivel]
				  
		self.f_contenedor = tk.Frame(self.f_borde_general, bg = self.FONDO)

		self.objeto_enemigo = Enemigo(self.f_contenedor,1, atacar=self.ataque_al_jugador)
		self.objeto_jugador = Jugador(self.f_contenedor, derrota=self.game_over, enemigo=self.objeto_enemigo, victoria = self.prox_enemigo)
		
		self.objeto_enemigo.grid(row=0,column=0,sticky="nw",padx = 10, pady = 20)
		self.objeto_jugador.grid(row=0,column=1,sticky="nw",padx = 10, pady = 20)
		
		self.objeto_jugador.objeto_ataques.stop_clock()
		
		
		boton_volver.grid(row = 0, 
						  column = 0, 
						  sticky = "nw",
						  padx = (20,35), 
						  pady = (20, 0))
		
		score_recompensa.grid(row = 0, 
						  column = 1, 
						  sticky = "nw",
						  padx = 5, 
						  pady = (20, 0))
		score_derrotados.grid(row = 0, 
						  column = 2, 
						  sticky = "nw",
						  padx = 5, 
						  pady = (20, 0))
		score_nivel.grid(row = 0, 
						  column = 3, 
						  sticky = "nw",
						  padx = 5, 
						  pady = (20, 0))

		self.f_sup.grid(row = 0, 
						column = 0, 
						sticky = "nw",
						pady  = 5)

		#self.f_contenedor.grid(row=0,column=0,)
		self.f_contenedor.grid(row=1,column=0,sticky="n")
		self.f_borde_general.grid(row=0,column=0,sticky="n")	

	def ataque_al_jugador(self):
		self.objeto_jugador.recibir_danio(self.objeto_enemigo.ataque)
	

	def llamar_prox_enemigo(self,*args):
		try:
			self.ventana_mensaje.destroy()
		except:
			pass
		self.objeto_jugador.objeto_ataques.resetear()
		self.objeto_jugador.inmunidad=False
		#self.objeto_jugador.objeto_ataques.start_clock()

		
	def prox_enemigo(self, *args):
		self.contador_dificultad+=1
		if self.contador_dificultad == self.prox_dificultad:
			self.contador_dificultad=0
			self.dificultad+=1
			self.prox_dificultad += self.dificultad
		self.nivel.set(self.dificultad)			
		self.after(2500,self.preguntar_prox)
		


	def reproducir_sonido(self,ruta):
		x = threading.Thread(target=lambda:PlaySound(self.ruta_sonido + ruta, SND_FILENAME | SND_ASYNC))
		x.daemon=True
		x.start()
		
	def preguntar_prox(self):
		ruta = f'/victoria.wav'
		self.reproducir_sonido(ruta)
		self.recompensa.set(self.recompensa.get()+self.objeto_enemigo.recompensa)
		self.derrotados.set(self.derrotados.get()+1)
		
		self.objeto_enemigo.reset_enemigo(self.nivel.get())
		
		boton = {"fuente":("Fixedsys", 17),"texto": " NO ","accion":self.salir, "normal_2" :"#A2A2A2", "resaltar_2" :"#4D4D4D", "boton_2": {"texto": " SI ","fuente":("Fixedsys", 17), "accion":self.llamar_prox_enemigo,"normal_2" :"#6EED9A", "resaltar_2" :"#4D4D4D"}}
		self.ventana_mensaje = Notificaciones.pregunta(self.winfo_toplevel(),fuente_pregunta=("Fixedsys", 17),ruta_icono='iconos\\espada.png', fondo="#88C3D6", pregunta="¿NOS ENFRENTAMOS AL PROXIMO ENEMIGO?", titulo="VICTORIA!", boton= boton,accion_al_cierre = self.llamar_prox_enemigo)	






if __name__ == "__main__":
	raiz = tk.Tk()
	raiz.columnconfigure(0, weight = 1)
	o=ventanaJuego(raiz, bg="#222323")
	o.pack(expand=True, fill=tk.BOTH)
	#o.game_over()
	raiz.mainloop()
	print('number of current threads is ', threading.active_count())
	print(threading.enumerate())
