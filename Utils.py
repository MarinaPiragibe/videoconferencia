from time import sleep
import socket
from Cliente import Cliente
import AudioStream
import VideoStream
import threading
from vidstream import *
import Cronometro
import multiprocessing

thread_running = True
def recebeCliente():
  print("\n------------- Login --------------")
  #input('> Informe seu usuário: ')
  nome = 'marina'
  ip = '26.84.232.20'
  porta = '9800'
  #input('> Informe seu IP: ')
  #porta = input('> Informe a porta: ')
  cliente = Cliente(nome, ip, porta)
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

def imprimeListaClientes(listaClientes):

  print("\n--------- Lista de Usuários Cadastrados ---------")
  for cliente in listaClientes:
    print("\n")
    print(f'> NOME: {cliente.nome}')
    print(f'> IP: {cliente.ip}')
    print(f'> PORTA: {cliente.porta}')
    print("---------------")

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

def buscaClienteServidor(parametroBusca, servidor, socketCliente):

  encontrado = False
  valorProcurado = servidor.recebeMensagem(socketCliente)
  print(f"Buscando o cliente com {parametroBusca} igual a {valorProcurado}\n")
  for cliente in servidor.listaClientes:
    if (hasattr(cliente, parametroBusca)):
      if (getattr(cliente, parametroBusca) == valorProcurado):
        encontrado = True
        servidor.enviaMensagem(socketCliente, cliente)
  if(not encontrado):
    servidor.enviaMensagem(socketCliente, [])

def desligarChamada(cliente, conexaoChamada):
  cliente.ocupado = False
  cliente.receiverAudio.stop_server()
  cliente.targetAudio.stop_stream()
  # cliente.hostClient.stop_server()
  cliente.targetClient.stop_stream()
  conexaoChamada.close()

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
    imprimeListaClientes(listaClientes)

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

      VideoStream.startVideoSteam(cliente, targetIP ,portaVideoHost,portaVideoTarget)

      AudioStream.startAudioStream(cliente, targetIP, portaAudioHost, portaAudioTarget)
      
      #thread_cronometro = multiprocessing.Process(target=Cronometro.cronometro, args=())
      #thread_cronometro.start()
      threadAguardaFinalizarChamada = threading.Thread(target=fecharChamadaOuvinte, args=[cliente,socketClienteChamada])
      threadAguardaFinalizarChamada.start()
      while True:
        if(input("Quer sair da chamada?").upper() == "S"):
          cliente.enviaMensagem(conexaoChamada,"desligar")
          thread_running = False
          threadAguardaFinalizarChamada.join()
          desligarChamada(cliente,conexaoChamada) 
          break
      #thread_cronometro.terminate()
              
    if(resposta.upper() == "R"):
      print("Chamada Recusada, tente novamente... \n")
      cliente.ocupado = False
      conexaoChamada.close()

  # Aceitar chamada
  elif (resposta == 6):

    conexaoChamada = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conexaoChamada.bind((str(cliente.ip), int(cliente.porta)))
    conexaoChamada.listen()
    socketClienteChamada, endereco = conexaoChamada.accept()

    print(socketClienteChamada)

    solicitacaoChamada = cliente.recebeMensagem(socketClienteChamada)
    print(solicitacaoChamada)

    cliente.ocupado = True
    resposta = str(input("Deseja aceitar (A) ou recusar (R) a chamada ??\n"))
    cliente.enviaMensagem(socketClienteChamada, resposta)

    if (resposta.upper() == "A"):
      
      targetIP = cliente.recebeMensagem(socketClienteChamada)
      
      portaAudioHost, portaVideoHost = recebePortasCliente(cliente, socketClienteChamada)

      portaVideoTarget = cliente.recebeMensagem(socketClienteChamada)
      portaAudioTarget = cliente.recebeMensagem(socketClienteChamada)

      VideoStream.startVideoSteam(cliente,targetIP,portaVideoHost,portaVideoTarget)

      AudioStream.startAudioStream(cliente, targetIP, portaAudioHost, portaAudioTarget)

      #thread_cronometro = multiprocessing.Process(target=Cronometro.cronometro, args=())
      #thread_cronometro.start()
      
      threadAguardaFinalizarChamada = threading.Thread(target=fecharChamadaOuvinte, args=[cliente,socketClienteChamada])
      threadAguardaFinalizarChamada.start()
      while True:
        if(input("Quer sair da chamada?").upper() == "S"):
          cliente.enviaMensagem(socketClienteChamada,"desligar")
          break
      
     
      #thread_cronometro.terminate()
      
    if(resposta.upper() == "R"):
      print("Chamada recusada.......\n")
      cliente.ocupado = False
      conexaoChamada.close()

def fecharChamadaOuvinte(cliente, conexaoChamada, thread_running):
  if(cliente.recebeMensagem(conexaoChamada) == "desligar"):
    cliente.enviaMensagem(conexaoChamada, "desligar")
    desligarChamada(cliente,conexaoChamada)

def menuServidor(servidor, socketCliente, cliente):

  escolhaDoCliente = servidor.recebeMensagem(socketCliente)

  if escolhaDoCliente == "listagem":
    servidor.enviaMensagem(socketCliente, servidor.listaClientes)

  elif escolhaDoCliente == "nome" or escolhaDoCliente == "ip":

    buscaClienteServidor(escolhaDoCliente, servidor, socketCliente)

  elif escolhaDoCliente == "desligar":

    try:
      servidor.enviaMensagem(socketCliente, "Sua conexão foi encerrada com sucesso. Adeus!")
      print("Desconectando o cliente ", cliente.nome, "\n")
      socketCliente.close()
      servidor.listaSockets.remove(socketCliente)
      servidor.listaClientes.remove(cliente)
      return False
    
    except:
      servidor.enviaMensagem(socketCliente,"Erro ao encerrar a conexão. Tente novamente")
      print("Erro ao desconectar o cliente")

  return True
