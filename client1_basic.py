'''
Created on Jun 11, 2018

@author: Andy
'''
# client.py

import socket
import gui


def clientcode(userinput1):
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    soc.connect(("192.168.1.123", 1234))
    
    print('userinput = ' + str(userinput1))
    
    clients_input = str(userinput1) 
    soc.send(clients_input.encode("utf8")) # we must encode the string to bytes  
    result_bytes = soc.recv(4096) # the number means how the response can be in bytes  
    result_string = result_bytes.decode("utf8") # the return will be in bytes, so decode
    
    print("Result from server is \n{}".format(result_string))  


def connectserver():
    client_socket = socket.socket()
    client_socket.connect(("192.168.1.123", 1234))
    return client_socket




if __name__ == '__main__':
    #gui.NotebookDemo().mainloop()
    #clientcode('testing')
    pass