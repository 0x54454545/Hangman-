#Server
import socket
from sys import argv
from random import *
from game import *


def main():
  # Parse command line args
  if len(argv) != 2:
    print("usage: python3 server.py <word to guess or '-r' for random word>")
    return 1

  print("Server is running...")

  HOST = ''                 # Symbolic name meaning all available interfaces
  PORT = 0              # Arbitrary non-privileged port
  TCPs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  port = int(PORT)
  TCPs.bind((HOST, PORT))
  sockName = TCPs.getsockname()
  print("The server is listening on port: ",sockName)
  TCPs.listen(1)
  #conn, addr = s.accept()
  #print 'Connected by', addr

  try:
    #First while loop
    while True:
      #Accept the TCP connection
      print("Waiting for a new client...")
      conn, addr = TCPs.accept()
      print("A new client is connected to the server!")
      print ('Connected by', addr)
      clientTCPport = addr[1]

      #TCP Loop
      #Second While loop
      while True:
      #Loop to continously reads in from TCP port

        #Keeps listening if it doesn't receive a hello message
        #receives name from server
        data = conn.recv(10)

        #Extracts username handling empty case
        print("User's name: " + data)
        sendHello = ("Hello " + str(data) + "!\n")
        conn.sendto(str(sendHello).encode(), (addr[0], int(addr[1])))
        #Creating UDP socket
        print("Creating UDP socket...")
        UDPs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        UDPs.bind(('', 0))

        #Timeout after 2 mins
        UDPs.settimeout(120)
        
        udpSockName = UDPs.getsockname()[1]
        print("Client will receive port number: "+str(udpSockName))
        print("Sending UDP port number to client using TCP connection...")
        conn.sendto(str(udpSockName), (addr[0], int(addr[1])))

         #"The UDP socket has port number ".format(udpSockName) 
        break
        #conn.sendall(data)
        #conn.sendto(str(udpSockName), (addr[0], int(addr[1])))
      
      

      active = False #Game not active by default

      #Game (UDP) loop
      #Third While Loop
      while True:
        try:
          #receive on UDP port here
          UDPdata, address = UDPs.recvfrom(128)
          UDPdata = UDPdata.lower()
          print(UDPdata)
          UDPdataGuess = UDPdata[:5]

          valid_commands = ['start', 'end', 'guess', 'exit']
          #valid_msg_types = ["instr", "stat", "end", "na", "bye"]

        except socket.timeout:
          print("Ending game due to timeout...")
          break

        if UDPdata == 'start':
          #Game startup
          active = True
          word, word_blanks, attempts, win = gameSetup(argv)
          print("Hidden Word: {}".format(word))
          print("Starting game...")

          #Start msg to send to client
          #UDPs.sendto('instr'.encode(), (address[0],int(address[1])))

          instr = """instr This is hangman. You will guess one letter at a time. If the letter is in the hidden word, the "-" will be replaced by the correct letter. Guessing multiple letters at a time will be considered as guessing the entire word (which will result in either a win or loss automatically - win if correct, loss if incorrect). You win if you either guess all of the correct letters or guess the word correctly. You lose if you run out of attempts. Attempts will be decremented in the case of an incorrect or repeated letter guess.\n\n"""
          UDPs.sendto(instr.encode(), (address[0],int(address[1])))
          
          #UDPs.sendto('stat'.encode(), (address[0],int(address[1])))

          i = "instr Word: " + str(word_blanks) + " Attempts left: " + str(attempts) + "\n"
          UDPs.sendto(i.encode(), (address[0],int(address[1])))

          
        
        elif UDPdataGuess == 'guess':
          active = True
          #UDPdata, address = UDPs.recvfrom(1024)
          try:
            # print("This is the word so far: " + word)
            
            # print("This is word_blank: " + word_blanks)
            if UDPdata == 'guess':
              errorMsg = "Incorrect format. Enter guess followed by the letter you want to guess (Example:guess e)\n"
              UDPs.sendto(errorMsg.encode(), (address[0],int(address[1])))
            else:

              guess = UDPdata[6:]
              print("This is the word so far: " + word)
            
              print("This is word_blank: " + word_blanks)
              print("This is what guess prints: " + guess + "\n")
              word_blanks, attempts, win = checkGuess(word, word_blanks, attempts, guess, win)
              
              #sends stat msg to client to let client know the stats
              #UDPs.sendto('stat'.encode(), (address[0],int(address[1])))

              # f = "stat Word: " + str(word_blanks) + " Attempts left: " + str(attempts) + "\n"
              # UDPs.sendto(f.encode(), (address[0],int(address[1])))

              #len(guess) is to guess the whole word
              if len(guess) > 1 and not win or attempts == 0 or win:

                print win
                win = str(win)

                if win == '1' or win == 'True':
                  print("this is win: " + win)
                  #sending end msg to client


                  winCondition = ("end You won! The word was " + word + ". Enter start to play again!\n")
                  UDPs.sendto(winCondition.encode(), (address[0],int(address[1])))

                  active = False
                  

                elif win == '0' or win == 'False' or attempts == 0:
                  print("This is lose: " + win)

                  loseCondition = ("end You lost. The word was " + word + ". Enter start to play again!\n")
                  UDPs.sendto(loseCondition.encode(), (address[0],int(address[1])))

                  active = False 
                  
                else:
                  continue
              f = "stat Word: " + str(word_blanks) + " Attempts left: " + str(attempts) + "\n"
              UDPs.sendto(f.encode(), (address[0],int(address[1])))

          except NameError:
              nError = "You must start the game first!!!!"
              UDPs.sendto(nError.encode(), (address[0],int(address[1])))

          except IndexError:
              iError = "The string is too long/short. Please enter in 'guess' preceded by the letter you want to \nguess"
              UDPs.sendto(iError.encode(), (address[0],int(address[1])))

        elif UDPdata == 'end':
          active = True
          print("User choose to end this game")
          UDPs.sendto('end'.encode(), (address[0],int(address[1])))
       
          end = "The game will now terminate. \n"
          UDPs.sendto(end.encode(), (address[0],int(address[1])))
  
          active = False
 
        elif UDPdata == 'exit':
          print("Client has ended session.")
          break
        elif UDPdata not in valid_commands:
          UDPs.sendto('na'.encode(), (address[0],int(address[1])))
          NA = "na Server does not recognize your command."
          UDPs.sendto(NA.encode(), (address[0],int(address[1])))
      #break

  except KeyboardInterrupt:
    print("Closing TCP and UDP sockets...")
    conn.close()
    UDPs.close()

  ###########################################

if __name__ == "__main__":
  main()