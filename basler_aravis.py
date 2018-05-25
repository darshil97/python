import sys
import gi
import numpy as np
from PIL import Image
import cv2
gi.require_version('Aravis', '0.4')
from gi.repository import Aravis

Aravis.enable_interface("Fake")

#checks if there is a camera availabe and opens the port
try:
    if len(sys.argv) > 1:
        camera = Aravis.Camera.new(sys.argv[1])
    else:
        camera = Aravis.Camera.new(None)
except:
    print("No Camera Found")
    exit()

#Setting the parameter for the camera

camera.set_region(0,0,1200,1200)
camera.set_frame_rate(10.0)
camera.set_pixel_format(Aravis.PIXEL_FORMAT_MONO_8)
camera.set_exposure_time(3000)

device = camera.get_device()        #gets the device ip address
device.set_string_feature_value("Acquisition", "SingleFrame")

payload = camera.get_payload()
[x,y,width,height] = camera.get_region()

print("Camera vendor : %s" %(camera.get_vendor_name ()))
print("Camera model  : %s" %(camera.get_model_name ()))
print("Camera id     : %s" %(camera.get_device_id ()))
print("ROI           : %dx%d at %d,%d" %(width, height, x, y))
print("Payload       : %d" %(payload))
print("Pixel format  : %s" %(camera.get_pixel_format_as_string ()))

stream = camera.create_stream()     #Creates a new ArvStream for video stream handling
stream.push_buffer(Aravis.Buffer.new_allocate(payload))     #Pushes the ArvBuffer to the stream thread

print("Start Acquisition")

camera.start_acquisition()

print("Acquisition")

imageBuffer = stream.pop_buffer()       #Pops the buffer from the output queue of stream
stream.push_buffer(imageBuffer)
dataFromBuffer = imageBuffer.get_data()     #Gets the data from the buffer
ImageIpl = Image.frombytes('L', (1200, 1200), dataFromBuffer)       #Creates a copy of image form buffer. Returns an Image object
imageArray = np.asarray(ImageIpl)

cv2.imwrite("IMAGE.jpg", imageArray)        #Saves the image.

print("Image acquired")
print("Stop Acquisition")

camera.stop_acquisition()