from stream import VideoStream, AudioStream
import threading
import socket
import keyboard

class Chamada:
    def __init__(self, conexao, videoStream, audioStream):
        self.cliente = None
        self.targetIP = None
        self.videoStream = videoStream
        self.audioStream = audioStream
        self.conexao = conexao

    def iniciarChamada(self, cliente):
        self.videoStream.startVideoSteam(cliente, self.targetIP)

        self.audioStream.startAudioStream(cliente, self.targetIP)

        #thread_cronometro = multiprocessing.Process(target=Cronometro.cronometro, args=())
        #thread_cronometro.start()
        
        threadAguardaFinalizarChamada = threading.Thread(target=self.desligarChamada, args=[cliente, self.conexao])
        threadAguardaFinalizarChamada.start()
        
        statusChamada = True

        while statusChamada:
            if keyboard.is_pressed('S'):
                cliente.enviaMensagem(self.conexao,"desligar")
                statusChamada = False
            elif not threadAguardaFinalizarChamada.is_alive():
                statusChamada = False

    def desligarChamada(self, cliente, conexaoChamada):
        if(cliente.recebeMensagem(conexaoChamada) == "desligar"):
            cliente.enviaMensagem(conexaoChamada, "desligar")
            self.desligarConexoes(cliente,conexaoChamada)

    def desligarConexoes(self,cliente, conexaoChamada):

        cliente.ocupado = False

        self.audioStream.hostClient.stop_server()
        self.audioStream.targetClient.stop_stream()

        self.videoStream.hostClient.stop_server()
        self.videoStream.targetClient.stop_stream()

        conexaoChamada.close()
        print("Chamada encerrada")

