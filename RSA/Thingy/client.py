'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

  ____________       ____________      ________      __________     
 | Plain Text | ->  | Public Key | -> | TCP/IP | -> | External |
  ------------       ------------      --------      ----------     


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import socket
import rsa
buffer = ''
HOST = '172.19.155.72' #'192.168.1.69'
PORT = 8080

def Create_key():
    public_key, private_key = rsa.newkeys(1024)
    with open("private.pem","wb") as f:
        f.write(private_key.save_pkcs1("PEM"))
    with open("public.pem","wb") as f:
        f.write(public_key.save_pkcs1("PEM"))
    
    
#create a socket object
def socket_handle(message):
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((HOST,PORT))
    client.send(bytes(message))
    print("----------sent message-------------")
    response = client.recv(1024)
    print("Getting from server-------")
    decryptor(response)
   
def decryptor(clear_message):
    with open("private.pem","rb") as f:
        private_key = rsa.PrivateKey.load_pkcs1(f.read())
    message = rsa.decrypt(clear_message, private_key)
    print(message)


def encryptor():
    with open("public.pem", "rb") as f:
        public_key = rsa.PublicKey.load_pkcs1(f.read())
    buffer = "Sending some data from client 1234"
    encrypted_message = rsa.encrypt(buffer.encode(), public_key)
    print("encrypted = ",encrypted_message)
    socket_handle(encrypted_message)

if __name__ == '__main__':
    #Create_key()
    encryptor()
    #socket_handle()