# Driver for camera
# TODO..

from picamera import PiCamera
from io import BytesIO
from time import sleep

class CameraDriver():

    """
    It stores the image in it.
    Currently a single image at a time is stored.
    """

    def __init__(self):
        self._image     = None
        self._imageData = None
        self._camera    = PiCamera()

    def capture(self):
        """
        Capture an image and return as stream object.
        """
        self._imageData = BytesIO()

        self._camera.start_preview()
        sleep(2)

        self._camera.capture(self._imageData, 'jpg')



    def getSize(self):
        """
        Get the size of the buffer
        """
        # TODO - int->str->byte->str->int probably not efficient
        # im = self._image
        #
        # width  = im.size[0]
        # height = im.size[1]
        #
        # size = width * height
        #
        # return str(size).encode()
        pass



    def getImageData(self):
        """
        Return the image as buffer
        """
        return self._imageData
