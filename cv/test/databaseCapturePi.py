from picamera import PiCamera
from shutil import copyfile


fileName = input('Name or id of the current sample : ')

camera = PiCamera()

camera.start_preview()

for i in range(100):
    saveName = fileName + '_' + str(i) + '.png'
    print('Taking image and saving image as ' + fileName + '_' + str(i) + '.png', i)
    camera.capture(saveName)

    copyfile(saveName, 'currentFrame.png')


camera.close()
