#!/bin/bash

logdirect=$PWD
cd /runelite/runelite/
git pull origin master &>> $logdirect/runelite_compile.log &
mvn install -Dskiptests &>> $logdirect/runelite_compile.log &