
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

  ____________        ____________       ______________       ________     
 | Plain Text | -->  | Public Key | --> | Cipher Text  | --> | TCP/IP | 
  ------------        ------------       --------------       --------     
     _____________       ________        ____________
--> | Cipher Text | --> | Private | --> | Plain Text |  
     -------------       ---------       ------------
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

from http import server
import socket
import rsa

PORT = 8080
HOST = '172.19.155.72' #'192.168.1.69'

# The function generates key pair for RSA 
def GenerateKeys():
    public_key, private_key = rsa.newkeys(1024)
    print("publickey--------")
    print(public_key)
    with open("public.pem","wb") as f:
        f.write(public_key.save_pkcs1("PEM"))
    with open("private.pem","wb") as f:
        f.write(private_key.save_pkcs1("PEM"))

def encrpytor(text):
    with open("public.pem", "rb") as f:
        public_key = rsa.PublicKey.load_pkcs1(f.read())
    cipher_text = rsa.encrypt(text,public_key)
    server.send(cipher_text)
    
# This  
def main():
    # Creates a socket object 
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # Bind completes the handshake on the port
    server.bind((HOST,PORT))
    # stays listening for activity on the port
    server.listen()
    while True:
        client, address = server.accept()
        request = client.recv(1024)
        print("receiving request from client-----------------")
        with open("private.pem","rb") as f:
            private_key= rsa.PrivateKey.load_pkcs1(f.read())
        clear_message = rsa.decrypt(request, private_key)
        #print(clear_message)
        print(clear_message.decode("utf-8"))
        #server.send("Got it!")
               
if __name__ == '__main__':
    #GenerateKeys()
    main()