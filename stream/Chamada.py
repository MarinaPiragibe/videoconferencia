from stream import VideoStream, AudioStream
import threading
import socket
import keyboard

def chamada(cliente, targetIP, portaVideoHost, portaAudioHost, portaVideoTarget, portaAudioTarget, socketClienteChamada):
  VideoStream.startVideoSteam(cliente,targetIP,portaVideoHost,portaVideoTarget)

  AudioStream.startAudioStream(cliente, targetIP, portaAudioHost, portaAudioTarget)

  #thread_cronometro = multiprocessing.Process(target=Cronometro.cronometro, args=())
  #thread_cronometro.start()
  
  threadAguardaFinalizarChamada = threading.Thread(target=fecharChamadaOuvinte, args=[cliente,socketClienteChamada])
  threadAguardaFinalizarChamada.start()
  
  statusChamada = True

  while statusChamada:
    if keyboard.is_pressed('S'):
      cliente.enviaMensagem(socketClienteChamada,"desligar")
      statusChamada = False
    elif not threadAguardaFinalizarChamada.is_alive():
      statusChamada = False

def fecharChamadaOuvinte(cliente, conexaoChamada):
  if(cliente.recebeMensagem(conexaoChamada) == "desligar"):
    cliente.enviaMensagem(conexaoChamada, "desligar")
    desligarChamada(cliente,conexaoChamada)

def desligarChamada(cliente, conexaoChamada):

  cliente.ocupado = False

  cliente.hostClientAudio.stop_server()
  cliente.targetClientAudio.stop_stream()

  cliente.hostClientVideo.stop_server()
  cliente.targetClientVideo.stop_stream()

  conexaoChamada.close()
  print("Chamada encerrada")

