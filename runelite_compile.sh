#!/bin/bash

logdirect=$PWD
cd /runelite/runelite/
git pull origin master &>> $logdirect/runelite_compile.log &
rm /runelite/runelite/runelite-client/target/*.jar
mvn install &>> $logdirect/runelite_compile.log &
