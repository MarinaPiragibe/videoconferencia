from vidstream import *
import threading
import time
import socket


localIpAddress = socket.gethostbyname(socket.gethostname())

class AudioStream:
    def __init__(self):
        self.portaAudioHost = None
        self.portaAudioTarget = None
        self.hostClient = None
        self.targetClient = None


    def startAudioStream(self, cliente, targetClientIP): 

        self.hostClient = AudioReceiver(str(cliente.ip), int(self.portaAudioHost))# Ip da sua máquina e porta receptora
        self.hostClient.start_server()

        self.targetClient = AudioSender(str(targetClientIP), int(self.portaAudioTarget)) # Ip da targetClient e porta receptora da targetClient
        self.targetClient.start_stream()



    