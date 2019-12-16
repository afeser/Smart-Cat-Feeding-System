# Driver for camera
# TODO..

from picamera import PiCamera
from io import BytesIO
from time import sleep
from PIL import Image

import logging

import subprocess

class CameraDriverUSB():

    """
    It stores the image in it.
    Currently a single image at a time is stored.
    """

    def __init__(self):
        self._image     = None
        self._imageData = BytesIO()
        # self._camera    = PiCamera()

        # self._camera.start_preview()

    # def __del__(self):
        # self._camera.stop_preview()
        #     pass

    def capture(self):
        '''
        Capture an image and return as stream object.
        '''
        # Reset imageData
        self._imageData.truncate(0)
        self._imageData.seek(0)


        subprocess.run(["fswebcam", "-r", "1280x720", "--no-banner", "test.jpg"], shell=True)
        im = Image.open('test.jpg')


        im.save(self._imageData, format='png')

        # Capture new image
        # self._camera.capture(self._imageData, 'png')


    def getImageDataSize(self):
        """
        Get the size of the buffer object that holds the image data in string type
        """
        # TODO - int->str->byte->str->int probably not efficient
        size = self._imageData.getbuffer().nbytes

        return str(size)



    def getImageData(self):
        """
        Return the image as buffer
        """
        return self._imageData

class CameraDriver():

    """
    It stores the image in it.
    Currently a single image at a time is stored.
    """

    def __init__(self):
        self._image     = None
        self._imageData = BytesIO()
        self._camera    = PiCamera()

        self._camera.start_preview()

    def __del__(self):
        self._camera.stop_preview()



    def capture(self):
        '''
        Capture an image and return as stream object.
        '''
        # Reset imageData
        self._imageData.truncate(0)
        self._imageData.seek(0)

        # Capture new image
        self._camera.capture(self._imageData, 'png')


    def getImageDataSize(self):
        """
        Get the size of the buffer object that holds the image data in string type
        """
        # TODO - int->str->byte->str->int probably not efficient
        size = self._imageData.getbuffer().nbytes

        return str(size)



    def getImageData(self):
        """
        Return the image as buffer
        """
        return self._imageData
