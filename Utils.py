from time import sleep
import socket
from Cliente import Cliente
import AudioStream
import VideoStream


def recebeCliente():
  print("\n------------- Login --------------")
  nome = input('> Informe seu usuário: ')
  ip = '26.84.232.20'
  porta = '9800'
  #input('> Informe seu IP: ')
  #porta = input('> Informe a porta: ')
  cliente = Cliente(nome, ip, porta)
  return cliente

def recebePortasCliente(cliente, socketClienteChamada):

  print("Iniciando a  chamada...\n")

  portaVideo = int(input("> Qual porta deseja usar para receber o video?"))
  cliente.enviaMensagem(socketClienteChamada, portaVideo)

  portaAudio = int(input("> Qual porta deseja usar para receber o audio?"))
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

  cliente.enviaMensagem(conexao, "buscarNome")

  nomeProcurado = input("Digite o nome do Cliente que deseja procurar: ")
  print(f'\nProcurando NOME: {nomeProcurado} ...')
  cliente.enviaMensagem(conexao, nomeProcurado)
  clienteProcurado = cliente.recebeMensagem(conexao)

  if (clienteProcurado != []):
    print( f"\nCliente encontrado! \n > NOME: {clienteProcurado.nome}\n > IP: {clienteProcurado.ip}\n > PORTA: {cliente.porta}\n")
  else:
    print("\nCliente com esse nome não encontrado! Tente novamente\n")

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

    cliente.enviaMensagem(conexao, "buscarNome")

    nomeProcurado = input("Digite o nome do Cliente que deseja procurar: ")
    print(f'\nProcurando NOME: {nomeProcurado} ...')
    cliente.enviaMensagem(conexao, nomeProcurado)
    clienteProcurado = cliente.recebeMensagem(conexao)

    if (clienteProcurado != []):
      print( f"\nCliente encontrado! \n > NOME: {clienteProcurado.nome}\n > IP: {clienteProcurado.ip}\n > PORTA: {cliente.porta}\n")
    else:
      print("\nCliente com esse nome não encontrado! Tente novamente\n")

  # Buscar pelo IP
  elif (resposta == 3):
    cliente.enviaMensagem(conexao, "buscarIP")

    ipProcurado = input("Digite o ip do Cliente que deseja procurar: ")
    print(f'\nProcurando IP: {ipProcurado} ...')
    cliente.enviaMensagem(conexao, ipProcurado)
    clienteProcurado = cliente.recebeMensagem(conexao)
    if (clienteProcurado != []):
      print(
          f"\nCliente encontrado! \n > NOME: {clienteProcurado.nome}\n > IP: {clienteProcurado.ip}\n > PORTA: {cliente.porta}\n"
      )
    else:
      print("Cliente com esse IP não encontrado! Tente novamente\n")

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

    targetIP = input("Digite o IP com quem deseja trocar mensagem ?\n")
    targetPorta = input("Digite a porta com quem deseja trocar mensagem ?\n")
    
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

      VideoStream.startVideoSteam(cliente.ip, targetIP ,portaVideoHost,portaVideoTarget)

      receiverAudio, targetAudio = AudioStream.startAudioStream(cliente.ip, targetIP, portaAudioHost, portaAudioTarget)
      
      
      while cliente.ocupado:
        print("Chamada em andamento...")
        desligar = input("> Desligar clique Q!")
        if(desligar.upper() == "Q"):
          cliente.ocupado = False
          AudioStream.closeAudioStream(receiverAudio, targetAudio)
          #videoStream
          conexaoChamada.close()
          
          break
        
        


    if(resposta.upper() == "R"):
      print("Chamada Recusada, tente novamente... \n")
      cliente.ocupado = False
    # conexaoChamada.close()

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

      VideoStream.startVideoSteam(cliente.ip,targetIP,portaVideoHost,portaVideoTarget)

      receiverAudio, targetAudio = AudioStream.startAudioStream(cliente.ip, targetIP, portaAudioHost, portaAudioTarget)
            
      while cliente.ocupado:
        print("Chamada em andamento...")
        desligar = input("> Desligar clique Q!")
        if(desligar.upper() == "Q"):
          AudioStream.closeAudioStream(receiverAudio, targetAudio)
          cliente.ocupado = False
          break
      
    if(resposta.upper() == "R"):
      print("Chamada recusada.......\n")
      cliente.ocupado = False
    # conexaoChamada.close()
    # socketClienteChamada.close()

def menuServidor(servidor, socketCliente, cliente):

  escolhaDoCliente = servidor.recebeMensagem(socketCliente)

  if escolhaDoCliente == "listagem":
    servidor.enviaMensagem(socketCliente, servidor.listaClientes)

  elif escolhaDoCliente == "buscarNome":

    nomeClienteProcurado = servidor.recebeMensagem(socketCliente)
    print("Buscando o cliente ", nomeClienteProcurado, "\n")
    for cliente in servidor.listaClientes:
      if (cliente.nome == nomeClienteProcurado):
        servidor.enviaMensagem(socketCliente, cliente)

  elif escolhaDoCliente == "buscarIP":

    ipClienteProcurado = servidor.recebeMensagem(socketCliente)
    print("Buscando o cliente ", ipClienteProcurado, "\n")
    for cliente in servidor.listaClientes:
      if (cliente.ip == ipClienteProcurado):
        servidor.enviaMensagem(socketCliente, cliente)
    servidor.enviaMensagem(socketCliente, [])

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
