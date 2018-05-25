import sys
import time
import gi
gi.require_version('Aravis','0.4')
from gi.repository import Aravis

import numpy as np
from PIL import Image
import cv2


Aravis.enable_interface("Fake") # using arv-fake-gv-camera-0.6
try:
	if len(sys.argv) > 1:
		camera = Aravis.Camera.new (sys.argv[1])
	else:
		camera = Aravis.Camera.new (None)
except:
	print ("No camera found")
	exit ()

camera.set_region(0,0,128,128)
camera.set_frame_rate (10.0)
camera.set_pixel_format(Aravis.PIXEL_FORMAT_MONO_8)
camera.set_exposure_time(980)
#camera = Aravis.Camera.new(None)
device = camera.get_device()
device.set_string_feature_value("AcquisitionMode","SingleFrame")
payload = camera.get_payload ()
[x,y,width,height] = camera.get_region()
stream = camera.create_stream ()

for i in range(0,50):
	stream.push_buffer (Aravis.Buffer.new_allocate (payload))

def convert(buf):
	''' explained later '''



    #continue code from above

print ("Start acquisition")
camera.start_acquisition()

while True:
	buffer = stream.try_pop_buffer()
	print(buffer)
	if buffer:
		frame = convert(buffer)
		stream.push_buffer(buffer) #push buffer back into stream
		cv2.imshow("frame", frame)
		ch = cv2.waitKey(1) & 0xFF
		if ch == 27 or ch == ord('q'):
                	break
		elif ch == ord('s'):
			cv2.imwrite("imagename.png",frame)


camera.stop_acquisition()
