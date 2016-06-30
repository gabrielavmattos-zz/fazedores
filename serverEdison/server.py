import socket
HOST = '192.168.0.225'              # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
orig = (HOST, PORT)
udp.bind(orig)
while True:
    msg, cliente = udp.recvfrom(1024)

    if (msg == "esquerda"):
	print "esquerda"
	
    if (msg == "direita"):
	print "direita"
    print cliente, msg
udp.close()
