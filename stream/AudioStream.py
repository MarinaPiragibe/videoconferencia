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
        thread_hostClient = threading.Thread(target=self.hostClient.start_server)
        thread_hostClient.start()

        self.targetClient = AudioSender(str(targetClientIP), int(self.portaAudioTarget)) # Ip da targetClient e porta receptora da targetClient
        thread_targetClient = threading.Thread(target=self.targetClient.start_stream)
        thread_targetClient.start()

    # def closeAudioStream(hostClient, targetClient):
    #     hostClient.stop_server()
    #     targetClient.stop_stream()


    