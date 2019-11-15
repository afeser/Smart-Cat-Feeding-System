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
This is under development. This will send important messages and commands such as open food gate, etc.

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
Under development.

## Constants
File to store constants and parameters of the project.

Only a single method exists :
`getConstants()`
