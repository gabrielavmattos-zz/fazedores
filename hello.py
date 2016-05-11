#!/usr/bin/env python
# -*- coding: utf-8 -*- 


#import mraa
import sys
import string
import time

# Possibilidades:
# LED porta
# BUZZER porta
# LCD frase


# Objetivo: fazer um interpretador de comandos básicos para interagir com componentes do kit grove e a galileo
# TO DO:
# - LED
# - LCD
# - BUZZER
# - Usar uma interface grafica pra permitir que a pessoa digite (EasyGUI)

def interpretador(msg):

	msg = msg.lower()
	print msg
	pos = 0
	begin = 0
	sair = 1
	while pos != -1 and sair:

		pos = msg.find('\n',begin)
		if (pos == -1):
			pos = len(msg)
			sair = 0
		print "posicao"+str(pos)
		linha =  msg[begin:pos+1]
		print "linha  "+linha
		identificaPalavra(linha[0:pos])
		begin = pos + 1
		
		
		 

	
def identificaPalavra(linha):

	pos = linha.find(' ')
	
	if pos == -1:
		print ("O comando digitado está incorreto, faltam informações.")
	else:
		token = linha[0:pos]

		print "token '"+token+"'"
	
		if token == "ligarled" or token == "ligarluzinha":

			print("Digitou led")
			print "porta" + linha[pos:]
			usarLed(linha[pos+1:],1)

		elif token == "desligarled" or token == "deligarluzinha":
			usarLed(linha[pos+1:],0)

		elif token == "ligarBuzzer" or token == "ligarSom":
			print("Digitou som")
			usarLed(linha[pos+1:],1)


		elif token == "desligarBuzzer" or token == "desligarSom":
			print("Digitou som")
			usarLed(linha[pos+1:],0)
			
		elif token == "ligarLcd":
			print("Digitou lcd")
			usarLcd(linha[pos+1:])

		elif token == "esperar":
			print("Usar o sleep")
			tempo = int(linha[pos+1:])
			time.sleep(tempo)
	
		else:
			print "Erro encontrado na palavra " + token + "."

	
def usarLed(porta, bit):

	print "porta "+porta
	led = mraa.Gpio(porta)
	led.dir(mraa.DIR_OUT)
	led.write(bit)


def usarBuz(porta):

	print "porta "+porta
	led = mraa.Gpio(porta)
	led.dir(mraa.DIR_OUT)
	led.write(bit)

#janela de ajuda e confirmação
msg = "\n\nVocê vai entrar agora no mundo mágico do IoT, deseja iniciar sua vida maker? \n S - SIM \n N - NAO \n A - Aprender sobre a LN\n\nDigite sua opção:   "
opcao = 1
while opcao:
	#reply =  easygui.buttonbox(msg, title, choice)
	reply = raw_input(msg).upper()
	if reply == "S" :
		#janela para inserção de texto
		msg = 'Entre com seu código para rodar na placa:'
		#entrada = easygui.textbox(msg, title='Interpretador de LN-IoT', text = '', codebox = 0)
		entrada = raw_input(msg)		
		interpretador(entrada)
		opcao = 0
	elif reply == "A":
		#janela para ajuda
		msg = "\n\nA linguagem LN permite que você seja um iniciante \"maker\". \nNessa primeira versão é possível você brincar com o LED, Buzzer e com o LCD. \n\n 1) Usando o LED: \n O LED é o dispositivo que permite acender e apagar uma luz \n - Para ligar o LED é preciso usar a funcao ligarled ou ligarluzinha em seguida a porta em que você conectou o LED. \n Ex: ligarled 5 \n - Para desligar o LED é preciso usar a funcao desligarled ou desligarluzinha em seguida a porta em que você conectou o LED. \n Ex: desligarled 5  \n\n 2) Usando o Buzzer: \n O Buzzer é o dispositivo que permite fazer barulho. \n- Para ligar o Buzzer é preciso usar a funcao ligarbuzzer ou ligarsom em seguida a porta que você conectou o buzzer.\n  Ex: ligarSom 3\n - Para desligar o Buzzer é preciso usar a funcao desligarbuzzer ou desligarsom em seguida a porta que você conectou o buzzer.\n  Ex: desligarSom 3\n\n 3) Função esperar: \n A função esperar vai permitir que você mande a luz ou som ficar ligado alguns segundos e depois desligar. Primeiro é necessário digitar a palavra esperar e depois o tempo de espera em segundos \n Ex: esperar 5\n"
		reply = raw_input(msg)
		
	else:

		#janela para saida
		msg = "Até mais, amiguinho!"
		print msg
		#easygui.msgbox(msg, 'AtéMais!')
		opcao = 0
