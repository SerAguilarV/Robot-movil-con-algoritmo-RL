import socket
import json
from bson import json_util

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 10701        # Port to listen on (non-privileged ports are > 1023)

RobotOmni = RobotOmnidireccional()

def MovimientoRobot(data):
    print("Mensaje: " + data["Mensaje"])
    if data["Laterales"]:
        RobotOmni.Run(Llanta=1,Sentido=1,Vel=0.5)
        RobotOmni.Run(Llanta=2,Sentido=1,Vel=0.5)
    else:
        
        RobotOmni.Run(Llanta=3,Sentido=1,Vel=0.5)
        RobotOmni.Run(Llanta=4,Sentido=1,Vel=0.5)
        
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(8192).decode('utf-8')
            if not data:
                break
            data = json.loads(data)
            print(data)
            post = {"Resp":"ok"}
            conn.sendall(json.dumps(post, default=json_util.default).encode('utf-8'))
            MovimientoRobot(data)
