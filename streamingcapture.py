import io
import socket
import struct
from PIL import Image
import time
import queue



# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)



#print('connected')

def streamcapture(client_socket):
    # Make a file-like object out of the connection
    connection = client_socket.makefile('rb')
    imagequeue = queue.LifoQueue()
    try:
        
        clients_input = str('go') 
        print('sent string')
        client_socket.sendall(clients_input.encode("utf8"))
        
        while True:
            # Read the length of the image as a 32-bit unsigned int. If the
            # length is zero, quit the loop
            image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
            if not image_len:
                break
            # Construct a stream to hold the image data and read the image
            # data from the connection
            currtime = time.time()
            image_stream = io.BytesIO()
            image_stream.write(connection.read(image_len))
            
            
            #test fitting images into queue instead of stream
            imagequeue.put(connection.read(image_len))
            
            image2 = Image.open(imagequeue.get())
            
            # Rewind the stream, open it as an image with PIL and do some
            # processing on it
            image_stream.seek(0)
            image = Image.open(image_stream)
            print('Image is %dx%d' % image.size)
            #print('Image frame number is %d' % image.tell)
            
            delay = currtime-time.time()
            print('delay of: ' + str(delay))
            #image.verify()
            #print('Image is verified')
            image.show()
            #image.close()
            
    finally:
        connection.close()
        client_socket.close()
    
    
    
    
    
if __name__ == '__main__':
    print('starting')
    client_socket = socket.socket()
    client_socket.connect(("192.168.1.123", 1234))
    
    streamcapture(client_socket)