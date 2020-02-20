# Raspberry Pi - Server Driver and Controller Framework

This is one of the most crucial part of the project. Overall framework, server-client
relations, resource management, sub-group interfaces, data communication are some
of the tasks defined in this part.

Interface properties and relation schema are already given in source files as
well as schema drawings. In this file, however, more descriptive information
will presented so that other parts can easily read and understand about the module.
This file is intended to be a documentation file. In future; however, further
documentation may be placed elsewhere causing this README.md to be rewritten.

Structure is written in order to make the use easy. Neither technical details, nor
exact code work is given, but only practical considerations are presented. Sections
present some possibly used module names, under the module name, description and example
use is included. The structure is as follows :
- Related Abstract Module
  - Actual Module
    - Methods - Functions

## Controller
This is a very powerful module that organizes everything and puts all stuff together.
It runs on server and manages all of the process. Not to be used during development
since operation is for self-management.

### Decision Making
Decision making module is embedded inside Controller module. Decisions are determined
before the operation and every possibility is considered. The followings are some
rules that determine the decision making process. Decision making module is designed
like a black box. There are inputs and outputs defining the situation and the action.
Inputs are listed, behaviour is defined per each action.

Classifying an image as cat triggers the followings.

**DecisionMaker.decideOnCat** :
Requirements :
  - Cat has not been fed 5 hours before now
  - Cat is in database, and it is allowed to eat, the amount is fetched
  -
Results :
  - Cat name is added to database as ate
  -

## Camera Driver
Camera driver for client camera.
- Holds camera resource throughout it's lifetime
- Always returns string(str), even though required value is integer

`camDriver = CameraDriver()``
Methods :
#### capture
Captures an image and stores inside the object.

`camDriver.capture()`

#### getImageDataSize
Returns the image data size. Return value is string of an integer.

`camDriver.getImageDataSize()`

#### getImageData
Returns the image data as BytesIO object.

`camDriver.getImageData()`

## Server
Server is an abstract module. It is used for single purpose, single client web server.

Creating a server requires only single argument, constants. This parameters are defined
under Constants.py.

Create a server:
`videoServer   = VideoServer(constants)`
`commandServer = CommandServer(constants)`

### VideoServer
Streaming of video, frame transfer, visual communication are all transacted through
this server. It simply wait for the client which will then become the commander of
the VideoServer. VideoServer sends a command and gets the result.

Important methods are :
#### Receive Frame
Receive a single frame. When called, request goes from server to client. Client captures
and sends the image to the server.

Example :
`newFrame = videoServer.receiveFrame()`


### CommandServer
Based on controller, sends commands to the client.

Available commands are, self explanatory :
- `greenLedOn()`
- `redLedOn()`
- `yellowLedOn()`
- `greenLedOff()`
- `redLedOff()`
- `yellowLedOff()`
- `allLedsOn()`
- `allLedsOff()`
- `openFoodGate()`
- `closeFoodGate()`
- `feedcat()`
- `sonarMeasure()`

## Client
Client is an abstract module, it can be used to create a client that connects to
the server. It need configuration read from "Constants.py" module.

Create a client:
`videoClient   = VideoClint(constants)`
`commandClient = CommandClient(constants)`

### Video Client
See "Video Server".

Important methods are :
#### Single Listener
In case of need for a single command listen, listener method waits for a command
and executes the corresponding action. "turnOnListenMode" is preferred since it
is more dynamic and meaningful with client operation.

Example :
`videoClient.listener()`

#### turnOnListenMode
Continuously listens for commands and executes the actions. Starts as a thread and
control directly returns to the main. Therefore non-blocking actions can easily be done.

Example :
`videoClient.turnOnListenMode()`

### Command Client
Client listening to the server and executes the commands requested. It (currently) only uses GPIODriver to take actions.

#### listenCommand
Listen to a single command from the server, take an action.

Example :
`commandClient.listenCommand()`

#### turnOnListenMode
Client switches into listen mode, calling listenCommand in a loop.

Example :
`commandClient.turnOnListenMode()`



## Constants
File to store constants and parameters of the project.

Only a single method exists :
`getConstants()`


## GPIODriver
Driver module for the GPIO pins of the Pi Zero. Pin assignments are embedded into `__init__`.
Functions are :
- `greenLedOn()`
- `redLedOn()`
- `yellowLedOn()`
- `greenLedOff()`
- `redLedOff()`
- `yellowLedOff()`
- `openFoodGate()`
- `closeFoodGate()`
- `feedcat()`
- `sonarMeasure()`


Methods :
#### colorLedOn
Turns on the LED. Green led is turned on when a cat is detected, red led is turned on when a dog is detected and yellow led is turned on when there is no cat or dog detection.

`GPIODriver.greenLedOn()`

`GPIODriver.redLedOn()`

`GPIODriver.yellowLedOn()`

#### colorLedOff
Turns off the LED. Green led is turned off when there is no cat detection. Red led is turned off where there is no dog detection. Yellow led is turned off when a cat or dog is detected.

`GPIODriver.greenLedOff()`

`GPIODriver.redLedOff()`

`GPIODriver.yellowLedOff()`

#### openFoodGate
Opens the gate when a cat is detected. Servo motor is controlled by changing the duty cycle of PWM signal.in this module. Food in the gate reservoir is dropped.

`GPIODriver.openFoodGate()`

#### closeFoodGate
Closes the gate. Gate is turned back to its initial position and food is stored in the reservoir of gate.

`GPIODriver.openFoodGate()`

#### feedCat
Opens and closes the gate when a cat is detected.

`GPIODriver.feedCat()`


#### sonarMeasure
Returns the distance between the top of the reservoir and food level. Remaining food level will be determined from the measured distance.

`GPIODriver.sonarMeasure()`
