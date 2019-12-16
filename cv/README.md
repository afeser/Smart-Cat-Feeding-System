DOCUMENTATION

Asude - pythonYOLO


Class Name: NeuralNetwork

classifyCatDog(frame,debug=False)

         Function: classifyCatDog

         Input :

                  - an OpenCV image object.
                  - debug = false to turn of debugging mode / debug = true to save frames with time stamps containing detcted object's position, label and confidence.

         Output:

                 - string:'dog' if there are any dogs present.
                 - string:'cat' if there are only cats present.
                 - string:'NA' if there are no cats and dogs present.


         Function: getObjectCoordinates

         Defines a rectangle containing the detected object.

         Input:
                 - No input just call the function.

         Output:  
                 - Returns four variables: [ top left corner's x dimension, top left corner's y dimension, width of the rectangle, height of the rectangle]
