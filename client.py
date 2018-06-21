import socket
from sys import argv
import sys
import re

def main():
	if len(argv) != 3 or not argv[2].isdigit():
		print("usage: python3 client.py <server name> <server port>")
		return 1

	hostname, serverTCPPort = argv[1], int(argv[2])
	print("Client is running...")
	print("Remote host: {}, remote TCP port: {}".format(hostname, serverTCPPort))
	port = int(serverTCPPort)
	port = int(port)
	# Prompt user for their name
	name = raw_input("What is your name?\n")

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serverhost = socket.gethostname()
	print("Server hostname is: " + serverhost)
	s.connect((hostname, port))

	#sends name to server
	s.sendall(name.encode()) 
	hello = s.recv(10)
	print(hello)
	#data = s.recv(1024)

	while True:
		#Receiving the UDP port on TCP 
		udpPort = s.recv(15)
		#print("Received UDP port ".format(udpPort))
		print ('Received UDP port: ' + udpPort)
		if not udpPort:
			break

		break
	#Create a UDP socket
	UDPc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)	
	end = False

	#Game loop
	while True:
		#Validating user input before starting game
		choice = raw_input("Enter 'start' to begin the game, 'guess' to guess the letter in word, 'end' to finish the game, 'exit' to exit the game entirely and close all TCP and UDP \nports.\nIf the entire word is spelled out during the guessing phase, then you win and \npress enter to continue.\n\n")
		cmd = choice[:5]
		valid_commands = ['start', 'end', 'guess', 'exit']


		while True:
			valid_msg_types = ["instr", "stat", "end", "na", "bye"]
			if cmd == 'start':
				UDPc.sendto(choice, (hostname, int(udpPort)))

			elif cmd == 'guess':
				UDPc.sendto(choice, (hostname, int(udpPort)))

			elif cmd == 'exit':
				bye = 'bye'
				UDPc.sendto(choice, (hostname, int(udpPort)))
				print("Closing TCP and UDP sockets...")
				s.close()
				UDPc.close()
				sys.exit(0)

			elif choice == 'end':
				print("Ending game...")
				#end = "The game will now terminate. \n"
				UDPc.sendto(choice.encode(), (address[0],int(address[1])))

			elif (cmd or choice) not in valid_commands:
				UDPc.sendto(choice.encode(), (address[0],int(address[1])))

			print('Sending command to server...')
			
			UDPdata, address = UDPc.recvfrom(1024)

			if UDPdata[:3] == 'end':
				#receiving end message from server
				# UDPdata, address = UDPc.recvfrom(1024)
				print(UDPdata)
				end = True
				UDPdata, address = UDPc.recvfrom(1024)
				break
			elif UDPdata[:5] == 'instr':
				print(UDPdata)

				#receiving instr message from server
				UDPdata, address = UDPc.recvfrom(1024)
				print(UDPdata)	
				# UDPdata, address = UDPc.recvfrom(1024)
				# print(UDPdata)
				break

			elif UDPdata[:4] == 'stat':
				#receiving stat message from server
				# UDPdata, address = UDPc.recvfrom(1024)
				print(UDPdata)
				break

			elif UDPdata[:2] == 'na':
				#receiving na message from server
				# UDPdata, address = UDPc.recvfrom(1024)
				print(UDPdata)

			else:
				break	

			
			break
	#Close sockets
	print("Closing TCP and UDP sockets...")
	s.close()
	UDPc.close()

if __name__ == "__main__":
	main()

