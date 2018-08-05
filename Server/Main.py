import io
import socket
import struct
import time
import picamera

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 1234))
print('binded')
server_socket.listen(0)
print('socket listening')

#conn, addr = server_socket.accept()
#ip, port = str(addr[0]), str(addr[1])
#print('Accepting connection from ' + ip + ':' + port)


# Make a file-like object out of the connection
connection = server_socket.accept()[0].makefile('wb')

try:
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.framerate = 15
        # Start a preview and let the camera warm up for 2 seconds
        camera.start_preview()
        time.sleep(1)
        
        #make the program wait for input to confirm connection wants to start
        #server_socket.recv(4096)
               
        # Note the start time and construct a stream to hold image data
        # temporarily (we could write it directly to connection but in this
        # case we want to find out the size of each capture first to keep
        # our protocol simple)
        start = time.time()
        stream = io.BytesIO()
        for foo in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
            # Write the length of the capture to the stream and flush to
            # ensure it actually gets sent
            connection.write(struct.pack('<L', stream.tell()))
            connection.flush()
            # Rewind the stream and send the image data over the wire
            stream.seek(0)
            connection.write(stream.read())
            # If we've been capturing for more than 30 seconds, quit
            if time.time() - start > 8:
                break
            # Reset the stream for the next capture
            stream.seek(0)
            stream.truncate()
    # Write a length of zero to the stream to signal we're done
    connection.write(struct.pack('<L', 0))
finally:
    connection.close()
    server_socket.close()