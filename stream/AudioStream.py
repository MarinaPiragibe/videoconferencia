from vidstream import *
import threading
import time
import socket


localIpAddress = socket.gethostbyname(socket.gethostname())

class AudioStream:
    def __init__(self, conexao):
        self.portaAudioHost = None
        self.portaAudioTarget = None

    def startAudioStream(self, cliente, targetClientIP='26.84.232.20'): 

        hostClient = AudioReceiver(str(cliente.ip), int(self.portaAudioHost))# Ip da sua máquina e porta receptora
        thread_hostClient = threading.Thread(target=hostClient.start_server)
        thread_hostClient.start()

        targetClient = AudioSender(str(targetClientIP), int(self.portaAudioTarget)) # Ip da targetClient e porta receptora da targetClient
        thread_targetClient = threading.Thread(target=targetClient.start_stream)
        thread_targetClient.start()

    # def closeAudioStream(hostClient, targetClient):
    #     hostClient.stop_server()
    #     targetClient.stop_stream()


    