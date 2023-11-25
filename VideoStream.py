from vidstream import CameraClient
from vidstream import StreamingServer
import socket
import threading
import time

localIpAddress = socket.gethostbyname(socket.gethostname())

def startVideoSteam(hostIP=localIpAddress, targetIP='26.162.121.69', hostPort=8888, targetPort=7777):
    
    hostClient = StreamingServer(str(hostIP), int(hostPort))
    thread_hostClient = threading.Thread(target=hostClient.start_server)
    thread_hostClient.start()

    targetClient = CameraClient(str(targetIP), int(targetPort))
    thread_targetClient = threading.Thread(target=targetClient.start_stream)
    thread_targetClient.start()

    return
    



