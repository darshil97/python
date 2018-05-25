import sys
import time
import gi
import numpy as np
from PIL import Image
import cv2
gi.require_version('Aravis','0.4')
from gi.repository import Aravis


Aravis.enable_interface ("Fake")
"""Opening the camera"""
try:
	if len(sys.argv) > 1:
		camera = Aravis.Camera.new (sys.argv[1])
	else:
		camera = Aravis.Camera.new (None)
except:
	print ("No camera found")
	exit ()

"""Setting up the camera"""
camera.set_region(0,0,1200,1200)
camera.set_frame_rate (10.0)
camera.set_pixel_format(Aravis.PIXEL_FORMAT_MONO_8)
camera.set_exposure_time(1500)
#print (camera.get_available_pixel_formats_as_strings())
device = camera.get_device()
device.set_string_feature_value("AcquisitionMode","SingleFrame")

payload = camera.get_payload()
[x,y,width,height] = camera.get_region()

print ("Camera vendor : %s" %(camera.get_vendor_name ()))
print ("Camera model  : %s" %(camera.get_model_name ()))
print ("Camera id     : %s" %(camera.get_device_id ()))
print ("ROI           : %dx%d at %d,%d" %(width, height, x, y))
print ("Payload       : %d" %(payload))
print ("Pixel format  : %s" %(camera.get_pixel_format_as_string ()))

stream = camera.create_stream()
stream.push_buffer(Aravis.Buffer.new_allocate(payload))
print ("Start acquisition")
camera.start_acquisition()
print ("Acquisition")

imageBuffer = stream.pop_buffer()
stream.push_buffer(imageBuffer)
dataFromBuffer = imageBuffer.get_data()
ImageIpl= Image.frombytes('L',(1200, 1200),dataFromBuffer)
imageArray = np.asarray(ImageIpl)
#imgRgb = cv2.cvtColor(imageArray,cv2.cv.CV_BayerGB2RGB)
imgData = np.ndarray(buffer = imageArray, dtype = np.uint8, shape =(height, width,1))
#rgb_imgData=cv2.cvtColor(imgData,cv2.COLOR_BAYER_BG2RGB)
cv2.imwrite("img2.jpeg", imgData)
print("Image captured")
print ("Stop acquisition")
camera.stop_acquisition ()








