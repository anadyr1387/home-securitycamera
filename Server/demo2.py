from picamera import PiCamera
from time import sleep
import io

from PIL import Image

stream = io.BytesIO()
camera = PiCamera()

#preview camera images
#camera.start_preview()
#sleep(5)
#camera.stop_preview()
with camera:
    #camera.start_preview()
    sleep(2)
    camera.capture(stream, format='jpeg')

stream.seek(0)
image = Image.open(stream)

