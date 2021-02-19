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
                                echo "Restarting Bot Command !$itemname"
                                echo "Restarting $itemname.py at $(date)" >> $PWD/$itemname.log
				kill $pid
                                $item &>> $PWD/$itemname.log &
                        else
                                echo "!$itemname is not running in $PWD. Use start.sh"
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
                                echo "Restarting bot command !$1"
                                echo "Restarting $1.py at $(date)" >> $PWD/$1.log
				kill $pid
                                $PWD/$1.py &>> $PWD/$1.log &
                        else
                                echo "!$1 is not running in $PWD. Use start.sh"
                        fi
                else
                        echo "Command !$1 does not exist in $PWD"
                fi
        fi
else
        echo "Must specify either 'all' or a command to start"
fi

