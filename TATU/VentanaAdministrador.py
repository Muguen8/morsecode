import tkinter as tk
from tkinter import ttk
import PIL
from PIL import Image, ImageTk
import CajonGeneral
from ScrollFrame import ScrollableFrame
import json



class administrador(tk.Frame):
	def __init__(self, maestro, **kwargs):
		super().__init__(maestro, **kwargs)

		self.maestro = maestro
		self.maestro.protocol("WM_DELETE_WINDOW", self.protocolo_cerrar_ventana)


	def poblar(self):
		f_contenedor = self
		
		self.rowconfigure(0, weight = 0)
		self.rowconfigure(1, weight = 1)
		self.columnconfigure(0, weight = 1)
		self.columnconfigure(1, weight = 0)
