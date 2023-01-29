from pickletools import uint8
import socket
import subprocess


if b'De_Boto_wifi' in subprocess.check_output("netsh wlan show interfaces"):
    serverAddressPort   = ("192.168.4.22", 8888)
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    serverAddressPort   = ("192.168.4.22", 8888)
    server.connect(serverAddressPort)
    lift_code = server.recv(16).decode('utf8')
    lower_code = server.recv(16).decode('utf8')
    print("lift code {} lower code {}".format(lift_code, lower_code))
    #TODO: save lift and lower codes

    def SEND_With_TCP(msgFromClient):
        """
        :param msgFromClient the massage to be sent to Leonardo de boto
        """
        server.sendall(bytes(msgFromClient))

else:
    print("not connected to Leonardo de boto please connect to the wifi AP and try again")

while(1):
    angles = []
    alpha = int(input("input alpha angle"))
    beta = int(input("input alpha angle"))
    angles.append(alpha)
    angles.append(beta)
    SEND_With_TCP(angles)