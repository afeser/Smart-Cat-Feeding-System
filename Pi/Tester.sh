#!/bin/bash

server=afeserpi.duckdns.org
port=8001

forwardPorts="-L 10004:localhost:10004 -L 10007:localhost:10007"

remoteDir="~/FinalProject/Server" # Server directory of the files

sshCommand="ssh -p $port $server"
scpCommand="scp -P $port Server.py Client.py Tester.py $server:$remoteDir"

$sshCommand $forwardPorts -fN

function test1() {
  # Command Test - sayHello
  testNum=1
  echo "Starting test $testNum..."
  message='sayHello'

  # Run on remote
  printf "\tSending files\n"
  $scpCommand  > /dev/null
  printf "\tStarting remote command\n"
  $sshCommand "cd $remoteDir; python3 Tester.py test1S $message" &

  # Wait for the server
  sleep 2

  #python3 Tester.py test1S $message &
  printf "\tGetting client response\n"
  clientResponse=$(python3 Tester.py test1C)
  if [ "$clientResponse" == "$message" ]
  then
    echo Success!
  else
    echo Fail!
    return 1
  fi


  # Clean
  printf "\tKilling remote server\n"
  $sshCommand "killall python3" &> /dev/null
  # TODO - below is missing
  # sshPID=$(netstat -lp | grep ":10007" | grep "tcp " | sed  's/tcp        0      0 localhost:10007          0.0.0.0:\*               LISTEN      //g' | sed 's/\/ssh//g')
  # printf "\tKilling local ssh session\n"
  # kill $sshPID &> /dev/null

  echo "Test $testNum finished!"

  return 0
}


function test2() {
  # Command Test - sayHello
  testNum=2
  echo "Starting test $testNum..."
  message='sayHello'

  # Run on remote
  printf "\tSending files\n"
  $scpCommand  > /dev/null
  printf "\tStarting remote command\n"
  $sshCommand "cd $remoteDir; python3 Tester.py test2S $message" &

  # Wait for the server
  sleep 2

  #python3 Tester.py test1S $message &
  printf "\tGetting client response\n"
  clientResponse=$(python3 Tester.py test2C)
  if [ "$clientResponse" == "$message" ]
  then
    echo Success!
  else
    echo Fail!
    return 1
  fi


  # Clean
  printf "\tKilling remote server\n"
  $sshCommand "killall python3" &> /dev/null
  # TODO - below is missing
  # sshPID=$(netstat -lp | grep ":10007" | grep "tcp " | sed  's/tcp        0      0 localhost:10007          0.0.0.0:\*               LISTEN      //g' | sed 's/\/ssh//g')
  # printf "\tKilling local ssh session\n"
  # kill $sshPID &> /dev/null

  echo "Test $testNum finished!"

  return 0
}


# Test1
test1
if [ $? -eq 1 ]; then exit 0; fi


test2
if [ $? -eq 1 ]; then exit 0; fi
