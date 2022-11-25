fuser -k 8080/tcp
fuser -k 8081/tcp
fuser -k 8082/tcp
fuser -k 8083/tcp
fuser -k 8084/tcp

gnome-terminal -- python3 main_server.py 8080
gnome-terminal -- python3 main_server.py 8081
gnome-terminal -- python3 main_server.py 8082
gnome-terminal -- python3 main_server.py 8083
gnome-terminal -- python3 main_server.py 8084
