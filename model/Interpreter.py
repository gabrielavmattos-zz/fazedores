class Interpreter():

	dataOutput = []
	symbolTable = []
	error = 0
	i = 0
	msgError = ""
	tokensDeclaration = ("constante", "declare", "tipo")
	tokensCmdSetup = ("ativar")
	tokensCmdLoop = ("ligar", "esperar", "desligar", "definirCor", "escrever")
	tokensDeviceOutput = ("luz", "led", "som", "buzzer")
	tokensDeviceInput = ("botao", "sensortoque", "potenciometro")


	def __init__(self, dataInput):		
		dataInputWithoutSpaces = self.removeSpaces(dataInput)
		self.dataInput = dataInputWithoutSpaces.split('\n')

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
			return self.dataOutput


	def setMsgError(self, msgError):
		error = 1
		self.msgError = msgError
		print ("Erro(linha %d): %s" % (self.i + 1,self.msgError))
		self.getDataOutput()


	def startInterpreter(self):

		# vai para declaracoes		
		while (self.declarations()):
			print("decl")
		# vai parar comandos_setup
		if (not self.cmdSetup()):
			return False
		
		if (not self.cmdLoop()):
			return False

		self.getDataOutput()
		return True

	
	def removeSpaces(self, dataInput):
		
		aux = ""

		for i in dataInput:
			if(i in ["(",")",","]):
				aux += "@"
			elif(not i == " "):
				aux += i
		return aux


	def declarations(self):
		i = self.i
		line = self.dataInput[i].split(' ')
		if (line[0] in self.tokensDeclaration):
			##
			i = i + 1
		else:
			self.i = i
			return False


	def cmdSetup(self):

		"""
		comandoSetup	: 'ativar' '(' dispositivo ',' pino ')'
				;
		"""

		line = self.dataInput[self.i].split('@')
		if (line[0] == "comando_setup"):
			print ("Entrou cmdSetup")
			self.i += 1			
			line = self.dataInput[self.i].split('@')
			j = 0
			while (line[j] in self.tokensCmdSetup and self.i < len(self.dataInput)):			
				print (line)				
				if (line[j] == "ativar"):
					j = j+1
					if(line[j] in self.tokensDeviceOutput):
						print (line[j])
						j = j+1;
						if(self.validatePinDevice(line[j], 0)):
							print(line[j])
						else:
							self.setMsgError("Pino "+line[j]+" inválido.")
							return False
					elif (line[j] in self.tokensDeviceInput):
						print (line[j])
						j = j+1;
						if(self.validatePinDevice(line[j], 1)):
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
					line = self.dataInput[self.i].split('@')
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
		line = self.dataInput[self.i].split(' ')
		
		print (line)		
		if (line[0] == "comando_loop"):
			self.i += 1			
			line = self.dataInput[self.i].split(' ')
			j = 0
			while (line[j] in self.tokensCmdLoop or line[j] in self.symbolTable):
				if (line[j] == "ligar"):
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
		return True;
	
	def validatePinDevice(self, pin, typeP):
		"""
			Porta utilizada não ser analógica/digital, depende do dispositivo;
			- 0 a 10 são portas digitais (led, som, luz, botão)
			- 3, 5, 3, 6 são portas PWM (led, som, luz, botão)
			- 10 a 20 portas analógicas (potenciômetro, sensor de toque)
			- 21 porta I2C (usada para o LCD)
			- Portas 'ativar' repetidas;
		"""
		# typeP = 1 deviceInput
		if(typeP):
			print ("input")
		else:	
			print ("output")
			
		return True
		
	


string1 = "comando_setup\nativar(led, pinSom)\nativar(soam, pinSom)\nfim_comando_setup"
teste1 = Interpreter(string1)
teste1.startInterpreter()
