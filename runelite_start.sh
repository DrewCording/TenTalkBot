#!/bin/bash

logdirect=$PWD
client=`ls -l /runelite/runelite/runelite-client/target/ | grep shaded | awk -v col=9 '{print $col}'`
cd /runelite/runelite/runelite-client/target/
java -ea -cp net.runelite.client.RuneLite -jar $client  --debug --developer-mode &>> $logdirect/runelite_start.log &
