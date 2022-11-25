
#!/bin/bash

cd ..
cd database
python3 initialise_database.py
cd ../client
echo "Close terminal when the process is completed"
xterm -e "python3 main_client.py < test_clients/test_client.txt > test_clients/test_output.txt"
