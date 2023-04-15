import os
import json


diccionario_morse = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    #"CH": "----",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "Ñ": "--.--",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "0": "-----",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    ".": ".-.-.-",
    ",": "--..--",}


palabras = ['tio','abu','mami','papa','pupo','tatu','milo','abre','sapo','amar','ando', 'años', 'aran', 'aras', 'arda', 'ardo', 'aren', 'ares', 'arme', 'asan', 'asas', 'asee', 'asen', 'aseo', 'ases', 'aspe', 'atas', 'ates', 'aves', 'ayas', 'bala', 'bañe', 'bisa', 'boas', 'boba', 'boja', 'bojo', 'bosa', 'boto', 'boya', 'boyo', 'cabe', 'cace', 'caen', 'caer', 'calo', 'case', 'cave', 'cayo', 'ceda', 'cede', 'cedo', 'cefo', 'ceno', 'cesa', 'coge', 'come', 'crea', 'cuba', 'dañe', 'deja', 'dijo', 'dime', 'dome', 'dora', 'dore', 'dura', 'echa', 'echo', 'ecos', 'egos', 'emes', 'enes', 'Enya', 'eran', 'eras', 'eres', 'esas', 'eses', 'eñes', 'fico', 'fumo', 'gato', 'goda', 'Guam', 'hace', 'haga', 'hago', 'hala', 'haya', 'hice', 'hile', 'hube', 'hubo', 'huna', 'huya', 'Iban', 'iban', 'ibas', 'ices', 'idas', 'idos', 'izas', 'jade', 'Kiev', 'lees', 'lega', 'Lima', 'loas', 'luca', 'lusa', 'mala', 'Mali', 'mazo', 'mece', 'mees', 'mesa', 'mese', 'meso', 'meto', 'mide', 'moja', 'mojo', 'mola', 'more', 'moza', 'moño', 'muca', 'nace', 'ndea', 'Niue', 'note', 'nuda', 'nuez', 'nula', 'odas', 'ojos', 'olas', 'opta', 'opte', 'oras', 'oren', 'ores', 'orno', 'orzo', 'osas', 'osea', 'osen', 'oses', 'osos', 'pace', 'peca', 'peco', 'pele', 'peos', 'Peña', 'pide', 'poca', 'pode', 'pone', 'poya', 'pude', 'pudo', 'pule', 'pura', 'puso', 'raen', 'rapa', 'rato', 'rece', 'reme', 'reta', 'reza', 'rezo', 'rial', 'riza', 'roce', 'roja', 'roso', 'royo', 'rozo', 'rusa', 'sabe', 'salo', 'sane', 'sedo', 'sera', 'seso', 'señe', 'sido', 'sola', 'spot', 'suba', 'sube', 'suda', 'sudo', 'supo', 'tale', 'temo', 'teta', 'time', 'tiño', 'Togo', 'tome', 'tosa', 'toza', 'trae', 'tuve', 'tuvo', 'unan', 'unen', 'unes', 'urda', 'urdo', 'usad', 'usas', 'usen', 'uses', 'usos', 'uvas', 'uñan', 'uñas', 'vaga', 'vaya', 'vete', 'vira', 'vota', 'vote', 'Yuba', 'zaca', 'ñuta', 'ñuto', 'ala', 'are', 'ase', 'ato', 'ayo', 'Ayo', 'bes', 'cae', 'del', 'Don', 'fes', 'fui', 'hoy', 'iba', 'ice', 'ida', 'ido', 'ira', 'lee', 'lis', 'loa', 'ojo', 'ore', 'pin', 'rae', 'rea', 'ten', 'une', 'usa', 'uve', 'ven', 'veo', 'ves', 'voy', 'pipo']

ruta_save_data = f"{os.path.abspath(os.path.dirname(__file__))}/config/data_config"
ruta_data_base = f"{os.path.abspath(os.path.dirname(__file__))}/config/data_base"



abecedario = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N','Ñ', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z','0','1','2','3','4','5','6','7','8','9']

				

SCORE_recompensa = False
SCORE_derrotados = False
SCORE_nivel      = False
SCORE_rubies     = False


CONN_ARDUINO = False
HILO_LECTURA = False
RECOLECTAR_DATA = False
FUNC_CAMBIAR_VENTANA=False
BUFFER = r""""""
USUARIO = "tatu"
ruta_save_data = f"{os.path.abspath(os.path.dirname(__file__))}/config/data_config"
ruta_data_base = f"{os.path.abspath(os.path.dirname(__file__))}/config/data_base"

DATA_CONFIG = {}
DATA_BASE = {}

with open(ruta_save_data,"r") as archivo:
	DATA_CONFIG = json.load(archivo)

with open(ruta_data_base,"r") as archivo:
	DATA_BASE = json.load(archivo)
	
FONDO = "#222323"
def limpiar_buffer():
	global BUFFER
	BUFFER = r""""""

