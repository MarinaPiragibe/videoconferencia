from vidstream import CameraClient
from vidstream import StreamingServer
import socket
import threading
import time

class VideoStream:
    def __init__(self):
        self.portaVideoHost = None
        self.portaVideoTarget = None

    localIpAddress = socket.gethostbyname(socket.gethostname())

    def startVideoSteam(self, cliente, targetIP='26.162.121.69'):
        
        hostClient = StreamingServer(str(cliente.ip), int(self.portaVideoHost))
        thread_hostClient = threading.Thread(target=hostClient.start_server)
        thread_hostClient.start()

        targetClient = CameraClient(str(targetIP), int(self.portaVideoTarget))
        thread_targetClient = threading.Thread(target=targetClient.start_stream)
        thread_targetClient.start()

    
    

