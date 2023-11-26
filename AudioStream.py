from vidstream import *
import threading
import time
import socket

localIpAddress = socket.gethostbyname(socket.gethostname())

def startAudioStream(cliente, targetClientIP='26.84.232.20', recvPort=7777, targetClientPort=8888): 

    hostClient = AudioReceiver(str(cliente.ip), int(recvPort))# Ip da sua máquina e porta receptora
    thread_hostClient = threading.Thread(target=hostClient.start_server)
    thread_hostClient.start()

    targetClient = AudioSender(str(targetClientIP), int(targetClientPort)) # Ip da targetClient e porta receptora da targetClient
    thread_targetClient = threading.Thread(target=targetClient.start_stream)
    thread_targetClient.start()

    cliente.receiverAudio= hostClient
    cliente.targetAudio = targetClient

def closeAudioStream(hostClient, targetClient):
    hostClient.stop_server()
    targetClient.stop_stream()