diccionario_morse = DATA_BASE["diccionario_morse"]
diccionario_to_morse = dict(zip(diccionario_morse.values(),diccionario_morse.keys(),))
palabras = DATA_BASE["palabras"]
cuentos  = DATA_BASE["cuentos"]

#d = """'.-', '-...', '-.-.', '----', '-..', '.', '..-.', '--.', '....', '..', '.---', '-.-', '.-..', '--', '-.', '--.--', '---', '.--.', '--.-', '.-.', '...', '-', '..-', '...-', '.--', '-..-', '-.--', '--..', '-----', '.----', '..---', '...--', '....-', '.....', '-....', '--...', '---..', '----.', '.-.-.-', '--..--'"""
#print((",").join([n.strip().replace("'",'"') for n in str(list(diccionario_morse.values())).split(",")]))


paleta = [
		"#7f708a",
		"#9babb2",
		"#c7dcd0",
		"#ffffff",
		"#6e2727",
		"#b33831",
		"#ea4f36",
		"#f57d4a",
		"#ae2334",
		"#e83b3b",
		"#fb6b1d",
		"#f79617",
		"#f9c22b",
		"#7a3045",
		"#9e4539",
		"#cd683d",
		"#e6904e",
		"#fbb954",
		"#4c3e24",
		"#676633",
		"#a2a947",
		"#d5e04b",
		"#fbff86",
		"#165a4c",
		"#239063",
		"#1ebc73",
		"#91db69",
		"#cddf6c",
		"#313638",
		"#374e4a",
		"#547e64",
		"#92a984",
		"#b2ba90",
		"#0b5e65",
		"#0b8a8f",
		"#0eaf9b",
		"#30e1b9",
		"#8ff8e2",
		"#323353",
		"#484a77",
		"#4d65b4",
		"#4d9be6",
		"#8fd3ff",
		"#45293f",
		"#6b3e75",
		"#905ea9",
		"#a884f3",
		"#eaaded",
		"#753c54",
		"#a24b6f",
		"#cf657f",
		"#ed8099",
		"#831c5d",
		"#c32454",
		"#f04f78",
		"#f68181",
		"#fca790",
		"#fdcbb0", 
]


paleta_neon =[
			"#FFD2ED",
			"#3DFF98",
			"#DFDFDF", 
			"#9D7CC5", 
			"#407EFA",
			"#FF4F69",
			"#43F4FF",
			"#FF8142",
			"#FBEF50", 
			]
#import unicodedata
#import re
#def eliminar_acentos(texto):
#	texto = re.sub('ñ',"\001", texto)
#	try:
#		texto = unicode(texto, 'utf-8')
#	except NameError:
#		pass
#	texto = unicodedata.normalize('NFD', texto).encode('ascii', 'ignore').decode("utf-8")
#	texto = re.sub("\001",'ñ', texto)
#	return texto
#
#
#texto_cuentos = {}
#cuentos = {"Bóreas y el Sol": r""" Bóreas y el Sol disputaban sobre sus poderes, y decidieron conceder la palma al que despojara a un viajero de sus vestidos. Bóreas empezó de primero, soplando con violencia; y apretó el hombre contra sí sus ropas, Bóreas asaltó entonces con más fuerza; pero el hombre, molesto por el frío, se colocó otro vestido. Bóreas, vencido, se lo entregó al Sol. Bóreas es el dios del frío viento del Norte en la mitología griega. Este empezó a iluminar suavemente, y el hombre se despojó de su segundo vestido; luego lentamente le envió el Sol sus rayos más ardientes, hasta que el hombre, no pudiendo resistir más el calor, se quitó sus ropas para ir a bañarse en el río vecino.""",
#		   "Diógenes de viaje":r"""Yendo de viaje, Diógenes el cínico llegó a la orilla de un río torrencial y se detuvo perplejo. Un hombre acostumbrado a hacer pasar a la gente el río, viéndole indeciso, se acercó a Diógenes, lo subió sobre sus hombros y lo pasó complaciente a la otra orilla. Quedó allí Diógenes, reprochándose su pobreza que le impedía pagar a su bienhechor. Y estando pensando en ello advirtió que el hombre, viendo a otro viajero que tampoco podía pasar el río, fue a buscarlo y lo transportó igualmente. Entonces Diógenes se acercó al hombre y le dijo: -No tengo que agradecerte ya tu servicio, pues veo que no lo haces por razonamiento, sino por manía.""",}
#
#for n in cuentos:
#	txt = eliminar_acentos(cuentos[n])
#	texto_cuentos[n] = txt
#	
#
#DATA_BASE ={}
#DATA_BASE["diccionario_morse"]=diccionario_morse
#DATA_BASE["palabras"]=palabras
#DATA_BASE["cuentos"]=texto_cuentos
#
#
#with open(ruta_data_base,"w") as archivo:
#	data = json.dumps(DATA_BASE, indent=3)
#	archivo.write(data)
#	print("save")
#
