# client.py

import socket

from PIL import Image

    

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
soc.connect(("192.168.1.123", 1234))

bufsize = 4096
#clients_input = input("What you want to proceed my dear client?\n")  
#soc.send(clients_input.encode("utf8")) # we must encode the string to bytes  
print('awaiting to receive')
result_bytes = soc.recv(bufsize) # the number means how the response can be in bytes  
print('received something')
while result_bytes[-2:] != "\xff\xd9":
    try:
        blk = soc.recv(bufsize)
        if blk != None:
            print('received data block length: ' +str(len(blk)))
            
        else:
            print('soc.recv got nothing')
            
    except:
        raise Exception("Exception from blocking soc.recv()")
    
    #result_string = result_bytes.decode("utf8") # the return will be in bytes, so decode
    
    print('result from server is')
      
    savedimage = Image.open(blk)
    savedimage.show()


def display(data):
    img = Image.open(data)
    if img != None:
        img.show()
        
        