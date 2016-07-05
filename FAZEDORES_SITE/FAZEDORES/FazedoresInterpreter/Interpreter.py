# -*- coding: utf-8 -*- 	

import socket
import string

HOST = '192.168.43.168'
PORT = 5000
	
class Interpreter():
	
	dataInput = []
	dataOutput = []
	symbolTable = {}
	devicesTable = {}
	portsAnalog = []
	portsDigits = [] 
	error = 0
	i = 0
	msgError = ""
	tokensDeclaration = ("constante", "declare")
	tokensCmdSetup = ("ativar")
	tokensCmdLoop = ("ligar", "esperar", "desligar", "definirCor", "escrever")
	# Definição dos dipositivos digitais que podem ser utilizados
	tokensDeviceDigits = ("luz", "led", "som", "buzzer", "botao", "sensortoque")
	# Definição dos dispositivos analógicos que podem ser utilizados
	tokensDeviceAnalogs = ("sensortoque", "potenciometro", "sensortemperatura", "sensorluz")
	types = ("literal", "inteiro", "real", "logico")


	def __init__(self, dataInput):

		#print(dataInput)
		dataInput += '\r\n'
		self.dataOutput = []
		self.setDataOutput("import mraa")

		if (dataInput.find("esperar") != -1):
			self.setDataOutput("import time")
		if (dataInput.find("lcd") != -1):
			self.setDataOutput("import pyupm_i2clcd as lcd")
		dataInput = self.replaceBT(dataInput)
		dataInput = dataInput.split('\n')
		self.setDataInput(dataInput)
		self.deleteLines()
		print(self.dataInput)


	def setDataInput(self, dataInput):
		self.dataInput = dataInput

	def setDataOutput(self, line):
		self.dataOutput.append(line)

	def getDataOutput(self):
		if (self.error):
			# retorna para a view
			print([False, self.msgError])
			return [False, self.msgError]
		else:

			saida = ""
			for i in self.dataOutput:
				saida += i + "\n"
			try: 
				servidorSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			
				resposta = servidorSocket.sendto(saida, (HOST, PORT))
				servidorSocket.close()	
				return[True, saida]			
			except:
			
				print ("Sem conexão")
				return [True,saida]

	def setMsgError(self, msgError):
		self.error = 1
		self.msgError = "Erro(linha %d): %s" % (self.i + 1,msgError)
		print (self.msgError)
		self.getDataOutput()

	def replaceBT(self, dataInput):
		aux = ""
		for i in range(0, len(dataInput)-1):
			print("'"+dataInput[i]+"'")
			if (dataInput[i] == '\t' or dataInput[i] == '\r'): 
				aux += ' '
			else:
				aux += dataInput[i]
		return aux
		

	def deleteLines(self):
		try:
			while (self.dataInput.index('')):
				self.dataInput.remove('')
		except:
			pass
		try:
			while (self.dataInput.index('\t')):
				self.dataInput.remove('\t')
		except:
			pass
		try:
			while (self.dataInput.index(' ')):
				self.dataInput.remove(' ')
		except:
			pass

		try:
			while (self.dataInput.index('\r')):
				self.dataInput.remove('\r')
		except:
			pass



	def startInterpreter(self):

		self.setDataOutput("")

		# vai para declaracoes		
		while (self.declarations()):
			pass
		else:	
			if (not self.cmdLoop()):
				return False
			else:	
				self.setDataOutput("")
				return self.getDataOutput()

	def removeSpaces(self, dataInput):
		
		aux = ""

		for i in dataInput:
			if (i in ["(",")",",", "<", "-"]):
				aux += "@"
			elif ((not i == " ") and (not i == "\t")):
				aux += i
		return aux

	def declarations(self):
		"""
		declaracao_local : 'declare' variavel
			| 'constante' IDENT  ':'  tipo_basico '=' valor_constante
			;
		"""	
	
		line = self.dataInput[self.i].split(' ')
		print ("adbahbsda")
		print (line)

		j = 0
		if (line[j] in self.tokensDeclaration):
			if (line[j] == "declare"):
				j += 1
				if (not self.validateVar(line, j)):
					return False
			elif (line[j] == "constante"):
				j += 1
				if (not self.validateConst(line, j)):
					self.setMsgError("Constante "+line[j]+" inválida.")
					return False
			else:
				self.setMsgError("Comando "+line[j]+" incorreto.")
				return False	
			self.i += 1
			return True
		elif(line[0] == "comando_setup"):
			#self.i += 1
			# vai parar comandos_setup
			if (not self.cmdSetup()):
				return False 		
		else:
			#self.setMsgError("O comando "+line[j]+" não é reconhecido.")
			return False


	def cmdSetup(self):

		"""
		comandoSetup	: 'ativar' '(' dispositivo ',' pino ')'
				;
		"""
		print("setup")
		#try:
		#	if (self.dataInput[self.i].index(' ')):
		dataInputWithoutSpaces = self.removeSpaces(self.dataInput[self.i])
		line = dataInputWithoutSpaces.split('@')
		print (line)
		if (line[0] == "comando_setup"):
			self.i += 1			
			j = 0
			dataInputWithoutSpaces = self.removeSpaces(self.dataInput[self.i])
			print("Esse "+ self.dataInput[self.i] +".")
			line = dataInputWithoutSpaces.split('@')
			while (line[j] in self.tokensCmdSetup and self.i < len(self.dataInput)):			
				print (line)				
				if (line[j] == "ativar"):
					j = j+1
					if(line[j] in self.tokensDeviceDigits):
						j = j+1;
						if(self.validatePinDevice(line,j,0)):
							pass
						else:
							self.setMsgError("Pino "+line[j]+" inválido.\nDica: \n- 0 a 3 portas analogicas\n- 4 a 8 são portas digitais\n- 5 e 6 são portas PWM\n- 21 porta I2C (usada para o LCD)\n")
							return False
					elif (line[j] in self.tokensDeviceAnalogs):
						#print (line[j])
						j = j+1;
						if(self.validatePinDevice(line,j,1)):
							pass
						else:
							self.setMsgError("Pino "+line[j]+" inválido.")
							return False
					elif (line[j] == 'lcd'):
						if(self.validatePinDevice(line,j, 2)):
							print(line[j])
							pass
						else:
							self.setMsgError("Pino "+line[j]+" inválido.")
							return False
						
					else:
						self.setMsgError("Comando incorreto no escopo comando_setup.")
						return False 
	
				else:
					self.setMsgError("Comando incorreto no escopo comando_setup.")
					return False

				self.i += 1
				if(self.i < len(self.dataInput)-1): 
					dataInputWithoutSpaces = self.removeSpaces(self.dataInput[self.i])
					line = dataInputWithoutSpaces.split('@')
					j = 0

			if ("fim_comando_setup" in self.dataInput[self.i]):
				self.i += 1
				return True	
			else:
				print("Aqui " + self.dataInput[self.i] +".")
				self.setMsgError("Comando 'fim_comando_setup' não encontrado!")
				return False
		else:	
			self.setMsgError("Comando 'comando_setup' não encontrado.")
			return False


	def cmdLoop(self):
		""" 
		cmdLoop : ('ligar' | 'desligar') '(' dispositivoSaida ',' pino  (',' volt)? ')'
			| IDENT '<-' 'ler' '(' dispositivoEntrada ',' pino ')'
			| 'esperar' '(' tempo ')'
			| comandoLCD
			;
		"""
		indentation = 1
		dataInputWithoutSpaces = self.removeSpaces(self.dataInput[self.i])
		line = dataInputWithoutSpaces.split('@')
		line = self.dataInput[self.i].split(' ')		
		#print (line)		
		if (line[0] == "comando_loop"):
			self.i += 1			
			dataInputWithoutSpaces = self.removeSpaces(self.dataInput[self.i])
			#print(dataInputWithoutSpaces)
			line = dataInputWithoutSpaces.split('@')
			
			print (line)
			j = 0
			self.setDataOutput("while True:")
			while (line[j] in self.tokensCmdLoop or line[j] in self.symbolTable):
				print ("Linha atual: " + line[j])
				if (self.cmdOutput(line, j, indentation)):
					pass 	
		
				elif (line[j] in self.symbolTable):
					print("here")
					self.cmdInput(line, j, indentation)
					
				elif (self.cmdSleep(line, j, indentation)):
					pass

				elif (self.cmdLCD(line, j, indentation)):
					pass		
										
				else:
					self.setMsgError("Comando '"+line[j]+"' não reconhecido.")
					return False
					
				self.i += 1		
				dataInputWithoutSpaces = self.removeSpaces(self.dataInput[self.i])
				line = dataInputWithoutSpaces.split('@')
				j = 0	
			else:
				print("Aqui" + line[j])
				if ("fim_comando_loop" in self.dataInput[self.i]):
					return True	
				else:
					#self.setMsgError("Comando '"+line[j]+"' não reconhecido.")
					return False

		else:
			#self.setMsgError("Comando "+line[0]+" não reconhecido.")
			return False
	
	def cmdOutput(self, line, j, indentation):
		if (line[j] == "ligar"):
			j = j + 1
			if(line[j+1].isdigit()):
				idDevice = line[j]+line[j+1]
			else: 
				if(line[j+1] in self.symbolTable):
					if (self.symbolTable[line[j+1]][1] == 'inteiro'):
						idDevice = line[j]+str(self.symbolTable[line[j+1]][2])
					else:
						self.setMsgError("Comando 'ligar' deve passar um valor inteiro.")
						return False
					
				else:
								self.setMsgError("Comando 'ligar' utilizado em dispositivo errado.")
								return False
			print(idDevice)

			if (idDevice in self.devicesTable):
				if (self.devicesTable[idDevice][0] == 'pwm'):
					if(len(line) > 4):
						if (line[3].isdigit()):
							#print ("Tá aqui")
							self.setDataOutput("\t"*indentation + idDevice + ".write("+line[3]+"/255.0)")					
							self.devicesTable[idDevice][2] = 'ativo'			
						elif(line[3] in self.symbolTable):
							if (self.symbolTable[line[3]][1] == 'inteiro'):
								self.setDataOutput("\t"*indentation + idDevice + ".write("+line[3]+"/255.0)")
								self.devicesTable[idDevice][2] = 'ativo'			
							else: 
								self.setMsgError("Comando 'ligar' em pwm deve passar um valor inteiro.")
								return False
						else:
							self.setMsgError("Comando 'ligar' em pwm deve passar um valor inteiro.")
							return False
					elif (self.devicesTable[idDevice][2] == 'desativo'):
						#print ("aui " +line[2]) 
						self.setDataOutput("\t"*indentation + idDevice + ".write(1)")
						self.devicesTable[idDevice][2] = 'ativo'
	
				elif (self.devicesTable[idDevice][0] == 'digitsIN'):
					if (self.devicesTable[idDevice][2] == 'desativo'):
						self.setDataOutput("\t"*indentation + idDevice + ".write(1)")
						self.devicesTable[idDevice][2] = 'ativo' 
				elif (self.devicesTable[idDevice][0] == 'digitsOUT'):
					if(len(line) > 4):
						if (line[3].isdigit()):
							self.setDataOutput("\t"*indentation + idDevice + ".write("+line[3]+"/255.0)")					
							self.devicesTable[idDevice][2] = 'ativo'			
						elif(line[3] in self.symbolTable):
							if (self.symbolTable[line[3]][1] == 'inteiro'):
								self.setDataOutput("\t"*indentation + idDevice + ".write("+line[3]+"/255.0)")
								self.devicesTable[idDevice][2] = 'ativo'			
							else: 
								self.setMsgError("Comando 'ligar' em pwm deve passar um valor inteiro.")
								return False
						else:
							self.setMsgError("Comando 'ligar' em pwm deve passar um valor inteiro.")
							return False
					elif (self.devicesTable[idDevice][2] == 'desativo'):
						#print ("aui " +line[2]) 
						self.setDataOutput("\t"*indentation + idDevice + ".write(1)")
						self.devicesTable[idDevice][2] = 'ativo'
				else:						
					self.setMsgError("Comando 'ligar' utilizado em dispositivo errado.")
					return False

			else:
				return False

		elif (line[j] == "desligar"):
			#print (line)
			j = j + 1
			if(line[j+1].isdigit()):
				idDevice = line[j]+line[j+1]
			else: 
				if(line[j+1] in self.symbolTable):
					idDevice = line[j]+str(self.symbolTable[line[j+1]][2])
					
					
				else:
								self.setMsgError("Comando 'desligar' utilizado em dispositivo errado.")
								return False
			#print(idDevice)
			if (idDevice in self.devicesTable):
				if (self.devicesTable[idDevice][0] in ('pwm', 'digitsOUT')):
					if (self.devicesTable[idDevice][2] == 'ativo'):
						self.setDataOutput("\t"*indentation + idDevice + ".write(0)")
						self.devicesTable[idDevice][2] = 'desativo'
				else:						
					self.setMsgError("Comando 'ligar' utilizado em dispositivo errada.")
					return False

			else:
				return False

		else:
				return False
		return True
			
	def cmdInput(self, line, j, indentation):

		output = line [j] + " = "
		j += 1
		if (len(line[j]) == 0):
			j += 1
			if(line[j] == 'ler'):
				j += 1
				if (line[j] in ('botao', 'sensortoque')):

					if(line[j+1].isdigit()):

						idDevice = line[j]+line[j+1]
					else: 
						if(line[j+1] in self.symbolTable):
							if (self.symbolTable[line[j+1]][1] == 'inteiro'):
								idDevice = line[j]+str(self.symbolTable[line[j+1]][2])
							else:			
								self.setMsgError("Comando 'ler' utilizado em dispositivo errado.")
								return False
						else:			
							self.setMsgError("Comando 'ler' utilizado em dispositivo errado.")
							return False
					print(self.devicesTable)
					if (idDevice in self.devicesTable):		
						if (self.devicesTable[idDevice][0] == 'digitsIN'):
							self.setDataOutput("\t"*indentation + output + idDevice + ".read()")
						else:
							self.setMsgError("Pino incorreto.")
							return False
	
					else:
						self.setMsgError("Pino informado não encontrado.")
						return False
	
				elif(line[j] in self.tokensDeviceAnalogs):

					if(line[j+1].isdigit()):
						idDevice = line[j]+line[j+1]
					else: 
						if(line[j+1] in self.symbolTable):
							if (self.symbolTable[line[j+1]][1] == 'inteiro'):
								idDevice = line[j]+str(self.symbolTable[line[j+1]][2])
							else:			
								self.setMsgError("Comando 'ler' utilizado em dispositivo errado.")
								return False
						else:			
							self.setMsgError("Comando 'ler' utilizado em dispositivo errado.")
							return False
								
					if (idDevice in self.devicesTable):

						if (self.devicesTable[idDevice][0] == 'analogic'):

							self.setDataOutput("\t"*indentation + output + idDevice + ".readFloat()")
						else:
							self.setMsgError("Pino incorreto.")
							return False
	
					else:
						self.setMsgError("Pino informado não encontrado.")
						return False
					
				else:
					self.setMsgError("Comando 'ler' utilizado em dispositivo errado.")
					return False
		else:
			return False


						
	def cmdSleep(self, line, j, indentation):
		if (line[j] == "esperar"):
			j = j+1

			if (line[j] in self.symbolTable):
				if (self.symbolTable[line[j]][1] in ('inteiro', 'real')):
					self.setDataOutput("\t"*indentation +"time.sleep("+line[j]+")")
					return True
				else: 
					self.setMsgError("Tempo deve ser númerico.")
					return False
			try: 
				time = int(line[j])
				self.setDataOutput("\t"*indentation +"time.sleep(%d)" % time)
				return True
			except:
				try: 
					time = float(line[j])
					self.setDataOutput("\t"*indentation +"time.sleep(%f)" % time)
					return True
				except:

					self.setMsgError("Tempo deve ser númerico.")
					return False

					
			else:
				self.setMsgError("Tempo deve ser númerico.")
				return False

		
		else:
			return False

	def cmdLCD(self, line, j, indentation):

		"""
		comandoLCD		: 'definirCor' '(' lcd ',' pino ',' cor ')'
					| 'escrever' '(' lcd ',' pino ',' (CADEIA | IDENT) ')'
					;
		"""
		if(line[j] == 'definirCor'):
			j += 1
			if (line[j] == 'lcd'):
				if(line[j+1].isdigit()):
					idDevice = line[j]+line[j+1]
				elif(line[j+1] in self.symbolTable):
					if (self.symbolTable[line[j+1]][1] == 'inteiro'):
						idDevice = line[j]+str(self.symbolTable[line[j+1]][2])
					else:			
						self.setMsgError("Comando 'lcd' utilizado em dispositivo errado.")
						return False
				else:			
					self.setMsgError("Comando 'lcd' utilizado em dispositivo errado.")
					return False

				if (idDevice in self.devicesTable):
					if (self.devicesTable[idDevice][0] == 'lcd'):
						try:
							c1 = int(line[j+3])
							c2 = int(line[j+4])
							c3 = int(line[j+5])
							
							if (c1 < 225 and c1>0 and c2 < 225 and c2 > 0 and c3 < 225 and c3 > 0):
								pass										
							else:
								self.setMsgError("Cores incorretas.")
								return False
						except:
							self.setMsgError("As cores devem ser números inteiros.")
							return False								

					else:
						self.setMsgError("Pino incorreto.")
						return False

				else:
					self.setMsgError("Pino informado não encontrado.")
					return False

			else:
				self.setMsgError("Comando 'definirCor' utilizado em dispositivo errado.")
				return False
		elif (line[j] == 'escrever'):
			j += 1
			if (line[j] == 'lcd'):
				if(line[j+1].isdigit()):
					idDevice = line[j]+line[j+1]
				elif(line[j+1] in self.symbolTable):
					if (self.symbolTable[line[j+1]][1] == 'inteiro'):
						idDevice = line[j]+str(self.symbolTable[line[j+1]][2])
					else:			
						self.setMsgError("Comando 'lcd' utilizado em dispositivo errado.")
						return False
				else:			
					self.setMsgError("Comando 'lcd' utilizado em dispositivo errado.")
					return False
				if (idDevice in self.devicesTable):
					if (self.devicesTable[idDevice][0] == 'lcd'):
						self.setDataOutput("\t"*indentation + idDevice + ".write("+line[j+2]+")")							
							#else:
							#	self.msgError = "Cores incorretas."
							#	return False					

					else:
						self.setMsgError("Pino incorreto.")
						return False

				else:
					self.setMsgError("Pino informado não encontrado.")
					return False

			else:
				self.setMsgError("Comando 'definirCor' utilizado em dispositivo errado.")
				return False
		else:
			self.setMsgError("Comando "+ line[j]+ " incorreto.")
			return False
			
		return True;
	
	def validatePinDevice(self, line, j, typeP):
		"""
			Porta utilizada não ser analógica/digital, depende do dispositivo;
			- 4 a 8 são portas digitais (led, som, luz, botão)
			- 5, 6 são portas PWM (led, som, luz)
			- 0, 1, 2, 3 portas analógicas (potenciômetro, sensor de toque)
			- 21 porta I2C (usada para o LCD)
			- Portas 'ativar' repetidas;
		"""
		# typeP = 1 deviceInput
		self.portsAnalog = ['0', '1', '2', '3']
		self.portsDigits = ['4', '5', '6', '7', '8'] 

		if (typeP == 2): 
			j+= 1
			if(line[j] == '21'):				
				idDevice = line[j-1]+line[j]
				if (not idDevice in self.devicesTable):
					self.devicesTable[idDevice] = ['lcd', line[j], ""]
					self.setDataOutput(idDevice + " = lcd.Jhd1313m1(1, 0x3E, 0x62)")
					self.setDataOutput(idDevice + ".setCursor(0,0)")			
				
			elif (line[j] in self.symbolTable.keys()):
				line[j] = str(self.symbolTable[line[j]][2])
				if (line[j] == '21' ):
					idDevice = line[j-1]+line[j]
					self.devicesTable[idDevice] = ['lcd', line[j], ""]
					self.setDataOutput(idDevice + " = lcd.Jhd1313m1(1, 0x3E, 0x62)")
					self.setDataOutput(idDevice + ".setCursor(0,0)")
			
					
		elif(typeP == 1):
			if (line[j] in self.portsAnalog):
				idDevice = line[j-1]+line[j]
				if (not idDevice in self.devicesTable):
					self.devicesTable[idDevice] = ['analogic', line[j], ""]
					self.setDataOutput(idDevice + " = mraa.Aio(" + line[j] +")")
					self.portsAnalog.remove(line[j])	
				else:
					return False
						
							
			elif (line[j] in self.symbolTable.keys()):
				line[j] = str(self.symbolTable[line[j]][2])
				if (line[j] in self.portsAnalog):
					idDevice = line[j-1]+line[j] 
					if (not idDevice in self.devicesTable):
						self.devicesTable[idDevice] = ['analogic', line[j], ""]
						self.setDataOutput(idDevice + " = mraa.Aio(" + line[j]+")")
						self.portsAnalog.remove(line[j])		
					else:
						return False						
			else:	
				return False
		else:	
			if (line[j] in self.portsDigits):
				if (line[j-1] in ('botao', 'sensortoque')):
					idDevice = line[1]+line[2]
					if (not idDevice in self.devicesTable):
						self.devicesTable[idDevice] = ['digitsIN', line[2], ""]
						self.setDataOutput(idDevice + " = mraa.Gpio(" + line[2]+")")
						self.setDataOutput(idDevice + ".dir(mraa.DIR_IN)")
						self.portsDigits.remove(line[j])
					else:
						return False
				else:					
					if (line[j]  in ('5', '6')):
						idDevice = line[1]+line[2]
						if (not idDevice in self.devicesTable):
							self.devicesTable[idDevice] = ['pwm', line[2], "desativo"]
							self.setDataOutput(idDevice + " = mraa.Pwm(" + line[2] +")")
							self.setDataOutput(idDevice +".period_us(700)")
							self.setDataOutput(idDevice +".enable(True)")
							self.portsDigits.remove(line[j])	
						else:
							return False
						
					else:			
						idDevice = line[1]+line[2]
						if (not idDevice in self.devicesTable):	
							self.devicesTable[idDevice] = ['digitsOUT', line[2], "desativo"]	
							self.setDataOutput(idDevice + " = mraa.Gpio(" + line[2]+")")
							self.setDataOutput(idDevice + ".dir(mraa.DIR_OUT)")
							self.portsDigits.remove(line[j])	
						else:
							return False
			
			elif (line[j] in self.symbolTable.keys()):
				print("Ol")
				if (str(self.symbolTable[line[j]][2]) in self.portsDigits):
					line[j] = str(self.symbolTable[line[j]][2])
					
					if (line[j-1] in ('botao', 'sensortoque')):
						idDevice = line[1]+line[j]
						if (not idDevice in self.devicesTable):
							self.devicesTable[idDevice] = ['digitsIN', line[2], ""]
							self.setDataOutput(idDevice + " = mraa.Gpio(" + line[2]+")")
							self.setDataOutput(idDevice + ".dir(mraa.DIR_IN)")
							self.portsDigits.remove(line[2])	
						else:
							return False
					else:					
						if (line[j]  in ('5', '6')):
							idDevice = line[1]+line[j]
							if (not idDevice in self.devicesTable):
								self.devicesTable[idDevice] = ['pwm', line[2], "desativo"]
								self.setDataOutput(idDevice + " = mraa.Pwm(" + line[2] +")")
								self.setDataOutput(idDevice +".period_us(700)")
								self.setDataOutput(idDevice +".enable(True)")
								self.portsDigits.remove(line[2])		
							else:
								return False
						
						else:			
							idDevice = line[1]+line[j]
							if (not idDevice in self.devicesTable):	
								self.devicesTable[idDevice] = ['digitsOUT', line[2], "desativo"]	
								self.setDataOutput(idDevice + " = mraa.Gpio(" + line[2]+")")
								self.setDataOutput(idDevice + ".dir(mraa.DIR_OUT)")
								self.portsDigits.remove(line[2])		
							else:
								return False
	
			else:	
				#print (symbolTable)
				return False
			#print ("output")
			
		return True
		
	def validateVar(self, line, j):
		"""
			variavel: IDENT  dimensao  mais_var  ':' tipo
		
		"""

		isIdent, symbol = self.validateIdent(line[j])
		if (isIdent):
			if(':' in line[j]):
				line[j] = line[j][:len(line[j])-1]
			j = j+1
			isValue, value = self.validateValue(line[j], '0')
			if (line[j] in self.types and isValue):	
				self.symbolTable[symbol] = ["var", line[j], value]
				self.setDataOutput(symbol +" = "+ str(value))
				print(self.symbolTable)
				return True
			else: 
				self.setMsgError("Verifique a variavel "+line[j-1]+" e seu tipo "+line[j]+".")
				return False
			
		else: 
			self.setMsgError("Verifique a variavel "+line[j-1]+" e seu tipo "+line[j]+".")
			
			return False
			
					
	

	def validateConst(self, line, j):
		"""
			 'constante' IDENT  ':'  tipo_basico '=' valor_constante
		"""
		isIdent, symbol = self.validateIdent(line[j])
		if (isIdent):
			if(':' in line[j]):
				line[j] = line[j][:len(line[j])-1]
			j += 1

			isValue, value = self.validateValue(line[j], line[j+2])
			if (line[j] in self.types and line[j+1] == '=' and isValue):				
				print(line[j])
				self.symbolTable[symbol] = ["const", line[j], value]
				self.setDataOutput(symbol +" = "+ str(value))
				return True
			else:
				return False		
		
		else:
			return False

		return True

	def validateIdent(self, line):
		"""

			// Definindo o identificador:
			IDENT       : ('a'..'z' | 'A'..'Z' | '_') ('a'..'z' | 'A'..'Z' | '0'..'9' | '_')*;	
		"""
		print(line)
		if (line[0].isalpha() or line[0] == '_'):
			if(line[len(line)-1:len(line)] == ':'):
				symbol = line.split(':')[0]
				if (symbol in self.symbolTable.keys()):
					return [False, ""]
		
				for i in symbol:
					if (not i.isalpha() and not i in string.digits and not i == '_'):
						return [False, ""]		
			else:
				return [False, ""]
		else:

			return [False, ""]
		return [True, symbol]
	
	def validateValue(self, typeS, value):

		if (typeS == "inteiro"):
			try:
				value = int(value)
				return [True, value]
			except:
				return [False, ""]
				
		elif (typeS == "literal"):
			try:
				value = str(value)
				return [True, value]
			except:
				return [False, ""]
		elif (typeS == "logico"):
			try:
				value = bool(value)
				return [True, value]
			except:
				return [False, ""]
		elif (typeS == "real"):
			try:
				value = float(value)
				return [True, value]
			except:
				return [False, ""]
		else:
			return [False, ""]

	def __del__(self):
		print("etejabsdadba")

		self.symbolTable.clear()
		self.devicesTable.clear()
		del self.portsAnalog
		del self.portsDigits 
		del self.dataOutput
		del self.dataInput
		
			
