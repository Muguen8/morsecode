# BuscandoPort
import serial
import serial.tools.list_ports
import time
import CajonGeneral


HANDSHAKE = "{milo}"
SALUDO    = "{tatu}"
EXIT_CONN = "{piolin}"
BAUDIOS   = 9600

S_MSJ ="("
F_MSJ =")"

def enviar_handshake(conn_arduino):
	bandera=True
	for n in range(0, 3):
		msj = HANDSHAKE + "\n"
		print("ENVIANDO HANDSHAKE : "+msj)
		try:
			val = conn_arduino.write(msj.encode("ascii"))
			time.sleep(0.5)
			bandera=True
		except Exception as e:
			bandera=False
	return bandera

def probar_puerto(puerto):
	INTENTOS=2
	try:
		conn_arduino = serial.Serial(puerto, 
									 BAUDIOS, 
									 timeout= 2,) 
		# print(conn_arduino) Serial<id=0x18d14610710, open=True>(port='COM4', baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=5, xonxoff=False, rtscts=False, dsrdtr=False)
		for n in range(0,INTENTOS):
			val = conn_arduino.readline()
			val = val.decode("ascii")
			val = val.strip()
			if len(val) > 0:
				print("MENSAJE RECIBIDO :: ", val, val == SALUDO)
				if val == SALUDO:
					conn_arduino.close()
					return puerto
					break
		conn_arduino.close()
	except Exception as e:
		print("Error ", e)
		return False



def reiniciar(puerto):
	##try:
	##	conn_arduino = serial.Serial(puerto, 
	##								 BAUDIOS, 
	##								 timeout= 2,) 
	##	msj = RESET + "\n"
	##	val = conn_arduino.write(msj.encode())
	##	time.sleep(0.2)
	##	print("REINCIANDO PUERTO :: ", puerto)
	##	val = conn_arduino.readline()
	##	val = val.decode("ascii")
	##	val = val.strip()
	##	
	##	if len(val) > 0:
	##		print("MENSAJE RECIBIDO :: ", val, val == SALUDO)
	##		if val == HANDSHAKE:
	##			conn_arduino.close()
	##			return puerto
	##		else:
	##			conn_arduino.close()
	##			return False
	##	
	##except Exception as e:
	##	print("Error ", e)
	##	return False
	pass
	
	
def buscar_puerto(comlist):
	print("LISTA DE PUERTOS :: ", comlist)
	for element in comlist:
		puerto = probar_puerto(element.device)
		if puerto:
			print("ARDUINO CONECTADO AL PUERTO ::: ", puerto)
			return puerto
			
def reinciar_puertos(comlist):
	print("REINICIAR ....... ")
	for element in comlist:
		puerto = reiniciar(element.device)
		if puerto:
			print("ARDUINO CONECTADO AL PUERTO ::: ", puerto)
			return puerto

def lista_puertos():
	return serial.tools.list_ports.comports()
	
def buscar():
	comlist = lista_puertos()
	puerto_arduino  = buscar_puerto(comlist)
	if not puerto_arduino:
		puerto_arduino = reinciar_puertos(comlist)
	return puerto_arduino

def conectar(puerto):
	if puerto:
		print("Arduino conectado al puerto :: ", puerto)
		INTENTOS = 5
		try:
			conn_arduino = serial.Serial(puerto, 
										 BAUDIOS, 
										 timeout= 2,) 
			conn = False
			for n in range(0,INTENTOS):
				val = conn_arduino.readline()
				val = val.decode("ascii")
				val = val.strip()
				if len(val) > 0:
					print("Esperando SALUDO :: ", val)
					if val == SALUDO:
						msj = SALUDO + "\n"
						val = conn_arduino.write(msj.encode())
						conn = conn_arduino
						#enviar_handshake(conn)
						break
					else:
						print(f"Error al conectar ... Mensaje no coincide con SALUDO\n\tSALUDO: {SALUDO}\n\tRECIBIDO: {val}")
						conn = False
			return conn_arduino
		except Exception as e:
			print("Error al conectar ... " + "Fallo el intento de conectar :: ", e)
			return False


def avisar_exit_conn(conn_arduino):
	for n in range(0,5):
		print("ENVIANDO EXIT_CON :: ", EXIT_CONN)
		msj = EXIT_CONN + "\n"
		val = conn_arduino.write(msj.encode("ascii"))
		time.sleep(0.3)

def recolectar_data_entrante():
	#time.sleep(1)
	if not CajonGeneral.RECOLECTAR_DATA:
		return
	try:
		while CajonGeneral.CONN_ARDUINO:
			try:
				val = CajonGeneral.CONN_ARDUINO.readline()
			except serial.serialutil.PortNotOpenError():
				CajonGeneral.CONN_ARDUINO = False
				return
			try:
				val = val.decode("ascii")
				val = val.strip()
				if len(val) > 0:
					if val[0] == S_MSJ and val[-1] == F_MSJ:
						print("*--->  incoming data :: ", val)
						try:
							CajonGeneral.BUFFER += val[1:-1]
						except IndexError:
							return ""
					else:
						print("Data error. Valor :: ", val)
						pass
			except Exception as e:
				print("Error en lectura de data entrante :: ", e, val)
				pass
			finally:
				time.sleep(0.3)
	except:
		avisar_exit_conn(CajonGeneral.CONN_ARDUINO)
		CajonGeneral.CONN_ARDUINO = False
		return
			
def leer_data_entrante(conn_arduino):
	#time.sleep(1)
	if conn_arduino:
		val = conn_arduino.readline()
		try:
			val = val.decode("utf-8")
			val = val.strip()
			if len(val) > 0:
				if val[0] == S_MSJ and val[-1] == F_MSJ:
					#print("*--->  incoming data :: ", val)
					try:
						return val[1:-1]
					except IndexError:
						return ""
				else:
					#print("Data error. Valor :: ", val)
					return False
		except Exception as e:
			print("Error en lectura de data entrante :: ", e, val)
			return False
	else:
		self.avisar_exit_conn(conn_arduino)
		return False
	#conn_arduino.close()


def leer_keyevent(*args):
	while not CajonGeneral.CONN_ARDUINO:
		print(args)
		time.sleep(0.3)

def cerrar_conn(conn_arduino):
	print("..............CERRANDO CONEXION")
	try:
		avisar_exit_conn(conn_arduino)
	except:
		pass
	try:
		conn_arduino.close()
	except:
		pass



if __name__ == "__main__":
	for p in buscar():
		probar_puerto(p)
