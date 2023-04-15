


class Main():
	def __init__(self, FONDO):
		#self.traerIconos()	
		self.objeto_ventana_data_actual= False
		self.directorio = os.path.abspath(os.path.dirname(__file__))
		self.actual = "objeto_ventana_data_actual"
		self.agenda_ventanas = {"objeto_ventana_data_actual": VentanaCurrentData.ventanaDataActual,
								"panel_principal": False,
								"juego"	: VentanaCurrentData.ventanaJuego,
								"traductor": VentanaCurrentData.traductor,
								"maquina": VentanaCurrentData.maquinaMorse,
								"cuento": VentanaCurrentData.tipear,
								"administrador": VentanaAdministrador.administrador,
								}
		CajonGeneral.FUNC_CAMBIAR_VENTANA=self.cambiar_ventana
		#self.abrirCurrentData()

		self.ruta_musica_base = f'{self.directorio}/sonido' + "/musica_espias.wav"
		self.duracion_cancion = 95000
		self.musica_en_reproduccion = False

		self.__construirMenu()
		raiz.state('zoomed')
		raiz.rowconfigure(0, weight = 1)
		raiz.columnconfigure(0, weight = 1)

		self.cambiar_ventana("objeto_ventana_data_actual")

		raiz.mainloop()
		
	def traerIconos(self):
		"Cargamos los ico que vamos a utilizar en el menu"
		pass
	
	def start_musica(self,*args):
		print("###########################  STAR MUSIC  ########################")
		self.stop_musica()
		PlaySound(self.ruta_musica_base, SND_FILENAME | SND_ASYNC)
		self.musica_en_reproduccion = True
		pass
		
	def loop_musica(self, *args):
		print(f"******************* loop : {self.reproducir_musica} ***************************")
		self.stop_musica()
		if self.reproducir_musica:
			if not self.musica_en_reproduccion:
				print(">>>>>>>>>> NEXT LOOP")
				self.start_musica()
				self.reproducir_musica = True
			raiz.after(self.duracion_cancion, self.loop_musica)
		pass
	def stop_musica(self):
		print("-----------------------------  STOP MUSIC  -----------------------------")
		PlaySound(None, SND_ASYNC)
		self.musica_en_reproduccion = False
		pass
	
	def cambiar_ventana(self,prox,destruir=False):
		if prox in ("panel_principal","objeto_ventana_data_actual"):
			self.reproducir_musica = True
			if not self.musica_en_reproduccion:
				self.loop_musica()
		else:
			self.reproducir_musica = False
			self.stop_musica()
			
		conservar = ("panel_principal",)
		if self.actual in conservar:
			self.objeto_ventana_data_actual.pack_forget()
		else:	
			if self.objeto_ventana_data_actual:
				self.objeto_ventana_data_actual.RECOLECTAR_BUFFER = False
				self.objeto_ventana_data_actual.destroy()
		
		if prox in conservar:
			if self.agenda_ventanas[prox]:
				self.objeto_ventana_data_actual = self.agenda_ventanas[prox]
			else:
				self.agenda_ventanas[prox] = VentanaCurrentData.panelPrincipal(raiz, bg = FONDO)
				self.objeto_ventana_data_actual = self.agenda_ventanas[prox]
		else:
			self.objeto_ventana_data_actual = self.agenda_ventanas[prox](raiz, bg = FONDO)

		self.objeto_ventana_data_actual.pack(fill   = tk.BOTH, 
											 expand = True,
											 anchor = "nw",)			
		CajonGeneral.limpiar_buffer()
		activar_leer_data=("maquina","juego","cuento")
		if prox in activar_leer_data:
			self.objeto_ventana_data_actual.RECOLECTAR_BUFFER = True
			self.objeto_ventana_data_actual.recolectar_data_entrante()
		self.actual = prox

	def __construirMenu(self):
		#"Construye un widget menu"
		#self.barraMenu = tk.Menu(raiz)
		#raiz.config(menu = self.barraMenu)
		#
		#"Pestanias"
		#MenuReadCurrentData = tk.Menu(self.barraMenu, tearoff=0)
		#MenuConfigurarPrograma = tk.Menu(self.barraMenu, tearoff=0)		
		#MenuReadImportVisualizeSdData = tk.Menu(self.barraMenu, tearoff=0)		
		#
		#self.barraMenu.add_command(label = "Current Data", 
		#						   command = self.abrirCurrentData)		
		pass
		
		
	def limpiarVentana(self,destruir=False):
		"Eliminar todos los widget excepto el Menu"
		if self.objeto_ventana_data_actual:
			if destruir:
				self.objeto_ventana_data_actual.destroy()
			else:
				self.objeto_ventana_data_actual.pack_forget()
		#except:
		#	pass
		#hijos = raiz.winfo_children()
		#for hijo in hijos:
		#	if type(hijo) != tk.Menu:
		#		if destruir:
		#			hijo.destroy()
		#		else:
		#			try:
		#				hijo.pack_forget()
		#			except:
		#				pass
							
	def abrirCurrentData(self):
		#self.limpiarVentana()
		objeto_ventana_data_actual = self.agenda_ventanas["objeto_ventana_data_actual"](raiz, bg = FONDO)
		objeto_ventana_data_actual.pack(fill   = tk.BOTH, 
								        expand = True,
								        anchor = "n",)


def habilitar(*args):
	CajonGeneral.LEER_KEY = True

		
if __name__ == "__main__":

	# App Tk Ppal
	import tkinter as tk
	import PIL
	from PIL import Image, ImageTk
	import CajonGeneral
	import VentanaCurrentData
	from winsound import *
	import VentanaAdministrador
	import os
	
	CajonGeneral.LEER_KEY = True
	CajonGeneral.CONN_ARDUINO = False
	
	FONDO = CajonGeneral.FONDO
	
	raiz = tk.Tk()
	raiz.configure(bg = FONDO)
	print("MORSE")
	raiz.title("MORSE")
	raiz.iconphoto(True, ImageTk.PhotoImage(file='iconos/app_icon.png'))
	raiz.full_screen = True
	def full(*args):
		raiz.attributes("-fullscreen", raiz.full_screen)
		raiz.full_screen = not raiz.full_screen
	raiz.bind('<F11>', full)

	#raiz.bind_all("<space>", leer_keyevent)
	raiz.minsize(800, 600)
	#raiz.resizable(0, 0)
	Main(FONDO)

#cerrar conexion
#CajonGeneral.CONN_ARDUINO
