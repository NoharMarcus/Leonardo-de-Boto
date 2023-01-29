# from distutils.log import debug
from encodings import utf_8
from pickletools import uint8
import socket
import subprocess
import numpy as np
import time

time_to_sleep = 1

debug = False

class tcp_connection:
    connected = b'De_Boto_wifi' in subprocess.check_output("netsh wlan show interfaces")
    serverAddressPort = ("192.168.4.22", 8888)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverAddressPort = ("192.168.4.22", 8888)
    if (connected):
        server.connect(serverAddressPort)
        lift_code = server.recv(16).decode('utf8')
        lift_code = int(lift_code)
        lower_code = server.recv(16).decode('utf8')
        lower_code = int(lower_code)
        # change_time_code = server.recv(16).decode('utf8')

    # the function to send the recived massage
    def SEND_With_TCP(self, msgFromClient):
        """
            :param msgFromClient the massage to be sent to Leonardo de boto
        """
        if (self.connected):
            # print(debug)
            if debug:
                print("\r")
                print("sending {}".format(msgFromClient))
            self.server.sendall(bytes(msgFromClient))

        else:
            print("not connected to Leonardo de boto please connect to the wifi AP and try again")

    def Change_delay_time(self, delay):

        if (self.connected):
            msgFromClient = [200, delay]
            self.server.sendall(bytes(msgFromClient))

        else:
            print("not connected to Leonardo de boto please connect to the wifi AP and try again")
    
    def Move_to_start(self):
        send = [self.lift_code,self.lift_code, 20, 180-20]
        print("moving to starting position")
        self.SEND_With_TCP(send)
    
    def prepare_data_to_send(self,alpha_vec, beta_vec):
        """
        This function recieves the angles vectors, convert the data into the format needed 
        to send to De-Boto.
        Including lifting and lowering the pen.
        This function assumes that each time the vectors are representing one full line
        (aka, one connected component. lowering the pen in the start,
        and lifting it at the end)

        Returns the data in the required format of (uint8)
        """

        # format to send: [alpha, beta, alpha, beta, alpha ...]
        # such that De-Boto will read them in pairs, each pair - a command.
        
        alpha_vec = np.array(alpha_vec)
        beta_vec = np.array(beta_vec)

        alpha_vec = np.insert(alpha_vec,1,self.lower_code)
        beta_vec = np.insert(beta_vec,1,self.lower_code)

        alpha_vec = np.append(alpha_vec,self.lift_code)
        beta_vec = np.append(beta_vec,self.lift_code)


        commands_vector = np.zeros(alpha_vec.shape[0] * 2)
        commands_vector[0::2] = alpha_vec
        commands_vector[1::2] = beta_vec


        return np.uint8(commands_vector)

if __name__ == "__main__":
    DE_boto = tcp_connection()
    send =[DE_boto.lift_code,DE_boto.lift_code, 20, 180 - 20, 20, 180 - 20, 20, 180 - 20, 20, 180 - 20, 20, 180 - 20
    , 20, 180 - 20, 20, 180 - 20, 20, 180 - 20, 20, 180 - 20]
    # DE_boto.Change_delay_time(5)
    #DE_boto.Move_to_start()
    DE_boto.SEND_With_TCP(send)
    # DE_boto.SEND_With_TCP([180 ,180])
    # DE_boto.SEND_With_TCP([90 ,90])
    # DE_boto.SEND_With_TCP([0 ,0])


# DE_boto.Change_delay_time(15)
# for i in range(100):
#     send1 = [45, 95]
#     send2 = [45, 135]
#     send3 = [75, 135]
# for i in range(100):
#     DE_boto.SEND_With_TCP(send)
#     DE_boto.SEND_With_TCP(send1)
#     time.sleep(1)
#     DE_boto.SEND_With_TCP(send1)
#     time.sleep(1)
#     DE_boto.SEND_With_TCP(send2)
#     time.sleep(1)
#     DE_boto.SEND_With_TCP(send3)
#     time.sleep(1)

##############
# code to test movment range
##############
# start = 140
# beta = np.arange(start,180,5)
# alpha = beta-start
# alpha = alpha.astype(np.int8)

# send = [DE_boto.lift_code,DE_boto.lift_code, alpha[0],beta[0],DE_boto.lower_code,DE_boto.lower_code]
# DE_boto.SEND_With_TCP(send)
# for i in range(1,alpha[1:].shape[0]):
#     send = [alpha[i],beta[i]]
#     DE_boto.SEND_With_TCP(send)