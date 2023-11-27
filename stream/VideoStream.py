from vidstream import CameraClient
from vidstream import StreamingServer
import socket
import threading
import time

class VideoStream:
    def __init__(self):
        self.portaVideoHost = None
        self.portaVideoTarget = None
        self.hostClient = None
        self.targetClient = None

    localIpAddress = socket.gethostbyname(socket.gethostname())

    def startVideoSteam(self, cliente, targetIP):
        
        self.hostClient = StreamingServer(str(cliente.ip), int(self.portaVideoHost))
        thread_hostClient = threading.Thread(target=self.hostClient.start_server)
        thread_hostClient.start()

        self.targetClient = CameraClient(str(targetIP), int(self.portaVideoTarget))
        thread_targetClient = threading.Thread(target=self.targetClient.start_stream)
        thread_targetClient.start()

    
    

