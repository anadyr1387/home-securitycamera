# server.py

from picamera import PiCamera
from time import sleep

from PIL import Image

import io
import time





camera = PiCamera()
#my_stream = io.BytesIO()


def do_some_stuffs_with_input(input_string):  
    """
    This is where all the processing happens.

    Let's just read the string backwards
    """

    print("Processing that nasty input!")
    return input_string[::-1]

def client_thread(conn, ip, port, MAX_BUFFER_SIZE = 4096):

    # the input is in bytes, so decode it
    #input_from_client_bytes = conn.recv(MAX_BUFFER_SIZE)

    # MAX_BUFFER_SIZE is how big the message can be
    # this is test if it's sufficiently big
    #import sys
    #siz = sys.getsizeof(input_from_client_bytes)
    #if  siz >= MAX_BUFFER_SIZE:
    #    print("The length of input is probably too long: {}".format(siz))

    # decode input and strip the end of line
    #input_from_client = input_from_client_bytes.decode("utf8").rstrip()

    #res = do_some_stuffs_with_input(input_from_client)
    #print("Result of processing {} is: {}".format(input_from_client, input_from_client))

    #vysl = input_from_client.encode("utf8")  # encode the result string
    camera.start_preview()
    sleep(2)
    #vysl = camera.captureJPEG(640,480)
    camera.capture('/home/pi/Desktop/testprogram/image1.jpg', resize=(640,480))
    camera.stop_preview()
    #vysl.show()
    
    conn.sendall('/home/pi/Desktop/testprogram/image1.jpg')  # send it to client
    conn.close()  # close connection
    print('Connection ' + ip + ':' + port + " ended")

def start_server():

    import socket
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this is for easy starting/killing the app
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print('Socket created')

    try:
        soc.bind(('0.0.0.0', 1234))
        print('Socket bind complete')
    except socket.error as msg:
        import sys
        print('Bind failed. Error : ' + str(sys.exc_info()))
        sys.exit()

    #Start listening on socket
    soc.listen(10)
    print('Socket now listening')

    # for handling task in separate jobs we need threading
    from threading import Thread

    # this will make an infinite loop needed for 
    # not reseting server for every client
    while True:
        conn, addr = soc.accept()
        ip, port = str(addr[0]), str(addr[1])
        print('Accepting connection from ' + ip + ':' + port)
        try:
            Thread(target=client_thread, args=(conn, ip, port)).start()
        except:
            print("Terible error!")
            import traceback
            traceback.print_exc()
    soc.close()

start_server()  
