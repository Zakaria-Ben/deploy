#!/bin/bash


if [ $# -ne 1 ]
  then
	  echo "usage: $0 interval"
	  echo "   where interval is the number of seconds between two calls to the laxparing API"
      echo "   example: $0 5"
	  exit
fi

# infinite loop
while :
do
	python3 test_mediator_laxparking.py
	echo "Press [CTRL+C] to stop.."
	sleep $1
done
