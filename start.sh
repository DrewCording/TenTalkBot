#!/bin/bash

commands=$PWD/*.py
pwdlen=${#PWD}
pwdlen=`expr $pwdlen + 1`

if [ $1 ]; then
	if [ $1 = "all" ]; then
		echo "Starting all scripts"
		for item in $commands; do
			itemname=${item:pwdlen}
			itemname=${itemname%.py}
			pid=`ps -ef | grep $item | grep -v grep | awk -v col=2 '{print $col}'`
			if [ $pid ]; then
				echo "!$itemname is already running in $PWD. PID is $pid"
			else
			       	echo "Starting bot command !$itemname"
				echo "Starting $itemname.py at $(date)" >> $PWD/$itemname.log
				$item &>> $PWD/$itemname.log &
			fi
		done
	else
		for item in $commands; do
			if [ "$PWD/$1.py" == $item ]; then
				flag=1
				break
			fi
		done
		if [ $flag ]; then
			pid=`ps -ef | grep $PWD/$1.py | grep -v grep | awk -v col=2 '{print $col}'`
			if [ $pid ]
			then
				echo "!$1 is already running in $PWD. PID is $pid"
			else
				echo "Starting bot command !$1"
				echo "Starting $1.py at $(date)" >> $PWD/$1.log
				$PWD/$1.py &>> $PWD/$1.log &
			fi
		else
			echo "Command !$1 does not exist in $PWD"
		fi
	fi
else
	echo "Must specify either 'all' or a command to start"
fi
