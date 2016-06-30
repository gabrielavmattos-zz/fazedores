import string

class Interpreter():

	dataOutput = []
	symbolTable = {}
	devicesTable = {}
	error = 0
	i = 0
	msgError = ""
	tokensDeclaration = ("constante", "declare", "tipo")
	tokensCmdSetup = ("ativar")
	tokensCmdLoop = ("ligar", "esperar", "desligar", "definirCor", "escrever")
	# Definição dos dipositivos digitais que podem ser utilizados
	tokensDeviceDigits = ("luz", "led", "som", "buzzer", "botao", "sensortoque")
	# Definição dos dispositivos analógicos que podem ser utilizados
	tokensDeviceAnalogs = ("sensortoque", "potenciometro", "sensortemperatura", "sensorluz")
	types = ("literal", "inteiro", "real", "logico")


	def __init__(self, dataInput):		
		self.dataInput = dataInput.split('\n')

	def setDataInput(self, dataInput):
		self.dataInput = dataInput

	def setDataOutput(self, line):
		self.dataOutput.append(line)

	def getDataOutput(self):
		if (self.error):
			# retorna para a view
			return self.msgError
		else:
			# conexão via socket com intel edison

			# se a conexao funcionar manda mensagem de ok
			# senão mostra mensagem que compilou, mas não existe uma conexão ativa.
			return self.dataOutput

	def setMsgError(self, msgError):
		self.error = 1
		self.msgError = msgError
		print ("Erro(linha %d): %s" % (self.i + 1,self.msgError))
		self.getDataOutput()


	def startInterpreter(self):

		self.setDataOutput("import mraa")
		self.setDataOutput("import time")

		# vai para declaracoes		
		while (self.declarations()):
			pass

		# vai parar comandos_setup
		if (not self.cmdSetup()):
			return False

		# vai parar comandos_loop		
		if (not self.cmdLoop()):
			return False

		self.getDataOutput()
		return True

	
	def removeSpaces(self, dataInput):
		
		aux = ""

		for i in dataInput:
			if (i in ["(",")",","]):
				aux += "@"
			elif (not i == " "):
				aux += i
		return aux


	def declarations(self):
		"""
		declaracao_local : 'declare' variavel
			| 'constante' IDENT  ':'  tipo_basico '=' valor_constante
			;
		"""	
	
		line = self.dataInput[self.i].split(' ')
		j = 0
		if (line[j] in self.tokensDeclaration):
			if (line[j] == "declare"):
				j += 1
				if (not self.validateVar(line, j)):
					self.setMsgError("Variavel "+line[j]+" inválida.")
					return False
			elif (line[j] == "constante"):
				j += 1
				if (not self.validateConst(line, j)):
					#self.setMsgError("Constante "+line[j]+" inválida.")
					return False
			else:
				return False	
			self.i += 1
			return True
		else:
			return False


	def cmdSetup(self):

		"""
		comandoSetup	: 'ativar' '(' dispositivo ',' pino ')'
				;
		"""

		dataInputWithoutSpaces = self.removeSpaces(self.dataInput[self.i])
		line = dataInputWithoutSpaces.split('@')
		if (line[0] == "comando_setup"):
			self.i += 1			
			j = 0
			print(line)
			dataInputWithoutSpaces = self.removeSpaces(self.dataInput[self.i])
			line = dataInputWithoutSpaces.split('@')
			while (line[j] in self.tokensCmdSetup and self.i < len(self.dataInput)):			
				print (line)				
				if (line[j] == "ativar"):
					j = j+1
					if(line[j] in self.tokensDeviceDigits):

						#### aquiiii #####
						print (line[j])
						j = j+1;
						# 
						if(self.validatePinDevice(line,j, 0)):
							print(line[j])
						else:
							self.setMsgError("Pino "+line[j]+" inválido.\nDica: \n- 0 a 3 portas analogicas\n- 4 a 8 são portas digitais\n- 5 e 6 são portas PWM\n- 21 porta I2C (usada para o LCD)\n")
							return False
					elif (line[j] in self.tokensDeviceAnalogs):
						print (line[j])
						j = j+1;
						if(self.validatePinDevice(line,j, 1)):

						#### aquiiii #####
							print(line[j])
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

			if (self.dataInput[self.i] == "fim_comando_setup"):
				return True	
			else:
				self.setMsgError("Comando 'fim_comando_setup' não encontrado!")
				return False
		else:	
			self.setMsgError("Comando 'comando_setup' não encontrado!")
			return False


	def cmdLoop(self):
		""" 
		cmdLoop : ('ligar' | 'desligar') '(' dispositivoSaida ',' pino  (',' volt)? ')'
			| IDENT '<-' 'ler' '(' dispositivoEntrada ',' pino ')'
			| 'esperar' '(' tempo ')'
			| comandoLCD
			;
		"""

		dataInputWithoutSpaces = self.removeSpaces(self.dataInput[self.i])
		line = dataInputWithoutSpaces.split('@')

		line = self.dataInput[self.i].split(' ')
		
		print (line)		
		if (line[0] == "comando_loop"):
			self.i += 1			
			line = self.dataInput[self.i].split(' ')
			j = 0
			while (line[j] in self.tokensCmdLoop or line[j] in self.symbolTable):
				if (line[j] == "ligar"):

						#### aquiiii #####
					print ("ligar")
				#elif (line[j] in ...) #verificar se tá na tabela de simbolos:
					
				elif (cmdSleep(line, j)):
					pass

				elif (cmdLCD(line, j)):
					pass		
										
				else:
					self.msgError = ""
					return False
					
				i = i + 1			
				line = self.dataInput[i].split(' ')

			if (self.dataInput[i] == "fim_comando_loop"):
				self.i = i				
				return True	
			else:
				return False

		else:
			self.setMsgError("Comando 'comando_loop' não encontrado.")
			return False


	def cmdSleep(self, line, j):
		if (line[j] == "esperar"):
			j = j+1
			if (line[j][0] == '(' and line[j][len(line[j])-1] == ')'):
					try: 
						time = int(line[j][1:len(line[j])])
						self.setDataOutput("time.sleep(0.%d)" % time)
					except:
						self.setMsgError("Tempo deve ser númerico.")
						return False
			else:
				self.setMsgError("")
				return False
		else:
			return False

	def cmdLCD(self, line, j):

		"""
		comandoLCD		: 'definirCor' '(' lcd ',' pino ',' cor ')'
					| 'escrever' '(' lcd ',' pino ',' (CADEIA | IDENT) ')'
					;
		"""

						#### aquiiii #####
		return True;
	
	def validatePinDevice(self, line, j, typeP):
		"""
			Porta utilizada não ser analógica/digital, depende do dispositivo;
			- 4 a 8 são portas digitais (led, som, luz, botão)
			- 5, 6 são portas PWM (led, som, luz, botão)
			- 0, 1, 2, 3 portas analógicas (potenciômetro, sensor de toque)
			- 21 porta I2C (usada para o LCD)
			- Portas 'ativar' repetidas;
		"""
		# typeP = 1 deviceInput
		portsAnalog = ['0', '1', '2', '3']
		portsDigits = ['4', '5', '6', '7', '8'] 

		if(typeP):
			j += 1
			if ((line[j] in portsAnalog)):
							
			
			elif (line[j] in self.symbolTable.keys()):
				if (self.symbolTable[line[j]] in portsAnalog)):	
					#print aqui			
			else:	
				print (symbolTable)
				return False
			print ("input")
		else:	
			if ((line[j] in portsDigits)):
					#print aqui			
			
			elif (line[j] in self.symbolTable.keys()):
				if (self.symbolTable[line[j]] in portsDigits)):	
					#print aqui			
			else:	
				print (symbolTable)
				return False
			print ("output")
			
		return True
		
	def validateVar(self, line, j):
		"""
			variavel: IDENT  dimensao  mais_var  ':' tipo
		
		"""

		isIdent, symbol = self.validateIdent(line, j)
		if (isIdent):
			if(':' in line):
				line.remove(':')
			j = j+1
			if (line[j] in self.types):				
				self.symbolTable[symbol] = ["var", line[j], ""]
				return True
			else: 
				return False
			
		else:
			return False
			
					
	

	def validateConst(self, line, j):
		"""
			 'constante' IDENT  ':'  tipo_basico '=' valor_constante
		"""

		isIdent, symbol = self.validateIdent(line, j)		
		if (isIdent):
			if(':' in line):
				line.remove(':')
			j = j+1
			if (len(line) >= 5):
				isValue, value = self.validateValue(line[j], line[j+2])
				if (line[j] in self.types and line[j+1] == '=' and isValue):				
					self.symbolTable[symbol] = ["const", line[j], value]
					return True
				else:
					return False		
			else: 
				return False
			
		else:
			return False

		return True

	def validateIdent(self, line, j):
		"""

			// Definindo o identificador:
			IDENT       : ('a'..'z' | 'A'..'Z' | '_') ('a'..'z' | 'A'..'Z' | '0'..'9' | '_')*;	
		"""
		if (line[j][0].isalpha() or line[j][0] == '_'):
			if(line[j][len(line[j])-1:len(line[j])] == ':' or line[j+1] == ':'):
				symbol = line[j].split(':')[0]
		
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


string1 = "declare gabi : inteiro\nconstante gabi1: inteiro = 10\ncomando_setup\nativar(led, pinSom)\nativar(som, pinSom)\nfim_comando_setup"
teste1 = Interpreter(string1)
teste1.startInterpreter()
