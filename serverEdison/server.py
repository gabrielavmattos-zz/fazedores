import subprocess
import os
import socket
HOST = '192.168.43.168'          # Endereco IP do Servidor
PORT = 5000                     # Porta que o Servidor esta
udp = socket.socket()

udp.bind((HOST,PORT))
udp.listen(5)

while True:
        conn, addr = udp.accept()
        print(str(addr))
        msg = conn.recv(1024)
        if (len(msg) > 0):
                print (msg)
                nomeA = "saida.py"
                arquivo = open(nomeA, 'w')
                arquivo.write(msg)
                arquivo.close()
                said = execfile("saida.py")
                print (said)
udp.close()
