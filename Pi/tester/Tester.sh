#!/bin/bash


# Test is written to be executed on the server machine

# Server : computation server
# Client : Raspberry Pi Zero W

# Old logs are confusing
clear
clear
clear

# Create directory etc.
cd ../src
cp ../tester/Tester.py ./

server=pi@192.168.1.13
port=22

forwardPorts="-R 10004:localhost:10004 -R 10007:localhost:10007"

remoteDir="~/ServerTest" # Server directory of the files

sshCommand="ssh -p $port $server"
scpCommand="scp -P $port Server.py Client.py Tester.py CameraDriver.py $server:$remoteDir"


# Some colors..
red=$'\e[1;31m'
grn=$'\e[1;32m'
yel=$'\e[1;33m'
blu=$'\e[1;34m'
mag=$'\e[1;35m'
cyn=$'\e[1;36m'
end=$'\e[0m'

yesil="printf $grn"
beyaz="printf $end"
# yellow -> python or ssh messages

# Send files
printf "Sending files...\n"
$scpCommand  > /dev/null
# Clean
printf "Cleaning...\n"
printf "\tKilling server\n"
killall python3 &> /dev/null
printf "\tKilling client ssh sessions\n"
$sshCommand "kill \$(sudo netstat -lp | grep ':10004' | grep 'tcp ' | sed  's/tcp        0      0 localhost:10004         0.0.0.0:\*               LISTEN      //g' | sed 's/\/sshd: pi//g')"
# $sshCommand "kill \$(sudo netstat -lp | grep ':10007' | grep 'tcp ' | sed  's/tcp        0      0 localhost:10007         0.0.0.0:\*               LISTEN      //g' | sed 's/\/sshd: pi//g')" # already the same as above line

sleep 3

printf "Establishing secure connection...\n"
printf $yel
$sshCommand $forwardPorts -fN
sleep 3
printf $end

function test1() {
  # Command Test - sayHello
  testNum=1
  $yesil
  echo "Starting test $testNum..."
  $beyaz
  message='sayHello'


  # Run the server
  printf "\tStarting server\n"
  printf $yel
  python3 Tester.py test1S $message &
  sleep 3
  printf $end

  if [ $? -ne 0 ]
  then
    echo "FATAL : Error establishing secure connection"
    exit 1
  fi


  # Wait for the server
  sleep 2

  # Start client
  printf "\tSending files\n"
  printf "\tGetting client response\n"
  clientResponse=$(python3 Tester.py test1C)
  if [ "$clientResponse" == "$message" ]
  then
    printf $grn
    printf "\tSuccess!\n"
    printf $end
  else
    printf $red
    printf "\tFail!\n"
    printf $end
    return 1
  fi

  $yesil
  echo "Test $testNum finished!"
  $beyaz

  return 0
}


function test2() {

  dirName=pictureTest7q8hd787h3f8u

  ln -s ../src/$dirName ../tester/
  # Frame test
  testNum=2
  $yesil
  echo "Starting test $testNum..."
  $beyaz


  # Run the server
  printf "\tStarting server\n"
  mkdir $dirName
  printf $yel
  python3 Tester.py test2S $dirName &
  sleep 3
  printf $end

  if [ $? -ne 0 ]
  then
    echo "FATAL : Error establishing secure connection"
    exit 1
  fi


  # Wait for the server
  sleep 2

  # Start client
  printf "\tStarting client\n"
  $sshCommand "cd $remoteDir; mkdir $dirName; python3 Tester.py test2C $dirName"
  printf "\tGetting remote images\n"
  scp -P $port $server:$remoteDir/$dirName/0.png $dirName/remote0.png  &> /dev/null
  printf "\tTesting images\n"
  printf "\t\tImage 1\n"
  diff $dirName/0.png $dirName/remote0.png
  if [ $? -eq 0 ]
  then
    printf $grn
    printf "\tSuccess!\n"
    printf $end
  else
    printf $red
    printf "\tFail!\n"
    printf $end
    return 1
  fi
  scp -P $port $server:$remoteDir/$dirName/1.png $dirName/remote1.png &> /dev/null
  printf "\t\tImage 2\n"
  diff $dirName/1.png $dirName/remote1.png
  if [ $? -eq 0 ]
  then
    printf $grn
    printf "\tSuccess!\n"
    printf $end
  else
    printf $red
    printf "\tFail!\n"
    printf $end
    return 1
  fi

  # Clean directories
  printf "\tCleaning directories\n"
  rm -r $dirName
  rm ../tester/$dirName
  $sshCommand "cd $remoteDir; rm -r $dirName"

  $yesil
  echo "Test $testNum finished!"
  $beyaz

  return 0
}


# Test1
test1
if [ $? -eq 1 ]; then exit 0; fi


test2
if [ $? -eq 1 ]; then exit 0; fi


rm ../src/Tester.py
