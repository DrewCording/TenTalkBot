#!/bin/bash

commands=$PWD/*.py
pwdlen=${#PWD}
pwdlen=`expr $pwdlen + 1`

if [ $1 ]; then
        if [ $1 = "all" ]; then
                echo "Restarting all scripts"
                for item in $commands; do
                        itemname=${item:pwdlen}
                        itemname=${itemname%.py}
                        pid=`ps -ef | grep $item | grep -v grep | awk -v col=2 '{print $col}'`
                        if [ $pid ]; then
                                echo "!$itemname is running in $PWD. PID: $pid."
                        else
                                echo "!$itemname is not running in $PWD."
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
                                echo "!$1 is running in $PWD. PID: $pid."
                        else
                                echo "!$1 is not running in $PWD."
                        fi
                else
                        echo "Command !$1 does not exist in $PWD"
                fi
        fi
else
        echo "Must specify either 'all' or a command to check status"
fi

