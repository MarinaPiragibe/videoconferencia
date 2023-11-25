from vidstream import *
import threading
import time
import socket

localIpAddress = socket.gethostbyname(socket.gethostname())

def startAudioStream(hostIP=localIpAddress, targetIP='26.162.121.69', recvPort=8888, targetPort=7777): 

    #server = StreamingServer(localIpAddress, 9999)# IP DA SUA MAQUINA
    receiver = AudioReceiver(hostIP, int(recvPort))# Ip da sua máquina e porta receptora

    #thread_audio_server = threading.Thread(target=server.start_server)
    thread_audio_receiver = threading.Thread(target=receiver.start_server)
    #thread_audio_server.start()
    thread_audio_receiver.start()

    target = AudioSender(targetIP, int(targetPort)) # Ip da target e porta receptora da target
    thread_audio_target = threading.Thread(target=target.start_stream)
    thread_audio_target.start()

    time.sleep(3)
    return