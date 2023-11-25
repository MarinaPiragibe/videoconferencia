from vidstream import CameraClient
from vidstream import StreamingServer

import threading
import time

def startVideoSteam(hostIP='26.162.121.69', targetIP='26.84.232.20', recvPort=7777, targetPort=8888):
    receiving = StreamingServer(str(hostIP), int(recvPort))
    sending = CameraClient(str(targetIP), int(targetPort))
    time.sleep(3)
    t1 = threading.Thread(target=receiving.start_server)
    t1.start()
    t2 = threading.Thread(target=sending.start_stream)
    t2.start()
    



