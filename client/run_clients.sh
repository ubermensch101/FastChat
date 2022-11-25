#!/bin/bash

while read line; do    
    echo $line
    value="$line""\n""$value"   
done < test_clients/client1.txt

echo $value

gnome-terminal -- echo $value | python3 main_client.py