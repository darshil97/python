try:
    import gi

    gi.require_version('Aravis', '0.4')
    from gi.repository import Aravis
    import numpy as np
    from PIL import Image
    import time

except ImportError as importError:
    print(importError)

class Gige_camera():
    def __init__(self, name=None, camResolution=None, frameRate=15, mode = 'mono8' ):
        '''
		:param name: datatype: string, optional
		:param camResolution: datatype: tuple, optional
		:param frameRate: data type: int, optional
		'''
        self._name = name if (type(name) == str or name == None) else str(name)
        self._camResolution = camResolution if type(camResolution) == tuple else None
        self._frameRate = frameRate if type(frameRate) == int else int(frameRate)
        self.threshTimeTrigExitDanger =0.0005
        try:
            if name is None:
                self._camera = Aravis.Camera.new()

            else:
                self._camera = Aravis.Camera.new(name)

            sensorSize = self._camera.get_sensor_size()
            if self._camResolution is None or self._camResolution[0] > sensorSize[0] or self._camResolution[1] > \
                    sensorSize[1]:
                self._camResolution = (sensorSize[0], sensorSize[1])
            print('name: ', name, '\n', 'cameraResolution: ', self._camResolution[0], 'x', self._camResolution[
                1], '\n', 'frameRate: ', frameRate)
            self._CameraInit(self._camera, self._camResolution, frameRate, mode)
        except Exception as error:
            if str(error) == 'constructor returned NULL':
                print('no camera found')
            else:
                print(error)

    def _CameraInit(self,a,b,c,d):
        try:
            camResolution=(320,480)
            frameRate=15
            mode='mono8'
            camera=self._camera
            camera.set_region(x=0, y=0, width=camResolution[0], height=camResolution[1])
            camera.set_frame_rate(frameRate)
            if mode == 'mono8':
                try:
                    camera.set_pixel_format(Aravis.PIXEL_FORMAT_MONO_8)
                except Exception as error:
                    print(error)
            elif mode == 'BRG8':
                try:
                    camera.set_pixel_format(Aravis.PIXEL_FORMAT_BAYER_RG_8)
                except Exception as error:
                    print(error)
            else:
                pass
            self._payload = camera.get_payload()
            self._stream = camera.create_stream()
            self._stream.push_buffer(Aravis.Buffer.new_allocate(self._payload))
            camera.start_acquisition()
            print("Camera vendor : %s" % (camera.get_vendor_name()))
        except Exception as error:
            print(error)


    def Capture(self):
        try:
            self._camera.software_trigger()
            tic = time.time()
            print("waiting for pop")
            while True:
                print("hi")
                imageBuffer = self._stream.pop_buffer()

                print(imageBuffer)
                if imageBuffer:
                    break
                elif (time.time() - tic) > self.threshTimeTrigExitDanger:
                    break
            print('pop done')
            if imageBuffer:
                self._stream.push_buffer(imageBuffer)
                dataFromBuffer = imageBuffer.get_data()
                print(dataFromBuffer)
            if imageBuffer:
                print("test 1")
                ImageIpl = Image.frombytes('L', (self._camResolution[0], self._camResolution[1]), dataFromBuffer, 'raw')
                print(ImageIpl)
                imageArray = np.asarray(ImageIpl)
                imgBayer = imageArray
                cv2.imwrite('fkjshfs.jpg', imgBayer)
                print("image saved")
                cv2.waitKey(0)
                return True, imgBayer

            else:
                return False, None
        except Exception as error:
            return False, error


    def SetTriggerMode(self, mode="Software"):
        try:
            if mode == 'software':
                self._camera.set_trigger("Software")
            elif mode == 'external':
                self._camera.set_trigger("Line1")
            else:
                self._camera.set_trigger("Any")
                print ('mode should either \'software\' or \'external\'.',)
            print ('current Triggering Mode: ', self._camera.get_trigger_source())
        except Exception as error:
            print (error)


    def SetExposure(self, exposure=None):
        if exposure == None:
            print ('Exposure time: ', self._camera.get_exposure_time())
            return
        try:
            self._camera.set_exposure_time(exposure)
            print ('Exposure time: ', self._camera.get_exposure_time())
        except Exception as error:
            print (error)
g=Gige_camera()
g.Capture()
#
#name=None, camResolution=None, frameRate=15, mode = 'BRG8'

#
# camera, camResolution, frameRate, mode

