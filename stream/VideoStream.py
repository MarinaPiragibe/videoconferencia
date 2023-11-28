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


    def startVideoSteam(self, cliente, targetIP):
        
        self.hostClient = StreamingServer(str(cliente.ip), int(self.portaVideoHost))
        self.hostClient.start_server()


        self.targetClient = CameraClient(str(targetIP), int(self.portaVideoTarget))
        self.targetClient.start_stream()

    
    

