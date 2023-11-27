import Cliente
from stream import Chamada
from time import sleep
from utils import Utils
import socket
from stream import AudioStream, VideoStream

def recebeCliente():
  print("\n------------- Login --------------")
  #input('> Informe seu usuário: ')
  nome = 'marina'
  ip = '26.84.232.20'
  porta = '9800'
  #input('> Informe seu IP: ')
  #porta = input('> Informe a porta: ')
  cliente = Cliente.Cliente(nome, ip, porta)
  return cliente

def recebePortasCliente(cliente, socketClienteChamada):

  print("Iniciando a  chamada...\n")

  portaVideo = 9810
  #int(input("> Qual porta deseja usar para receber o video?"))
  cliente.enviaMensagem(socketClienteChamada, portaVideo)

  portaAudio = 9811
  #int(input("> Qual porta deseja usar para receber o audio?"))
  cliente.enviaMensagem(socketClienteChamada, portaAudio)

  return portaAudio, portaVideo

def buscaCliente(cliente, conexao, parametroBusca):

  cliente.enviaMensagem(conexao, parametroBusca)

  valorProcurado = input(f"Digite o {parametroBusca} do Cliente que deseja procurar: ")
  print(f'\nProcurando {parametroBusca}: {valorProcurado} ...')
  cliente.enviaMensagem(conexao, valorProcurado)
  clienteProcurado = cliente.recebeMensagem(conexao)

  if (clienteProcurado != []):
    print(f"\nCliente encontrado! \n > NOME: {clienteProcurado.nome}\n > IP: {clienteProcurado.ip}\n > PORTA: {cliente.porta}\n")
  else:
    print(f"\nCliente com esse {parametroBusca} não encontrado! Tente novamente\n")

def menuCliente(conexao, cliente):

  print("\n-------------------- Menu --------------------")
  print("Escolha uma opção: \n")
  print("1 - Lista todas os usuários cadastrados")
  print("2 - Buscar pelo nome de um usuário")
  print("3 - Buscar pelo ip de um usuário")
  print("4 - Desligar conexão com servidor e sair")
  print("5 - Iniciar chamada com outro cliente")
  print("6 - Responder a chamado do outro Cliente")
  resposta = int(input("\n> "))

  # Listar todos os usuários
  if (resposta == 1):

    cliente.enviaMensagem(conexao, "listagem")
    listaClientes = cliente.recebeMensagem(conexao)
    Utils.imprimeListaClientes(listaClientes)

  # Buscar pelo nome
  elif (resposta == 2):
    buscaCliente(cliente, conexao, "nome")

  # Buscar pelo IP
  elif (resposta == 3):
    buscaCliente(cliente, conexao, "ip")

  # Desligar
  elif (resposta == 4):
    cliente.enviaMensagem(conexao, "desligar")
    mensagem = cliente.recebeMensagem(conexao)
    print(mensagem)
    conexao.close()
    sleep(2)
    quit()

  # Iniciar chamada
  elif (resposta == 5):

    targetIP = "26.162.121.69"
    #input("Digite o IP com quem deseja trocar mensagem ?\n")
    targetPorta = 9600
    #input("Digite a porta com quem deseja trocar mensagem ?\n")
    
    conexaoChamada = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conexaoChamada.settimeout(None)
    conexaoChamada.connect((str(targetIP), int(targetPorta)))

    cliente.enviaMensagem(conexaoChamada, f"Chamada do cliente {cliente.nome}")
    
    print("Aguardando resposta do cliente .......\n")
    resposta = cliente.recebeMensagem(conexaoChamada)
    
    if (resposta.upper() == "A"):
      
        print("Iniciando a  chamada.......\n")
        cliente.enviaMensagem(conexaoChamada, cliente.ip)
        
        portaVideoTarget = cliente.recebeMensagem(conexaoChamada)
        portaAudioTarget = cliente.recebeMensagem(conexaoChamada)
        
        portaAudioHost, portaVideoHost = recebePortasCliente(cliente, conexaoChamada)

        Chamada.chamada(cliente, targetIP, portaVideoHost, portaAudioHost, portaVideoTarget, portaAudioTarget, conexaoChamada)
                
    if(resposta.upper() == "R"):
        print("Chamada Recusada, tente novamente... \n")
        cliente.ocupado = False
        conexaoChamada.close()

  # Aceitar chamada
  elif (resposta == 6):

    conexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conexao.bind((str(cliente.ip), int(cliente.porta)))
    conexao.listen()
    conexaoChamada, endereco = conexao.accept()

    print(conexaoChamada)

    solicitacaoChamada = cliente.recebeMensagem(conexaoChamada)
    print(solicitacaoChamada)

    cliente.ocupado = True
    resposta = str(input("Deseja aceitar (A) ou recusar (R) a chamada ??\n"))
    cliente.enviaMensagem(conexaoChamada, resposta)

    if (resposta.upper() == "A"):
        
        videoStream = VideoStream.VideoStream()
        audioStream = AudioStream.AudioStream()
        
        audioStream.portaAudioHost, videoStream.portaVideoHost = recebePortasCliente(cliente, conexaoChamada)

        videoStream.portaVideoTarget = cliente.recebeMensagem(conexaoChamada)
        audioStream.portaAudioTarget = cliente.recebeMensagem(conexaoChamada)

        chamada = Chamada.Chamada(conexaoChamada, videoStream, audioStream)
        chamada.targetIP = cliente.recebeMensagem(conexaoChamada)

        chamada.iniciarChamada(cliente, videoStream, audioStream)
        
        #thread_cronometro.terminate()
      
    if(resposta.upper() == "R"):
        print("Chamada recusada.......\n")
        cliente.ocupado = False
        conexaoChamada.close()

